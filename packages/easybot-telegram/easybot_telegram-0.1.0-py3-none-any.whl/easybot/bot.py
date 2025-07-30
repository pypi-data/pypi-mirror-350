import requests
import json
import time
from typing import List, Dict, Any, Callable

class Button:
    """Простое создание кнопок"""
    def __init__(self, text: str, callback: str = None, url: str = None):
        self.text = text
        self.callback = callback
        self.url = url
    
    def to_dict(self):
        btn = {"text": self.text}
        if self.callback:
            btn["callback_data"] = self.callback
        if self.url:
            btn["url"] = self.url
        return btn

class Keyboard:
    """Простое создание клавиатур"""
    def __init__(self, *rows):
        self.rows = rows
    
    def to_dict(self):
        keyboard = []
        for row in self.rows:
            if isinstance(row, list):
                keyboard.append([btn.to_dict() for btn in row])
            else:
                keyboard.append([row.to_dict()])
        return {"inline_keyboard": keyboard}

class Message:
    """Удобная обёртка для сообщений"""
    def __init__(self, data: dict, bot):
        self._data = data
        self._bot = bot
        
        # Основные поля
        self.id = data.get("message_id")
        self.chat_id = data["chat"]["id"]
        self.user_id = data["from"]["id"]
        self.username = data["from"].get("username", "")
        self.first_name = data["from"].get("first_name", "")
        
        # Типы контента
        self.text = data.get("text", "")
        self.photo = data.get("photo", [])
        self.video = data.get("video")
        self.audio = data.get("audio")
        self.voice = data.get("voice")
        self.document = data.get("document")
        self.sticker = data.get("sticker")
        self.location = data.get("location")
        self.contact = data.get("contact")
        
        # Определяем тип
        if self.text:
            self.type = "text"
        elif self.photo:
            self.type = "photo"
        elif self.video:
            self.type = "video"
        elif self.audio:
            self.type = "audio"
        elif self.voice:
            self.type = "voice"
        elif self.document:
            self.type = "document"
        elif self.sticker:
            self.type = "sticker"
        elif self.location:
            self.type = "location"
        elif self.contact:
            self.type = "contact"
        else:
            self.type = "unknown"
    
    def reply(self, text: str = None, photo: str = None, keyboard: Keyboard = None, **kwargs):
        """Быстрый ответ на сообщение"""
        if text:
            return self._bot.send(self.chat_id, text, keyboard=keyboard, **kwargs)
        elif photo:
            return self._bot.send_photo(self.chat_id, photo, keyboard=keyboard, **kwargs)
    
    def answer(self, text: str = None, **kwargs):
        """Ответ без reply (просто отправка в чат)"""
        return self.reply(text, **kwargs)

class CallbackQuery:
    """Удобная обёртка для callback-запросов"""
    def __init__(self, data: dict, bot):
        self._data = data
        self._bot = bot
        
        self.id = data["id"]
        self.data = data["data"]
        self.user_id = data["from"]["id"]
        self.username = data["from"].get("username", "")
        self.message = Message(data["message"], bot) if "message" in data else None
    
    def answer(self, text: str = None, show_alert: bool = False):
        """Ответ на callback (всплывающее уведомление)"""
        return self._bot.answer_callback(self.id, text, show_alert)
    
    def edit(self, text: str = None, keyboard: Keyboard = None):
        """Редактирование сообщения с кнопкой"""
        if self.message:
            return self._bot.edit_message(
                self.message.chat_id, 
                self.message.id, 
                text, 
                keyboard
            )

class Bot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.offset = 0
        
        # Хранилище обработчиков
        self._handlers = {
            "message": [],
            "command": {},
            "callback": {},
            "type": {},
            "any": []
        }
        
        # Хранилище данных пользователей
        self.users = {}
    
    def _api_request(self, method: str, data: dict = None, files: dict = None):
        """Универсальный метод для API запросов"""
        url = self.base_url + method
        try:
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return {"ok": False}
    
    # === ДЕКОРАТОРЫ ДЛЯ ОБРАБОТЧИКОВ ===
    
    def message(self, text: str = None):
        """Обработчик текстовых сообщений"""
        def decorator(func):
            self._handlers["message"].append((text, func))
            return func
        return decorator
    
    def command(self, cmd: str):
        """Обработчик команд"""
        def decorator(func):
            if not cmd.startswith("/"):
                cmd_with_slash = "/" + cmd
            else:
                cmd_with_slash = cmd
            self._handlers["command"][cmd_with_slash] = func
            return func
        return decorator
    
    def callback(self, data: str = None):
        """Обработчик callback-кнопок"""
        def decorator(func):
            if data:
                self._handlers["callback"][data] = func
            else:
                self._handlers["callback"]["*"] = func
            return func
        return decorator
    
    def on(self, content_type: str):
        """Обработчик по типу контента: photo, video, audio, etc."""
        def decorator(func):
            if content_type not in self._handlers["type"]:
                self._handlers["type"][content_type] = []
            self._handlers["type"][content_type].append(func)
            return func
        return decorator
    
    def any_message(self):
        """Обработчик любых сообщений"""
        def decorator(func):
            self._handlers["any"].append(func)
            return func
        return decorator
    
    # === МЕТОДЫ ОТПРАВКИ ===
    
    def send(self, chat_id: int, text: str, keyboard: Keyboard = None, parse_mode: str = None):
        """Отправка текстового сообщения"""
        data = {"chat_id": chat_id, "text": text}
        if keyboard:
            data["reply_markup"] = keyboard.to_dict()
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._api_request("sendMessage", data)
    
    def send_photo(self, chat_id: int, photo: str, caption: str = None, keyboard: Keyboard = None):
        """Отправка фото"""
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard.to_dict())
        
        if photo.startswith("http"):
            data["photo"] = photo
            return self._api_request("sendPhoto", data)
        else:
            files = {"photo": open(photo, "rb")}
            return self._api_request("sendPhoto", data, files=files)
    
    def send_video(self, chat_id: int, video: str, caption: str = None, keyboard: Keyboard = None):
        """Отправка видео"""
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard.to_dict())
        
        if video.startswith("http"):
            data["video"] = video
            return self._api_request("sendVideo", data)
        else:
            files = {"video": open(video, "rb")}
            return self._api_request("sendVideo", data, files=files)
    
    def send_document(self, chat_id: int, document: str, caption: str = None, keyboard: Keyboard = None):
        """Отправка документа"""
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard.to_dict())
        
        if document.startswith("http"):
            data["document"] = document
            return self._api_request("sendDocument", data)
        else:
            files = {"document": open(document, "rb")}
            return self._api_request("sendDocument", data, files=files)
    
    def edit_message(self, chat_id: int, message_id: int, text: str, keyboard: Keyboard = None):
        """Редактирование сообщения"""
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
        if keyboard:
            data["reply_markup"] = keyboard.to_dict()
        return self._api_request("editMessageText", data)
    
    def answer_callback(self, callback_id: str, text: str = None, show_alert: bool = False):
        """Ответ на callback-запрос"""
        data = {"callback_query_id": callback_id}
        if text:
            data["text"] = text
        data["show_alert"] = show_alert
        return self._api_request("answerCallbackQuery", data)
    
    # === ОБРАБОТКА ОБНОВЛЕНИЙ ===
    
    def _process_message(self, msg_data: dict):
        """Обработка входящих сообщений"""
        msg = Message(msg_data, self)
        
        # Команды
        if msg.text.startswith("/"):
            cmd = msg.text.split()[0]
            if cmd in self._handlers["command"]:
                self._handlers["command"][cmd](msg)
                return
        
        # Текстовые сообщения
        if msg.type == "text":
            for pattern, handler in self._handlers["message"]:
                if pattern is None or pattern in msg.text:
                    handler(msg)
        
        # По типу контента
        if msg.type in self._handlers["type"]:
            for handler in self._handlers["type"][msg.type]:
                handler(msg)
        
        # Любые сообщения
        for handler in self._handlers["any"]:
            handler(msg)
    
    def _process_callback(self, callback_data: dict):
        """Обработка callback-запросов"""
        callback = CallbackQuery(callback_data, self)
        
        # Точное совпадение
        if callback.data in self._handlers["callback"]:
            self._handlers["callback"][callback.data](callback)
        # Универсальный обработчик
        elif "*" in self._handlers["callback"]:
            self._handlers["callback"]["*"](callback)
    
    def run(self):
        """Запуск бота"""
        print("🤖 Бот запущен!")
        
        while True:
            try:
                # Получаем обновления
                response = requests.get(
                    self.base_url + "getUpdates",
                    params={"offset": self.offset, "timeout": 30}
                ).json()
                
                if response["ok"]:
                    for update in response["result"]:
                        self.offset = update["update_id"] + 1
                        
                        # Обрабатываем разные типы обновлений
                        if "message" in update:
                            self._process_message(update["message"])
                        elif "callback_query" in update:
                            self._process_callback(update["callback_query"])
                
            except KeyboardInterrupt:
                print("\n👋 Бот остановлен")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                time.sleep(5)
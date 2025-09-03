import json

import requests
from django.conf import settings


class TelegramService:
    def __init__(self, token):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.token = token

    def send_worker_message(self, client_name, pass_id, chat_id):
        text = f"К вам пришёл {client_name}. Выдать доступ?"
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Да", "callback_data": f"approve_{pass_id}"},
                    {"text": "Нет", "callback_data": f"decline_{pass_id}"}
                ]
            ]
        }
        params = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps(keyboard)}
        requests.get(url, params=params)

telegram_message = TelegramService(settings.BOT_TOKEN)

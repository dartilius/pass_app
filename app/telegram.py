import requests


class TelegramService:
    def __init__(self, token):
        token = token

    def send_worker_message(self, _pass):
        chat_id = "your_chatId"
        text = f"К вам пришёл {_pass["name"]}. Выдать доступ?"
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        requests.get(url, params=params)

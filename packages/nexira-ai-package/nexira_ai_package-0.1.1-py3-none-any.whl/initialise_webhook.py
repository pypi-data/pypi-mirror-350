import requests

class InitialiseWebhook:
    def __init__(self, bot_token: str, api_url: str):
        self.bot_token = bot_token
        self.api_url = api_url

    def initialise(self):
        WEBHOOK_URL = f"{self.api_url}/webhook"
        TELEGRAM_URL = f"https://api.telegram.org/bot{self.bot_token}"
        res = requests.get(f"{TELEGRAM_URL}/getWebhookInfo")
        print(res.json())
        res = requests.post(f"{TELEGRAM_URL}/setWebhook", data={"url": WEBHOOK_URL})
        print(res.json())
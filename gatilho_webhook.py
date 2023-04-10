import requests
import os

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_URL = os.environ["TELEGRAM_URL"]
dados = {"url" : f"{TELEGRAM_URL}"}
resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/setWebhook", data=dados)
print(resposta.text)

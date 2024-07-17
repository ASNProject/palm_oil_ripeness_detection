import requests

TOKEN = "7261947544:AAFTGs0bnyuBEBIWydw9oL5RCZP65YGHpg0"  # CHANGE YOUR BOT TOKEN
CHAT_ID = '1587088624'  # CHANGE YOUR CHAT ID (Search Get My ID in Telegram)


def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={f'Hasil Klasifikasi: {message}'}"

    r = requests.get(url)
    print(r.json())

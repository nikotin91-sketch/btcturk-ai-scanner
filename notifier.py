import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message: str) -> bool:
    """
    Telegram'a mesaj gönderir.
    Başarılıysa True, hata olursa False döndürür.
    """

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

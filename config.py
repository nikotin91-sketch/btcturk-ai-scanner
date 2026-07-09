import os

# ------------------------
# Telegram
# ------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ------------------------
# Tarama Ayarları
# ------------------------
SCAN_INTERVAL = 60          # saniye
MAX_COINS = 100
MIN_AI_SCORE = 70

# ------------------------
# Teknik Analiz
# ------------------------
RSI_PERIOD = 14

EMA_FAST = 9
EMA_MID = 21
EMA_SLOW = 50

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ------------------------
# Bildirim
# ------------------------
NOTIFICATION_COOLDOWN = 900   # 15 dakika

# ------------------------
# Web
# ------------------------
TIMEZONE = "Europe/Istanbul"

# ------------------------
# Log
# ------------------------
LOG_FOLDER = "logs"
DATA_FOLDER = "data"

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import pytz

from btcturk_api import get_try_pairs, get_klines
from indicators import ema, rsi
from analyzer import calculate_score
from notifier import send_telegram
from cache import can_send
from config import NOTIFICATION_COOLDOWN

app = Flask(__name__)
CORS(app)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def telegram_gonder(mesaj):

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": mesaj
            },
            timeout=10
        )

    except:
        pass



@app.route("/app")
def uygulama():
    return send_file("index.html")



@app.route("/")
def home():
    return "BTCTurk AI Scanner Aktif"



@app.route("/firsatlar")
def firsatlar():

    url = "https://api.btcturk.com/api/v2/ticker"

    try:
        veri = requests.get(
            url,
            timeout=10
        ).json()

    except:

        return jsonify({
            "saat":"",
            "coinler":[]
        })


    liste=[]


    for coin in veri.get("data", []):

        try:

            isim = coin["pairNormalized"]

            if not isim.endswith("_TRY"):
                continue


            fiyat = float(coin["last"])
            degisim = float(coin["dailyPercent"])
            hacim = float(coin["volume"])


            skor = 40

 # Teknik analiz testi
try:
    mum = get_klines(
        coin["pair"].replace("/", ""),
        resolution=1,
        candle_count=100
    )

    if mum:
        fiyatlar = mum["close"]

        rsi_deger = rsi(fiyatlar)

        ema9 = ema(fiyatlar, 9)
        ema21 = ema(fiyatlar, 21)

except Exception:
    pass


if degisim >= 2:
    skor += 10

            if degisim >= 5:
                skor += 20


            if hacim >= 5:
                skor += 10

            if hacim >= 20:
                skor += 10



            if skor >= 80:

                sinyal = "🟢 GÜÇLÜ AL"


                telegram_gonder(
                    f"🚀 BTCTürk AI Sinyal\n\n"
                    f"Coin: {isim}\n"
                    f"Fiyat: {fiyat} TL\n"
                    f"Değişim: %{degisim}\n"
                    f"Hacim: {hacim}\n"
                    f"AI Skor: {skor}"
                )


            elif skor >= 60:

                sinyal="🟡 TAKİP"


            else:

                sinyal="⚪ BEKLE"



            if skor >= 60:

                liste.append({

                    "coin":isim,
                    "fiyat":fiyat,
                    "degisim":round(degisim,2),
                    "hacim":round(hacim,2),
                    "ai":skor,
                    "sinyal":sinyal

                })


        except:

            continue



    liste.sort(
        key=lambda x:x["ai"],
        reverse=True
    )


    saat=datetime.now(
        pytz.timezone("Europe/Istanbul")
    ).strftime("%H:%M:%S")


    return jsonify({

        "saat":saat,
        "coinler":liste[:20]

    })



if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

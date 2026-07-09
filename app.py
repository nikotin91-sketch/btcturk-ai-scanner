from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests
from datetime import datetime
import pytz
import os

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

@app.route("/test_api")
def test_api():

    from btcturk_api import get_klines
    from indicators import ema, rsi

    try:
        data = get_klines(
            "BTCTRY",
            resolution=1,
            candle_count=100
        )

        prices = data["close"]

        ema9 = ema(prices, 9)
        ema21 = ema(prices, 21)

        return jsonify({
            "fiyat": prices[-1],
            "rsi": rsi(prices),
            "ema9": ema9[-1],
            "ema21": ema21[-1]
        })

    except Exception as e:
        return jsonify({
            "hata": str(e)
        })


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
            "saat": "",
            "coinler": []
        })


    liste = []


    for coin in veri.get("data", []):

        try:

            isim = coin["pairNormalized"]

            if not isim.endswith("_TRY"):
                continue


            fiyat = float(coin["last"])
            degisim = float(coin["dailyPercent"])
            hacim = float(coin["volume"])


            skor = 40


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

                sinyal = "🟡 TAKİP"


            else:

                sinyal = "⚪ BEKLE"



            if skor >= 60:

                liste.append({

                    "coin": isim,
                    "fiyat": fiyat,
                    "degisim": round(degisim, 2),
                    "hacim": round(hacim, 2),
                    "ai": skor,
                    "sinyal": sinyal

                })


        except:

            continue



    liste.sort(
        key=lambda x: x["ai"],
        reverse=True
    )


    saat = datetime.now(
        pytz.timezone("Europe/Istanbul")
    ).strftime("%H:%M:%S")


    return jsonify({

        "saat": saat,
        "coinler": liste[:20]

    })



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

from flask import Flask, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import pytz

from btcturk_api import get_try_pairs
from scanner import scan_coin
from cache import can_send
from notifier import send_telegram
from config import NOTIFICATION_COOLDOWN


app = Flask(__name__)
CORS(app)


@app.route("/app")
def uygulama():
    return send_file("index.html")


@app.route("/")
def home():
    return "BTCTurk AI Scanner Aktif"


@app.route("/test_scanner")
def test_scanner():

    result = scan_coin("BTCTRY")

    if result is None:
        return jsonify({
            "durum": "hata"
        })

    return jsonify(result)



@app.route("/firsatlar")
def firsatlar():

    liste = []

    try:

        pairs = get_try_pairs()

        pairs = pairs[:20]


        for pair in pairs:

            try:

                result = scan_coin(pair["symbol"])


                if result is None:
                    continue


                score = result["score"]


                # Telegram güçlü sinyal
                if score["score"] >= 75:


                    if can_send(
                        pair["symbol"],
                        NOTIFICATION_COOLDOWN
                    ):


                        mesaj = f"""
🚀 <b>BTCTürk AI SİNYAL</b>

🪙 Coin:
{pair["display"]}

💰 Fiyat:
{result["price"]}

📊 AI Skor:
{score["score"]}/100

📌 Sinyal:
{score["signal"]}

🎯 Hedef 1:
{result["target1"]}

🚀 Hedef 2:
{result["target2"]}

🛑 Stop:
{result["stop"]}

📈 Analiz:
{", ".join(score["reasons"])}

⏰ Saat:
{datetime.now(
    pytz.timezone("Europe/Istanbul")
).strftime("%H:%M:%S")}

🤖 BTCTürk AI Scanner
"""


                        send_telegram(mesaj)



                liste.append({

                    "coin": pair["display"],

                    "fiyat": result["price"],

                    "ai": score["score"],

                    "sinyal": score["signal"],

                    "nedenler": score["reasons"]

                })


            except Exception:

                continue



    except Exception:

        return jsonify({

            "saat": "",

            "coinler": []

        })



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

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)


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
        veri = requests.get(url, timeout=10).json()
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


            # Fiyat hareketi
            if degisim >= 3:
                skor += 15

            if degisim >= 5:
                skor += 15


            # Hacim gücü
            if hacim >= 5:
                skor += 10

            if hacim >= 20:
                skor += 10



            if skor >= 80:
                sinyal = "🟢 GÜÇLÜ AL"

            elif skor >= 65:
                sinyal = "🟡 TAKİP"

            else:
                sinyal = "⚪ BEKLE"



            if skor >= 65:

                liste.append({

                    "coin": isim,
                    "fiyat": fiyat,
                    "degisim": round(degisimi, 2) if False else round(degisism,2),
                    "hacim": round(hacim,2),
                    "ai": skor,
                    "sinyal": sinyal

                })


        except:
            pass



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

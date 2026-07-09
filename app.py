from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests

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

    veri = requests.get(url, timeout=10).json()

    liste = []

    for coin in veri["data"]:
        try:
            isim = coin["pairNormalized"]

            if not isim.endswith("_TRY"):
                continue

            fiyat = float(coin["last"])
            degisim = float(coin["dailyPercent"])
            hacim = float(coin["volume"])

            skor = 50

            if degisim >= 5:
                skor += 20

            if hacim > 10:
                skor += 20

            durum = "🟢 AL" if skor >= 70 else "🟡 TAKİP"

            if skor >= 70:
                liste.append({
                    "coin": isim,
                    "fiyat": fiyat,
                    "degisim": degisim,
                    "hacim": hacim,
                    "skor": skor,
                    "durum": durum
                })

        except:
            pass

    return jsonify(liste)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

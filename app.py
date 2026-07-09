from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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

            if isim.endswith("_TRY"):

                liste.append({
                    "coin": isim,
                    "fiyat": coin["last"],
                    "degisim": coin["dailyPercent"]
                })

        except:
            pass

    return jsonify(liste)

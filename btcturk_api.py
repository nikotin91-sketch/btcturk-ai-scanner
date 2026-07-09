import requests
import time

GRAPH_API = "https://graph-api.btcturk.com/v1/klines/history"
TICKER_API = "https://api.btcturk.com/api/v2/ticker"


def get_try_pairs():

    r = requests.get(TICKER_API, timeout=10)
    r.raise_for_status()

    data = r.json()["data"]

    pairs = []

    for item in data:

        if item["pairNormalized"].endswith("_TRY"):

            pairs.append({
                "symbol": item["pair"].replace("/", ""),
                "display": item["pairNormalized"]
            })

    return pairs

def get_klines(symbol, resolution=1, candle_count=200):

    now = int(time.time())

    start = now - (resolution * 60 * candle_count)

    url = (
        f"{GRAPH_API}"
        f"?symbol={symbol}"
        f"&resolution={resolution}"
        f"&from={start}"
        f"&to={now}"
    )

    r = requests.get(url, timeout=10)
    r.raise_for_status()

    raw = r.json()

    if raw.get("s") != "ok":
        return None

    return {
        "close": [float(x) for x in raw.get("c", [])],
        "open": [float(x) for x in raw.get("o", [])],
        "high": [float(x) for x in raw.get("h", [])],
        "low": [float(x) for x in raw.get("l", [])],
        "volume": [float(x) for x in raw.get("v", [])],
        "time": raw.get("t", []),
        "last_price": float(raw["c"][-1])
    }

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

    print(raw)

    return raw

    closes = []
    volumes = []

    for candle in candles:

        try:
            closes.append(float(candle["close"]))
            volumes.append(float(candle["volume"]))
        except:
            continue

    if not closes:
        return None

    return {
        "close": closes,
        "volume": volumes,
        "last_price": closes[-1]
    }

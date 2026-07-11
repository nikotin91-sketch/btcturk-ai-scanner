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

    closes = [float(x) for x in raw.get("c", [])]
    opens = [float(x) for x in raw.get("o", [])]
    highs = [float(x) for x in raw.get("h", [])]
    lows = [float(x) for x in raw.get("l", [])]
    volumes = [float(x) for x in raw.get("v", [])]
    times = raw.get("t", [])

    print("=" * 50)
    print("Sembol:", symbol)
    print("Son Fiyat:", closes[-1] if closes else None)
    print("Son 5 Hacim:", volumes[-5:] if volumes else [])
    print("Son 5 Kapanış:", closes[-5:] if closes else [])
    print("=" * 50)

    return {
        "close": closes,
        "open": opens,
        "high": highs,
        "low": lows,
        "volume": volumes,
        "time": times,
        "last_price": closes[-1]
    }

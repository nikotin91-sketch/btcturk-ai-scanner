from btcturk_api import get_klines
from indicators import ema, rsi, macd
from analyzer import calculate_score


def scan_coin(symbol):

    data = get_klines(symbol, resolution=1, candle_count=100)

    if not data:
        return None

    prices = data["close"]

    ema9 = ema(prices, 9)
    ema21 = ema(prices, 21)

    if not ema9 or not ema21:
        return None

    volumes = data["volume"]

    avg_volume = sum(volumes[-20:]) / 20

    volume_spike = volumes[-1] > avg_volume * 1.5

    last_high = max(prices[-20:-1])

    breakout = prices[-1] > last_high


    analysis = {
        "rsi": rsi(prices),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "macd": macd(prices),
        "volume_spike": volume_spike,
        "breakout": breakout
    }

    result = calculate_score(analysis)

    return {
        "price": data["last_price"],
        "analysis": analysis,
        "score": result
    }

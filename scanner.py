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

    volume_ratio = volumes[-1] / avg_volume

    volume_spike = volume_ratio > 1.2

    last_high = max(prices[-20:-1])

    breakout = prices[-1] > last_high


    analysis = {
        "rsi": rsi(prices),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "macd": macd(prices),
        "volume_spike": volume_spike,
        "volume_ratio": volume_ratio,
        "breakout": breakout
    }

    result = calculate_score(analysis)

    price = data["last_price"]

    target1 = round(price * 1.02, 2)   # %2 hedef
    target2 = round(price * 1.05, 2)   # %5 hedef
    stop = round(price * 0.985, 2)     # %1.5 stop


    return {
        "price": price,
        "target1": target1,
        "target2": target2,
        "stop": stop,
        "analysis": analysis,
        "score": result
    }

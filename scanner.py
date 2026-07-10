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

    volume_now = volumes[-1]

    # Son mum hacmi 0 gelirse son 5 mum ortalamasını kullan
    if volume_now == 0:
        volume_now = sum(volumes[-5:]) / 5


    if avg_volume > 0:
        volume_ratio = round(volume_now / avg_volume, 2)
    else:
        volume_ratio = 0


    volume_spike = volume_ratio >= 1.2


    last_high = max(prices[-20:-1])

    breakout = prices[-1] > last_high

    breakout_strength = round(
        ((prices[-1] - last_high) / last_high) * 100,
        2
    )


    analysis = {
        "rsi": rsi(prices),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "macd": macd(prices),
        "volume_spike": volume_spike,
        "volume_ratio": volume_ratio,
        "breakout": breakout,
        "breakout_strength": breakout_strength,
    }


    result = calculate_score(analysis)


    price = data["last_price"]

    target1 = round(price * 1.02, 2)
    target2 = round(price * 1.05, 2)
    stop = round(price * 0.985, 2)


    return {
        "price": price,
        "target1": target1,
        "target2": target2,
        "stop": stop,
        "analysis": analysis,
        "score": result
    }

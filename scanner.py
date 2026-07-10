from btcturk_api import get_klines
from indicators import ema, rsi, macd
from analyzer import calculate_score
from atr import atr


def scan_coin(symbol):

    data = get_klines(symbol, resolution=1, candle_count=200)

    if not data:
        return None

    close = data["close"]
    high = data["high"]
    low = data["low"]

    ema9 = ema(close, 9)
    ema21 = ema(close, 21)
    ema50 = ema(close, 50)

    if not ema9 or not ema21 or not ema50:
        return None

    atr_value = atr(high, low, close)

    if atr_value is None:
        return None

    volumes = data["volume"]

    avg_volume = sum(volumes[-20:]) / 20
    volume_now = volumes[-1]

    if avg_volume > 0:
        volume_ratio = round(volume_now / avg_volume, 2)
    else:
        volume_ratio = 0

    volume_spike = volume_ratio >= 1.2

    last_high = max(close[-20:-1])

    breakout = close[-1] > last_high

    breakout_strength = round(
        ((close[-1] - last_high) / last_high) * 100,
        2
    )

    analysis = {
        "rsi": rsi(close),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "ema50": ema50[-1],
        "macd": macd(close),
        "volume_spike": volume_spike,
        "volume_ratio": volume_ratio,
        "breakout": breakout,
        "breakout_strength": breakout_strength,
    }

    result = calculate_score(analysis)

    price = data["last_price"]

    stop = round(price - atr_value * 1.5, 2)
    target1 = round(price + atr_value * 2, 2)
    target2 = round(price + atr_value * 4, 2)

    return {
        "price": price,
        "target1": target1,
        "target2": target2,
        "stop": stop,
        "atr": round(atr_value, 2),
        "analysis": analysis,
        "score": result
    }

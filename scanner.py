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
    volume = data["volume"]

    ema9 = ema(close, 9)
    ema21 = ema(close, 21)
    ema50 = ema(close, 50)

    if not ema9 or not ema21 or not ema50:
        return None

    atr_value = atr(high, low, close)

    if atr_value is None:
        return None

    # HACİM
    avg_volume = sum(volume[-20:]) / 20 if len(volume) >= 20 else 0
    volume_now = volume[-1] if volume else 0

    if avg_volume > 0:
        volume_ratio = volume_now / avg_volume

        # Çok düşük hacimleri tamamen sıfırlama
        if volume_ratio < 0.10:
            volume_ratio = 0.10

        volume_ratio = round(volume_ratio, 2)
    else:
        volume_ratio = 0.10

    volume_spike = volume_ratio >= 1.2

    # BREAKOUT
    last_high = max(close[-20:-1])

    breakout = close[-1] > last_high

    breakout_strength = round(
        ((close[-1] - last_high) / last_high) * 100,
        2
    )

    # TREND GÜCÜ
    trend_strength = 0

    if ema9[-1] > ema21[-1]:
        trend_strength += 1

    if ema21[-1] > ema50[-1]:
        trend_strength += 1

    if volume_ratio >= 1.2:
        trend_strength += 1

    # RİSK / ÖDÜL
    risk = atr_value * 1.2
    reward = atr_value * 3

    risk_reward = round(reward / risk, 2) if risk else 0

    # ANALİZ
    analysis = {
        "rsi": rsi(close),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "ema50": ema50[-1],
        "macd": macd(close),
        "volume_ratio": volume_ratio,
        "volume_spike": volume_spike,
        "breakout": breakout,
        "breakout_strength": breakout_strength,
        "higher_tf_up": ema9[-1] > ema21[-1],
        "trend_strength": trend_strength,
        "risk_reward": risk_reward
    }

    result = calculate_score(analysis)

    price = data["last_price"]

    stop = round(price - risk, 2)
    target1 = round(price + reward, 2)
    target2 = round(price + reward * 2, 2)

    return {
        "price": price,
        "atr": round(atr_value, 2),
        "stop": stop,
        "target1": target1,
        "target2": target2,
        "analysis": analysis,
        "score": result
    }

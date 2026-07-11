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

    avg_volume = sum(volume[-20:]) / 20 if len(volume) >= 20 else 0
    volume_now = volume[-1] if volume else 0
    volume_ratio = round(volume_now / avg_volume, 2) if avg_volume else 0

    breakout = close[-1] > max(close[-20:-1])
    breakout_strength = round(
        ((close[-1] - max(close[-20:-1])) / max(close[-20:-1])) * 100,
        2
    )

    trend_strength = 0
    if ema9[-1] > ema21[-1]:
        trend_strength += 1
    if ema21[-1] > ema50[-1]:
        trend_strength += 1
    if volume_ratio >= 1.2:
        trend_strength += 1

    # Güncellendi
    risk = atr_value * 1.2
    reward = atr_value * 3
    risk_reward = round(reward / risk, 2) if risk else 0

    analysis = {
        "rsi": rsi(close),
        "ema9": ema9[-1],
        "ema21": ema21[-1],
        "ema50": ema50[-1],
        "macd": macd(close),
        "volume_ratio": volume_ratio,
        "volume_spike": volume_ratio >= 1.2,
        "breakout": breakout,
        "breakout_strength": breakout_strength,
        "higher_tf_up": ema9[-1] > ema21[-1],
        "trend_strength": trend_strength,
        "risk_reward": risk_reward
    }

    result = calculate_score(analysis)
    price = data["last_price"]

    return {
        "price": price,
        "atr": round(atr_value, 2),
        "stop": round(price - risk, 2),
        "target1": round(price + reward, 2),
        "target2": round(price + reward * 2, 2),
        "analysis": analysis,
        "score": result
    }

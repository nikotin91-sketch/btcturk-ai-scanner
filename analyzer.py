from config import MIN_AI_SCORE


def calculate_score(data):
    """
    data örneği:
    {
        "rsi": 48,
        "ema_trend": True,
        "macd_cross": True,
        "volume_spike": False,
        "price_change": 3.2,
        "breakout": False
    }
    """

    score = 0
    reasons = []

    rsi = data.get("rsi", 50)

    if 40 <= rsi <= 60:
        score += 20
        reasons.append("RSI")

    if data.get("ema_trend", False):
        score += 20
        reasons.append("EMA")

    if data.get("macd_cross", False):
        score += 20
        reasons.append("MACD")

    if data.get("volume_spike", False):
        score += 20
        reasons.append("HACİM")

    if data.get("breakout", False):
        score += 20
        reasons.append("BREAKOUT")

    if score >= 90:
        signal = "🟢 GÜÇLÜ AL"
    elif score >= MIN_AI_SCORE:
        signal = "🟡 TAKİP"
    else:
        signal = "⚪ BEKLE"

    return {
        "score": score,
        "signal": signal,
        "reasons": reasons
    }

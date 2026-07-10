from config import MIN_AI_SCORE


def calculate_score(data):

    rsi = data.get("rsi")

    if rsi is None:
        return {
            "score": 0,
            "signal": "⚪ WAIT",
            "reasons": ["YETERSİZ VERİ"]
        }

    score = 0
    reasons = []

    if 45 <= rsi <= 65:
        score += 20
        reasons.append("RSI")

    elif 35 <= rsi < 45:
        score += 10

    elif 65 < rsi <= 75:
        score += 5

    if data["ema9"] > data["ema21"]:
        score += 25
        reasons.append("EMA TREND")

    macd = data.get("macd")

    if macd and macd["macd"] > macd["signal"]:
        score += 25
        reasons.append("MACD")

    if data.get("volume_spike", False):
        score += 15
        reasons.append("HACİM")

    if data.get("breakout", False):
        score += 15
        reasons.append("BREAKOUT")

    score = min(score, 100)

    if score >= 90:
        signal = "🚀 STRONG BUY"
    elif score >= 75:
        signal = "🟢 BUY"
    elif score >= MIN_AI_SCORE:
        signal = "🟡 WATCH"
    else:
        signal = "⚪ WAIT"

    return {
        "score": score,
        "signal": signal,
        "reasons": reasons
    }

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


    # RSI
    if 50 <= rsi <= 65:
        score += 20
        reasons.append("RSI GÜÇLÜ")

    elif 40 <= rsi < 50:
        score += 10
        reasons.append("RSI TOPARLANMA")

    elif 65 < rsi <= 70:
        score += 10
        reasons.append("RSI YÜKSEK")


    # EMA Trend
    ema9 = data["ema9"]
    ema21 = data["ema21"]

    if ema9 > ema21:
        score += 25
        reasons.append("EMA TREND")

    elif ema9 > ema21 * 0.9995:
        score += 10
        reasons.append("EMA YAKLAŞIYOR")


    # MACD
    macd = data.get("macd")

    if macd:

        if macd["macd"] > macd["signal"]:
            score += 25
            reasons.append("MACD POZİTİF")

        elif macd.get("histogram", 0) > 0:
            score += 10
            reasons.append("MACD TOPARLANMA")


    # Hacim
    if data.get("volume_spike", False):
        score += 15
        reasons.append("HACİM ARTIŞI")


    # Breakout
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

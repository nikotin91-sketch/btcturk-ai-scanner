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

    # EMA Trend
    ema9 = data.get("ema9", 0)
    ema21 = data.get("ema21", 0)
    ema50 = data.get("ema50", 0)

    if ema9 > ema21:
        score += 25
        reasons.append("EMA TREND")

    elif ema9 > ema21 * 0.9995:
        score += 10
        reasons.append("EMA YAKLAŞIYOR")

    if ema9 > ema21 > ema50:
        score += 15
        reasons.append("GÜÇLÜ TREND")

    # MACD
    macd = data.get("macd")
    macd_positive = False

    if macd:

        if macd["macd"] > macd["signal"]:
            score += 25
            reasons.append("MACD POZİTİF")
            macd_positive = True

        elif macd.get("histogram", 0) > 0:
            score += 10
            reasons.append("MACD TOPARLANMA")

    # Hacim
    volume_ratio = data.get("volume_ratio", 0)
    volume_good = False

    if volume_ratio >= 1.5:
        score += 15
        reasons.append("GÜÇLÜ HACİM")
        volume_good = True

    elif volume_ratio >= 1.2:
        score += 10
        reasons.append("HACİM ARTIŞI")
        volume_good = True

    elif volume_ratio < 0.5:
        score -= 10
        reasons.append("DÜŞÜK HACİM")

    # Breakout
    breakout = data.get("breakout", False)

    if breakout:
        score += 15
        reasons.append("BREAKOUT")

    if score < 0:
        score = 0

    score = min(score, 100)

    # Sinyal Filtresi
    if (
        score >= 90
        and macd_positive
        and volume_good
        and breakout
    ):
        signal = "🚀 STRONG BUY"

    elif score >= 80:

        if macd_positive:
            signal = "🟢 BUY"
        else:
            signal = "🟡 WATCH"

    elif score >= MIN_AI_SCORE:
        signal = "🟡 WATCH"

    else:
        signal = "⚪ WAIT"

    return {
        "score": score,
        "signal": signal,
        "reasons": reasons
    }

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


    # EMA
    ema9 = data.get("ema9", 0)
    ema21 = data.get("ema21", 0)

    ema_up = False

    if ema9 > ema21:
        score += 25
        reasons.append("EMA TREND")
        ema_up = True

    elif ema9 > ema21 * 0.9995:
        score += 10
        reasons.append("EMA YAKLAŞIYOR")


    # MACD
    macd = data.get("macd")

    macd_positive = False

    if macd:

        macd_value = macd.get("macd", 0)
        signal_value = macd.get("signal", 0)
        histogram = macd.get("histogram", 0)


        if macd_value > signal_value:
            score += 25
            reasons.append("MACD POZİTİF")
            macd_positive = True

        elif histogram > 0:
            score += 10
            reasons.append("MACD TOPARLANMA")

        elif abs(macd_value - signal_value) < abs(signal_value) * 0.20:
            score += 5
            reasons.append("MACD YAKLAŞIYOR")


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


    # Son sinyal filtresi
    if score >= 90 and macd_positive and volume_good:
        signal = "🚀 STRONG BUY"

    elif score >= 75 and macd_positive:
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

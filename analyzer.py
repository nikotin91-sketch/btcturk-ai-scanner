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
    ema9 = data.get("ema9", 0)
    ema21 = data.get("ema21", 0)

    if ema9 > ema21:
        score += 25
        reasons.append("EMA TREND")

    elif ema9 > ema21 * 0.9995:
        score += 10
        reasons.append("EMA YAKLAŞIYOR")


    # MACD
    macd = data.get("macd")

    if macd:

        macd_value = macd.get("macd", 0)
        signal_value = macd.get("signal", 0)
        histogram = macd.get("histogram", 0)


        if macd_value > signal_value:
            score += 25
            reasons.append("MACD POZİTİF")

        elif histogram > 0:
            score += 10
            reasons.append("MACD TOPARLANMA")

        elif abs(macd_value - signal_value) < abs(signal_value) * 0.20:
            score += 5
            reasons.append("MACD YAKLAŞIYOR")


    # Hacim
    volume_ratio = data.get("volume_ratio", 0)

    if volume_ratio >= 1.5:
        score += 15
        reasons.append("GÜÇLÜ HACİM")

    elif volume_ratio >= 1.2:
        score += 10
        reasons.append("HACİM ARTIŞI")


    # Breakout
    if data.get("breakout", False):
        score += 15
        reasons.append("BREAKOUT")


    score = min(score, 100)


    # Sinyal sistemi
    if score >= 90:
        signal = "🚀 STRONG BUY"

    elif score >= 75:

        if (
            data.get("volume_spike", False)
            or data.get("breakout_strength", 0) >= 0.10
        ):
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

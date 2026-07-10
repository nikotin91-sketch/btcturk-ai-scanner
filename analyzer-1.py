from config import MIN_AI_SCORE.

def calculate_score(data):
    rsi = data.get("rsi")
    if rsi is None:
        return {"score":0,"signal":"⚪ WAIT","reasons":["YETERSİZ VERİ"]}

    score = 0
    reasons = []

    if 50 <= rsi <= 65:
        score += 20
        reasons.append("RSI GÜÇLÜ")
    elif 40 <= rsi < 50:
        score += 10
        reasons.append("RSI TOPARLANMA")
    elif rsi > 70:
        score -= 10
        reasons.append("RSI AŞIRI ALIM")
    elif rsi < 35:
        score -= 10
        reasons.append("RSI ZAYIF")

    ema9 = data.get("ema9", 0)
    ema21 = data.get("ema21", 0)
    ema50 = data.get("ema50", 0)

    if ema9 > ema21:
        score += 25
        reasons.append("EMA TREND")
    elif ema9 > ema21 * 0.9995:
        score += 10
        reasons.append("EMA YAKLAŞIYOR")
    else:
        reasons.append("EMA ZAYIF")

    if ema9 > ema21 > ema50:
        score += 15
        reasons.append("GÜÇLÜ TREND")
    elif ema9 < ema21 < ema50:
        reasons.append("DÜŞÜŞ TRENDİ")

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
        else:
            reasons.append("MACD NEGATİF")

    volume_ratio = data.get("volume_ratio", 0)
    volume_good = False
    if volume_ratio >= 2.0:
        score += 20; reasons.append("ÇOK GÜÇLÜ HACİM"); volume_good = True
    elif volume_ratio >= 1.5:
        score += 15; reasons.append("GÜÇLÜ HACİM"); volume_good = True
    elif volume_ratio >= 1.2:
        score += 10; reasons.append("HACİM ARTIŞI"); volume_good = True
    elif volume_ratio >= 1.1:
        score += 5; reasons.append("HAFİF HACİM DESTEĞİ"); volume_good = True
    elif volume_ratio < 0.5:
        score -= 20; reasons.append("ÇOK DÜŞÜK HACİM")

    breakout = data.get("breakout", False)
    if breakout:
        score += 15
        reasons.append("BREAKOUT")
    else:
        reasons.append("BREAKOUT YOK")

    trend_strength = data.get("trend_strength", 0)
    if trend_strength == 3:
        score += 10
        reasons.append("TREND ÇOK GÜÇLÜ")
    elif trend_strength == 2:
        score += 5

    if data.get("higher_tf_up", False):
        score += 10
        reasons.append("5M/15M ONAY")
    else:
        reasons.append("ÜST TF ZAYIF")

    rr = data.get("risk_reward", 0)
    if rr >= 2.5:
        score += 10
        reasons.append("RR GÜÇLÜ")
    elif rr >= 2:
        score += 5
    elif rr < 1.5:
        score -= 10
        reasons.append("RR ZAYIF")

    score = max(0, min(score, 100))

    if score >= 90 and macd_positive and volume_good and breakout and data.get("higher_tf_up", False):
        signal = "🚀 STRONG BUY"
    elif score >= 80 and macd_positive:
        signal = "🟢 BUY"
    elif score >= MIN_AI_SCORE:
        signal = "🟡 WATCH"
    else:
        signal = "⚪ WAIT"

    return {"score": score, "signal": signal, "reasons": reasons}

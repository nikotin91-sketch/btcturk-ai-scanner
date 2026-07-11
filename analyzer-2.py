from config import MIN_AI_SCORE

def calculate_score(data):
    score = 0
    reasons = []

    rsi = data.get("rsi")
    if rsi is None:
        return {"score":0,"signal":"⚪ WAIT","reasons":["YETERSİZ VERİ"]}

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

    ema9 = data.get("ema9",0)
    ema21 = data.get("ema21",0)
    ema50 = data.get("ema50",0)

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
            macd_positive = True
            reasons.append("MACD POZİTİF")
        elif macd.get("histogram",0) > 0:
            score += 10
            reasons.append("MACD TOPARLANMA")
        else:
            reasons.append("MACD NEGATİF")

    vr = data.get("volume_ratio",0)
    volume_good = False
    if vr >= 2:
        score += 20; volume_good = True; reasons.append("ÇOK GÜÇLÜ HACİM")
    elif vr >= 1.5:
        score += 15; volume_good = True; reasons.append("GÜÇLÜ HACİM")
    elif vr >= 1.2:
        score += 10; volume_good = True; reasons.append("HACİM ARTIŞI")
    elif vr >= 1.1:
        score += 5; volume_good = True; reasons.append("HAFİF HACİM")
    elif vr < 0.2:
        score -= 5
        reasons.append("DÜŞÜK HACİM")

    if data.get("breakout",False):
        score += 15
        reasons.append("BREAKOUT")
    else:
        reasons.append("BREAKOUT YOK")

    if data.get("higher_tf_up",False):
        score += 10
        reasons.append("5M/15M ONAY")

    trend = data.get("trend_strength",0)
    if trend == 3:
        score += 10
        reasons.append("TREND ÇOK GÜÇLÜ")
    elif trend == 2:
        score += 5

    rr = data.get("risk_reward",0)
    if rr >= 2.5:
        score += 10
        reasons.append("RR GÜÇLÜ")
    elif rr >= 2:
        score += 5
    elif rr and rr < 1.5:
        score -= 10
        reasons.append("RR ZAYIF")

    score = max(0,min(score,100))

    if score >= 90 and macd_positive and volume_good and data.get("breakout",False):
        signal = "🚀 STRONG BUY"
    elif score >= 80 and macd_positive:
        signal = "🟢 BUY"
    elif score >= MIN_AI_SCORE:
        signal = "🟡 WATCH"
    else:
        signal = "⚪ WAIT"

    return {"score":score,"signal":signal,"reasons":reasons}

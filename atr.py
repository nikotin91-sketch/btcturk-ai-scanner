def atr(high, low, close, period=14):

    if len(close) < period + 1:
        return None

    tr = []

    for i in range(1, len(close)):
        tr.append(max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1])
        ))

    return sum(tr[-period:]) / period

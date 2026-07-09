def ema(prices, period):
    """
    Exponential Moving Average (EMA)
    prices: kapanış fiyatları listesi
    period: örn. 9, 21, 50
    """

    if len(prices) < period:
        return []

    multiplier = 2 / (period + 1)

    ema_values = []

    sma = sum(prices[:period]) / period
    ema_values.append(sma)

    for price in prices[period:]:
        ema_now = (price - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema_now)

    return ema_values

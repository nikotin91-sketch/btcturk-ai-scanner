import math


def ema(prices, period):
    """
    Exponential Moving Average
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


def rsi(prices, period=14):
    """
    Relative Strength Index
    """

    if len(prices) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, period + 1):

        change = prices[i] - prices[i - 1]

        if change >= 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    for i in range(period + 1, len(prices)):

        change = prices[i] - prices[i - 1]

        gain = max(change, 0)
        loss = abs(min(change, 0))

        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(prices, fast=12, slow=26, signal=9):
    """
    MACD (Moving Average Convergence Divergence)
    """

    if len(prices) < slow + signal:
        return None

    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)

    offset = len(ema_fast) - len(ema_slow)
    ema_fast = ema_fast[offset:]

    macd_line = [
        fast_val - slow_val
        for fast_val, slow_val in zip(ema_fast, ema_slow)
    ]

    signal_line = ema(macd_line, signal)

    if not signal_line:
        return None

    macd_value = macd_line[-1]
    signal_value = signal_line[-1]

    return {
        "macd": macd_value,
        "signal": signal_value,
        "histogram": macd_value - signal_value
    }

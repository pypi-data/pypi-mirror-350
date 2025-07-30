from numba import njit
import numpy as np
from rexilion.backtest.formula_numba import (
    rolling_mean,
    rolling_ema,
    rolling_wma
)

# Mode IDs
MODE_MR = 0
MODE_MR_0 = 1
MODE_0_SIDELINE = 2
MODE_MOMENTUM = 3
MODE_MOMENTUM_SIDELINE = 4
MODE_MOMENTUM_0 = 5
MODE_MR_SMA = 6
MODE_MR_EMA = 7
MODE_MR_WMA = 8
MODE_MOMENTUM_SMA = 9
MODE_MOMENTUM_EMA = 10
MODE_MOMENTUM_WMA = 11

@njit(cache=True)
def entry_exit_threshold(
    processed: np.ndarray,
    rolling_window: int,
    threshold: float,
    mode_id: int
) -> np.ndarray:
    n = processed.shape[0]
    pos = np.empty(n, np.int8)
    # initialize
    for i in range(rolling_window):
        pos[i] = 0

    # precompute SMA/EMA/WMA when needed
    sma = np.empty(0, np.float64)
    ema = np.empty(0, np.float64)
    wma = np.empty(0, np.float64)
    if mode_id in (MODE_MR_SMA, MODE_MOMENTUM_SMA):
        sma = rolling_mean(processed, rolling_window)
    elif mode_id in (MODE_MR_EMA, MODE_MOMENTUM_EMA):
        ema = rolling_ema(processed, rolling_window)
    elif mode_id in (MODE_MR_WMA, MODE_MOMENTUM_WMA):
        wma = rolling_wma(processed, rolling_window)

    # main loop
    for i in range(rolling_window, n):
        x = processed[i]
        prev = pos[i-1]
        # mean-reversion
        if mode_id == MODE_MR:
            if x < -threshold:
                pos[i] = 1
            elif x > threshold:
                pos[i] = -1
            else:
                pos[i] = prev
        # mr_0
        elif mode_id == MODE_MR_0:
            if x < -threshold:
                pos[i] = 1
            elif x > threshold:
                pos[i] = -1
            elif (x >= 0 and prev == 1) or (x <= 0 and prev == -1):
                pos[i] = 0
            else:
                pos[i] = prev
        # 0_sideline
        elif mode_id == MODE_0_SIDELINE:
            if 0 < x < threshold:
                pos[i] = 1
            elif 0 > x > -threshold:
                pos[i] = -1
            elif ((x >= threshold and prev == 1) or
                  (x <= -threshold and prev == -1)):
                pos[i] = 0
            else:
                pos[i] = prev
        # momentum
        elif mode_id == MODE_MOMENTUM:
            if x < -threshold:
                pos[i] = -1
            elif x > threshold:
                pos[i] = 1
            else:
                pos[i] = prev
        # momentum_0
        elif mode_id == MODE_MOMENTUM_0:
            if x < -threshold:
                pos[i] = -1
            elif x > threshold:
                pos[i] = 1
            elif (x <= 0 and prev == 1) or (x >= 0 and prev == -1):
                pos[i] = 0
            else:
                pos[i] = prev
        # mr(sma)
        elif mode_id == MODE_MR_SMA:
            m = sma[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = -1
            elif x < lo:
                pos[i] = 1
            else:
                pos[i] = prev
        # momentum(sma)
        elif mode_id == MODE_MOMENTUM_SMA:
            m = sma[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = 1
            elif x < lo:
                pos[i] = -1
            else:
                pos[i] = prev
        # mr(ema)
        elif mode_id == MODE_MR_EMA:
            m = ema[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = -1
            elif x < lo:
                pos[i] = 1
            else:
                pos[i] = prev
        # momentum(ema)
        elif mode_id == MODE_MOMENTUM_EMA:
            m = ema[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = 1
            elif x < lo:
                pos[i] = -1
            else:
                pos[i] = prev
        # mr(wma)
        elif mode_id == MODE_MR_WMA:
            m = wma[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = -1
            elif x < lo:
                pos[i] = 1
            else:
                pos[i] = prev
        # momentum(wma)
        elif mode_id == MODE_MOMENTUM_WMA:
            m = wma[i]
            if m > 0:
                up = m * (1 + threshold)
                lo = m * (1 - threshold)
            else:
                up = m * (1 - threshold)
                lo = m * (1 + threshold)
            if x > up:
                pos[i] = 1
            elif x < lo:
                pos[i] = -1
            else:
                pos[i] = prev
        else:
            # default: hold
            pos[i] = prev
    return pos

@njit(cache=True)
def entry_exit_band(
    data: np.ndarray,
    upper: np.ndarray,
    lower: np.ndarray,
    sma: np.ndarray,
    ema: np.ndarray,
    wma: np.ndarray,
    rolling_window: int,
    mode_id: int
) -> np.ndarray:
    n = data.shape[0]
    pos = np.empty(n, np.int8)
    for i in range(rolling_window):
        pos[i] = 0
    for i in range(rolling_window, n):
        x = data[i]
        prev = pos[i-1]
        up = upper[i]
        lo = lower[i]
        if mode_id == MODE_MR:
            if x < lo:
                pos[i] = 1
            elif x > up:
                pos[i] = -1
            else:
                pos[i] = prev
        elif mode_id == MODE_MR_SMA:
            m = sma[i]
            if (x < lo): pos[i] = 1
            elif (x > up): pos[i] = -1
            elif ((x >= m and prev == 1) or (x <= m and prev == -1)): pos[i] = 0
            else: pos[i] = prev
        elif mode_id == MODE_MR_EMA:
            m = ema[i]
            if (x < lo): pos[i] = 1
            elif (x > up): pos[i] = -1
            elif ((x >= m and prev == 1) or (x <= m and prev == -1)): pos[i] = 0
            else: pos[i] = prev
        elif mode_id == MODE_MR_WMA:
            m = wma[i]
            if (x < lo): pos[i] = 1
            elif (x > up): pos[i] = -1
            elif ((x >= m and prev == 1) or (x <= m and prev == -1)): pos[i] = 0
            else: pos[i] = prev
        elif mode_id == MODE_MOMENTUM:
            if x > up:
                pos[i] = 1
            elif x < lo:
                pos[i] = -1
            else:
                pos[i] = prev
        else:
            pos[i] = prev
    return pos

@njit(cache=True)
def entry_exit_macd(
    macd: np.ndarray,
    signal: np.ndarray,
    rolling_window: int
) -> np.ndarray:
    n = macd.shape[0]
    pos = np.empty(n, np.int8)
    for i in range(rolling_window):
        pos[i] = 0
    for i in range(rolling_window, n):
        if macd[i] >= signal[i]:
            pos[i] = 1
        elif macd[i] <= signal[i]:
            pos[i] = -1
        else:
            pos[i] = pos[i-1]
    return pos

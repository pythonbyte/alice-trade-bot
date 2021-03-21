"""File responsible to have all the functions that do calculations."""
import pandas as pd

from datetime import datetime
from typing import List, Optional, Tuple


def calculate_values(
        close_value: float,
        total_amount: float,
        action: str,
        shares: int,
        sold_price: float,
        is_sold: bool,
    ) -> Tuple[float, int, float]:
    """Function responsible to calculate the values and assign the sold_price."""
    if action == 'buy' and shares > 0:
        sold_price = close_value

    elif action == 'sell' and shares != 0:
        if is_sold:
            total_amount += ((sold_price - close_value) * shares) * 0.20
        else:
            total_amount += ((close_value - sold_price) * shares) * 0.20
        sold_price = 0

    return total_amount, shares, sold_price


def identify_doji(
        open_value: float,
        close_value: float,
        low_value: float,
        high_value: float,
        high_doji_trigger: float,
        low_doji_trigger: float
    ) -> Optional[bool]:
    """Function to identify the pattern Doji on the candle."""
    if open_value == close_value and high_value >= close_value + high_doji_trigger:
        return True
    elif open_value == close_value and low_value <= close_value - low_doji_trigger:
        return False

    return None


def calculate_vwap(
        first_stock_values: dict,
        pv: float,
        sum_volume: float,
        actual_pv: float,
        actual_vol: float
    ) -> Tuple[float, float, float]:
    """
    Function to calculate the VWAP.

    Volume-weighted average price(VWAP)
    """
    if not pv:
        avg_stock_price = (first_stock_values['C'] + first_stock_values['H'] + first_stock_values['L']) / 3
        pv =  avg_stock_price * first_stock_values['V']
        sum_volume = first_stock_values['V']
        vwap = pv / first_stock_values['V']
    else:
        pv += actual_pv
        sum_volume += actual_vol

        vwap = pv / sum_volume

    return vwap, pv, sum_volume


def calculate_mov_avg(
        candles_list: List[dict],
        field: str = 'close',
        period: int = 20
    ) -> float:
    """Function to calculte moving average."""
    mov_avg = 0.

    df = pd.DataFrame(candles_list, columns=['T','C', 'O', 'L', 'H', 'V'])
    values = df.iloc[-(period + 1): -1]

    if field == 'min':
        min_values = [i['L'] for _, i in values.iterrows()]
        mov_avg = sum(min_values)/period

    elif field == 'max':
        high_values = [i['H'] for _, i in values.iterrows()]
        mov_avg = sum(high_values)/period

    elif field == 'close':
        close_values = [i['C'] for _, i in values.iterrows()]
        mov_avg = sum(close_values)/period

    return mov_avg


def calculate_ema(
        closing_price: float,
        max_mov_avg: float,
        ema: float = 0.,
        period: int = 9
    ) -> float:
    """
    Function to calculate the EMA.

    Exponential Moving Averga(EMA)
    """
    ema_mov_avg = 0.
    weighted_mult = 2 / (period + 1)

    if ema == 0. :
        ema_mov_avg = (closing_price - max_mov_avg ) * weighted_mult + max_mov_avg
    elif ema:
        ema_mov_avg = (closing_price - ema ) * weighted_mult + ema

    return ema_mov_avg


def calculate_block_buying(
        df: pd.DataFrame,
        end_index: int,
        vwap: float,
        field: str,
        period: int = 60
    ) -> bool:
    """Strategy to block buying stocks in certain hours of the day."""
    start_index = end_index - period
    start = start_index if start_index >= period else 0

    values = df.iloc[start: start + period]

    if len(values) < 60 :
        return False

    if field == 'max':
        for _,i in values.iterrows():
            if i['C'] > vwap or datetime.strptime(i['T'], "%Y-%m-%d %H:%M:%S").hour == 12:
                return False
        return True

    elif field == 'min':
        for _,i in values.iterrows():
            if i['C'] < vwap or datetime.strptime(i['T'], "%Y-%m-%d %H:%M:%S").hour == 12:
                return False
        return True

    return False

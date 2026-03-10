import os
from pathlib import Path
import pandas as pd
import pandas_ta as ta

SL = 0.0029
TRAILING_SL = 2 * SL


def get_signal(r):
    signal = False
    if r['open_s1'] < r['close_s1'] <= r['high_s1'] - 0.1 and (r['Open'] < r['Close'] == r['High'] and r['High'] > r['high_s1']):
        # Nen 01 xanh va co bong nen tren
        # Nen 02(hien tai) xanh va khong co bong nen tren + High nen 02 > High nen 01
        signal = True
    return signal

def define_trap(df: pd.DataFrame):
    df['is_trap'] = None
    for i, row in df.iterrows():
        if row['signal'] == True:
            is_trap = False
            current_date = row.name.strftime('%Y-%m-%d ').format()
            current_time = row.name
            entry_price = row['Close']
            data_to_end_day = df[(df.index > current_time) & (df.index < current_date+' 14:30:00')]
            max_price = entry_price
            min_price = entry_price
            for k, wrow in data_to_end_day.iterrows():
                if wrow['Low'] < min_price:
                    min_price = wrow['Low']
                if wrow['High'] > max_price:
                    max_price = wrow['High']
                if max_price >= entry_price * (1 + TRAILING_SL):
                    is_trap = False
                    break
                if min_price < entry_price * (1 - SL): # Force SL
                    is_trap = True
                    break
            df.at[i, 'is_trap'] = is_trap
    return df

def prepare_data(df: pd.DataFrame):
    df['open_s1'] = df['Open'].shift(1)
    df['close_s1'] = df['Close'].shift(1)
    df['high_s1'] = df['High'].shift(1)
    df['signal'] = df.apply(get_signal, axis=1)
    df = define_trap(df)
    return df[df.signal == True].dropna()

# dataset = pd.read_csv("https://raw.githubusercontent.com/zuongthaotn/vn-stock-data/main/VN30ps/VN30F1M_5minutes.csv", index_col='Date', parse_dates=True)
# data = prepare_data(dataset)
# print(data)
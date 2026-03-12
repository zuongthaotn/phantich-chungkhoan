import os
from pathlib import Path
import pandas as pd

def get_tf5m_ohlvc_dataset():
    notebook_path = os.getcwd()
    target_dir = Path(notebook_path).parent.parent
    csv_file = str(target_dir) + '/vn-stock-data/VN30F1M/data_ohlcv/VN30F1M_5m.csv'
    is_file = os.path.isfile(csv_file)
    if is_file:
        dataset = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
    else:
        print('remote')
        dataset = pd.read_csv("https://raw.githubusercontent.com/tempusoneps/vn-stock-data/refs/heads/main/VN30F1M/data_ohlcv/VN30F1M_5m.csv", index_col='Date', parse_dates=True)
    return dataset
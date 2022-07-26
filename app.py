from backtest_lib import BacktestLib
import pandas as pd

import multiprocessing
import os

from v1_pullback import V1Pullback
# from twel_b import twel


BACKTEST_DIR = "../backtest"
DATA_DIR = "../data"
TIMEFRAME = "10min"

def vwap(df):
    typical_price = (df.High + df.Low + df.Close) / 3
    vp = typical_price * df.vol
    total_vp = vp.cumsum()
    total_volume = df.vol.cumsum()
    return df.assign(vwap = total_vp / total_volume)

def main():
    # symbol = "NSE-ABB-EQ"
    path = '../data/10min'
    files = os.listdir(path)
    for sym in files:
        if sym.startswith('.'):
            continue
        symbol = sym.split('.csv')[0]

        if os.path.exists(f"{BACKTEST_DIR}/{TIMEFRAME}/{V1Pullback.get_str_name()}/{symbol}"):
            continue

        data = pd.read_csv(f'{DATA_DIR}/{TIMEFRAME}/{symbol}.csv')
        data['datetime'] = pd.to_datetime(data['datetime'])
        data.set_index('datetime', inplace=True)
        data = data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'})
        data = data.groupby(data.index.date, group_keys=False).apply(vwap)
        
        x = BacktestLib(symbol ,data, margin=1, initial_balance=100000)

        params_dict = {
            'sl_multiplier': range(1, 5),
            'tp_multiplier': range(1, 5)
        }

        x.do_backtest(V1Pullback, optimize=True, params_dict=params_dict)

        print(x.stats)

        print(x.get_strategy_name())

        stats = x.stats

        # MAKE REQUIRED FOLDERS
        if not os.path.exists(f"{BACKTEST_DIR}/{TIMEFRAME}"):
            os.mkdir(f"{BACKTEST_DIR}/{TIMEFRAME}")
        if not os.path.exists(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}"):
            os.mkdir(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}")
        if not os.path.exists(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}/{x.symbol}"):
            os.mkdir(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}/{x.symbol}")

        # SAVE STATS AND TRADES
        stats._trades.to_csv(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}/{x.symbol}/trades_{x.symbol}.csv")
        stats.to_csv(f"{BACKTEST_DIR}/{TIMEFRAME}/{x.strategy_name}/{x.symbol}/stats_{x.symbol}.csv")

def get_summary(folder):
    f = list()
    for (dirpath, dirnames, filenames) in os.walk("{}/".format(folder)):
        f.extend(dirnames)
        break
    folders = [ fi for fi in f if not fi.startswith(".") and not fi.startswith("__") ]
    x = BacktestLib()
    print(folders)



if __name__ == '__main__':
    # multiprocessing.set_start_method('fork')
    # main()
    get_summary(f"{BACKTEST_DIR}/{TIMEFRAME}/{V1Pullback.get_str_name()}")
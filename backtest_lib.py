from backtesting import Backtest
import numpy as np
import pandas as pd

class BacktestLib:

    def __init__(self, symbol=None, data=None, margin=1, initial_balance=10_000, commission=0, maximize='Equity Final [$]'):
        self.data = data
        self.symbol = symbol
        self.margin = margin
        self.initial_balance = initial_balance
        self.maximize = maximize
        self.commission = commission
        self.strategy_name = None
        self.backtest_class = None
        self.stats = None

    def do_backtest(self, strategy_class, optimize = False, params_dict = dict()):
        self.backtest_class = Backtest(self.data, strategy_class, margin=self.margin, 
                            cash=self.initial_balance, commission=self.commission, exclusive_orders=True)

        self.strategy_name = strategy_class.get_str_name()

        if optimize is False:
            self.stats = self.backtest_class.run()
        else:
            self.stats = self.backtest_class.optimize(
                maximize=self.maximize,
                **params_dict
            )

        # stats = bt.optimize(n1=range(5, 30, 5),
        #                     n2=range(10, 70, 5),
        #                     maximize='Equity Final [$]',
        #                     constraint=lambda param: param.n1 < param.n2)

    def save_summaries(base_path, folders):
        trades = pd.read_csv('{base_path}/trades_{}'.format(folder, stock[:-4], stock))
        trades['EntryTime'] = pd.to_datetime(trades['EntryTime'])
        trades.set_index('EntryTime', inplace=True)

        # Get monthly data
        new = trades.groupby([trades.index.year, trades.index.month])
        monthly_averages = new.aggregate({"PnL":np.sum})
        monthly_averages.to_csv('{}/{}/monthly_{}'.format(folder, stock[:-4], stock))

        # Get weekly data
        trades = pd.read_csv('{}/{}/trades_{}'.format(folder, stock[:-4], stock))
        trades['EntryTime'] = pd.to_datetime(trades['EntryTime']) - pd.to_timedelta(7, unit='d')
        new = trades.groupby([pd.Grouper(key='EntryTime', freq='W-SUN')])
        weekly_averages = new.aggregate({"PnL":np.sum})
        weekly_averages.to_csv('{}/{}/weekly_{}'.format(folder, stock[:-4], stock))

        # Get summary file
        summary = {
            'Scrip': list(),
            'Return %': list(),
            'Equity Final': list(),
            'Equity Peak': list(),
            'Trades': list(),
            'Accuracy': list(),
            'Buy/Hold Return': list(),
            'Max Drawdown': list(),
            'Max Drawdown duration': list(),
            'Best Trade': list(),
            'Worst Trade': list(),
            'Avg Trade': list(),
            'Max Trade duration': list(),
            'SQN': list()
        }
        for i in range(len(folders)):
            stats = pd.read_csv('%s/%s/stats_%s.csv' % (folder, folders[i], folders[i]))
            summary['Scrip'].append(folders[i])
            summary['Return %'].append(stats.loc[6][1])
            summary['Equity Final'].append(stats.loc[4][1])
            summary['Trades'].append(stats.loc[17][1])
            summary['Accuracy'].append(stats.loc[18][1])
            summary['Equity Peak'].append(stats.loc[5][1])
            summary['Buy/Hold Return'].append(stats.loc[7][1])
            summary['Max Drawdown'].append(stats.loc[13][1])
            summary['Max Drawdown duration'].append(stats.loc[15][1])
            summary['Best Trade'].append(stats.loc[19][1])
            summary['Worst Trade'].append(stats.loc[20][1])
            summary['Avg Trade'].append(stats.loc[21][1])
            summary['Max Trade duration'].append(stats.loc[22][1])
            summary['SQN'].append(stats.loc[26][1])

    def get_stats(self):
        return self.stats

    def get_strategy_name(self):
        return self.strategy_name

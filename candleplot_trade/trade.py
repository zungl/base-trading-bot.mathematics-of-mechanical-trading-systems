from time import sleep
from .errors import *
import pandas as pd
from .simple_trade import simple_trade

class trade(simple_trade):
    def __init__(self):
        self.all_indicators = ['ivar', 'atr',
                                'macd', 'rsi', 'bollinger',
                                'aroon', 'stohasctic', 'stohasctic_sma',
                                'black_maribozu', 'white_maribozu',
                                'solders', 'crows']
        self.indicators_range = ['macd', 'rsi', 'bollinger',
                                'aroon', 'stohasctic', 'stohasctic_sma',
                                'black_maribozu', 'white_maribozu',
                                'solders', 'crows']

    def clear_stats(self):
        self.buy_sell_list = [0]*len(self.data.df) ## contains values: 1: buy, -1: sell, 0: do nothing
                                                   ## indexes refers to dates in self.data.df.index
        self.start_money = 0
        self.money = 0
        self.shares = 0
        self.income = 0
        self.operations = 0

    def organise_buy_sell(self):
        i = 0
        for idx, decision in enumerate(self.buy_sell_list):
            if i != 0:
                if prev_decision == decision:
                    self.buy_sell_list[idx] = 0
                if (decision == 1) or (decision == -1):
                    prev_decision = decision
                    # print(f'removed{self.data.df.index[idx]}')
            else:
                i = 1
                prev_decision = decision

    def count_income(self, start_idx = None, final = False):
        if start_idx is None:
            start_idx = self.start_idx
        operations = 0
        for idx in range(start_idx, len(self.data.df)):
            if (self.buy_sell_list[idx] == 1) and (self.money > 0):
                price = self.data.CLOSE[idx]
                self.shares = self.money//(price*(1+self.buy_commission))
                self.money = self.money - (self.money//price)*price
                operations += 1
            if (self.buy_sell_list[idx] == -1) and (self.shares > 0):
                price = self.data.CLOSE[idx]
                self.money += self.shares*(price*(1-self.sell_commission))
                self.shares = 0
                operations += 1
        if (self.shares != 0) and final:
            price = self.data.CLOSE[idx]
            self.money += self.shares*(price*(1-self.sell_commission))
            self.shares = 0
            operations += 1

        price = self.data.CLOSE[idx]
        self.income = (self.money + (price*(1-self.sell_commission))*self.shares) - self.start_money

        self.operations = operations
        if self.console_log:
            print(f'{"="*30}')
            print(f'Статистика по доходности:')
            print(f'Стартовый капитал: {self.start_money}')
            print(f'Текущая доходность: {self.income}')
            print(f'Кол-во операций: {operations}')
            print(f'Использованные индикаторы: {self.strategy_indicators}')

    def set_traid_strategy(self, strategy = 'simple', indicators = ['all'], money = 1000):
        self.strategy = strategy.lower()
        if self.strategy == 'simple':
            self.strategy_indicators = indicators
            self.clear_stats()
            self.money = money
            self.start_money = money
            if self.full_console_log:
                print(f'Стратегия торговли установлена на {self.strategy}')
        else:
            raise StrategyNameError(strategy)

    def trade(self, idx = -1):
        if self.strategy == 'simple':
            if self.full_console_log:
                print(f'Принятие решение по стратегии {self.strategy} на данных за {idx}, дата: {self.data.df.index[idx]}')
            self.__simple_trade_trade(idx = idx)

    def train(self, end = None, money = 10000):
        if self.strategy == 'simple':
            self.__simple_trade_train(money = money,end = end)

    def trade_several(self, start_idx = None, plot = True):
        if start_idx is None:
            start_idx = self.start_idx
        self.start_line = start_idx
        if self.strategy == 'simple':
            if self.full_console_log:
                print(f'Торговля по датам, начиная с {self.data.df.index[start_idx]} по стратегии {self.strategy}')
            for idx in range(start_idx, len(self.data.df)):
                self.trade(idx = idx)
            self.organise_buy_sell()
            self.count_income(start_idx = start_idx, final = True)
            if plot:
                self.plot()

    def start(self, refresh_time = 10, get_period = None):
        self.get_period = get_period
        if self.strategy is None:
            raise NoStrategyError
        self.trade()
        self.plot()
        while True:
            new_data = self.data.update_data(period=self.get_period)
            if new_data is not None:
                if len(new_data) > 2:
                    print(f'Было получено {len(new_data)-1} новых значений за раз! Уменьшите refresh_time!')
                if self.console_log or self.full_console_log:
                    print(f'Данные о цене за {list(new_data[:-1].index)}')
                self.trade()
                self.organise_buy_sell()
                self.count_income(start_idx = self.start_idx)
                if self.html_log:
                    self.plot()
                if self.console_log:
                    print(f'{"="*30}')
            else:
                if self.full_console_log:
                    print(f'изменений нет')
                    print(f'{"="*30}')
            sleep(refresh_time)

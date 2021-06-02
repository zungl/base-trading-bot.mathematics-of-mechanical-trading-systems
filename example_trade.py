from errors import *
import pandas as pd

class simple_trade():
    def __init__(self):
        pass
    def __simple_trade_trade(self):
        self.indicators.load_data(self.data)
        if self.full_console_log:
            print('Торгуем...')

    def __simple_trade_train(self, end = None):
        if self.full_console_log:
            print(f'Обучение стратегии {self.strategy}')

    def __simple_trade_train_test(self, test_size = test_size, plot = plot):
        if self.full_console_log:
            print(f'Тестирование стратегии {self.strategy}')
        self.train(end = int(len(self.data.df)*test_size))

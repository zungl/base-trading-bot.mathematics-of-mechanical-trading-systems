import numpy as np
import pandas as pd
import yfinance as yf

class data_class():
    def __init__(self, ticker, interval, full_console_log):
        self.ticker = ticker
        self.interval = interval
        self.full_console_log = full_console_log

    def get_data(self, start = None, period = None):
        if self.full_console_log:
            print(f'Получение данных о цене {self.ticker}...')
        ticker = self.ticker
        tickerData = yf.Ticker(ticker)
        new_data = tickerData.history(interval = self.interval, start=start, period = period)
        if self.full_console_log:
            print(f'Данные получены. Кол-во наблюдений: {len(new_data)-1}')
        return new_data

    def load_data(self, df):
        self.df = df.copy()
        ## Шкалированные данные
        ## Для нахождения фигур будут исользоваться шкалированные данные
        ## Для построения графиков - исходные
        # self.OPEN = (self.df.Open - np.min(self.df.Open))/(np.max(self.df.Open) -
        #                                                                np.min(self.df.Open))
        # self.CLOSE = (self.df.Close - np.min(self.df.Close))/(np.max(self.df.Close) -
        #                                                                   np.min(self.df.Close))
        # self.LOW = (self.df.Low - np.min(self.df.Low))/(np.max(self.df.Low) -
        #                                                             np.min(self.df.Low))
        # self.HIGH = (self.df.High - np.min(self.df.High))/(np.max(self.df.High) -
        #                                                                np.min(self.df.High))
        # self.DATE = np.array(df.index)

        self.OPEN = self.df.Open
        self.CLOSE = self.df.Close
        self.LOW = self.df.Low
        self.HIGH =  self.df.High

        ## Создаём списик экстремумов
        self.__local_extrems()

    def update_data(self, period = None):
        if self.full_console_log:
            print(f'Последняя известная стоимость: {self.df.index[-1]}')
        if period is None:
            new_data = self.get_data(start = self.df.index[-1])
        else:
            new_data = self.get_data(period = period)
        new_data = new_data[new_data.index > self.df.index[-1]]
        if len(new_data) > 1:
            self.load_data(pd.concat([self.df, new_data[:-1]]))
            return new_data
        else:
            return None

    def __local_extrems(self):
        '''
        Находит и сохраняет в классе списк локальных
        максимумов и минимумов

        Сохраняет списки внутри класса:
        self.local_<type>_min - индексы минимумов
        (даты, когда цена в следующий и предыдущий день были выше текущей)

        self.local_<type>_max - индексы максимумов
        (даты, когда цена в следующий и предыдущий день были ниже текущей)
        где type: body (тело свечи), high, low
        '''
        self.body_top_original = np.maximum(self.df.Open, self.df.Close)
        self.body_down_original = np.minimum(self.df.Open, self.df.Close)

        # self.body_top = np.maximum(self.OPEN, self.CLOSE)
        # self.body_down = np.minimum(self.OPEN, self.CLOSE)
        #
        # self.local_body_min = (self.body_down <= np.concatenate([[max(self.body_down)],
        #                                                          self.body_down[:-1]])) & (self.body_down <
        #                                                 np.concatenate([self.body_down[1:], [max(self.body_down)]]))
        # self.local_body_min = np.where(self.local_body_min==True)[0]
        #
        # self.local_body_max = (self.body_top >= np.concatenate([[0], self.body_top[:-1]])) & (self.body_top >
        #                                                 np.concatenate([self.body_top[1:], [0]]))
        # self.local_body_max = np.where(self.local_body_max==True)[0]
        #
        # self.local_high_max = (self.HIGH >= np.concatenate([[0], self.HIGH[:-1]])) & (self.HIGH >
        #                                                 np.concatenate([self.HIGH[1:], [0]]))
        # self.local_high_max = np.where(self.local_high_max==True)[0]
        #
        # self.local_low_min = (self.LOW <= np.concatenate([[max(self.LOW)], self.LOW[:-1]])) & (self.LOW <
        #                                                 np.concatenate([self.LOW[1:], [max(self.LOW)]]))
        # self.local_low_min = np.where(self.local_low_min==True)[0]


    def rolling(self, data, m = 4):

        data = list(data)
        data_new = []
        for i in range(len(data) - m):
            data_new.append(sum(data[i:i + m])/m)

        return data_new

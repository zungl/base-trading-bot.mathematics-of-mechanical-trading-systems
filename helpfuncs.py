import numpy as np
import pandas as pd

class helpfuncs():
    def __init__(self, df):
        pass

    def preprocessing(self, df):
        self.df = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<DATE>']].reset_index()

        ## Шкалированные данные
        ## Для нахождения фигур будут исользоваться шкалированные данные
        ## Для построения графиков - исходные
        self.OPEN = (self.df['<OPEN>'] - np.min(self.df['<OPEN>']))/(np.max(self.df['<OPEN>']) -
                                                                       np.min(self.df['<OPEN>']))
        self.CLOSE = (self.df['<CLOSE>'] - np.min(self.df['<CLOSE>']))/(np.max(self.df['<CLOSE>']) -
                                                                          np.min(self.df['<CLOSE>']))
        self.LOW = (self.df['<LOW>'] - np.min(self.df['<LOW>']))/(np.max(self.df['<LOW>']) -
                                                                    np.min(self.df['<LOW>']))
        self.HIGH = (self.df['<HIGH>'] - np.min(self.df['<HIGH>']))/(np.max(self.df['<HIGH>']) -
                                                                       np.min(self.df['<HIGH>']))

        self.DATE = np.array(df['<DATE>'])

        # ## создание маски свечей
        # self.red_candles = [True if x[0] > x[1] else False
        #                  for x in zip(self.OPEN, self.CLOSE)]
        # self.green_candles = [False if x[0] > x[1] else True
        #                  for x in zip(self.OPEN, self.CLOSE)]

        ## Создаём списик экстремумов
        self.__local_extrems()


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
        self.body_top_original = np.maximum(self.df['<OPEN>'], self.df['<CLOSE>'])
        self.body_down_original = np.minimum(self.df['<OPEN>'], self.df['<CLOSE>'])

        self.body_top = np.maximum(self.OPEN, self.CLOSE)
        self.body_down = np.minimum(self.OPEN, self.CLOSE)

        self.local_body_min = (self.body_down <= np.concatenate([[max(self.body_down)],
                                                                 self.body_down[:-1]])) & (self.body_down <
                                                        np.concatenate([self.body_down[1:], [max(self.body_down)]]))
        self.local_body_min = np.where(self.local_body_min==True)[0]

        self.local_body_max = (self.body_top >= np.concatenate([[0], self.body_top[:-1]])) & (self.body_top >
                                                        np.concatenate([self.body_top[1:], [0]]))
        self.local_body_max = np.where(self.local_body_max==True)[0]

        self.local_high_max = (self.HIGH >= np.concatenate([[0], self.HIGH[:-1]])) & (self.HIGH >
                                                        np.concatenate([self.HIGH[1:], [0]]))
        self.local_high_max = np.where(self.local_high_max==True)[0]

        self.local_low_min = (self.LOW <= np.concatenate([[max(self.LOW)], self.LOW[:-1]])) & (self.LOW <
                                                        np.concatenate([self.LOW[1:], [max(self.LOW)]]))
        self.local_low_min = np.where(self.local_low_min==True)[0]


    def rolling(self, data, m = 4):

        data = list(data)
        data_new = []
        for i in range(len(data) - m):
            data_new.append(sum(data[i:i + m])/m)

        return data_new

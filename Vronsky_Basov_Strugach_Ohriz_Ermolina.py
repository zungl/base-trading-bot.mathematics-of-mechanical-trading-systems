import pandas as pd
import numpy as np

# from scipy.optimize import curve_fit

from plot import plot_class
from figures import figures
from indicators import indicators
from candles import candles
from trade import trade

class candleplotfigures(plot_class, trade):
    def __init__(self):
        '''
    Определение и отрисовка фигур на графике свечей

    Параметры инициализации:
    df - pd.DataFrame() c атрибутами: <OPEN>, <CLOSE>,
                                <HIGH>, <LOW>, <DATE>
         формат даты - DD/MM/YY
    title - название компании (или название индекса)

    Поддерживаемые фигуры:
    ##TODO
    '''
    def __init__(self,
                 df,
                 title = ''):

        self.df = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<DATE>']].reset_index()
        ## Исходные данные
        self.OPEN_original = np.array(df['<OPEN>'])
        self.CLOSE_original = np.array(df['<CLOSE>'])
        self.LOW_original = np.array(df['<LOW>'])
        self.HIGH_original = np.array(df['<HIGH>'])
        self.DATE = np.array(df['<DATE>'])
        self.title = title

        ## Создаю экземляры классов - обработчики
        self.fugures = figures(df)
        self.indicators = indicators(df)
        self.candles = candles(df)

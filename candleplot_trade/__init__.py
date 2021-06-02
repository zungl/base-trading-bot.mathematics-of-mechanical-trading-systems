import pandas as pd
import numpy as np

from .errors import *
from .params import *
from .plot import plot_class
from .figures import figures
from .indicators import indicators
from .candles import candles
from .trade import trade
from .helpfuncs import data_class

class candleplotfigures(plot_class, trade, data_class):
    '''
Определение и отрисовка фигур на графике свечей

Параметры инициализации:
title - название компании (или название индекса)

df - pd.DataFrame()
Поддерживаемые фигуры:
##TODO
    '''
    def __init__(self,
                 df = None,
                 ticker = None,
                 start = None,
                 end = None,
                 title = '',
                 period = None,
                 interval = None,
                 console_log = True,
                 full_console_log =False,
                 txt_log = True,
                 html_log = False,
                 buy_commission = 0,
                 sell_commission = 0,
                 return_plot = True,
                 save_html = False,
                 text_size = 8):
        super().__init__()
        self.text_size = text_size
        self.return_plot = return_plot
        self.save_html = save_html
        self.strategy = None
        self.ticker = ticker
        self.interval = interval
        self.console_log = console_log
        self.full_console_log = full_console_log
        self.txt_log = txt_log
        self.html_log = html_log
        self.buy_commission = buy_commission
        self.sell_commission = sell_commission
        ## экземляр класса с данными
        self.data = data_class(ticker=ticker, interval=self.interval, full_console_log = self.full_console_log)
        if df != None:
            self.df = df[['Open', 'High', 'Low', 'Close']].reset_index()
        elif ticker != None:
            df = self.data.get_data(start=start, period=period)[:-1]
            self.start_idx = len(df)-1
            self.start_line = self.start_idx-1
        else:
            raise DataError()

        ## Выполняем необходимую предобработку
        self.data.load_data(df)
        self.clear_stats()

        if title == '':
            title = str(ticker)
        self.title = title

        ## экземляры классов - обработчики
        self.fugures = figures(self.data, indicator_params)
        self.indicators = indicators(self.data, indicator_params)
        self.candles = candles(self.data, candles_params)

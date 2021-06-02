# from helpfuncs import helpfuncs
import pandas as pd
import numpy as np
from decisions import *

class indicators(indicators_decision):
    def __init__(self, data, indicator_params):
        self.indicator_params = indicator_params()
        self.load_data(data)

    def refresh_indicators(self):
        self.atr()
        self.macd()
        self.rsi()
        self.bollinger()
        self.ivar()
        self.aroon()
        self.stohasctic()
        self.income()

    def load_data(self, data):
        self.data = data
        self.size = len(self.data.df)
        self.refresh_indicators()

    def reshape(self, data, size):
        new_data = [np.nan]*size
        for i, el in enumerate(data[::-1],1):
            new_data[size - i] = el
        return new_data

    def atr(self, TR = None):
        '''
        Average true range
        '''
        if TR is None:
            TR = self.indicator_params.atr_TR
        else:
            self.indicator_params.atr_TR = TR
        self.truerange = []
        for i in range(1, len(self.data.CLOSE)):
            self.truerange.append(float(max(self.data.HIGH[i] - self.data.LOW[i],
                                self.data.HIGH[i] - self.data.CLOSE[i-1],
                                self.data.CLOSE[i-1] - self.data.LOW[i])))
        self.truerange = self.reshape(self.truerange, self.size)
        self.atr_plots = []
        for m in TR:
            self.atr_plots.append(self.reshape(self.data.rolling(data = self.truerange, m = m), self.size))


    def macd(self, EMA1 = None, EMA2 = None, EMA_signal = None):
        if EMA1 is None:
            EMA1 = self.indicator_params.macd_ema1
        else:
            self.indicator_params.macd_ema1 = EMA1
        if EMA2 is None:
            EMA2 = self.indicator_params.macd_ema2
        else:
            self.indicator_params.macd_ema2 = EMA2
        if EMA_signal is None:
            EMA_signal = self.indicator_params.macd_ema_signal
        else:
            self.indicator_params.macd_ema_signal = EMA_signal
        self.macd_plot = pd.Series.ewm(self.data.df.Close, span=EMA1).mean() - pd.Series.ewm(self.data.df.Close, span=EMA2).mean() #MCAD
        self.macd_ema_signal = pd.Series.ewm(self.macd_plot, span=EMA_signal).mean() #signal
        self.macd_hist = self.macd_ema_signal - self.macd_plot
        self.macd_plot = self.reshape(self.macd_plot, self.size)
        self.macd_hist = self.reshape(self.macd_hist, self.size)
        self.macd_ema_signal = self.reshape(self.macd_ema_signal, self.size)
        # self.macd_buy = [0] + [1 if (self.MACD_hist[i-1]>0) and (self.MACD_hist[i]<0) else 0 for i in range(1, len(self.MACD_hist))]
        # self.macd_sell = [0] + [1 if (self.MACD_hist[i-1]<0) and (self.MACD_hist[i]>0) else 0 for i in range(1, len(self.MACD_hist))]

    def rsi(self, EMA1 = None, EMA2 = None):
        if EMA1 is None:
            EMA1 = self.indicator_params.rsi_ema1
        else:
            self.indicator_params.rsi_ema1 = N
        if EMA2 is None:
            EMA2 = self.indicator_params.rsi_ema2
        else:
            self.indicator_params.rsi_ema2 = EMA2
        self.data.df['SMA_M'] = self.data.df.Close.rolling(window = EMA2).mean()
        self.data.df['U']=[0]+ [self.data.df.Close[i] - self.data.df.Close[i-1] for i in range(1,len(self.data.df))]
        self.data.df['D']=[0] + [self.data.df.Close[i-1] - self.data.df.Close[i] for i in range(1,len(self.data.df))]
        pd.options.mode.chained_assignment = None
        for i in range(len(self.data.df['U'])):
            if self.data.df['U'][i] <= 0:
                self.data.df['U'][i]=0
        for i in range(len(self.data.df['D'])):
            if self.data.df['D'][i] <= 0:
                self.data.df['D'][i]=0
        self.data.df['RS']=self.data.df['U'].rolling(window = EMA1).mean()/self.data.df['D'].rolling(window = EMA1).mean()
        self.rsi_plot=100-100/(1+self.data.df['RS'])
        self.rsi_plot = self.reshape(self.rsi_plot, self.size)

    def std_window(self, WINDOW = 20):
        std = [np.std(x) for x in self.data.df.Close.rolling(window = WINDOW)][:]
        self.std = std

    def bollinger(self, WINDOW = None, K = None):
        if K is None:
            K = self.indicator_params.bollinger_k
        else:
            self.indicator_params.bollinger_k = K
        if WINDOW is None:
            WINDOW = self.indicator_params.bollinger_window
        else:
            self.indicator_params.bollinger_window = WINDOW
        self.std_window(WINDOW)
        self.bollinger_sma_m = list(self.data.df.Close.rolling(window = WINDOW).mean())
        self.bollinger_sma_u = [self.bollinger_sma_m[i] + self.std[i] * K for i in range(len(self.std))]
        self.bollinger_sma_l = [self.bollinger_sma_m[i] - self.std[i] * K for i in range(len(self.std))]
        self.bollinger_sma_m = self.reshape(self.bollinger_sma_m, self.size)
        self.bollinger_sma_u = self.reshape(self.bollinger_sma_u, self.size)
        self.bollinger_sma_l = self.reshape(self.bollinger_sma_l, self.size)

    def ivar(self, WINDOW = None):
        if WINDOW is None:
            WINDOW = self.indicator_params.ivar_window
        else:
            self.indicator_params.ivar_window = WINDOW
        self.ivar_plot = [np.std(x) for x in self.data.df.Close.rolling(window = WINDOW)][WINDOW-1:]
        self.ivar_plot = 1-self.ivar_plot/np.max(self.ivar_plot)
        self.ivar_plot = self.reshape(self.ivar_plot, self.size)

    def aroon(self, WINDOW = None):
        if WINDOW is None:
            WINDOW = self.indicator_params.aroon_window
        else:
            self.indicator_params.aroon_window = WINDOW
        self.aroon_up = [(WINDOW- (WINDOW - (np.argmax(x))))*100/WINDOW for x in self.data.df.High.rolling(window = WINDOW + 1)]
        self.aroon_down = [(WINDOW - (WINDOW - (np.argmin(x))))*100/WINDOW for x in self.data.df.Low.rolling(window = WINDOW + 1)]
        self.aroon_up = self.reshape(self.aroon_up, self.size)
        self.aroon_down = self.reshape(self.aroon_down, self.size)

    def stohasctic(self, WINDOW = None, EMA1 = None, EMA2 = None):
        if WINDOW is None:
            WINDOW = self.indicator_params.stohasctic_window
        else:
            self.indicator_params.stohasctic_window = WINDOW
        if EMA1 is None:
            EMA1 = self.indicator_params.stohasctic_ema1
        else:
            self.indicator_params.stohasctic_ema1 = EMA1
        if EMA2 is None:
            EMA2 = self.indicator_params.stohasctic_ema2
        else:
            self.indicator_params.stohasctic_ema2 = EMA2
        self.stohasctic_plot = []
        for idx in range(WINDOW, self.size):
            # print(f'Числитель: {self.data.CLOSE[idx]-np.min(self.data.LOW[idx-WINDOW:idx])}')
            # print(f'Знаменатель: {max(self.data.HIGH[idx-WINDOW:idx])-min(self.data.LOW[idx-WINDOW:idx])}')
            value = 100*((self.data.CLOSE[idx]-np.min(self.data.LOW[idx-WINDOW:idx+1])) / (max(self.data.HIGH[idx-WINDOW:idx+1])-min(self.data.LOW[idx-WINDOW:idx+1])))
            self.stohasctic_plot.append(value)
        self.stohasctic_sma1_plot = self.data.rolling(data = self.stohasctic_plot, m = EMA1)
        self.stohasctic_sma2_plot = self.data.rolling(data = self.stohasctic_sma1_plot, m = EMA2)
        self.stohasctic_plot = self.reshape(self.stohasctic_plot, self.size)
        self.stohasctic_sma1_plot = self.reshape(self.stohasctic_sma1_plot, self.size)
        self.stohasctic_sma2_plot = self.reshape(self.stohasctic_sma2_plot, self.size)

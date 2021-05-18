from helpfuncs import helpfuncs
import pandas as pd
import numpy as np

class indicators(helpfuncs):
    def __init__(self, df):
        self.preprocessing(df)

    def atr(self, TR = [14, 40]):

        self.TrueRange = []

        for i in range(1, len(self.CLOSE)):
            self.TrueRange.append(max(self.HIGH[i] - self.LOW[i],
                                self.HIGH[i] - self.CLOSE[i-1],
                                self.CLOSE[i-1] - self.LOW[i]))

        self.ATR_list = []

        for m in TR:
            self.ATR_list.append(self.rolling(data = self.TrueRange, m = m))

    def macd(self, EMA1 = 12, EMA2 = 26, EMA_signal = 9):
        df = self.df
        self.MACD_plot = pd.Series.ewm(df['<CLOSE>'], span=12).mean() - pd.Series.ewm(df['<CLOSE>'], span=26).mean() #MCAD
        self.EMA_signal = pd.Series.ewm(self.MACD_plot, span=9).mean() #signal
        self.MACD_hist = self.EMA_signal - self.MACD_plot

        self.macd_buy = [0] + [1 if (self.MACD_hist[i-1]>0) and (self.MACD_hist[i]<0) else 0 for i in range(1, len(self.MACD_hist))]
        self.macd_sell = [0] + [1 if (self.MACD_hist[i-1]<0) and (self.MACD_hist[i]>0) else 0 for i in range(1, len(self.MACD_hist))]

    def rsi(self, N = 14, N1 = 20):
        df = self.df
        df['SMA_M'] = df['<CLOSE>'].rolling(window = 20).mean()
        df['U']=[0]+ [df['<CLOSE>'][i] - df['<CLOSE>'][i-1] for i in range(1,len(df))]
        df['D']=[0] + [df['<CLOSE>'][i-1] - df['<CLOSE>'][i] for i in range(1,len(df))]

        pd.options.mode.chained_assignment = None
        for i in range(len(df['U'])):
            if df['U'][i] <= 0:
                df['U'][i]=0
        for i in range(len(df['D'])):
            if df['D'][i] <= 0:
                df['D'][i]=0

        df['RS']=df['U'].rolling(window = 14).mean()/df['D'].rolling(window = 14).mean()
        self.RSI_plot=100-100/(1+df['RS'])


    def bollinger(self, N = 20, k = 2):
        df = self.df
        self.SMA_M = list(df['<CLOSE>'].rolling(window = N).mean()[N-1:])

        std = [np.std(x) for x in df['<CLOSE>'].rolling(window = N)][N-1:]
        self.std = std
        self.SMA_U = [self.SMA_M[i] + std[i] * k for i in range(len(std))]
        self.SMA_L = [self.SMA_M[i] - std[i] * k for i in range(len(std))]

    def ivar(self, m = 10):
        self.ivar_plot = [np.std(x)/np.mean(x) for x in self.df['<CLOSE>'].rolling(window = m)]

    def aroon(self, window = 14):
        self.aroon_up = [(window - (window - (np.argmax(x))))*100/window for x in self.df['<HIGH>'].rolling(window = window + 1)]
        self.aroon_down = [(window - (window - (np.argmin(x))))*100/window for x in self.df['<LOW>'].rolling(window = window + 1)]

    def stohasctic(self, window = 12, m = 3):
        self.stohasctic_plot = [(x.iloc[-1] - np.min(x))/(np.max(x) - np.min(x)) for x in self.df['<HIGH>'].rolling(window = window + 1)]
        self.stohasctic_sma_plot = self.rolling(data = self.stohasctic_plot, m = m)

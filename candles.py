import pandas as pd
import numpy as np
from decisions import *

class candles(candles_decision):
    def __init__(self, data, candles_params):
        self.params = candles_params()
        self.load_data(data)

    def load_data(self, data):
        self.data = data
        self.size = len(self.data.df)
        self.refresh_candles()

    def refresh_candles(self):
        self.black_maribozu()
        self.white_maribozu()
        self.three_white_solders()
        self.three_black_crows()

    def black_maribozu(self, percent_up = None, percent_down = None):
        self.black_maribozu_plot = []
        if percent_up is None:
            percent_up = self.params.black_maribozu_up
        else:
            self.params.black_maribozu_up = percent_up
        if percent_down is None:
            percent_down = self.params.black_maribozu_down
        else:
            self.params.black_maribozu_down = percent_down
        for idx in range(self.size):
            candle_len = self.data.OPEN[idx] - self.data.CLOSE[idx]
            if (candle_len > 0) & (((self.data.HIGH[idx] - self.data.OPEN[idx])<candle_len *
            percent_up) | ((self.data.CLOSE[idx] - self.data.LOW[idx]) < candle_len * percent_down)):
                self.black_maribozu_plot.append(-1)
            else:
                self.black_maribozu_plot.append(0)

    def white_maribozu(self, percent_up = None, percent_down = None):
        self.white_maribozu_plot = []
        if percent_up is None:
            percent_up = self.params.white_maribozu_up
        else:
            self.params.white_maribozu_up = percent_up
        if percent_down is None:
            percent_down = self.params.white_maribozu_down
        else:
            self.params.white_maribozu_down = percent_down
        for idx in range(self.size):
            candle_len = self.data.CLOSE[idx] - self.data.OPEN[idx]
            if (candle_len > 0) & (((self.data.HIGH[idx] - self.data.CLOSE[idx]) < candle_len *
            percent_up) | ((self.data.OPEN[idx] - self.data.LOW[idx]) < candle_len * percent_down)):
                self.white_maribozu_plot.append(1)
            else:
                self.white_maribozu_plot.append(0)

    def three_white_solders(self, percent = None):
        self.solders_plot = [0, 0]
        if percent is None:
            percent = self.params.three_white_solders_percent
        else:
            self.params.three_white_solders_percent = percent
        for idx in range(2, self.size):
            if (self.data.CLOSE[idx]-self.data.OPEN[idx] > 0) and (self.data.CLOSE[idx-1]-
                self.data.OPEN[idx-1] > 0) and (self.data.CLOSE[idx-2]-
                self.data.OPEN[idx-2] > 0) and (self.data.CLOSE[idx]>self.data.CLOSE[idx-1]>self.data.CLOSE[idx-2]):
                if ((self.data.CLOSE[idx-2]-self.data.OPEN[idx-2])<=(self.data.CLOSE[idx-1]-self.data.OPEN[idx-1])*(1+percent)):
                    if ((self.data.CLOSE[idx-1]-self.data.OPEN[idx-1])<=(self.data.CLOSE[idx]-self.data.OPEN[idx])*(1+percent)):
                        self.solders_plot.append(1)
                        continue
            self.solders_plot.append(0)

    def three_black_crows(self, percent = None):
        self.crows_plot = [0, 0]
        if percent is None:
            percent = self.params.three_black_crows_percent
        else:
            self.params.three_black_crows_percent = percent
        for idx in range(2, self.size):
            if (self.data.OPEN[idx]-self.data.CLOSE[idx] > 0) and (self.data.OPEN[idx-1]-
                self.data.CLOSE[idx-1] > 0) and (self.data.OPEN[idx-2]-
                self.data.CLOSE[idx-2] > 0) and (self.data.OPEN[idx]<self.data.OPEN[idx-1]<self.data.OPEN[idx-2]):
                if ((self.data.OPEN[idx-2]-self.data.CLOSE[idx-2])<=(self.data.OPEN[idx-1]-self.data.CLOSE[idx-1])*(1+percent)):
                    if ((self.data.OPEN[idx-1]-self.data.CLOSE[idx-1])<=(self.data.OPEN[idx]-self.data.CLOSE[idx])*(1+percent)):
                        self.crows_plot.append(-1)
                        continue
            self.crows_plot.append(0)



    # def example(self):
    #     if  is None:
    #          = self.indicator_params.

class indicators_decision():
    '''
    creates lists of actions by indicators:
    buy/sell/do nothing
    and
    flat/not flat
    '''
    def __init__(self):
        pass

    def income(self):
        '''
        saves values in candleplotfigures.indicators

        self.<indicator_name>_flat:
        0 - flat
        1 - not a flat

        self.<indicator_name>_income:
        -1 - sell
        0 - do nothing
        1 - buy
        '''
        ## ATR
        self.atr_flat = [0] * self.indicator_params.atr_TR[1]
        for idx in range(self.indicator_params.atr_TR[1], self.size):
            if self.atr_plots[0][idx] > self.atr_plots[1][idx]:
                self.atr_flat.append(1)
            else:
                self.atr_flat.append(0)
        ## MACD
        self.macd_income = [0]
        for idx in range(1, self.size):
            if (self.macd_hist[idx-1]<0) & (self.macd_hist[idx]>0):
                self.macd_income.append(-1)
            elif (self.macd_hist[idx-1]>0) & (self.macd_hist[idx]<0):
                self.macd_income.append(1)
            else:
                self.macd_income.append(0)
        ## RSI
        self.rsi_income = [0] * self.indicator_params.rsi_ema1
        for idx in range(self.indicator_params.rsi_ema1, self.size):
            if self.data.CLOSE[idx-1]>self.data.CLOSE[idx]:
                if self.rsi_plot[idx-1]<self.rsi_plot[idx]:
                    self.rsi_income.append(1)
                    continue
            if self.data.CLOSE[idx-1]<self.data.CLOSE[idx]:
                if self.rsi_plot[idx-1]>self.rsi_plot[idx]:
                    self.rsi_income.append(-1)
                    continue
            self.rsi_income.append(0)
        ## bollinger
        self.bollinger_income = [0] * self.indicator_params.bollinger_window
        for idx in range(self.indicator_params.bollinger_window, self.size):
            if self.data.HIGH[idx] > self.bollinger_sma_u[idx]:
                self.bollinger_income.append(-1)
                continue
            if self.data.LOW[idx] < self.bollinger_sma_l[idx]:
                self.bollinger_income.append(1)
                continue
            self.bollinger_income.append(0)

        '''
        1 - alternative action
        0 - noting
        '''
        self.bollinger_size = [0] * self.indicator_params.bollinger_window
        for idx in range(self.indicator_params.bollinger_window, self.size):
            if self.std[idx-1] > self.std[idx]:
                if self.std[idx-2] < self.std[idx-1]:
                    self.bollinger_size.append(1)
                    continue
            self.bollinger_size.append(0)

        ## ivar
        self.ivar_flat = [0]*self.indicator_params.ivar_window
        for idx in range(self.indicator_params.ivar_window, self.size):
            if self.ivar_plot[idx] > 0.5:
                self.ivar_flat.append(0)
            else:
                self.ivar_flat.append(1)

        ## aroon
        self.aroon_income = [0]*self.indicator_params.aroon_window
        for idx in range(self.indicator_params.aroon_window, self.size):
            if self.aroon_up[idx-1] < self.aroon_down[idx-1]:
                if self.aroon_up[idx] > self.aroon_down[idx]:
                    self.aroon_income.append(1)
                    continue
            if self.aroon_up[idx-1] > self.aroon_down[idx-1]:
                if self.aroon_up[idx] < self.aroon_down[idx]:
                    self.aroon_income.append(-1)
                    continue
            self.aroon_income.append(0)

        ## stohasctic
        start_idx = self.indicator_params.stohasctic_window
        self.stohasctic_income = [0]*start_idx
        for idx in range(start_idx , self.size):
            if self.stohasctic_plot[idx] > 80:
                self.stohasctic_income.append(-1)
                continue
            if self.stohasctic_plot[idx] < 20:
                self.stohasctic_income.append(1)
                continue
            self.stohasctic_income.append(0)

        start_idx = self.indicator_params.stohasctic_window + self.indicator_params.stohasctic_ema1 + self.indicator_params.stohasctic_ema1 + 1
        self.stohasctic_sma_income = [0]*start_idx
        for idx in range(start_idx , self.size):
            if self.stohasctic_sma1_plot[idx-1]<self.stohasctic_sma2_plot[idx-1]:
                if self.stohasctic_sma1_plot[idx]>self.stohasctic_sma2_plot[idx]:
                    self.stohasctic_sma_income.append(1)
                    continue
            if self.stohasctic_sma1_plot[idx-1]>self.stohasctic_sma2_plot[idx-1]:
                if self.stohasctic_sma1_plot[idx]<self.stohasctic_sma2_plot[idx]:
                    self.stohasctic_sma_income.append(-1)
                    continue
            self.stohasctic_sma_income.append(0)



class candles_decision():
    '''
    creates lists of actions by candles:
    buy/sell/do nothing
    '''
    def __init__(self):
        pass

    def income(self):
        '''
        saves values in candleplotfigures.candles

        self.<candle_name>_income:
        -1 - sell
        0 - do nothing
        1 - buy
        '''
        pass

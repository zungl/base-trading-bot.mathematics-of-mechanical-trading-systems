class indicator_params():
    '''
    Init and stores default parametres for indicators
    '''
    def __init__(self):
        self.atr_TR = [14, 40]
        self.macd_ema1 = 12
        self.macd_ema2 = 26
        self.macd_ema_signal = 9
        self.rsi_ema1 = 14
        self.rsi_ema2 = 20
        self.bollinger_window = 20
        self.bollinger_k = 2
        self.ivar_window = 10
        self.aroon_window = 14
        self.stohasctic_window = 5 ## 9 - 21 (на практике 5)
        self.stohasctic_ema1 = 3
        self.stohasctic_ema2 = 3

class candles_params():
    '''
    Init and stores default parametres for candles
    '''
    def __init__(self):
        self.black_maribozu_up = 0.02
        self.black_maribozu_down = 0.02
        self.white_maribozu_up = 0.02
        self.white_maribozu_down = 0.02
        self.three_white_solders_percent = 1.5
        self.three_black_crows_percent = 1.5

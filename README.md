# base trading bot. mathematics of mechanical trading systems
 
This simple library allows to count and to plot several indicators.

Supported indicators:
'ivar', 'atr', 'macd', 'rsi', 'bollinger', 'aroon', 'stohasctic'

Supported candles:
'black_maribozu', 'white_maribozu', 'solders', 'crows'

example of usage:
## importing
from candleplot_trade_library import candleplotfigures

## creating instance
CPF = candleplotfigures(ticker = 'BTC-USD', # 'BTC-USD', 'GOOG'<br>
                        period = "1d",<br>
                        # start= '2021-05-25 14:38:00-04:00',<br>
                        interval = "1m",<br>
                        html_log = True,<br>
                        full_console_log = True,<br>
                        buy_commission = 0.003,<br>
                        sell_commission = 0.003)
                        
## getting indicators plot
CPF.indicators.atr(TR = [14, 100])<br>
CPF.indicators.macd(EMA1 = 12, EMA2 = 26, EMA_signal = 9)<br>
CPF.indicators.rsi(N = 14, N1 = 20)<br>
CPF.indicators.bollinger(window = 10, k = 2)<br>
CPF.indicators.ivar(m = 10)<br>
CPF.indicators.aroon(window = 14)<br>
CPF.indicators.stohasctic(window = 12, m = 3)<br>
CPF.plot(['all'])<br>

## getting candle plot
CPF.candles.black_maribozu(percent_up = 0.1, percent_down = 0.1)<br>
CPF.candles.white_maribozu(percent_up = 0.1, percent_down = 0.1)<br>
CPF.candles.three_white_solders(percent = 0.5)<br>
CPF.candles.three_black_crows(percent = 0.5)<br>
CPF.plot(['white_maribozu', 'black_maribozu', 'three_white_solders', 'three_black_crows'])<br>

## getting plot for everything in library
CPF.plot(['all'])<br>
                        
## defining indicators                     
indicators = [<br>
            'ivar',<br>
            'atr',<br>
            'macd',<br>
            'rsi',<br>
            'bollinger',<br>
            'aroon',<br>
            'stohasctic',<br>
            'stohasctic_sma',<br>
            'black_maribozu', 'white_maribozu',<br>
            'solders', 'crows'<br>
            ]
            
## defining strategy (though its only one by now)
CPF.set_traid_strategy('simple', indicators = indicators, money = 300000)

## run test trade for previous periods
CPF.trade_several(start_idx = 220)

## run trade in real time
CPF.start(refresh_time = 5)


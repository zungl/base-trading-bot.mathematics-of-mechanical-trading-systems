# base trading bot. mathematics of mechanical trading systems
#This simple library allows to count and to plot several indicators.

#Supported indicators:
#'ivar', 'atr', 'macd', 'rsi', 'bollinger', 'aroon', 'stohasctic'

#Supported candles:
#'black_maribozu', 'white_maribozu', 'solders', 'crows'

#example of usage:
## importing
from candleplot_trade_library import candleplotfigures

## creating instance
CPF = candleplotfigures(ticker = 'BTC-USD', # 'BTC-USD', 'GOOG'
                        period = "1d",
                        # start= '2021-05-25 14:38:00-04:00',
                        interval = "1m",
                        html_log = True,
                        full_console_log = True,
                        buy_commission = 0.003,
                        sell_commission = 0.003)

## getting indicators plot
CPF.indicators.atr(TR = [14, 100])

CPF.indicators.macd(EMA1 = 12, EMA2 = 26, EMA_signal = 9)

CPF.indicators.rsi(EMA1 = 14, EMA2 = 20)

CPF.indicators.bollinger(WINDOW = 20, K = 2)

CPF.indicators.ivar(WINDOW = 10)

CPF.indicators.aroon(WINDOW = 14)

CPF.indicators.stohasctic(WINDOW = 5, EMA1 = 3, EMA2 = 3)

CPF.plot(['all'])

## getting candle plot
CPF.candles.black_maribozu(percent_up = 0.1, percent_down = 0.1)

CPF.candles.white_maribozu(percent_up = 0.1, percent_down = 0.1)

CPF.candles.three_white_solders(percent = 0.5)

CPF.candles.three_black_crows(percent = 0.5)

CPF.plot(['white_maribozu', 'black_maribozu', 'three_white_solders', 'three_black_crows'])

## getting plot for everything in library
CPF.plot(['all'])

## defining indicators                     
indicators = [
            'ivar',
            'atr',
            'macd',
            'rsi',
            'bollinger',
            'aroon',
            'stohasctic',
            'stohasctic_sma',
            'black_maribozu', 'white_maribozu',
            'solders', 'crows'
            ]

## defining strategy (though its only one by now)
CPF.set_traid_strategy('simple', indicators = indicators, money = 300000)

## run test trade for previous periods
CPF.trade_several(start_idx = 220)

## get profit by each indicator
CPF.train(end = None, money = 100000)

## run trade in real time
CPF.start(refresh_time = 5)

## Link to github page
https://github.com/zungl/base-trading-bot.mathematics-of-mechanical-trading-systems

## Link to pip
https://pypi.org/project/candleplot-trade/

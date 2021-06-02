## Импорт библиотеки
from candleplot_trade import candleplotfigures

## Создание эеземпляра с параметрами для тикера
CPF = candleplotfigures(ticker = 'QIWI', # 'BTC-USD', 'GOOG', 'SBER.ME', 'AFLT.ME'
                        period = "50d",
                        # start= '2021-05-25 14:38:00-04:00',
                        interval = "1d",
                        html_log = True,
                        console_log = True,
                        full_console_log = False,
                        buy_commission = 0.003,
                        sell_commission = 0.003,
                        return_plot = True,
                        save_html = False,
                        text_size = 8)

## Полигон
# indicators = ['ivar', 'atr',
#             'macd', 'rsi', 'bollinger',
#             'aroon', 'stohasctic', 'stohasctic_sma',
#             'black_maribozu', 'white_maribozu',
#             'solders', 'crows']
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

CPF.set_traid_strategy('simple', indicators = indicators, money = 300000)

## Тестовая торговля
# CPF.trade_several(start_idx = 300)

## Начать торговлю в реальном времени
# CPF.start(refresh_time = 5, get_period = '10m')

## Проверка дохоности отдельных индикаторов
CPF.train(end = None, money = 100000)

# # График индикаторов
# CPF.indicators.atr(TR = [14, 100])
# CPF.indicators.macd(EMA1 = 12, EMA2 = 26, EMA_signal = 9)
# CPF.indicators.rsi(EMA1 = 14, EMA2 = 20)
# CPF.indicators.bollinger(WINDOW = 20, K = 2)
# CPF.indicators.ivar(WINDOW = 10)
# CPF.indicators.aroon(WINDOW = 14)
# CPF.indicators.stohasctic(WINDOW = 5, EMA1 = 3, EMA2 = 3)
# CPF.plot(['all'])

# График свечей
# CPF.candles.black_maribozu(percent_up = 0.1, percent_down = 0.1)
# CPF.candles.white_maribozu(percent_up = 0.1, percent_down = 0.1)
# CPF.candles.three_white_solders(percent = 0.5)
# CPF.candles.three_black_crows(percent = 0.5)
# CPF.plot(['white_maribozu', 'black_maribozu', 'three_white_solders', 'three_black_crows'])

## График всех индикаторов/свечей
# print(len(CPF.indicators.ivar_flat))
# print(CPF.indicators.ivar_flat)
# print(CPF.indicators.std)
# CPF.plot(['all'])

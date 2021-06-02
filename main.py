## Импорт библиотеки
from candleplot_trade_library import candleplotfigures

## Создание эеземпляра с параметрами для тикера
CPF = candleplotfigures(ticker = 'BTC-USD', # 'BTC-USD', 'GOOG'
                        period = "1d",
                        # start= '2021-05-25 14:38:00-04:00',
                        interval = "1m",
                        html_log = True,
                        full_console_log = True,
                        buy_commission = 0.003,
                        sell_commission = 0.003)

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
# CPF.trade_several(start_idx = 220)

## Начать торговлю в реальном времени
CPF.start(refresh_time = 5)

## График индикаторов
# CPF.indicators.atr(TR = [14, 100])
# CPF.indicators.macd(EMA1 = 12, EMA2 = 26, EMA_signal = 9)
# CPF.indicators.rsi(N = 14, N1 = 20)
# CPF.indicators.bollinger(window = 10, k = 2)
# CPF.indicators.ivar(m = 10)
# CPF.indicators.aroon(window = 14)
# CPF.indicators.stohasctic(window = 12, m = 3)
# CPF.plot(['all'])

## График свечей
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

## Запуск простой стратегии
# CPF.set_traid_strategy('simple')
# CPF.train_test()
# print(CPF.simple_df)
# CPF.start(refresh_time = 10)

## Вывод сведений о библиотеке
# print(candleplotfigures.__doc__)
## Вывод документации для конкретной функции
# print(help(CPF.indicators.atr))

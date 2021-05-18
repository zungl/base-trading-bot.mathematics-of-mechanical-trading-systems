## Импорт необходимых библиотек
import pandas as pd
from Vronsky_Basov_Strugach_Ohriz_Ermolina import candleplotfigures

shares = pd.read_csv('mfd_tickers_17032018_17032021.txt', sep = ';')

shares_names_list = shares["<TICKER>"].unique()
# print(f'Список акций в датасете: {", ".join(shares_names_list)}')

title = 'МТС-ао'

CPF = candleplotfigures(df = shares[shares['<TICKER>'] == 'МТС-ао'][-250:],
                        title = title)
# CPF.indicators.atr(TR = [14, 40])
CPF.indicators.macd(EMA1 = 12, EMA2 = 26, EMA_signal = 9)
# CPF.indicators.rsi(N = 14, N1 = 20)
# CPF.indicators.bollinger(N = 20, k = 2)
# CPF.indicators.ivar(m = 32)
# CPF.indicators.aroon(window = 14)
CPF.indicators.ivar(m = 10)
CPF.plot(['macd'])

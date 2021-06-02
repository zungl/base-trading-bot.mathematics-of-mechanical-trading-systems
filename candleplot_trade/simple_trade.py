from .errors import *
import pandas as pd

class simple_trade():
    def __init__(self):
        pass

    def _trade__simple_trade_trade(self, idx = -1):
        self.indicators.load_data(self.data)
        self.candles.load_data(self.data)
        if self.full_console_log:
            print(f'Торгуем по стратегии: {self.strategy}')

        if len(self.data.df) - len(self.buy_sell_list)>0:
            self.buy_sell_list += [0]*(len(self.data.df) - len(self.buy_sell_list))

        decision = {}
        if ('ivar' in self.strategy_indicators) or ('atr' in self.strategy_indicators):
            flat = True
        else:
            flat = False
        ## Flat recognition
        if ('ivar' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            if self.indicators.ivar_flat[idx] < 0.5:
                flat = False
        if ('atr' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            if self.indicators.atr_flat[idx] == 1:
                flat = False

        ## indicators decisions
        if ('macd' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['macd'] = self.indicators.macd_income[idx]
        if ('rsi' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['rsi'] = self.indicators.rsi_income[idx]
        if ('bollinger' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['bollinger'] = self.indicators.bollinger_income[idx]
        if ('aroon' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['aroon'] = self.indicators.aroon_income[idx]
        if ('stohasctic' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['stohasctic'] = self.indicators.stohasctic_income[idx]
        if ('stohasctic_sma' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['stohasctic_sma'] = self.indicators.stohasctic_sma_income[idx]
        ## candles decisions
        if ('black_maribozu' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['black_maribozu'] = self.candles.black_maribozu_plot[idx]
        if ('white_maribozu' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['white_maribozu'] = self.candles.white_maribozu_plot[idx]
        if ('solders' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['solders'] = self.candles.solders_plot[idx]
        if ('crows' in self.strategy_indicators) or ('all' in self.strategy_indicators):
            decision['crows'] = self.candles.crows_plot[idx]

        ## bollinger_size
        # if ('bollinger_size' in self.strategy_indicators) or ('all' in self.strategy_indicators):
        #     decision['bollinger_size'] = self.indicators.bollinger_size[idx]
        if not flat:
            for ind in self.indicators_range:
                # print(ind, decision[ind])
                if ind in decision.keys():
                    if decision[ind] == 0:
                        continue
                    if decision[ind] == 1:
                        self.buy_sell_list[idx] = 1
                    if decision[ind] == -1:
                        self.buy_sell_list[idx] = -1

    def _trade__simple_trade_train(self, money, end = None):
        if self.full_console_log:
            print(f'Обучение стратегии {self.strategy}')
        self.income_dict = {}
        indicators_list = [['buy_and_hold'], ['atr', 'macd'], ['atr', 'rsi'], ['atr', 'bollinger'],
                        ['atr', 'aroon'], ['atr', 'stohasctic'], ['atr', 'stohasctic_sma'],
                                 ['macd'], ['rsi'], ['bollinger'],
                                 ['aroon'], ['stohasctic'], ['stohasctic_sma'],
                                 ['atr', 'black_maribozu', 'white_maribozu'], ['atr', 'solders', 'crows'],
                                 ['black_maribozu', 'white_maribozu'],
                                ['solders', 'crows']]
        for ind in indicators_list:
            print(f'Работа индекса {ind}')
            if ind == ['buy_and_hold']:
                self.income_dict[str(ind)] = (money//(self.data.CLOSE[0])) * (self.data.CLOSE[-1]) - money
                # print((self.income_dict[str(ind)]/money))
            else:
                self.set_traid_strategy(strategy = 'simple', indicators = ind, money = money)
                self.trade_several(start_idx = 1, plot = True)
                self.income_dict[str(ind)] = self.income
        # indicators_list_2 = []
        # for ind, profit in self.income_dict.items():
        #     if profit > 0:
                # indicators_list_2 +=
        if self.console_log:
            print('Своднаятаблица результатов')
            for ind, profit in self.income_dict.items():
                print(f'{ind}: {profit/money*100:.2f}%')
            # print(self.income_dict)

        if end == None:
            end = len(self.data.df)
        # indexes = list(range(0, end))
        # self.indicators.load_data(self.data)
        # self.candles.load_data(self.data)
        # for idx in indexes:
        #     pass

    def _trade__simple_trade_trade_test(self, test_size, plot):
        if self.full_console_log:
            print(f'Тестирование стратегии {self.strategy}')
        # self.train(end = int(len(self.data.df)*test_size))

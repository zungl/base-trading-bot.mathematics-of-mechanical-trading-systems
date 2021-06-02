import matplotlib.pyplot as plt
import plotly.graph_objects as go ## Для отрисовки графиков свечей
import plotly.subplots as subplots
import plotly
import numpy as np
from IPython.display import clear_output

class plot_class():
    def __plotly_Candlestick(self, rows = 1, cols = 1, row_heights = [1]):
        '''
        Построение свечевого графика с помощью библиотеки plotly

        Возваращет объект plotly.graph_objs._figure.Figure,
        который является адаптивным свечевым графиком
        '''
        self.fig = subplots.make_subplots(rows, cols,
                                   row_heights = row_heights)

        self.fig.add_trace(go.Candlestick(x = self.data.df.index,
                        open = self.data.df.Open,
                        high = self.data.df.High,
                        low = self.data.df.Low,
                        close = self.data.df.Close,
                        name = 'Цены акций'), row = 1, col = 1
                     )

        self.fig.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1),
                title=f'Цены акций компании {self.title}',
                xaxis_title="Даты",
                yaxis_title="Цены акции",
                legend_title="Элементы графика",
                font=dict(
#                             family="Courier New, monospace",
                    size=12,
                    color="black"
              ))

        self.fig.update(layout_xaxis_rangeslider_visible=False)
        # self.fig.update(margin=dict(t=150))
        return self.fig

    def plot(self, figures = None, return_plot = None, save_html = None):
        if return_plot is None:
            return_plot = self.return_plot
        if save_html is None:
            save_html = self.save_html

        if figures is None:
            figures = self.strategy_indicators
            if 'train_line_plot' not in self.strategy_indicators:
                figures += ['train_line_plot', 'stats']
        rows, cols = 1, 1
        row_heights = [1]

        if ('all' in figures) or ('atr' in figures) or ('macd' in figures) or ('rsi' in figures) or ('bollinger' in figures) or ('ivar' in figures) or ('aroon' in figures) or ('stohasctic' in figures):
            rows = 2
            cols = 1
            row_heights = [0.8, 0.2]

        self.fig = self.__plotly_Candlestick(rows = rows,
                                        cols = cols,
                                        row_heights = row_heights)
        ## Вызываю функции индикаторов
        if (('atr' in figures) or ('all' in figures)):
            self.atr_plot()
        if (('macd' in figures) or ('all' in figures)):
            self.macd_plot()
        if (('bollinger' in figures) or ('all' in figures) or ('bollinger_size' in figures)):
            self.bollinger_plot()
        if (('rsi' in figures) or ('all' in figures)):
            self.rsi_plot()
        if (('ivar' in figures) or ('all' in figures)):
            self.ivar_plot()
        if (('aroon' in figures) or ('all' in figures)):
            self.aroon_plot()
        if (('stohasctic' in figures) or ('all' in figures) or ('stohasctic_sma' in figures)):
            self.stohasctic_plot()
        if ('train_line_plot' in figures) or ('all' in figures):
            self.train_line_plot()
        self.buy_sell_plot()
        if (('black_maribozu' in figures) or ('all' in figures)):
            self.black_maribozu_plot()
        if (('white_maribozu' in figures) or ('all' in figures)):
            self.white_maribozu_plot()
        if (('three_white_solders' in figures) or ('all' in figures) or ('solders' in figures)):
            self.three_white_solders_plot()
        if (('three_black_crows' in figures) or ('all' in figures) or ('crows' in figures)):
            self.three_black_crows_plot()

        if ('stats' in figures):
            self.stats_plot()

        # self.fig['layout'].update(yaxis = dict(range = [self.DATE[0], self.DATE[-1]]))
        ## Возвращаем страницу html с полученным графиком
        if save_html:
            plotly.offline.plot(self.fig, filename = f'График фигур для цен акций {self.title}.html')
        if return_plot:
            clear_output()
            self.fig.show()
            return self.fig

    ## Служебные графики:
    def train_line_plot(self):
        ## plot self.start_line
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.data.df.index[self.start_line], self.data.df.index[self.start_line]],
                      y=[min(self.data.LOW), max(self.data.HIGH)],
                      mode="lines",
                      legendgroup="start_trade_line",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'start_trade_line'),
            row = 1, col = 1)

    def stats_plot(self):
        self.fig.add_annotation(dict(font=dict(color="black",size=self.text_size),
                            x=self.data.df.index[int(len(self.data.df.index)*0.6)],
                            y=1.125,
                            showarrow=False,
                            text=f'<b>Стартовый капитал: </b>{self.start_money}<br><b>Денег: </b>{self.money}, <b>Акций: </b>{self.shares}<br><b>Текущая доходность:</b> {self.income}<br><b>Кол-во операций:</b> {self.operations}<br><b>Использованные индикаторы: </b>{", ".join(self.strategy_indicators[:-2])}',
                            textangle=0,
                            xref="x",
                            yref="paper",
                            align="right"
                           ))

    def buy_sell_plot(self):
        buy = [np.nan]*len(self.data.df)
        sell = [np.nan]*len(self.data.df)
        for idx, decision in enumerate(self.buy_sell_list):
            if decision == 1:
                buy[idx] = self.data.HIGH[idx]
                continue
            if decision == -1:
                sell[idx] = self.data.HIGH[idx]
                continue
        self.fig.add_trace(
              go.Scatter(
                  x = self.data.df.index,
                  y = buy,
                  mode="markers",
                  marker_symbol = 'triangle-down',
                  legendgroup='buy_points',
                  marker=dict(color='green', size = 14,
                            line=dict(color="black", width=2)),
                  showlegend=True,
              name = 'buy_points'))
        self.fig.add_trace(
              go.Scatter(
                  x = self.data.df.index,
                  y = sell,
                  mode="markers",
                  marker_symbol = 'triangle-down',
                  legendgroup='sell_points',
                  marker=dict(color='red', size = 14,
                            line=dict(color="black", width=2)),
                  showlegend=True,
              name = 'sell_points'))

    ## Свечи:

    def black_maribozu_plot(self):
        dots_y = []
        dots_x = []
        for idx in range(len(self.data.df)):
            if self.candles.black_maribozu_plot[idx] == -1:
                dots_y.append(self.data.df.index[idx])
                dots_x.append([self.data.body_down_original[idx] + (self.data.body_top_original[idx] - self.data.body_down_original[idx])/2][0])
        self.fig.add_trace(
              go.Scatter(
                  x = dots_y,
                  y = dots_x,
                  mode="markers",
                  legendgroup='black_maribozu',
                  marker=dict(color='black', size = 6,
                            line=dict(color="black", width=2)),
                  showlegend=True,
              name = 'black_maribozu'))

    def white_maribozu_plot(self):
        dots_y = []
        dots_x = []
        for idx in range(len(self.data.df)):
            if self.candles.white_maribozu_plot[idx] == 1:
                dots_y.append(self.data.df.index[idx])
                dots_x.append([self.data.body_down_original[idx] + (self.data.body_top_original[idx] - self.data.body_down_original[idx])/2][0])
        self.fig.add_trace(
              go.Scatter(
                  x = dots_y,
                  y = dots_x,
                  mode="markers",
                  marker=dict(color='white', size = 6,
                            line=dict(color="black", width=2)),
                  legendgroup='white_maribozu',
                  showlegend=True,
              name = 'white_maribozu'))

    def three_white_solders_plot(self):
        dots_y = []
        dots_x = []
        for idx in range(len(self.data.df)):
            if self.candles.solders_plot[idx] == 1:
                dots_y.append(self.data.df.index[idx])
                dots_x.append([self.data.body_down_original[idx] + (self.data.body_top_original[idx] - self.data.body_down_original[idx])/2][0])
        self.fig.add_trace(
              go.Scatter(
                  x = dots_y,
                  y = dots_x,
                  mode="markers",
                  marker=dict(color='green', size = 6,
                            line=dict(color="black", width=2)),
                  legendgroup='three_white_solders',
                  showlegend=True,
              name = 'three_white_solders'))

    def three_black_crows_plot(self):
        dots_y = []
        dots_x = []
        for idx in range(len(self.data.df)):
            if self.candles.crows_plot[idx] == -1:
                dots_y.append(self.data.df.index[idx])
                dots_x.append([self.data.body_down_original[idx] + (self.data.body_top_original[idx] - self.data.body_down_original[idx])/2][0])
        self.fig.add_trace(
              go.Scatter(
                  x = dots_y,
                  y = dots_x,
                  mode="markers",
                  marker=dict(color='red', size = 6,
                            line=dict(color="black", width=2)),
                  legendgroup='three_black_crows',
                  showlegend=True,
              name = 'three_black_crows'))


    ## Индикаторы:

    def atr_plot(self):
        # line = self.indicators.truerange
        # self.fig.add_trace(
        #           go.Scatter(
        #               x=self.data.df.index,
        #               y=line,
        #               mode="lines",
        #               legendgroup="ATR",
        #               line=go.scatter.Line(color="black"),
        #               showlegend=True,
        #           name = 'ATR'),
        #           row = 2, col = 1)

        color = ['blue', 'red']
        i = 0
        for line in self.indicators.atr_plots:
            self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="ATR",
                      line=go.scatter.Line(color=color[i%2]),
                      showlegend=True,
                  name = str('ATR ' + str(self.indicators.indicator_params.atr_TR[i]))),
                  row = 2, col = 1)
            i += 1

    def macd_plot(self):
        line = self.indicators.macd_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="MACD",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'MACD'),
            row = 2, col = 1)
        line = self.indicators.macd_ema_signal
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="MACD",
                      line=go.scatter.Line(color="orange"),
                      showlegend=False,
                  name = 'MACD_signal'),
            row = 2, col = 1)
        line = self.indicators.macd_hist
        self.fig.add_trace(
                  go.Bar(
                      x=self.data.df.index,
                      y=line,
                      legendgroup="MACD",
                      showlegend=False,
                  name = 'MACD_hist'),
            row = 2, col = 1)

    def rsi_plot(self):
        line = self.indicators.rsi_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="RSI",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'RSI'),
            row = 2, col = 1)

    def bollinger_plot(self):
        line = self.indicators.bollinger_sma_m
        self.fig.add_trace(
                  go.Scatter(
                      # x=self.data.df.index,
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'Bollinger SMA_M'),
            row = 1, col = 1)

        line = self.indicators.bollinger_sma_u
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="orange"),
                      showlegend=False,
                  name = 'Bollinger SMA_U'),
            row = 1, col = 1)

        line = self.indicators.bollinger_sma_l
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="green"),
                      showlegend=False,
                  name = 'Bollinger SMA_L'),
            row = 1, col = 1)

    def aroon_plot(self):
        line = self.indicators.aroon_up
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="aroon",
                      line=go.scatter.Line(color="orange"),
                      showlegend=True,
                  name = 'aroon up'),
            row = 2, col = 1)

        line = self.indicators.aroon_down
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="aroon",
                      line=go.scatter.Line(color="blue"),
                      showlegend=True,
                  name = 'aroon down'),
            row = 2, col = 1)

    def ivar_plot(self):
        line = self.indicators.ivar_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="iVar",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'iVar'),
            row = 2, col = 1)
        line = [0.5, 0.5]
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.data.df.index[0],self.data.df.index[-1]],
                      y=line,
                      mode="lines",
                      legendgroup="iVar",
                      line=go.scatter.Line(color="orange"),
                      showlegend=True,
                  name = 'iVar_level'),
            row = 2, col = 1)


    def stohasctic_plot(self):
        # line = self.indicators.stohasctic_plot
        # self.fig.add_trace(
        #           go.Scatter(
        #               x=self.data.df.index,
        #               y=line,
        #               mode="lines",
        #               legendgroup="stohasctic",
        #               line=go.scatter.Line(color="black"),
        #               showlegend=True,
        #           name = 'stohasctic'),
        #     row = 2, col = 1)

        line = self.indicators.stohasctic_sma1_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="stohasctic",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'stohasctic sma k'),
            row = 2, col = 1)

        line = self.indicators.stohasctic_sma2_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=self.data.df.index,
                      y=line,
                      mode="lines",
                      legendgroup="stohasctic",
                      line=go.scatter.Line(color="orange",dash='dash'),
                      showlegend=True,
                  name = 'stohasctic sma d'),
            row = 2, col = 1)

import matplotlib.pyplot as plt
import plotly.graph_objects as go ## Для отрисовки графиков свечей
import plotly.subplots as subplots
import plotly

class plot_class():
    def __plotly_Candlestick(self, rows = 1, cols = 1, row_heights = [1]):
        '''
        Построение свечевого графика с помощью библиотеки plotly

        Возваращет объект plotly.graph_objs._figure.Figure,
        который является адаптивным свечевым графиком
        '''

        self.fig = subplots.make_subplots(rows, cols,
                                   row_heights = row_heights)

        self.fig.add_trace(go.Candlestick(x = self.df['<DATE>'],
                        open = self.df['<OPEN>'],
                        high = self.df['<HIGH>'],
                        low = self.df['<LOW>'],
                        close = self.df['<CLOSE>']), row = 1, col = 1
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

        return self.fig

    def plot(self, figures = ['all'], return_plot = False):
        rows, cols = 1, 1
        row_heights = [1]

        if ('all' in figures) or ('atr' in figures) or ('macd' in figures) or ('rsi' in figures) or ('bollinger' in figures) or ('ivar' in figures) or ('aroon' in figures) or ('stohasctic' in figures):
            rows = 2
            cols = 1
            row_heights = [0.8, 0.2]

        self.fig = self.__plotly_Candlestick(rows = rows,
                                        cols = cols,
                                        row_heights = row_heights)
        # if rows == 2:
        #     self.fig.update_xaxes(range=[self.DATE[0], self.DATE[-1]], row=2, col=1)

        ## Вызываю функции индикаторов
        if (('atr' in figures) or ('all' in figures)):
            self.atr_plot()

        if (('macd' in figures) or ('all' in figures)):
            self.macd_plot()

        if (('bollinger' in figures) or ('all' in figures)):
            self.bollinger_plot()

        if (('rsi' in figures) or ('all' in figures)):
            self.rsi_plot()

        if (('ivar' in figures) or ('all' in figures)):
            self.ivar_plot()

        if (('aroon' in figures) or ('all' in figures)):
            self.aroon_plot()

        if (('stohasctic' in figures) or ('all' in figures)):
            self.stohasctic_plot()

        self.fig['layout'].update(yaxis = dict(range = [self.DATE[0], self.DATE[-1]]))

        ## Возвращаем страницу html с полученным графиком
        plotly.offline.plot(self.fig, filename = f'График фигур для цен акций {self.title}.html')

        if return_plot:
            return self.fig

    ## Индикаторы:
    def atr_plot(self):

        y = self.indicators.TrueRange

        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[x] for x in range(1, len(self.CLOSE_original))],
                      y=y,
                      mode="lines",
                      legendgroup="ATR",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'ATR'),
                  row = 2, col = 1)

        color = ['blue', 'red']
        i = 0
        for line in self.indicators.ATR_list:
            self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="ATR",
                      line=go.scatter.Line(color=color[i%2]),
                      showlegend=False,
                  name = 'ATR'),
                  row = 2, col = 1)
            i += 1

    def macd_plot(self):

        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[x] for x in range(1, len(self.CLOSE_original))],
                      y=self.indicators.MACD_plot,
                      mode="lines",
                      legendgroup="MACD",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'MACD'),
            row = 2, col = 1)

        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[x] for x in range(1, len(self.CLOSE_original))],
                      y=self.indicators.EMA_signal,
                      mode="lines",
                      legendgroup="MACD",
                      line=go.scatter.Line(color="orange"),
                      showlegend=False,
                  name = 'MACD_signal'),
            row = 2, col = 1)

        self.fig.add_trace(
                  go.Bar(
                      x=[self.DATE[x] for x in range(1, len(self.CLOSE_original))],
                      y=self.indicators.MACD_hist,
                      legendgroup="MACD",
                      showlegend=False,
                  name = 'MACD_hist'),
            row = 2, col = 1)

    def rsi_plot(self):
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[x] for x in range(1, len(self.CLOSE_original))],
                      y=self.indicators.RSI_plot,
                      mode="lines",
                      legendgroup="RSI",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'RSI'),
            row = 2, col = 1)

    def bollinger_plot(self):
        line = self.indicators.SMA_M
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'Bollinger SMA_M'),
            row = 1, col = 1)

        line = self.indicators.SMA_U
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="orange"),
                      showlegend=False,
                  name = 'Bollinger SMA_U'),
            row = 1, col = 1)

        line = self.indicators.SMA_L
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="Bollinger",
                      line=go.scatter.Line(color="green"),
                      showlegend=False,
                  name = 'Bollinger SMA_L'),
            row = 1, col = 1)


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

    def aroon_plot(self):
        line = self.indicators.aroon_up
        self.fig.add_trace(
                  go.Scatter(
                      x=self.DATE,
                      y=line,
                      mode="lines",
                      legendgroup="aroon",
                      line=go.scatter.Line(color="orange"),
                      showlegend=True,
                  name = 'aroon'),
            row = 2, col = 1)

        line = self.indicators.aroon_down
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="aroon",
                      line=go.scatter.Line(color="blue"),
                      showlegend=True,
                  name = 'aroon'),
            row = 2, col = 1)

    def ivar_plot(self):
        line = self.indicators.ivar_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="iVar",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'iVar'),
            row = 2, col = 1)

    def stohasctic_plot(self):
        line = self.indicators.stohasctic_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="stohasctic",
                      line=go.scatter.Line(color="black"),
                      showlegend=True,
                  name = 'stohasctic'),
            row = 2, col = 1)

        line = self.indicators.stohasctic_sma_plot
        self.fig.add_trace(
                  go.Scatter(
                      x=[self.DATE[len(self.CLOSE_original)-len(line)+x] for x in range(1, len(line))],
                      y=line,
                      mode="lines",
                      legendgroup="stohasctic",
                      line=go.scatter.Line(color="orange"),
                      showlegend=False,
                  name = 'stohasctic'),
            row = 2, col = 1)

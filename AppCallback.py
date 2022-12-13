from cmath import e
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import callback_context
import pandas as pd;
import matplotlib.pyplot as plt;
from sklearn.linear_model import LogisticRegression;
from sklearn import datasets;
import numpy as np;


class AppCallback:
    def __init__(self, app, data):
        self.app = app
        self.data = data
        self.fig = self.blank_fig() #initialize candlestick graph with an empty graph

        self.app.callback(
        [Output('candlestickGraph', 'figure')],
        [
        Input('interval-component', "n_intervals"),
        Input('interval-component', "max_intervals"),
        State('store-data', 'data')
        ]
        )(self.renderGraph)

        self.app.callback(
        [Output('store-data', 'data')],
        [Input('interval-component', "n_intervals"),
        Input('interval-component', "max_intervals"),
        State('store-data', 'data')],
        )(self.storeData)

        self.app.callback(
        [Output('interval-component', 'max_intervals')],
        [Input('fetch_data', "n_clicks"),
        Input('stop_stream', "n_clicks")]
        )(self.start_stop_interval)

        self.app.callback(
        [Output('message', "children")],
        [Input('interval-component', 'max_intervals'),
        Input('fetch_data', "n_clicks"),
        Input('stop_stream', "n_clicks")]
        )(self.stream_message)
    
    # just a function to print empty candlestick Graph
    def blank_fig(self):
        fig = go.Figure(data=[go.Candlestick(x=[None],
        open=[None],
        high=[None],
        low=[None],
        close=[None],
        )])
        fig.update_xaxes(
            type='date',
            tickformat = "%H:%M\n%b %d, %Y",
            tickangle=0,
            showgrid= False
            )
        fig.update_yaxes(
            type= 'linear',
            title= 'Price',
            autorange= True,
            showgrid= True)
        fig.update_layout(uirevision= 'data', hovermode="closest",
            font= dict(
            size=12,
            # color="#000000"
            color="#ffffff"
            ),
            title='Stock Price',
            title_x=0.5,
            template='plotly_dark',
            # template='seaborn',
        )
        fig['layout']['title']['font'] = dict(size=20)
        return fig
    
    # this method starts and stops the live stream
    def start_stop_interval(self, fetch_button, stop_button):
        if fetch_button > 0:
            trigger = callback_context.triggered[0]
            button_id = trigger["prop_id"].split(".")[0]
            max_intervals = 0
            if button_id == 'fetch_data':
                max_intervals = -1
        else:
            max_intervals = 0
        return [max_intervals]
    
    # this method determines what message to show according to button clicked
    def stream_message(self, max_intervals, fetch_button, stop_button):
        if fetch_button == 0 and stop_button == 0:
            data_stream_message = ''
            self.fig = self.blank_fig()
        else:
            if max_intervals == -1:
                data_stream_message = 'Streaming...'
            elif max_intervals == 0:
                data_stream_message = 'Stream Ended'
        return [data_stream_message]
    
    # method to get data and store it in memory
    def storeData(self, n_intervals, max_intervals, data):
        if max_intervals == -1:
            try:
                new_row = self.data.get_next_pandas_row()
                data.append(new_row.to_dict('records')[0]) #apend the new row with previous rows
                return [data]
            except Exception as e:
                print(e)
        else:
            raise PreventUpdate


    # this method controlls the live graph and controlls
    def renderGraph(self, n_intervals, max_intervals, data):
        if max_intervals == -1 and n_intervals !=0:
            try:
                df = pd.DataFrame(data) #make a dataframe from the data
                # plot the graph
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                )])
                line_rows = df.loc[df['Purchase_Decision'] !=0]
                shapes = []
                # draw vertical lines on the graph
                for index, row in line_rows.iterrows():
                    if row['Purchase_Decision'] == 1:
                        shapes.append(dict(type='line',
                                    xref='x', 
                                    yref='paper',
                                    x0=row['Date'],
                                    y0=0,
                                    x1=row['Date'],
                                    y1=1,
                                    layer='below',
                                    opacity=0.8,
                                line=dict(color='green', width=1.5, dash="dot")))# vertical line for buy
                    elif row['Purchase_Decision'] == 2: # vertical line for sell
                        shapes.append(dict(type='line',
                                    xref='x',
                                    yref='paper',
                                    x0=str(row['Date']),
                                    y0=0,
                                    x1=str(row['Date']),
                                    y1=1,
                                    layer='below',
                                    opacity=0.8,
                                line=dict(color='red', width=1.5, dash="dot")))# vertical line for sell

                fig.update_xaxes(
                    type='date',
                    tickformat = "%H:%M\n%b %d, %Y",
                    tickangle=0,
                    autorange= True,
                    showgrid= False,
                    )
                fig.update_yaxes(
                    type= 'linear',
                    title= 'Price',
                    autorange= True,
                    showgrid= True)
                fig.update_layout(uirevision= 'data', hovermode="closest",
                    font= dict(
                    size=12,
                    # color="#000000"
                    color="#ffffff"
                    ),
                    title='Stock Price',
                    title_x=0.5,
                    # template='seaborn',
                    template='plotly_dark',
                    shapes=shapes
                )
                fig['layout']['title']['font'] = dict(size=20)
                self.fig = fig
            except Exception as e:
                print(e)
        else:
            fig = self.fig
        return [fig]

    def ml_model(self):
        pd1=pd.read_csv('D:\Live-Stock-Price-Dashboard-main\Live-Stock-Price-Dashboard-main\AMZN.csv')

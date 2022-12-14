import dash_bootstrap_components as dbc
from dash import Dash
from Data import SimData
from Layout import AppLayout
import pandas as pd
from AppCallback import AppCallback
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('./sample.csv')
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

class App:
    def __init__(self):
        styles = [dbc.themes.BOOTSTRAP]
        self.layout = AppLayout()
        self.data = SimData("./AMZN.csv")  # here we initionlize Data class object
        self.app = Dash(name = __name__, external_stylesheets=styles)
        self.app.layout = self.layout.getAppLayout()
        AppCallback(self.app, self.data)
        fig1 = go.Figure(data=go.Ohlc(x=df['Date'],
                                     open=df['AAPL.Open'],
                                     high=df['AAPL.High'],
                                     low=df['AAPL.Low'],
                                     close=df['AAPL.Close']))
        fig1.show()

        fig2 = go.Figure([go.Scatter(x=df['Date'], y=df['AAPL.High'])])
        fig2.show()

        fig3 = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['AAPL.Open'],
                                             high=df['AAPL.High'],
                                             low=df['AAPL.Low'],
                                             close=df['AAPL.Close'])])

        fig3.show()
        fig4 = go.Figure(data=[go.Candlestick(x=df['Date'],
                                              open=df['AAPL.Open'],
                                              high=df['AAPL.High'],
                                              low=df['AAPL.Low'],
                                              close=df['AAPL.Close'])])

        fig4.show()

        fig = go.Figure(data=fig1.data + fig2.data + fig3.data)
        fig.show()

    def initializeApp(self):
        return self.app

if __name__ == "__main__":
    app = App()
    app_instance = app.initializeApp()
    app_instance.run_server(debug=False, port=443)
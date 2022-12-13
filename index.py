import dash_bootstrap_components as dbc
from dash import Dash
from Data import SimData
from Layout import AppLayout
import pandas as pd
from AppCallback import AppCallback


class App:
    def __init__(self):
        styles = [dbc.themes.BOOTSTRAP]
        self.layout = AppLayout()
        self.data = SimData("./sample.csv")  # here we initionlize Data class object
        self.app = Dash(name = __name__, external_stylesheets=styles)
        self.app.layout = self.layout.getAppLayout()
        AppCallback(self.app, self.data)

    def initializeApp(self):
        return self.app

if __name__ == "__main__":
    app = App()
    app_instance = app.initializeApp()
    app_instance.run_server(debug=False, port=443)
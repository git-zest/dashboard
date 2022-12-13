from dash import dcc, html
import dash_bootstrap_components as dbc
from Data import SimData



class AppLayout():
    def __init__(self):
        self.sidebar =  self.generateSidebarLayout()
        self.content =  self.generateContentLayout()
    
    # this method generates Sidebar Layout
    def generateSidebarLayout(self):
        sidebar = html.Div(
            id='sidebar',
            children=[
                html.H2("Controls", className="display-9 text-center"),
                html.Hr(),
                html.Div(
                    [
                        dbc.Button("Fetch", id='fetch_data',  n_clicks=0, outline=True, color="primary", className="me-1"),
                        dbc.Button("Stop", id='stop_stream',  n_clicks=0, outline=True, color="danger", className="me-1"),
                    ],
                    className="d-grid gap-2 col-6 mx-auto",
                ),
                html.Div(id="message", className='m-4 text-center')
            ],
        )
        return sidebar
    # this method generates content Page Layout
    def generateContentLayout(self):
        content = html.Div(id="content",
        children=[
            dcc.Interval(
                id='interval-component',
                disabled=False,
                interval=2*1000, # in milliseconds
                n_intervals=0,
                max_intervals=0
            ),
            dcc.Store(id="store-data", data=[], storage_type='memory'),
            dbc.Col(dcc.Graph(id="candlestickGraph", style={'height' : '90vh'})),
        ],
        )
        return content
    
    # ------This method generates Overall App's Layout ---------
    def getAppLayout(self):
        layout = html.Div(children=[dcc.Location(id="url"), self.sidebar, self.content])
        return layout

    # ------------------ Layout Settings End --------------------
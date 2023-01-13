

from dash import Dash, html, dcc, Input, Output, State, callback
import dash
import plotly.express as px
import pandas as pd
import flask
import db_classes

server = flask.Flask(__name__)

app = Dash(__name__, server= server, use_pages=True)



app.layout = html.Div(children=[
    html.Div(children=
    [html.Div(dcc.Link(f"{page['name']}", href=page["relative_path"]))
    for page in dash.page_registry.values()],
    style = {"display":"flex","flex-direction":"row"}),
    dash.page_container
])
        

if __name__ == '__main__':
    app.run_server(debug=True)

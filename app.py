

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
    [html.Div(dcc.Link(html.Div(f"{page['name']}"),href=page["relative_path"],className="navintbox"),className="navbox")
    for page in dash.page_registry.values()],
    className="navbar"),
    html.Div(children=[
        dcc.Input(id="user_input", type="text", placeholder="Username"),
        dcc.Input(id="password_input", type="password", placeholder="Password"),
        html.Button("Log in", id = "submit_button", n_clicks=0)
    ],className="login"),
    dash.page_container
])
        

if __name__ == '__main__':
    app.run_server(debug=True)

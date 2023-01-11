# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import flask
import db_classes

server = flask.Flask(__name__)

app = Dash(__name__, server= server)

user = db_classes.User.get_from_db("torin")
user.get_house()
df = user.house.get_data()

fig = px.bar(df, x=df.index, y="usage")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

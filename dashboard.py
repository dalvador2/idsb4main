

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import flask
import db_classes

server = flask.Flask(__name__)

app = Dash(__name__, server= server)

df = pd.DataFrame(data=None, columns= ["usage","generation","house_id"])
fig1 = px.bar(df, x=df.index, y="usage")
fig2 = px.bar(df, x=df.index, y = "generation")

app.layout = html.Div(children=[
    html.H1(children='EcoHome'),

    html.Div(children='''
        Helping you to save the planet
    '''),
    dcc.Input(id="user_input", type="text", placeholder="Username"),
    dcc.Input(id="password_input", type="password", placeholder="Password"),
    html.Button("Log in", id = "submit_button", n_clicks=0),
    dcc.Graph(
        id='Usage',
        figure=fig1
    ),
    dcc.Graph(
        id="generation",
        figure=fig2
    )
])
@app.callback(Output(component_id="Usage", component_property= "figure"),
    Output(component_id="generation", component_property="figure"),
    Input(component_id="submit_button", component_property="n_clicks"),
    State(component_id="user_input",component_property="value"),
    State(component_id="password_input", component_property="value"))
def update_usage(_,user_name, password):
    user = db_classes.User.get_from_db(user_name)
    if user.verify_password(password):
        user.get_house()
        df = user.house.get_data()
        fig1 = px.bar(df, x=df.index, y="usage")
        fig2 = px.bar(df, x=df.index, y = "generation")
        return fig1, fig2
    else:
        df = pd.DataFrame(data=None, columns= ["usage","generation","house_id"])
        fig1 = px.bar(df, x=df.index, y="usage")
        fig2 = px.bar(df, x=df.index, y = "generation")
        return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)

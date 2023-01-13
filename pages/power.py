import dash
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
import db_classes
import plotly.express as px

dash.register_page(__name__, path="/", order=0)
df = pd.DataFrame(data=None, columns= ["usage","generation","house_id"])
fig1 = px.bar(df, x=df.index, y="usage")
fig2 = px.bar(df, x=df.index, y = "generation")


layout = html.Div(children=[
     dcc.Graph(
        id='Usage',
        figure=fig1
    ),
    dcc.Graph(
        id="generation",
        figure=fig2
    )

])
@callback(Output(component_id="Usage", component_property= "figure"),
    Output(component_id="generation", component_property="figure"),
    Input(component_id="submit_button", component_property="n_clicks"),
    State(component_id="user_input",component_property="value"),
    State(component_id="password_input", component_property="value"))
def update_usage(_,user_name, password):
    def return_blank():
        df = pd.DataFrame(data=None, columns= ["usage","generation","house_id"])
        fig1 = px.bar(df, x=df.index, y="usage")
        fig2 = px.bar(df, x=df.index, y = "generation")
        return fig1, fig2
    try:
        user = db_classes.User.get_from_db(user_name)
    except db_classes.PresenceError:
        return return_blank()
    if user.verify_password(password):
        user.get_house()
        df = user.house.get_data()
        fig1 = px.bar(df, x=df.index, y="usage")
        fig2 = px.bar(df, x=df.index, y = "generation")
        return fig1, fig2
    else:
        return return_blank()
        

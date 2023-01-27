import dash
from dash import html, dcc, dash_table, callback, Input, Output, State
import pandas as pd
import db_classes

dash.register_page(__name__,order=1)
df = pd.DataFrame()

layout = html.Div(children=[
    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="leaderboard")

])

@callback(Output(component_id="leaderboard", component_property="data"),
    Output(component_id="leaderboard", component_property="columns"),
    Input(component_id="submit_button", component_property="n_clicks"),
    State(component_id="user_input",component_property="value"),
    State(component_id="password_input", component_property="value"))
def update_usage(_,user_name, password):
    def return_blank():
        df = pd.DataFrame()
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
    try:
        user = db_classes.User.get_from_db(user_name)
    except db_classes.PresenceError:
        return return_blank()
    if user.verify_password(password):
        df = db_classes.ScoreUtils.leaderboard(user.house_id)
        print(df.to_dict())
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
    else:
        return return_blank()

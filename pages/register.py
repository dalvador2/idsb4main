import dash
from dash import html, dcc, callback, Output, Input, State
import db_classes
import plotly.express as px
dash.register_page(__name__,order=2)


layout = html.Div(children=[
    html.H1(children='Registration'),

    dcc.Input(id="Username", type="text", placeholder="Username"),html.P(),
    dcc.Input(id="Password", type="password",placeholder="Password"),html.P(),
    dcc.Input(id="address", type="text", placeholder = "Address"),
    dcc.Checklist(["Check if adding user to already enrolled house"],id="house_check"),
    dcc.Input(id="occupants",type="text", placeholder="occupants"),html.P(),
    dcc.Input(id="floor_area", type="text", placeholder="Floor Area in m^2"),
    html.Button("Submit",)

])
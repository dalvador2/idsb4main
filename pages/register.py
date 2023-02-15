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
    html.Button("Submit",id="go_button", n_clicks=0),
    dcc.Checklist(["Populate me with random data"],id="populate_check"),
    html.H3(children = "sorted", id="conformation")

])
@callback(
    Output(component_id="conformation",component_property="children"),
    Input(component_id="go_button",component_property="n_clicks"),
    State(component_id="Username",component_property="value"),
    State(component_id="Password",component_property="value"),
    State(component_id="address",component_property="value"),
    State(component_id="occupants",component_property="value"),
    State(component_id="floor_area",component_property="value"),
    State(component_id="house_check",component_property="value"),
    State(component_id="populate_check", component_property="value")
)
def enroller(n_clicks,uname,password,address,occupants,floor_area,house_check, populate_check):
    checked = ['Check if adding user to already enrolled house']
    p_check = ["Populate me with random data"]
    if uname is None:
        return "waiting"
    house_check = (house_check == checked)
    populate_check = (populate_check == p_check)
    print(populate_check)
    x = db_classes.User.gen_from_password(uname,password,None)
    if house_check:
        x.get_house(address)
        x.enroll_to_db()
        if populate_check:
            db_classes.data_gen(x.house_id)
        return "Done"
    else:
        h = db_classes.House(floor_area, occupants,address)
        h.enroll_into_db()
        x.get_house(address)
        x.enroll_to_db()
        if populate_check:
            db_classes.data_gen(x.house_id)
        return "Done"
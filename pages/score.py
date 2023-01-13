import dash
from dash import html, dcc

dash.register_page(__name__,order=1)

layout = html.Div(children=[
    html.H1(children='This is our score page'),

    html.Div(children='''
        This is our score page content.
    '''),

])
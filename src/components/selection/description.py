from dash import dcc, Dash, html
import dash_bootstrap_components as dbc
from src.components.selection.selection_sidebar import create_sidebar
from src.components.selection.selection_visualisation import create_visualisation

def description():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                create_sidebar(),
                xs=12, sm=12, md=4, lg=3, xl=3,
                className="mb-1 p-0",
                style={'padding-left': '10px'},
            ),
            dbc.Col(
                create_visualisation(),
                xs=12, sm=12, md=8, lg=9, xl=9,
                className="mb-1 p-0"
            ),
        ],
            style={'margin-left':'30px'},
        ),

    ], fluid=True, className="container-custom"),
from dash import dcc, Dash, html
import dash_bootstrap_components as dbc
from src.components.accueil.graph import graph
from src.components.accueil.map import create_map
from src.components.accueil.sidebar import sidebar

def layout(app: Dash):
    return dbc.Container([
        dcc.Store(id='selected-thematiques', data=[]),
        dbc.Row([
            dbc.Col(
                sidebar(app),
                id='sidebar-col',
                xs=12, sm=12, md=4, lg=2, xl=2,  # Largeur pour différentes tailles d'écran
                className="mb-1 p-0"
            ),
            dbc.Col(
                html.Div([
                    html.Div(
                        create_map(app),
                        id='map-col',
                        style={'width': '50%', 'padding': '0', 'height': '90vh'}  # Largeur initiale
                    ),
                    html.Div(
                        graph(app),
                        id='graph-col',
                        style={'width': '50%', 'padding': '0', 'height': '90vh',
                               'overflow-y': 'auto'}  # Largeur initiale
                    ),
                ],
                style={'display': 'flex', 'width': '100%'}),  # Flexbox pour aligner horizontalement
                xs=12, sm=12, md=8, lg=10, xl=10,  # Largeur pour différentes tailles d'écran
                className="mb-1 p-0"
            ),
        ]),
    ], fluid=True, className="container-custom")

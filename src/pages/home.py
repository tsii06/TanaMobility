from dash import dcc, Dash
import dash_bootstrap_components as dbc
from src.components.graph import graph
from src.components.map import create_map
from src.components.sidebar import sidebar

def layout(app: Dash):
    return dbc.Container([
        dcc.Store(id='selected-carto', data=[]),
        dcc.Store(id='selected-thematiques', data=[]),
        dcc.Store(id='selected-route', data=[]),
        dbc.Row([
            dbc.Col(
                sidebar(app),
                xs=12, sm=12, md=4, lg=2, xl=2,  # Largeur pour différentes tailles d'écran
                className="mb-1 p-0"  # Espacement en bas
            ),
            dbc.Col(
                create_map(app),
                xs=12, sm=12, md=8, lg=5, xl=5,  # Largeur pour différentes tailles d'écran
                className="mb-1 p-0"  # Espacement en bas
            ),
            dbc.Col(
                graph(app),
                xs=12, sm=12, md=12, lg=5, xl=5,  # Largeur pour différentes tailles d'écran
                className="p-0"  # Espacement en bas
            ),
        ]),
    ], fluid=True, className="container-custom")  # 'fluid=True' permet au conteneur de s'adapter à la largeur de l'écran

# Assuming you have the rest of your Dash app setup somewhere



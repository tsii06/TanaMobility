from dash import dcc, Dash, html
import dash_bootstrap_components as dbc

from src.components.selection.selection_header import create_header
def detail_zone():
    return dbc.Container([
        html.Div(create_header()),
        dcc.Store(id='selected-section', data='DESCRIPTION DU TERRITOIRE'),  # Stocker la section sélectionnée
        html.Div(id='dynamic-content'),  # Conteneur pour le contenu dynamique
    ], fluid=True, className="container-custom")



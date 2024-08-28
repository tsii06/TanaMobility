import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Création d'un exemple de DataFrame
data = {
    'zone_id': ['Zone 1', 'Zone 2', 'Zone 3'],
    'current_population': [5000, 8000, 3000],  # Population actuelle
    'current_traffic': [200, 350, 120],  # Trafic en véhicules par heure
    'current_co2': [150, 280, 90],  # Émissions de CO2 en tonnes par an
    'housing_units': [1000, 1500, 800],  # Nombre d'unités de logement
    'commercial_area': [10, 15, 5]  # Surface commerciale en hectares
}

df_zone = pd.DataFrame(data)


def simulation():
    """
    Fonction pour créer une interface de simulation de scénarios de développement urbain.

    :return: Composant html.Div contenant l'interface de simulation.
    """
    return html.Div([
        html.H1("Simulation des Scénarios de Développement Urbain"),

        dbc.Row([
            dbc.Col([
                html.Label("Sélectionnez une zone"),
                dcc.Dropdown(
                    id='zone-selector',
                    options=[{'label': zone, 'value': zone} for zone in df_zone['zone_id']],
                    value='Zone 1'
                ),
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Ajout de nouvelles unités de logement"),
                dcc.Slider(
                    id='housing-slider',
                    min=0,
                    max=1000,
                    step=50,
                    value=0,
                    marks={i: f'{i} unités' for i in range(0, 1001, 200)},
                ),
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Ajout de nouvelles zones commerciales (hectares)"),
                dcc.Slider(
                    id='commercial-slider',
                    min=0,
                    max=20,
                    step=1,
                    value=0,
                    marks={i: f'{i} ha' for i in range(0, 21, 5)},
                ),
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Button("Simuler le scénario", id="simulate-btn", color="primary", className="w-100"),
            ]),
        ], className="my-3"),

        dbc.Row([
            dbc.Col([
                html.H3("Résultats du Scénario Simulé"),
                dcc.Graph(id='simulation-results'),
                html.Div(id='scenario-description', style={'margin-top': '20px'})
            ])
        ])
    ], style={
        'background-color': '#f9f9f9',  # Couleur de fond gris clair
        'border-radius': '8px',  # Coins arrondis
        'margin': '30px',  # Espace entre les divs
        'padding': '30px',
        'display': 'flex',
        'flex-direction': 'column',
        'justify-content': 'center'
    })

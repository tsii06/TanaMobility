import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Création d'un exemple de DataFrame avec des scénarios fictifs
data = {
    'scenario_id': [1, 2, 3],
    'scenario_name': ['Ajout de routes', 'Amélioration des transports publics', 'Développement urbain'],
    'population_growth': [10, 5, 20],  # Croissance démographique prévue (%)
    'traffic_change': [15, -10, 25],  # Changement prévu du trafic (%)
    'co2_emissions': [200, 150, 300]  # Émissions de CO2 prévues (tonnes)
}

df_scenarios = pd.DataFrame(data)

def comparaison():
    return html.Div([
        html.H1("Analyse et Comparaison de Scénarios"),

        dbc.Row([
            dbc.Col([
                html.Label("Sélectionnez le premier scénario"),
                dcc.Dropdown(
                    id='scenario-selector-1',
                    options=[{'label': scenario, 'value': scenario} for scenario in df_scenarios['scenario_name']],
                    value='Ajout de routes'
                ),
            ]),
            dbc.Col([
                html.Label("Sélectionnez le deuxième scénario"),
                dcc.Dropdown(
                    id='scenario-selector-2',
                    options=[{'label': scenario, 'value': scenario} for scenario in df_scenarios['scenario_name']],
                    value='Amélioration des transports publics'
                ),
            ]),
        ], className="my-3"),

        dbc.Row([
            dbc.Col([
                html.H3("Comparaison des Scénarios"),
                dcc.Graph(id='comparison-chart'),
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(id='scenario-description-1', style={'margin-top': '20px'}),
            ]),
            dbc.Col([
                html.Div(id='scenario-description-2', style={'margin-top': '20px'}),
            ])
        ])
    ])


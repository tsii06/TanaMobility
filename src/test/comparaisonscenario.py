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

# Initialisation de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de l'application
app.layout = dbc.Container([
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


# Callback pour mettre à jour le graphique comparatif et les descriptions
@app.callback(
    [Output('comparison-chart', 'figure'),
     Output('scenario-description-1', 'children'),
     Output('scenario-description-2', 'children')],
    [Input('scenario-selector-1', 'value'),
     Input('scenario-selector-2', 'value')]
)
def update_comparison(scenario_name_1, scenario_name_2):
    # Filtrer les données pour les deux scénarios sélectionnés
    scenario_1 = df_scenarios[df_scenarios['scenario_name'] == scenario_name_1].iloc[0]
    scenario_2 = df_scenarios[df_scenarios['scenario_name'] == scenario_name_2].iloc[0]

    # Créer un DataFrame pour la comparaison
    comparison_df = pd.DataFrame({
        'Metric': ['Croissance démographique (%)', 'Changement du trafic (%)', 'Émissions de CO2 (tonnes)'],
        scenario_name_1: [scenario_1['population_growth'], scenario_1['traffic_change'], scenario_1['co2_emissions']],
        scenario_name_2: [scenario_2['population_growth'], scenario_2['traffic_change'], scenario_2['co2_emissions']]
    })

    # Créer un graphique comparatif
    fig = px.bar(comparison_df, x='Metric', y=[scenario_name_1, scenario_name_2],
                 barmode='group', title="Comparaison des Scénarios")

    # Descriptions des scénarios
    description_1 = (f"{scenario_name_1} : Croissance démographique de {scenario_1['population_growth']}%, "
                     f"changement du trafic de {scenario_1['traffic_change']}%, "
                     f"et émissions de CO2 estimées à {scenario_1['co2_emissions']} tonnes.")

    description_2 = (f"{scenario_name_2} : Croissance démographique de {scenario_2['population_growth']}%, "
                     f"changement du trafic de {scenario_2['traffic_change']}%, "
                     f"et émissions de CO2 estimées à {scenario_2['co2_emissions']} tonnes.")

    return fig, description_1, description_2


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)

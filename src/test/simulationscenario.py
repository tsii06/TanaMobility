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

# Initialisation de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de l'application
app.layout = dbc.Container([
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
])


# Callback pour exécuter la simulation et mettre à jour les résultats
@app.callback(
    Output('simulation-results', 'figure'),
    Output('scenario-description', 'children'),
    Input('zone-selector', 'value'),
    Input('housing-slider', 'value'),
    Input('commercial-slider', 'value'),
    Input('simulate-btn', 'n_clicks')
)
def simulate_scenario(zone_id, new_housing_units, new_commercial_area, n_clicks):
    if not n_clicks:
        return dash.no_update

    # Filtrer les données pour la zone sélectionnée
    zone_data = df_zone[df_zone['zone_id'] == zone_id].iloc[0]

    # Calculer les impacts simulés
    new_population = zone_data[
                         'current_population'] + new_housing_units * 2.5  # Supposons 2,5 personnes par unité de logement
    new_traffic = zone_data['current_traffic'] + (new_housing_units * 0.5) + (new_commercial_area * 10)
    new_co2 = zone_data['current_co2'] + (
                new_traffic * 0.1)  # Supposons que chaque véhicule émet 0,1 tonne de CO2 par an

    # Créer un DataFrame pour les résultats
    results = pd.DataFrame({
        'Metric': ['Population simulée', 'Trafic simulé (véhicules/h)', 'Émissions de CO2 simulées (tonnes/an)'],
        'Value': [new_population, new_traffic, new_co2]
    })

    fig = px.bar(results, x='Metric', y='Value', title=f"Impact du Scénario pour {zone_id}")

    # Description du scénario
    scenario_description = (
        f"Le scénario pour {zone_id} inclut l'ajout de {new_housing_units} nouvelles unités de logement "
        f"et de {new_commercial_area} hectares de zones commerciales. "
        f"Cela entraîne une augmentation de la population à {new_population:.0f} habitants, "
        f"un trafic estimé à {new_traffic:.0f} véhicules par heure, "
        f"et des émissions de CO2 d'environ {new_co2:.0f} tonnes par an.")

    return fig, scenario_description


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)

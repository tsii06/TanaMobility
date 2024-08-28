import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Création d'un exemple de DataFrame avec des routes fictives
data = {
    'route_id': [1, 2, 3, 4, 5],
    'route_name': ['Route A', 'Route B', 'Route C', 'Route D', 'Route E'],
    'capacity': [2000, 1500, 1800, 1000, 1200],  # Capacité maximale (véhicules/h)
    'current_traffic': [1800, 1200, 1900, 800, 1300]  # Trafic actuel (véhicules/h)
}

df_routes = pd.DataFrame(data)

# Initialisation de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de l'application
app.layout = dbc.Container([
    html.H1("Analyse de la Capacité Routière"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='capacity-analysis-chart')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Interprétation des Résultats"),
            html.Div(id='interpretation-text', style={'margin-top': '20px'})
        ])
    ])
])


# Callback pour générer le graphique et l'interprétation
@app.callback(
    Output('capacity-analysis-chart', 'figure'),
    Output('interpretation-text', 'children'),
    Input('capacity-analysis-chart', 'id')
)
def update_capacity_chart(_):
    # Créer un DataFrame pour l'analyse avec les pourcentages d'utilisation
    df_routes['utilization'] = df_routes['current_traffic'] / df_routes['capacity'] * 100

    # Créer un diagramme à barres empilées
    fig = px.bar(df_routes, x='route_name', y=['current_traffic', 'capacity'],
                 title="Capacité Routière vs Trafic Actuel",
                 labels={'value': 'Nombre de véhicules', 'variable': 'Indicateur'},
                 barmode='group')

    # Interprétation des résultats
    under_utilized = df_routes[df_routes['utilization'] < 70]['route_name'].tolist()
    over_utilized = df_routes[df_routes['utilization'] > 100]['route_name'].tolist()

    interpretation = []

    if under_utilized:
        interpretation.append(f"Les routes sous-utilisées ({len(under_utilized)}): {', '.join(under_utilized)}. "
                              "Ces routes ont une capacité bien supérieure à leur trafic actuel.")
    if over_utilized:
        interpretation.append(f"Les routes surchargées ({len(over_utilized)}): {', '.join(over_utilized)}. "
                              "Ces routes dépassent leur capacité maximale et nécessitent une intervention.")

    if not interpretation:
        interpretation.append("Toutes les routes sont utilisées dans des limites acceptables.")

    return fig, " ".join(interpretation)


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)

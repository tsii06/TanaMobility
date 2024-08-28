import pandas as pd
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

from src.figure.graphique import generate_graph_density
from src.figure.tableau import table_population

data = {
    "Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4"],
    "Valeur": [10, 20, 30, 40]
}

df = pd.DataFrame(data)
def create_visualisation(viz_type="graphique"):
    if viz_type == "graphique":
        content = generate_graph_density()
    elif viz_type == "tableau":
        content = table_population()

    else:
        content = html.Div("Visualisation non disponible.", style={'height': '70vh'})

    # Création d'un groupe de boutons pour choisir le type de visualisation
    button_group = dbc.ButtonGroup(
        [
            dbc.Button("Tableau", id="table-button", color="secondary", outline=True),
            dbc.Button("Graphique", id="graph-button", color="secondary", outline=True),
            dbc.Button("Carte", id="map-button", color="secondary", outline=True),
        ],
        className="me-2",
        style={"gap": "10px"}  # Ajout du gap de 10px entre les boutons
    )

    return html.Div(
        id="visualisation",
        children=[
            content,
            button_group,
        ],
        style={
            'padding': '10px',
            'background-color': '#f8f9fa',
            'border-radius': '8px',
            'margin-bottom': '20px',
            'height': '80vh'
        }
    )

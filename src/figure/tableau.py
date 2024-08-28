import dash_bootstrap_components as dbc
from dash import html

from src.data.traitement_data_visualisation import create_od_matrix, get_od_count, get_population


def table_od_matrix():
    dff = create_od_matrix(get_od_count())
    table = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)
    content = html.Div(
        table,
        style={
            'overflowX': 'auto',  # Scroll horizontal
            'overflowY': 'auto',  # Scroll vertical
            'max-height': '70vh',  # Limiter la hauteur du conteneur pour activer le scroll si nécessaire
            'max-width': '100%',  # S'assurer que le conteneur ne dépasse pas la largeur de la page
        }
    )
    return content


def table_population():
    # Charger les données de population à l'aide de la fonction get_population
    dff = get_population()

    # Créer le tableau à partir du DataFrame
    table = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)

    # Créer un conteneur avec des options de style pour le défilement
    content = html.Div(
        table,
        style={
            'overflowX': 'auto',  # Activer le scroll horizontal
            'overflowY': 'auto',  # Activer le scroll vertical
            'max-height': '70vh',  # Limiter la hauteur pour le scroll vertical si nécessaire
            'max-width': '100%',  # Limiter la largeur du tableau au conteneur
        }
    )

    return content
from dash.dependencies import Input, Output, State
import dash
from dash import html

from src.components.selection.deplacement import deplacement
from src.components.selection.description import description
from src.figure.graphique import generate_sankey_diagram
from src.figure.tableau import table_od_matrix


def detail_callback(app):
    @app.callback(
        Output('dynamic-content', 'children'),
        Input('description', 'n_clicks'),
        Input('offre_transport', 'n_clicks'),
        Input('pratiques_deplacement', 'n_clicks'),
        State('selected-section', 'data')
    )
    def update_content(n_clicks_desc, n_clicks_transport, n_clicks_deplacement, selected_section):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'description'  # Valeur par défaut
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Mettre à jour le contenu en fonction de l'élément du header cliqué
        if button_id == 'description':
            return description()
        elif button_id == 'offre_transport':
            return html.Div("Donnée non disponible"),

        elif button_id == 'pratiques_deplacement':
            return html.Div(
                [
                    deplacement(),
                    generate_sankey_diagram(),
                    table_od_matrix()
                ],
                style={
                    'background-color': '#f9f9f9',  # Couleur de fond gris clair
                    'border-radius': '8px',  # Coins arrondis
                    'margin': '30px',  # Espace entre les divs
                    'padding': '30px',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'justify-content': 'center'
                }
            )

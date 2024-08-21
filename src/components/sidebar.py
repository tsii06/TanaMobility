from dash import html, dcc, Dash, Output, Input
import dash_bootstrap_components as dbc

def sidebar(app):
    return html.Div(
        [
            html.Div(
                [
                    html.H3("Couches carto", style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ],
                style={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'display': 'flex',
                    'alignItems': 'center',  # Centrage vertical
                    'justifyContent': 'center'  # Centrage horizontal
                }
            ),

            # Démographie et Population
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dcc.RadioItems(
                                id='checklist-thematiques',
                                options=[
                                    {
                                        'label': html.Span([
                                            'Densité de la Population'
                                        ]),
                                        'value': 'densite'
                                    },
                                    {
                                        'label': html.Span([
                                            'Revenu Médian'
                                        ]),
                                        'value': 'revenu'
                                    },
                                ],
                                className="checklist-custom",
                                style={'padding': '10px'},
                                # value='densite'
                            ),
                        ],
                        title="Carte Choroplète",
                    ),
                ],
                flush=True
            ),
            html.Div(
                [
                    html.H3("Route", style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ],
                style={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'display': 'flex',
                    'alignItems': 'center',  # Centrage vertical
                    'justifyContent': 'center'  # Centrage horizontal
                }
            ),

            # Démographie et Population
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dcc.Checklist(
                                id='checklist-route',
                                options=[
                                    {
                                        'label': html.Span([
                                            'Segments routières avec le plus grand traffic'
                                        ]),
                                        'value': 'segment'
                                    },
                                    {
                                        'label': html.Span([
                                            'Densité du trafic le plus de volume '
                                        ]),
                                        'value': 'densitetrafic'
                                    },
                                    {
                                        'label': html.Span([
                                            'Itinéraire le plus empruntés'
                                        ]),
                                        'value': 'itineraire'
                                    },
                                ],
                                className="checklist-custom",
                                style={'padding': '10px'},
                            ),
                        ],
                        title="Couche routieres",
                    ),
                ],
                flush=True
            ),
            html.Div(
                [
                    html.H3("Thèmes", style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ],
                style={
                    'textAlign': 'center',
                    'padding': '10px',
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'display': 'flex',
                    'alignItems': 'center',  # Centrage vertical
                    'justifyContent': 'center'  # Centrage horizontal
                }
            ),

            # Économie et Revenu
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dcc.Checklist(
                                id='checklist',
                                options=[
                                    {
                                        'label': html.Span([
                                            'Densite de population'
                                        ]),
                                        'value': 'densite'
                                    },
                                    {
                                        'label': html.Span([
                                            'Volume de deplacement'
                                        ]),
                                        'value': 'deplacement'
                                    },
                                    {
                                        'label': html.Span([
                                            'Typologie modale'
                                        ]),
                                        'value': 'typologie'
                                    },
                                    {
                                        'label': html.Span([
                                            'Matrice OD'
                                        ]),
                                        'value': 'matrice'
                                    },
                                ],
                                className="checklist-custom",
                                style={'padding': '10px'},
                            ),
                        ],
                        title="Économie et Revenu",
                    ),
                ],
                flush=True
            ),


        ],
        style={
            'height': '90vh',  # Ajustez la hauteur selon vos besoins
            'overflow-y': 'auto',  # Active le défilement vertical
            'backgroundColor': '#2c3e50',  # Couleur de fond du sidebar
            'color': 'white',  # Couleur du texte
        }
    )
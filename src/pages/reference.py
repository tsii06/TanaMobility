from dash import html
import dash_bootstrap_components as dbc

def reference():
    # Contenu de la référence dans un dbc.Container
    content = dbc.Container(
        children=[
            dbc.Row(
                dbc.Col(
                    html.H4("Références et Sources de Données", className='mb-4'),  # mb-4 est une classe Bootstrap pour la marge
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P([
                        "Cette application appartient à ",
                        html.A("AGETIPA", href="https://www.agetipa.mg", target="_blank"),
                    ]),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Technologies utilisées : PostgreSQL, Plotly Dash, Python"),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Ul([
                        html.Li("Source de données avec liens de téléchargement :"),
                        html.Ul([
                            html.Li(html.A("GeoJSON - Répartition zonale PMUD", href="https://www.exemple.com/repartition_zonale.geojson", target="_blank")),
                            html.Li(html.A("GeoJSON - Routes (Primaire, Secondaire, Tertiaire)", href="https://www.exemple.com/routes.geojson", target="_blank")),
                            html.Li(html.A("Données de Population (INSTAT)", href="https://www.exemple.com/donnees_population_instat.csv", target="_blank")),
                            html.Li(html.A("Données de Volume de Déplacement (Comptage Réel sur Terrain)", href="https://www.exemple.com/donnees_volume_deplacement.csv", target="_blank")),
                        ]),
                    ]),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Pour plus d'informations sur les sources et les méthodologies utilisées, veuillez consulter les liens ci-dessus ou contacter notre équipe."),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.Span(
                            html.I(className='fas fa-info-circle', style={'cursor': 'pointer', 'margin-left': '5px'}),
                            id='info-icon',  # ID pour cibler dans le callback
                            style={'display': 'inline-block'}
                        ),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader("Information additionnelle"),
                                dbc.PopoverBody("Les données utilisées sont issues de sources fiables et vérifiées par des experts en démographie et en mobilité."),
                            ],
                            id="popover",
                            target="info-icon",
                            trigger="hover",
                        )
                    ],
                    width=12
                )
            )
        ],
        style={
            'padding': '20px',
            'border': '1px solid #ddd',
            'border-radius': '5px',
            'margin-top': '20px',
            'background-color': '#f9f9f9'
        }
    )

    return content

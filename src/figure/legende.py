from dash import html
import dash_bootstrap_components as dbc  # Assurez-vous d'importer dash_bootstrap_components

def generate_legend(titre, couleurs, valeurs, legend_id):
    legend_items = []

    for couleur, valeur in zip(couleurs, valeurs):
        legend_items.append(
            html.Div(
                children=[
                    html.Span(
                        style={
                            'background-color': couleur,
                            'display': 'inline-block',
                            'width': '20px',
                            'height': '20px',
                            'margin-right': '10px',
                            'border-radius': '50%',
                        }
                    ),
                    html.Span(str(valeur))
                ],
                className='legend-attribut-div'
            )
        )

    # Utilisation d'un identifiant unique pour chaque icône et popover
    info_icon_id = f'info-icon-{legend_id}'
    popover_id = f'popover-{legend_id}'

    return html.Div(
        children=[
            html.H4(
                children=[
                    titre,
                    html.Span(
                        html.I(className='fas fa-info-circle', style={'margin-left': '0.5rem', 'font-size': '1rem'}),
                        id=info_icon_id,  # Identifiant unique pour chaque popover
                        style={'cursor': 'pointer'}
                    ),
                ],
                className='legend-div'
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Information sur la visualisation"),
                    dbc.PopoverBody([
                        "Cette visualisation montre la distribution de la population masculine et féminine par tranche d'âge.",
                        html.Br(),
                        "Source de données: ",
                        html.A("AGETIPA", href="https://www.exemple.com", target="_blank", style={'color': '#007bff'})
                    ])
                ],
                id=popover_id,  # Cible le nouvel icône d'information
                target=info_icon_id,
                trigger="hover",
                placement='right',
                style={'font-size': '0.8rem', 'max-width': '250px'}
            ),
            *legend_items
        ],
    )

from dash import html

def generate_legend(titre, couleurs, valeurs):
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

    return html.Div(
        children=[
            html.H4(titre, className='legend-div'),  # Ajout du titre
            *legend_items
        ],
    )

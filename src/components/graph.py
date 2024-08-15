from dash import html, Dash
def graph(app: Dash):
    return html.Div([
        html.Div(id='graph-content', children=[
            html.Div(id='densite',),
            html.Div(id='typologie', ),
            html.Div(id='finances',),
            html.Div(id='distance',)
        ])
    ], style={
        'height': '90vh',  # Ajustez la hauteur selon vos besoins
        'overflow-y': 'auto',  # Active le défilement vertical
    })



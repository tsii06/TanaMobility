from dash import dcc, html, Dash, Input, Output

def create_map(app: Dash):

    return html.Div(
        children=[
            dcc.Graph(
                id='map',
                config={
                    'displayModeBar': False
                },
                style={'width': '100%', 'height': 'calc(80vh - 60px)'}
            ),
            html.Div(
                id='legend',
                children=[
                    html.Div(
                        'Légende personnalisée 1',
                        style={'color': 'blue'}
                    ),
                    html.Div(
                        'Légende personnalisée 2',
                        style={'color': 'green'}
                    ),
                    # Ajoutez ici d'autres légendes personnalisées selon vos besoins
                ],
                style={'height': '20vh', 'padding': '10px', 'background-color': '#f8f9fa'}
            )
        ],
        style={'display': 'flex', 'flex-direction': 'column', 'height': '100vh'}
    )

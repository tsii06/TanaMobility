from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
def create_map(app: Dash):
    return html.Div(
        children=[
            dcc.Graph(
                id='map',
                config={
                    'displayModeBar': False
                },
                style={'width': '100%', 'height': 'calc(100vh - 70px)'}
            ),
            html.Div(
                style={
                    'position': 'absolute',  # Permet de superposer la légende sur la carte
                    'top': '20px',  # Ajuste la position de la légende en haut
                    'right': '10px',  # Ajuste la position de la légende à gauche
                    'background-color': 'rgba(255, 255, 255, 0.8)',  # Fond blanc semi-transparent
                    'padding': '10px',  # Ajoute un peu de padding autour du contenu
                    'border-radius': '5px',  # Coins arrondis pour un style plus moderne
                    'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)',  # Légère ombre pour se démarquer
                    'z-index': '1000',  # Assure que la légende est au-dessus de la carte
                    'max-height': '40vh',  # Limite la hauteur maximale
                    'overflow-y': 'auto',  # Ajoute le défilement vertical si le contenu dépasse la hauteur
                },
                className='scroll-style',
                children=[
                    html.Div(id='population-legend'),
                    html.Div(id='segment-legend'),
                    html.Div(id='route-legend'),
                    html.Div(id='density-legend')
                ]
            ),
            html.Button(
                html.I(className="fas fa-expand"),  # Utilisation de l'icône "expand"
                id='fullscreen-btn',
                style={
                    'position': 'absolute',
                    'bottom': '80px',  # Positionné en bas
                    'right': '10px',  # Positionné à droite
                    'z-index': '1001',  # Assure que le bouton est au-dessus de la carte
                    'padding': '5px',
                    'border-radius': '5px',
                    'background-color': '#cfe2ff',
                    'color': 'white',
                    'border': 'none',
                    'cursor': 'pointer',
                    'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)',
                }
            ),
            html.Div(id='popup-div', style={'display': 'none'}, children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='zone-title'),
                        html.P("Cliquez sur le bouton ci-dessous pour plus de détails."),
                        dbc.Button("Voir les détails", id='details-button', color="primary")
                    ])
                ], style={'position': 'absolute', 'top': '10%', 'left': '50%', 'transform': 'translate(-50%, -50%)'})
            ])
        ],
        style={'position': 'relative', 'height': '100vh'}  # Position relative pour le conteneur parent
    )

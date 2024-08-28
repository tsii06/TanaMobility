from dash import html, dash, no_update
from dash.dependencies import Input, Output, State

def register_double_click(app):
    @app.callback(
        Output('url', 'pathname'),  # Modifie l'URL de l'application
        Input('map', 'clickData'),  # Capture les données du clic
        State('map', 'clickData')  # Capture les données de l'état du clic
    )
    def on_double_click(click_data, state_click_data):
        if click_data:
            # Extraire le nom de la zone
            zone = click_data['points'][0]['location']

            # Mettre à jour l'URL pour inclure l'identifiant de la zone
            return f"/details/{zone}"

        # Ne rien faire si aucun clic détecté
        print("Aucun clic détecté")
        return no_update

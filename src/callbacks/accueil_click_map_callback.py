from dash.dependencies import Input, Output, State

from src.data.utils import find_zone_by_coordinates

# callback pour detecter le zone cliqué sur le carte
def register_click_map_callback(app, gdf_communes):
    @app.callback(
        Output('clicked-zones', 'data'),
        [Input('map', 'clickData')],
        [State('clicked-zones', 'data')]
    )
    def update_graph_based_on_click(clickData, clicked_zones):
        if clickData is None:
            return clicked_zones

        # Vérifier si 'location' est présent dans clickData
        if 'location' in clickData['points'][0]:
            clicked_location = clickData['points'][0]['location']
        else:
            # Récupérer lat et lon si 'location' n'est pas présent
            lat = clickData['points'][0]['lat']
            lon = clickData['points'][0]['lon']
            clicked_location = find_zone_by_coordinates(lat, lon, gdf_communes)

        # Si une zone est trouvée, ajouter à la liste des zones cliquées
        if clicked_location and clicked_location not in clicked_zones:
            clicked_zones.append(clicked_location)

        return clicked_zones

# callback pour detecter l'agrandissement du carte
def plein_ecran_carte(app):
    @app.callback(
        [Output('map-col', 'style'),
         Output('graph-col', 'style')],
        [Input('fullscreen-btn', 'n_clicks')],
        [State('map-col', 'style')]
    )
    def toggle_view(n_clicks, map_style):
        if n_clicks:
            if map_style and map_style.get('width') == '100%':
                return ({'width': 'calc(100% / 2)', 'padding': '0'}
                        , {'width': 'calc(100% / 2)', 'padding': '0','height': '90vh',  'overflow-y': 'auto' })
            else:
                # Agrandir la carte et masquer le graphique
                return { 'width': '100%', 'padding': '0'}, {'display':'none'}
        return map_style, {'width': 'calc(100% / 2)', 'padding': '0','height': '90vh',  'overflow-y': 'auto' }

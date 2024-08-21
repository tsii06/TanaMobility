from dash.dependencies import Input, Output, State
def register_click_map_callback(app):
    @app.callback(
         Output('clicked-zones', 'data'),
        [Input('map', 'clickData')],
        [State('clicked-zones', 'data')]
    )
    def update_graph_based_on_click(clickData, clicked_zones):
        if clickData is None:
            return clicked_zones

        clicked_location = clickData['points'][0]['location']
        print(clicked_location)
        print(clickData)

        # Ajouter la zone cliquée à la liste
        if clicked_location not in clicked_zones:
            clicked_zones.append(clicked_location)

        return clicked_zones

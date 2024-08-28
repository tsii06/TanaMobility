from dash.dependencies import Input, Output
from src.figure.graphique import generate_graph_density, generate_graph_deplacement, generate_graph_vehicules, \
    generate_sankey_diagram
from dash import html


def register_callbacks(app):
    @app.callback(
        [Output('selected-carto', 'data'),
         Output('selected-thematiques', 'data'),
         Output('selected-route', 'data')],
        [Input('checklist-carto', 'value'),
         Input('checklist-thematiques', 'value'),
         Input('checklist-route', 'value')]
    )
    def update_selected(selected_values, selected_carto, selected_route):
        # Ajouter des valeurs par défaut si les valeurs sont None
        selected_values = selected_values or []
        selected_carto = selected_carto or []
        selected_route = selected_route or []

        return selected_values, selected_carto, selected_route

    @app.callback(
        Output('densite', 'children'),
        [Input('selected-thematiques', 'data')]
    )
    def update_density_graph(selected_thematiques):
        # Vérifier si selected_thematiques n'est pas None
        if selected_thematiques and 'densite' in selected_thematiques:
            return generate_graph_density()
        return html.Div()

    @app.callback(
        Output('typologie', 'children'),
        [Input('selected-thematiques', 'data'),
         Input('clicked-zones', 'data')]
    )
    def update_typology_graph(selected_thematiques, clicked_zones):
        # Vérifier si selected_thematiques et clicked_zones ne sont pas None
        if selected_thematiques and 'typologie' in selected_thematiques:
            return generate_graph_vehicules(noms_zones=clicked_zones)
        return html.Div()

    @app.callback(
        Output('matrice', 'children'),
        [Input('selected-thematiques', 'data'),
         Input('clicked-zones', 'data')]
    )
    def update_matrice_graph(selected_thematiques, clicked_zones):
        # Vérifier si selected_thematiques et clicked_zones ne sont pas None
        if selected_thematiques and 'matrice' in selected_thematiques:
            return generate_sankey_diagram(noms_zones=clicked_zones)
        return html.Div()

    @app.callback(
        Output('finances', 'children'),
        [Input('selected-thematiques', 'data'),
         Input('clicked-zones', 'data')]
    )
    def update_finances_graph(selected_thematiques, clicked_zones):
        # Vérifier si selected_thematiques et clicked_zones ne sont pas None
        if selected_thematiques and 'deplacement' in selected_thematiques:
            return generate_graph_deplacement(noms_zones=clicked_zones)
        return html.Div()

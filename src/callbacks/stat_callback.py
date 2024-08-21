from dash.dependencies import Input, Output
from src.figure.graphique import generate_graph_density, generate_graph_deplacement, generate_graph_vehicules, \
    generate_sankey_diagram, generate_chord_diagram
from dash import html, dcc


def register_callbacks(app):
    @app.callback(
        [Output('selected-thematiques', 'data'),
         Output('selected-carto', 'data'),
         Output('selected-route', 'data')],
        [Input('checklist-thematiques', 'value'),
         Input('checklist', 'value'),
         Input('checklist-route', 'value')]
    )
    def update_selected(selected_values, selected_carto,selected_route):
        return selected_values, selected_carto,selected_route

    @app.callback(
        [Output('densite', 'children'),
         Output('typologie', 'children'),
         Output('finances', 'children'),
         Output('matrice', 'children')],
        [Input('selected-carto', 'data'),
         Input('selected-thematiques', 'data'),
         Input('clicked-zones', 'data')
    ]
    )
    def update_graphs(selected_carto, selected_thematiques, clicked_zones):
        if not selected_thematiques or not selected_carto:
            return html.Div(), html.Div(), html.Div(), html.Div()

        # Utiliser les zones cliquées dans les graphiques
        if 'matrice' in selected_thematiques or 'matrice' in selected_carto:
            matrice_od = generate_sankey_diagram(noms_zones=clicked_zones)
        else:
            matrice_od = html.Div()

        if 'densite' in selected_thematiques or 'densite' in selected_carto:
            densite_content = generate_graph_density()
        else:
            densite_content = html.Div()

        if 'deplacement' in selected_thematiques or 'deplacement' in selected_carto:
            distance_content = generate_graph_deplacement(noms_zones=clicked_zones)
        else:
            distance_content = html.Div()

        if 'typologie' in selected_thematiques or 'typologie' in selected_carto:
            typologie_content = generate_graph_vehicules(noms_zones=clicked_zones)
        else:
            typologie_content = html.Div()

        return densite_content, typologie_content, matrice_od, distance_content

    @app.callback(
        Output('content', 'children'),
        Input('checklist-thematiques', 'value'),
        Input('checklist', 'value')
    )
    def update_graph(selected_thematique, selected_checklist):
        # Créer un composant Graph en fonction de l'option sélectionnée
        scroll_id = ''
        if selected_thematique == 'densite':
            scroll_id = 'graph-densite'
        elif selected_thematique == 'revenu':
            scroll_id = 'graph-revenu'
        elif selected_checklist == 'deplacement':
            scroll_id = 'deplacement-graph'
        elif selected_checklist == 'typologie':
            scroll_id = 'graph-typologie'
        elif selected_checklist == 'matrice':
            scroll_id = 'graph-taux-pauvrete'

        if scroll_id:
            return dcc.Location(id='scroll', href=f'#{scroll_id}', refresh=False)

        return dcc.Graph(id=scroll_id)
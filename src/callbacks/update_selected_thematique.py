from dash.dependencies import Input, Output

def register_callbacks(app):
    @app.callback(
        Output('selected-thematiques', 'data'),
        [Input('checklist-thematiques', 'value'),
         Input('checklist-route', 'value')]
    )
    def update_selected(selected_values, selected_route):
        # Ajouter des valeurs par défaut si les valeurs sont None
        selected_values = selected_values or []
        selected_route = selected_route or []
        combined_selection = list(set(selected_values + selected_route))
        return combined_selection



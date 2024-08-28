from dash import Output, Input, callback
import dash
from src.components.selection.selection_visualisation import create_visualisation

def selection_callback(app):
    @app.callback(
        Output("visualisation", "children"),
        [Input("table-button", "n_clicks"),
         Input("graph-button", "n_clicks"),
         Input("map-button", "n_clicks")]
    )
    def update_visualisation(table_clicks, graph_clicks, map_clicks):
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'graph-button'  # Valeur par défaut
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "table-button":
            return create_visualisation(viz_type="tableau")
        elif button_id == "graph-button":
            return create_visualisation(viz_type="graphique")
        elif button_id == "map-button":
            return create_visualisation(viz_type="carte")  # À implémenter par vous
        else:
            return create_visualisation(viz_type="graphique")  # Par défaut

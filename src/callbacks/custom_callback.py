from dash.dependencies import Input, Output, State

def custom_callback(app):
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


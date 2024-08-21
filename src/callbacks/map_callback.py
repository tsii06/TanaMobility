from dash.dependencies import Input, Output
from src.figure.carte import create_density_map, create_revenue_map, create_default_map, create_route, \
    create_traffic_markers, create_traffic_density_map, create_route_with_traffic
import plotly.graph_objs as go
from src.data.traitement import loadRevenuCarte, join_centroids_and_pivoted_data


def register_map_callbacks(app, gdf_merged, density, gdf_geojson):
    @app.callback(
        Output('map', 'figure'),
        [Input('checklist-thematiques', 'value'),
         Input('checklist-route', 'value'),]
    )
    def update_figure(selected_thematiques,selected_route):
        fig = go.Figure()

        # Initialiser la carte avec Open Street Map et la répartition régionale sans population par défaut
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=-18.8792, lon=47.5079),
                zoom=9
            ),
            paper_bgcolor="lightgrey",
            showlegend=False,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        # Vérifier si selected_thematiques n'est pas None et ajouter les traces seulement si les thématiques correspondantes sont sélectionnées
        if selected_thematiques:
            if 'densite' in selected_thematiques:
                fig.add_trace(create_density_map(density, gdf_merged))

            if 'revenu' in selected_thematiques:
                df = loadRevenuCarte()  # Récupérer les données du revenu médian
                fig.add_trace(create_revenue_map(density, df))
        else:
            fig.add_trace(create_default_map(gdf_geojson))

        fig.add_trace(create_route())

        if selected_route:
            if 'densitetrafic' in selected_route:
                fig.add_trace(create_traffic_density_map())

            if 'segment' in selected_route:
                fig.add_trace(create_traffic_markers())

            if 'itineraire' in selected_route:
                traces = create_route_with_traffic()
                fig.add_traces(traces)


        return fig

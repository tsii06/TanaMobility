from dash.dependencies import Input, Output
from src.figure.carte import create_density_map, create_revenue_map, create_default_map, create_vehicle_distribution_map
import plotly.graph_objs as go
from src.data.traitement import loadRevenuCarte, join_centroids_and_pivoted_data


def register_map_callbacks(app, gdf_merged, density, gdf_geojson):
    @app.callback(
        Output('map', 'figure'),
        [Input('checklist-thematiques', 'value')]
    )
    def update_figure(selected_thematiques):
        fig = go.Figure()

        # Initialiser la carte avec Open Street Map et la répartition régionale sans population par défaut
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
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
            if 'typologie' in selected_thematiques:
                df = join_centroids_and_pivoted_data()
                fig.add_trace(create_vehicle_distribution_map(df))
        else:
            # Default case when no thematics are selected
            fig.add_trace(create_default_map(gdf_geojson))

        return fig

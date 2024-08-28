from dash.dependencies import Input, Output
from src.figure.carte import create_density_map, create_revenue_map, create_default_map, create_route, \
    create_traffic_markers, create_traffic_density_map, create_route_with_traffic, create_contour_map
import plotly.graph_objs as go


def carte_update_callback(app, gdf_merged,df, density, gdf_geojson,lats, lons,congestion,df_filtered):
    @app.callback(
        Output('map', 'figure'),
        [Input('selected-thematiques', 'data')]
    )
    def update_figure(selected_thematiques):
        fig = go.Figure()

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
        fig.add_trace(create_route(lats, lons))
        if selected_thematiques:
            if 'densite' in selected_thematiques:
                fig.add_trace(create_density_map(density, gdf_merged))
                # traces =create_contour_map((gdf_merged))
                # for trace in traces:
                #     fig.add_trace(trace)

            if 'revenu' in selected_thematiques:
                fig.add_trace(create_revenue_map(density,df))

            if 'densitetrafic' in selected_thematiques:
                fig.add_trace(create_traffic_density_map(congestion))

            if 'segment' in selected_thematiques:
                fig.add_trace(create_traffic_markers(congestion))

            if 'itineraire' in selected_thematiques:
                traces = create_route_with_traffic(df_filtered)
                fig.add_traces(traces)

        else:
            fig.add_trace(create_default_map(gdf_geojson))



        return fig

# src/map_creation.py

import plotly.graph_objs as go

def create_density_map(density, gdf_merged):
    """Crée une carte choroplèthe pour la densité de population."""
    return go.Choroplethmapbox(
        geojson=density,
        locations=gdf_merged['ensemble_concat'],
        z=gdf_merged['population_totale'],
        colorscale='Reds',
        marker_opacity=0.8,
        marker_line_width=1,
        featureidkey='properties.ensemble_concat',
        marker_line_color='black',
        hoverinfo='text',
        hovertext=gdf_merged['ensemble_1'] + '<br>Population: ' + gdf_merged['population_totale'].astype(str),
        colorbar=dict(
            title="AVG",
            x=1,
            y=0.5,
            xanchor="left",
            yanchor="middle",
        )
    )

def create_revenue_map(density, df):
    """Crée une carte choroplèthe pour le revenu médian."""
    return go.Choroplethmapbox(
        geojson=density,
        locations=df['ensemble_concat'],
        z=df['revenu_median'],
        colorscale="Blues",
        marker_opacity=0.8,
        marker_line_width=1,
        featureidkey="properties.ensemble_concat",
        marker_line_color='black',
        hoverinfo='text',
        hovertext=df['ensemble_concat'] + '<br>Revenu Médian: ' + df['revenu_median'].astype(str),
        colorbar=dict(
            title="AVG",
            x=1,
            y=0.5,
            xanchor="left",
            yanchor="middle",
        )
    )

def create_default_map(gdf_geojson):
    """Crée une carte par défaut avec un thème grisé."""
    return go.Choroplethmapbox(
        geojson=gdf_geojson.__geo_interface__,
        locations=gdf_geojson['combined'],
        z=[0] * len(gdf_geojson),
        colorscale='Greys',
        marker_opacity=0,
        marker_line_width=1,
        featureidkey='properties.combined',
        marker_line_color='black',
        hoverinfo='text',
        hovertext=gdf_geojson['ensemble_1'],
    )


def create_vehicle_distribution_map(df_merged):
    """Crée une carte avec des diagrammes circulaires représentant la répartition des types de véhicules."""
    fig = go.Figure()

    # Ajouter chaque pie chart à la figure
    for _, row in df_merged.iterrows():
        labels = [col for col in df_merged.columns if
                  col not in ['ensemble_concat', 'centroid_x', 'centroid_y', 'zone_nom', 'total_vehicules']]
        values = [row[col] for col in labels]

        # Ajouter un diagramme circulaire (pie chart) pour chaque zone
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            textinfo='label+percent',
            hoverinfo='label+value',
            name=row['ensemble_concat'],
            marker=dict(line=dict(color='black', width=1)),
            domain=dict(
                x=[row['centroid_x'] - 0.01, row['centroid_x'] + 0.01],
                y=[row['centroid_y'] - 0.01, row['centroid_y'] + 0.01]
            )
        ))
    return fig

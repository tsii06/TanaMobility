# src/map_creation.py
import geopandas as gpd
import plotly.graph_objs as go

from src.data.traitement import get_congestion_point


def create_density_map(density, gdf_merged):
    """Crée une carte choroplèthe pour la densité de population."""
    return go.Choroplethmapbox(
        geojson=density,
        locations=gdf_merged['identifiant_commune'],
        z=gdf_merged['population_totale'],
        colorscale='Reds',
        marker_opacity=0.6,
        marker_line_width=1,
        featureidkey='properties.identifiant_commune',
        marker_line_color='black',
        hoverinfo='text',
        hovertext=gdf_merged['ensemble_concat'] + '<br>Revenu Médian: ' + gdf_merged['population_totale'].astype(str),
        showscale=False
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
        showscale=False
    )

def create_default_map(gdf_geojson):
    """Crée une carte par défaut avec un thème grisé."""
    return go.Choroplethmapbox(
        geojson=gdf_geojson.__geo_interface__,
        locations=gdf_geojson['combined'],
        z=[0] * len(gdf_geojson),
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
        marker_opacity=0.8,
        marker_line_width=1,
        featureidkey='properties.combined',
        marker_line_color='black',
        hoverinfo='text',
        hovertext=gdf_geojson['combined'],
        showscale=False
    )

def create_route():
    # Charger le fichier GeoJSON
    gdf = gpd.read_file(r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson")

    # Filtrer les routes par type (primary, secondary, tertiary)
    gdf_filtered = gdf[gdf['highway'].isin(['primary', 'secondary', 'tertiary'])]

    # Reprojection en EPSG:3857 pour un calcul correct du centroid
    gdf_filtered = gdf_filtered.to_crs(epsg=3857)

    # Reprojection en EPSG:4326 pour l'affichage correct
    gdf_filtered = gdf_filtered.to_crs(epsg=4326)

    # Extraire les coordonnées des lignes
    lats, lons = [], []
    for geom in gdf_filtered.geometry:
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                lons.extend([coord[0] for coord in line.coords] + [None])
                lats.extend([coord[1] for coord in line.coords] + [None])
        elif geom.geom_type == 'LineString':
            lons.extend([coord[0] for coord in geom.coords] + [None])
            lats.extend([coord[1] for coord in geom.coords] + [None])

    # Créer une trace pour afficher toutes les routes avec la même couleur et la même largeur
    return go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='lines',
        line=dict(width=3, color='rgba(128, 128, 128, 0.8)'),
        name='Routes',
        hoverinfo='skip'
    )

def create_traffic_markers():
    # Créer une trace pour les marqueurs de trafic
    df = get_congestion_point()
    marker_trace = go.Scattermapbox(
        lat=df['centroid'].apply(lambda point: point.y),  # Latitude
        lon=df['centroid'].apply(lambda point: point.x),  # Longitude
        mode='markers',
        marker=dict(
            size=20,  # Ajuster la taille en fonction du volume
            color=df['total_traffic_volume'],       # Couleur en fonction du volume
            colorscale='YlOrRd',                    # Echelle de couleurs (jaune à rouge)
            cmin=df['total_traffic_volume'].min(),
            cmax=df['total_traffic_volume'].max(),
            showscale=False
        ),

        text=df['total_traffic_volume'],
        name='Congestion',
        hoverinfo='skip'

    )
    return marker_trace


def create_traffic_density_map():
    df = get_congestion_point()

    # Assurez-vous que les coordonnées sont bien des flottants
    df['lat'] = df['centroid'].apply(lambda point: point.y if point else None)
    df['lon'] = df['centroid'].apply(lambda point: point.x if point else None)

    # Vérifiez que les données ne contiennent pas de valeurs manquantes
    df = df.dropna(subset=['lat', 'lon', 'total_traffic_volume'])

    # Créer une trace pour la carte de densité
    return go.Densitymapbox(
        lat=df['lat'],  # Latitude
        lon=df['lon'],  # Longitude
        z=df['total_traffic_volume'],  # Volume de trafic utilisé pour l'intensité
        radius=50,  # Taille des points, ajuster selon la densité souhaitée
        colorscale='Reds',  # Echelle de couleurs
        zmin=df['total_traffic_volume'].min(),
        zmax=df['total_traffic_volume'].max(),
        opacity=0.9,
        showscale=False
    )
    # Configurer la carte


def create_route_with_traffic():
    # Charger le fichier GeoJSON
    gdf = gpd.read_file(r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson")

    # Charger les volumes de trafic depuis une autre source (par exemple, une base de données ou un CSV)
    df_traffic = get_congestion_point()  # Cette fonction doit retourner un DataFrame avec les volumes de trafic
    df_traffic['id_osm'] = df_traffic['id_osm'].astype('int32')  # Assurez-vous que les types sont cohérents
    # Filtrer les routes par type (primary, secondary, tertiary)
    gdf_filtered = gdf[gdf['highway'].isin(['primary', 'secondary', 'tertiary'])]

    # Reprojection en EPSG:3857 pour un calcul correct des coordonnées
    gdf_filtered = gdf_filtered.to_crs(epsg=3857)

    # Reprojection en EPSG:4326 pour l'affichage correct
    gdf_filtered = gdf_filtered.to_crs(epsg=4326)

    # Jointure des données de trafic avec les données géométriques
    gdf_filtered = gdf_filtered.merge(df_traffic[['id_osm', 'total_traffic_volume']], left_on='osm_id', right_on='id_osm', how='left')
    gdf_filtered['total_traffic_volume'] = gdf_filtered['total_traffic_volume'].fillna(0)
    # Extraire les coordonnées des lignes et ajuster les largeurs/couleurs en fonction du volume de trafic
    traces = []
    for _, row in gdf_filtered.iterrows():
        lats, lons = [], []
        geom = row['geometry']
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                lons.extend([coord[0] for coord in line.coords] + [None])
                lats.extend([coord[1] for coord in line.coords] + [None])
        elif geom.geom_type == 'LineString':
            lons.extend([coord[0] for coord in geom.coords] + [None])
            lats.extend([coord[1] for coord in geom.coords] + [None])

        if row['total_traffic_volume'] > 0:
            traces.append(go.Scattermapbox(
                lat=lats,
                lon=lons,
                mode='lines',
                line=dict(
                    width=max(row['total_traffic_volume'] / 50, 1),  # Ajuster la largeur des lignes selon le volume
                    color='blue'  # Vous pouvez ajuster la couleur ici ou ajouter une échelle de couleurs
                ),
                opacity=min(row['total_traffic_volume'] / 1000, 1),  # Ajuster l'opacité au niveau de la trace
                hoverinfo='skip',
                name=row['osm_id']
            ))

    # Créer la figure
    return traces

from dash import dcc, html, Dash
import geopandas as gpd
import plotly.graph_objs as go

# Charger le fichier GeoJSON
gdf = gpd.read_file('Antananarivo_voiries_primaires-secondaires-tertiaire.geojson')

# Filtrer les routes par type
gdf_primary = gdf[gdf['highway'] == 'primary']
gdf_secondary = gdf[gdf['highway'] == 'secondary']
gdf_tertiary = gdf[gdf['highway'] == 'tertiary']

# Reprojection en EPSG:3857 pour un calcul correct du centroid
gdf_primary = gdf_primary.to_crs(epsg=3857)
gdf_secondary = gdf_secondary.to_crs(epsg=3857)
gdf_tertiary = gdf_tertiary.to_crs(epsg=3857)

# Reprojection en EPSG:4326 pour l'affichage correct
gdf_primary = gdf_primary.to_crs(epsg=4326)
gdf_secondary = gdf_secondary.to_crs(epsg=4326)
gdf_tertiary = gdf_tertiary.to_crs(epsg=4326)

# Fonction pour extraire les coordonnées et d'autres informations
def get_line_info(geometry, road_type):
    lats, lons, texts = [], [], []
    for geom in geometry:
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                lons.extend([coord[0] for coord in line.coords] + [None])
                lats.extend([coord[1] for coord in line.coords] + [None])
                texts.extend([f"Type: {road_type}"] * len(line.coords) + [None])
        elif geom.geom_type == 'LineString':
            lons.extend([coord[0] for coord in geom.coords] + [None])
            lats.extend([coord[1] for coord in geom.coords] + [None])
            texts.extend([f"Type: {road_type}"] * len(geom.coords) + [None])
    return lats, lons, texts

# Extraire les coordonnées et les informations pour chaque type de route
lats_primary, lons_primary, texts_primary = get_line_info(gdf_primary.geometry, 'Primary')
lats_secondary, lons_secondary, texts_secondary = get_line_info(gdf_secondary.geometry, 'Secondary')
lats_tertiary, lons_tertiary, texts_tertiary = get_line_info(gdf_tertiary.geometry, 'Tertiary')

# Calcul du centroïde après la reprojection
# Calcul du centroïde après la reprojection en EPSG:3857
centroid = gdf_primary.to_crs(epsg=3857).geometry.centroid

# Reprojeter le centroïde en EPSG:4326 pour l'utiliser sur la carte
centroid_lat = centroid.to_crs(epsg=4326).y.mean()
centroid_lon = centroid.to_crs(epsg=4326).x.mean()


# Créer des traces pour chaque type de route avec des lignes continues et texte de survol
trace_primary = go.Scattermapbox(
    lat=lats_primary,
    lon=lons_primary,
    mode='lines',
    line=dict(width=5, color='red'),
    name='Routes Primaires',
    text=texts_primary,
    hoverinfo='text'
)

trace_secondary = go.Scattermapbox(
    lat=lats_secondary,
    lon=lons_secondary,
    mode='lines',
    line=dict(width=3, color='blue'),
    name='Routes Secondaires',
    text=texts_secondary,
    hoverinfo='text'
)

trace_tertiary = go.Scattermapbox(
    lat=lats_tertiary,
    lon=lons_tertiary,
    mode='lines',
    line=dict(width=2, color='green'),
    name='Routes Tertiaires',
    text=texts_tertiary,
    hoverinfo='text'
)

layout = go.Layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=centroid_lat, lon=centroid_lon),
        zoom=12
    )
)

fig = go.Figure(data=[trace_primary, trace_secondary, trace_tertiary], layout=layout)

# Initialiser l'application Dash
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

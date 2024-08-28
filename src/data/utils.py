from shapely import Point
import geopandas as gpd

gdf = gpd.read_file(r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson")
def find_zone_by_coordinates(lat, lon, gdf_communes):
    point = Point(lon, lat)
    for _, row in gdf_communes.iterrows():
        if row['geometry'].contains(point):
            return row['identifiant_commune']
    return None

def extract_lat_lon():
    gdf_filtered = gdf[gdf['highway'].isin(['primary', 'secondary', 'tertiary'])]
    gdf_filtered = gdf_filtered.to_crs(epsg=3857)
    gdf_filtered = gdf_filtered.to_crs(epsg=4326)
    lats, lons = [], []
    for geom in gdf_filtered.geometry:
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                lons.extend([coord[0] for coord in line.coords] + [None])
                lats.extend([coord[1] for coord in line.coords] + [None])
        elif geom.geom_type == 'LineString':
            lons.extend([coord[0] for coord in geom.coords] + [None])
            lats.extend([coord[1] for coord in geom.coords] + [None])
    return lats, lons

def calculate_centroids_by_zone():
    gdf_geojson = loadGeojson()
    gdf_projected = gdf_geojson.to_crs(epsg=3857)
    gdf_projected['centroid'] = gdf_projected.geometry.centroid
    gdf_geojson['centroid'] = gdf_projected['centroid'].to_crs(epsg=4326)
    gdf_geojson['centroid_x'] = gdf_geojson['centroid'].x
    gdf_geojson['centroid_y'] = gdf_geojson['centroid'].y
    df_centroids = gdf_geojson[['ensemble_concat', 'centroid_x', 'centroid_y']]
    return df_centroids

def loadGeojson():
    geojson_path = r"data/Zonage_interne_externe_PMUD.geojson"
    gdf_geojson = gpd.read_file(geojson_path)
    gdf_geojson['ensemble_concat'] = gdf_geojson['ensemble d'].astype(str) + '_' + gdf_geojson['ensemble_1'].astype(
        str).str.lower()
    if gdf_geojson.crs != "EPSG:4326":
        gdf_geojson = gdf_geojson.to_crs(epsg=4326)

    return gdf_geojson
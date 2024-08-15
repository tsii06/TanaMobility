import xml.etree.ElementTree as ET
import pandas as pd
from pyproj import Proj, Transformer
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# Fonction pour parser les polygones du fichier XML
def parse_polygons(file):
    tree = ET.parse(file)
    root = tree.getroot()

    # Extraire les paramètres de la balise <location>
    location = root.find('location')
    netOffset = tuple(map(float, location.get('netOffset').split(',')))
    convBoundary = tuple(map(float, location.get('convBoundary').split(',')))
    origBoundary = tuple(map(float, location.get('origBoundary').split(',')))
    projParameter = location.get('projParameter')

    polygons = []
    for poly in root.findall('poly'):
        poly_id = poly.get('id')
        shape = poly.get('shape')
        coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in shape.split()]

        # Extraire les paramètres du polygone
        params = {param.get('key'): param.get('value') for param in poly.findall('param')}
        params['id'] = poly_id
        params['coordinates'] = coordinates
        polygons.append(params)

    return pd.DataFrame(polygons), netOffset, convBoundary, origBoundary, projParameter


# Remplacez 'path_to_your_file.xml' par le chemin de votre fichier XML
df_polygons, netOffset, convBoundary, origBoundary, projParameter = parse_polygons('Sdt-MacroZone.taz.xml')

# Initialisation des projections
utm_proj = Proj(proj='utm', zone=38, ellps='WGS84', datum='WGS84', units='m', no_defs=True)
latlon_proj = Proj(proj='latlong', datum='WGS84')

# Initialisation du transformateur de projections
transformer = Transformer.from_proj(utm_proj, latlon_proj)


# Fonction de conversion des coordonnées avec offset
def convert_utm_to_geo(coords, offset):
    utm_coords_with_offset = [(x + offset[0], y + offset[1]) for x, y in coords]
    converted_coords = [transformer.transform(x, y) for x, y in utm_coords_with_offset]
    # Inverser les latitudes
    converted_coords = [(lon, -lat) for lon, lat in converted_coords]

    return converted_coords


# Conversion des coordonnées pour chaque polygone avec netOffset
df_polygons['geo_coordinates'] = df_polygons['coordinates'].apply(lambda coords: convert_utm_to_geo(coords, netOffset))

# Debug: Vérifier les premières lignes du DataFrame
print("Aperçu des polygones après conversion:")
# print(df_polygons.head())

# Création de l'application Dash
app = dash.Dash(__name__)

# Création des traces de polygones pour la carte
map_fig = go.Figure()



for index, row in df_polygons.iterrows():
    lons, lats = zip(*row['geo_coordinates'])
    print(lons, lats)
    map_fig.add_trace(go.Scattermapbox(
        lon=lons,
        lat=lats,
        mode='lines',
        fill='toself',
        name=row['id'],
        text=f"Commune: {row.get('COMMUNE', 'N/A')}, District: {row.get('DISTRICT', 'N/A')}, Region: {row.get('REGION', 'N/A')}",
        hoverinfo='text'
    ))

# Configuration de la mise en page de la carte
map_fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lon=47.5, lat=-18.9),
        zoom=10
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Disposition de l'application Dash
app.layout = html.Div([
    html.H1('Visualisation des Polygones de SUMO sur OpenStreetMap'),
    dcc.Graph(figure=map_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

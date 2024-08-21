from dash import html, dcc, Dash
import plotly.express as px
import json
import pandas as pd

# Fonction pour charger les données GeoJSON à partir d'un fichier
def charger_geojson(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        donnees_geojson = json.load(f)
    return donnees_geojson

# Fonction pour extraire les coordonnées des données GeoJSON et les transformer en DataFrame
def extraire_coordonnees_en_df(donnees_geojson):
    coordonnees = []
    for feature in donnees_geojson['features']:
        name = feature['properties'].get('name', 'Sans nom')
        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            for line in feature['geometry']['coordinates']:
                for lon, lat in line:
                    coordonnees.append({'lat': lat, 'lon': lon, 'name': name})
    return pd.DataFrame(coordonnees)

# Chemin vers le fichier GeoJSON
chemin_fichier_geojson = 'Antananarivo_voiries_primaires-secondaires-tertiaire.geojson'

# Charger les données GeoJSON
donnees_geojson = charger_geojson(chemin_fichier_geojson)

# Extraire les coordonnées et les transformer en DataFrame
df_coordonnees = extraire_coordonnees_en_df(donnees_geojson)
print(df_coordonnees.head())

# Créer la figure Plotly
fig = px.scatter_mapbox(
    df_coordonnees,
    lat='lat',
    lon='lon',
    hover_name='name',
    zoom=12,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox=dict(
        center=dict(lat=-19.0, lon=47.5),
        zoom=12
    )
)

# Créer l'application Dash
app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig)
])

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)

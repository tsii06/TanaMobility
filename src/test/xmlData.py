import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Charger le fichier GeoJSON
with open('sumo_network.geojson') as f:
    geojson_data = json.load(f)

# Extraire les coordonnées pour les tracés et les mettre dans un DataFrame
data = []
for feature in geojson_data['features']:
    coordinates = feature['geometry']['coordinates']
    for line in coordinates:
        for lon, lat in line:
            data.append({
                'lon': lon,
                'lat': lat,
                'id': feature['properties']['id']
            })

df = pd.DataFrame(data)

fig = px.scatter_mapbox(
    df,
    lat='lat',
    lon='lon',
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

# Création de l'application Dash pour afficher la figure
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)  # Spécifiez le port désiré ici



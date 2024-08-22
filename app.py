import json
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from src.callbacks.click_map_callback import register_click_map_callback
from src.callbacks.page_callback import page_callback
from src.components.header import header
from src.data.traitement import loadPopulationCarte, loadRepartitionZonale, loadRevenuCarte, get_congestion_point
from src.callbacks.map_callback import register_map_callbacks
from src.callbacks.stat_callback import register_callbacks
from src.figure.carte import extract_lat_lon, load_and_prepare_traffic_data

gdf_merged = loadPopulationCarte()
density = json.loads(gdf_merged.to_json())
gdf_geojson = loadRepartitionZonale()
df = loadRevenuCarte()
congestion = get_congestion_point()
lats, lons = extract_lat_lon()
df_filtre = load_and_prepare_traffic_data(
        geojson_path=r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson",
        traffic_data_function=get_congestion_point
    )

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'], suppress_callback_exceptions=True)
app.layout = html.Div([
    header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={"marginTop": "2px", "overflowY": "hidden"}), # Désactive le défilement vertical pour cet élément
    html.Div(id='dd')
])


# loadCallback
register_map_callbacks(app, gdf_merged,df, density,gdf_geojson,lats, lons,congestion,df_filtre)
register_callbacks(app)
page_callback(app)
register_click_map_callback(app)
# register_double_click(app)






server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)

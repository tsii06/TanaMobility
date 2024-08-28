import json
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from src.callbacks.accueil_click_map_callback import register_click_map_callback, plein_ecran_carte
from src.callbacks.detail_callback import detail_callback
from src.callbacks.accueil_graphique_update_callback import graphique_update_callback
from src.callbacks.accueil_legend_update_callback import register_legend_callback
from src.callbacks.page_content_update_callback import page_callback
from src.callbacks.scenario_callback import scenario_callback
from src.callbacks.type_visualisation_callback import selection_callback
from src.components.accueil.header import header

from src.callbacks.accueil_carte_update_callback import carte_update_callback
from src.callbacks.update_selected_thematique import register_callbacks
from src.data.traitement_data_spatiale import loadPopulationCarte, loadRepartitionZonale, loadRevenuCarte, \
    get_congestion_point
from src.data.utils import extract_lat_lon
from src.figure.carte import  load_and_prepare_traffic_data


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
carte_update_callback(app, gdf_merged,df, density,gdf_geojson,lats, lons,congestion,df_filtre)
graphique_update_callback(app)
register_callbacks(app)
page_callback(app)
register_click_map_callback(app,gdf_merged)
# register_double_click(app)
register_legend_callback(app)
plein_ecran_carte(app)
selection_callback(app)
detail_callback(app)
scenario_callback(app)

# print(find_zone_by_coordinates( -18.736279099999997,  47.4446467,gdf_merged))

server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)

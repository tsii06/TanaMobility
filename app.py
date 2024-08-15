import json
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from src.callbacks.page_callback import page_callback
from src.components.header import header
from src.data.traitement import loadPopulationCarte, loadRepartitionZonale, get_volume_deplacements, \
    get_nombre_vehicules_par_zone, get_pivoted_df, join_centroids_and_pivoted_data
from src.callbacks.map_callback import register_map_callbacks
from src.callbacks.stat_callback import register_callbacks

gdf_merged = loadPopulationCarte()
density = json.loads(gdf_merged.to_json())
gdf_geojson = loadRepartitionZonale()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'], suppress_callback_exceptions=True)
app.layout = html.Div([
    header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={"marginTop": "2px", "overflowY": "hidden"})  # Désactive le défilement vertical pour cet élément
])


# loadCallback
register_map_callbacks(app, gdf_merged, density,gdf_geojson)
register_callbacks(app)
page_callback(app)

regionale = r"data/Zonage_interne_externe_PMUD.geojson"
route = r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson"

# insert_zones(regionale)
# insert_random_population()
# insert_vehicules()
# insert_matriceOD()
# insert_activite()
# insert_zone_activite()
# insert_hierarchie_fonctionnelle()
# insert_typologie_modale()
# insert_routes_from_geojson_with_hierarchy(route)
# insert_menage()
# insert_revenu()
# insert_emploi()
# insert_flux_trafic()
# insert_iri()
# insert_debit_vitesse()
join_centroids_and_pivoted_data()
# get_nombre_vehicules_par_zone()
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)

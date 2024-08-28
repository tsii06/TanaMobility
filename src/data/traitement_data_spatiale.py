import pandas as pd
import geopandas as gpd

from src.data.database import get_session
from sqlalchemy import MetaData, Table, select, func  # Pour interagir avec la base de données

from src.data.utils import loadGeojson


def loadPopulationCarte():
    gdf_geojson = loadGeojson()
    session = get_session()
    metadata = MetaData()

    # Charger la vue population_view
    population_view = Table('population_view', metadata, autoload_with=session.bind)

    query = select(population_view)

    # Exécuter la requête et récupérer les résultats
    result = session.execute(query).fetchall()

    df_population = pd.DataFrame(result, columns=population_view.columns.keys())
    df_population['identifiant_commune'] = df_population['identifiant_commune'].astype(str).str.lower()
    gdf_merged = gdf_geojson.merge(df_population, how='inner', left_on='ensemble_concat',
                                   right_on='identifiant_commune')
    session.close()

    return gdf_merged


def loadRepartitionZonale():
    # Exemple de chemin d'accès au fichier GeoJSON (à adapter en figure de votre fichier réel)
    geojson_path = r"data/Zonage_interne_externe_PMUD.geojson"

    # Charger le GeoDataFrame à partir du fichier GeoJSON
    gdf_geojson = gpd.read_file(geojson_path)

    # Vérification des systèmes de coordonnées
    if gdf_geojson.crs != "EPSG:4326":
        gdf_geojson = gdf_geojson.to_crs(epsg=4326)

    # Ajouter une nouvelle colonne qui combine 'ensemble_1' et 'ensemble d'
    gdf_geojson = gdf_geojson.assign(combined=gdf_geojson['ensemble_1'] + " " + gdf_geojson['ensemble d'].astype(str))

    return gdf_geojson



def loadRevenuCarte():
    gdf_geojson = loadGeojson()

    metadata = MetaData()
    session = get_session()
    try:
        revenu_view = Table('revenu_view', metadata, autoload_with=session.bind)

        # Requête pour obtenir les données de la vue revenu_view
        query = select(
            revenu_view.c.revenu_median,
            revenu_view.c.taux_pauvrete,
            revenu_view.c.identifiant_commune
        )

        # Exécuter la requête et récupérer les résultats
        result = session.execute(query).fetchall()
        df_revenu = pd.DataFrame(result, columns=['revenu_median', 'taux_pauvrete', 'identifiant_commune'])

        df_revenu['identifiant_commune'] = df_revenu['identifiant_commune'].astype(str).str.lower()

        median_revenu = df_revenu['revenu_median'].median()
        median_pauvrete = df_revenu['taux_pauvrete'].median()

        df_revenu['revenu_median'] = df_revenu['revenu_median'].fillna(median_revenu)
        df_revenu['taux_pauvrete'] = df_revenu['taux_pauvrete'].fillna(median_pauvrete)

        gdf_merged = gdf_geojson.merge(df_revenu, how='left', left_on='ensemble_concat', right_on='identifiant_commune')

        # Si des zones du gdf_geojson n'ont pas de correspondance, remplir avec la médiane
        gdf_merged['revenu_median'] = gdf_merged['revenu_median'].fillna(median_revenu)
        gdf_merged['taux_pauvrete'] = gdf_merged['taux_pauvrete'].fillna(median_pauvrete)

        session.close()
        return gdf_merged

    except Exception as e:
        session.rollback()
        print(f"Erreur : {str(e)}")
        raise
    finally:
        session.close()





def get_congestion_point():
    metadata = MetaData()
    session = get_session()

    try:
        vue = Table('congestion', metadata, autoload_with=session.bind)
        query = select(vue)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        df['id_osm'] = df['id_osm'].astype('int32')
        gdf = gpd.read_file(r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson")
        gdf.loc[:, 'osm_id'] = gdf['osm_id'].astype('int32')
        gdf = gdf.to_crs(epsg=3857)
        gdf['centroid'] = gdf.centroid
        gdf_centroids = gdf[['osm_id', 'centroid']].copy()  # Créer une copie explicite
        gdf_centroids.loc[:, 'centroid'] = gdf_centroids['centroid'].to_crs(epsg=4326)
        df = df.merge(gdf_centroids, left_on='id_osm', right_on='osm_id', how='left')

        return df

    except Exception as e:
        print(f"Erreur lors de l'accès à la vue ou au GeoJSON : {e}")
        return None


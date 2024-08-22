import pandas as pd
import geopandas as gpd

from src.data.database import get_session
from sqlalchemy import MetaData, Table, select, func  # Pour interagir avec la base de données


# Chemins relatifs à la racine du projet

def loadGeojson():
    geojson_path = r"data/Zonage_interne_externe_PMUD.geojson"


    # Charger le GeoDataFrame à partir du fichier GeoJSON
    gdf_geojson = gpd.read_file(geojson_path)
    gdf_geojson['ensemble_concat'] = gdf_geojson['ensemble d'].astype(str) + '_' + gdf_geojson['ensemble_1'].astype(
        str).str.lower()

    if gdf_geojson.crs != "EPSG:4326":
        gdf_geojson = gdf_geojson.to_crs(epsg=4326)

    return gdf_geojson


def calculate_centroids_by_zone():
    gdf_geojson = loadGeojson()
    # Reprojeter dans un système de coordonnées projeté (par exemple, EPSG:3857 pour Web Mercator)
    gdf_projected = gdf_geojson.to_crs(epsg=3857)

    # Calculer les centroïdes dans le système de coordonnées projeté
    gdf_projected['centroid'] = gdf_projected.geometry.centroid

    # Reprojeter les centroïdes dans le système de coordonnées géographiques si nécessaire
    gdf_geojson['centroid'] = gdf_projected['centroid'].to_crs(epsg=4326)

    # Extraire les coordonnées des centroïdes dans des colonnes séparées
    gdf_geojson['centroid_x'] = gdf_geojson['centroid'].x
    gdf_geojson['centroid_y'] = gdf_geojson['centroid'].y

    # Optionnel: Vous pouvez retourner un DataFrame contenant uniquement les informations utiles
    df_centroids = gdf_geojson[['ensemble_concat', 'centroid_x', 'centroid_y']]
    # print(df_centroids)
    return df_centroids

def loadPopulationCarte():

    gdf_geojson = loadGeojson()
    session = get_session()
    metadata = MetaData()
    # Charger la vue population_view
    population_view = Table('population_view', metadata, autoload_with=session.bind)

    # Requête pour obtenir la population totale par zone à partir de la vue
    query = select(
        population_view.c.nom,
        population_view.c.population_totale,
        population_view.c.population_masculine_totale,
        population_view.c.population_feminine_totale,
        population_view.c.identifiant_commune
    )

    # Exécuter la requête et récupérer les résultats
    result = session.execute(query).fetchall()
    df_population = pd.DataFrame(result, columns=['nom', 'population_totale','population_masculine_totale','population_feminine_totale','identifiant_commune'])

    # Assurer que les colonnes sont de type chaîne de caractères pour la fusion
    df_population['identifiant_commune'] = df_population['identifiant_commune'].astype(str).str.lower()

    gdf_merged = gdf_geojson.merge(df_population, how='inner', left_on='ensemble_concat', right_on='identifiant_commune')
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
def load_data_population_bar_chart():
    metadata = MetaData()
    session = get_session()
    try:
        population_view = Table('population_par_tranche_age', metadata, autoload_with=session.bind)
        query = select(population_view.c.tranche,
                        population_view.c.population_masculine_totale,
                        population_view.c.population_feminine_totale)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(),
                          columns=['tranche', 'population_masculine_totale', 'population_feminine_totale'])
        return df

    finally:
        # Assurez-vous de fermer la session
        session.close()


def get_volume_deplacements(noms_zones=None):
    session = get_session()
    metadata = MetaData()

    try:
        # Charger la vue
        vue = Table('vue_productions_attractions', metadata, autoload_with=session.bind)

        # Si noms_zones est fourni et non vide, filtrer par les noms des zones
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.zone_nom).in_([nom.lower() for nom in noms_zones]))

        else:
            # Si noms_zones est None ou vide, sélectionner les 8 premières zones par volume total croissant
            query = select(vue).order_by(vue.c.total_volume.desc()).limit(8)

        # Exécuter la requête et transformer les résultats en DataFrame
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        # print(df)

        return df

    finally:
        # Fermer la session
        session.close()


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
        print('dklsd',gdf_merged.shape[0])
        return gdf_merged

    except Exception as e:
        session.rollback()
        print(f"Erreur : {str(e)}")
        raise
    finally:
        session.close()


def get_nombre_vehicules_par_zone(noms_zones=None):
    metadata = MetaData()
    session = get_session()

    try:
        # Charger la vue
        vue = Table('resultat_jointure', metadata, autoload_with=session.bind)

        # Construire la requête en fonction de noms_zones
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.zone_nom).in_([nom.lower() for nom in noms_zones]))
        else:
            # Si noms_zones est None ou vide, sélectionner les 8 premières zones par nombre total décroissant
            query = select(vue).order_by(vue.c.nombre_total.desc()).limit(8)

        # Exécuter la requête et transformer les résultats en DataFrame
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    finally:
        # Fermer la session
        session.close()

def get_pivoted_df():
    session = get_session()
    metadata = MetaData()

    try:
        # Charger la vue
        vue = Table('resultat_jointure', metadata, autoload_with=session.bind)

        query = select(vue)

        # Exécuter la requête et transformer les résultats en DataFrame
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Créer un DataFrame pivoté
        df_pivot = df.pivot_table(
            index='zone_nom',  # Utiliser le nom de la zone comme index
            columns='type_vehicule',  # Utiliser le type de véhicule comme colonnes
            values='nombre_total',  # Les valeurs à remplir sont le nombre total de véhicules
            fill_value=0  # Remplir les valeurs manquantes avec 0
        )

        # Ajouter une colonne pour le nombre total de véhicules par zone
        df_pivot['total_vehicules'] = df_pivot.sum(axis=1)

        return df_pivot

    finally:
        # Fermer la session
        session.close()
def join_centroids_and_pivoted_data():
    # Obtenir les données pivotées
    df_pivoted = get_pivoted_df()
    print(df_pivoted.shape[0])

    # Réinitialiser l'index pour convertir 'zone_nom' en une colonne
    df_pivoted = df_pivoted.reset_index()

    # Charger et calculer les centroïdes
    df_centroids = calculate_centroids_by_zone()
    print(df_centroids.shape[0])

    # Convertir les colonnes de jointure en minuscules et s'assurer qu'elles sont de type chaîne de caractères
    df_centroids['ensemble_concat'] = df_centroids['ensemble_concat'].astype(str).str.lower()
    df_pivoted['zone_nom'] = df_pivoted['zone_nom'].astype(str).str.lower()

    # Effectuer la jointure sur les colonnes ajustées
    df_merged = pd.merge(df_centroids, df_pivoted, left_on='ensemble_concat', right_on='zone_nom', how='inner')

    # Afficher le DataFrame résultant pour débogage
    # print(df_merged.shape[0])

    return df_merged

def get_matrice_od_data(noms_zones=None):
    metadata = MetaData()
    session = get_session()

    try:
        # Charger la vue
        vue = Table('vue_matrice', metadata, autoload_with=session.bind)

        # Construire la requête en fonction des noms_zones
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.nom_origine).in_([nom.lower() for nom in noms_zones]))
        else:
            # Sélectionner toutes les zones si noms_zones est None
            query = select(vue).order_by(vue.c.nombre.desc()).limit(10)

        # Exécuter la requête et transformer les résultats en DataFrame
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        # print(df)
        return df

    finally:
        # Fermer la session
        session.close()


def get_congestion_point():
    metadata = MetaData()
    session = get_session()

    try:
        # Charger la vue dans SQLAlchemy
        vue = Table('congestion', metadata, autoload_with=session.bind)

        # Créer une requête SELECT pour la vue
        query = select(vue)

        # Exécuter la requête et transformer les résultats en DataFrame
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Vérifier et convertir `id_osm` dans `df` en type entier (int64)
        df['id_osm'] = df['id_osm'].astype('int32')

        # Charger le GeoDataFrame avec les routes
        gdf = gpd.read_file(r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson")

        # Vérifier et convertir `osm_id` dans `gdf` en type entier (int64)
        gdf.loc[:, 'osm_id'] = gdf['osm_id'].astype('int32')

        # Reprojection en EPSG:3857 pour un calcul correct des centroides
        gdf = gdf.to_crs(epsg=3857)

        # Calculer les centroides des segments de routes
        gdf['centroid'] = gdf.centroid
        gdf_centroids = gdf[['osm_id', 'centroid']].copy()  # Créer une copie explicite

        # Reprojection en EPSG:4326 pour l'affichage correct
        gdf_centroids.loc[:, 'centroid'] = gdf_centroids['centroid'].to_crs(epsg=4326)

        # Jointure des centroides avec le DataFrame `congestion`
        df = df.merge(gdf_centroids, left_on='id_osm', right_on='osm_id', how='left')
        print(df.shape[0])

        return df

    except Exception as e:
        print(f"Erreur lors de l'accès à la vue ou au GeoJSON : {e}")
        return None
def get_zone_coordinate(zone):
    zone_coordinate = 0
    return zone_coordinate
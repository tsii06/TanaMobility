import pandas as pd

from src.data.database import get_session
from sqlalchemy import MetaData, Table, select, func

# Ce fonction permet d'avoir le nombre de population (par genre,par tranche d'age)
def get_population():
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
        session.close()


# Ce fonction permet d'avoir le volume de deplacement par zone(entrée et sortie)
def get_volume_deplacements(noms_zones=None):
    session = get_session()
    metadata = MetaData()

    try:
        vue = Table('vue_productions_attractions', metadata, autoload_with=session.bind)
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.zone_nom).in_([nom.lower() for nom in noms_zones]))

        else:
            query = select(vue).order_by(vue.c.total_volume.desc()).limit(8)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    finally:
        session.close()

# Ce fonction permet d'avoir le nombre de vehicule par type et  par zone
def get_nombre_vehicules_par_zone(noms_zones=None):
    metadata = MetaData()
    session = get_session()

    try:
        vue = Table('resultat_jointure', metadata, autoload_with=session.bind)
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.zone_nom).in_([nom.lower() for nom in noms_zones]))
        else:
            query = select(vue).order_by(vue.c.nombre_total.desc()).limit(8)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    finally:
        session.close()



def create_od_matrix(df_matrice):
    od_matrix = df_matrice.pivot_table(
        index='nom_origine',
        columns='nom_destination',
        values='nombre_deplacements',
        fill_value=0
    ).reset_index()
    return od_matrix

# fonction pour avoir le nombre de deplacement entre origine destination
def get_od_count(noms_zones=None):
    metadata = MetaData()
    session = get_session()
    try:
        vue = Table('vue_matrice_od', metadata, autoload_with=session.bind)
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.nom_origine).in_([nom.lower() for nom in noms_zones]))
        else:
            query = select(vue).order_by(vue.c.nombre_deplacements.desc()).limit(10)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    finally:
        session.close()

# fonction pour avoir le matrice le nombre par type de vehicule sur un origine destination
def get_vehicule_count_od(noms_zones=None):
    metadata = MetaData()
    session = get_session()

    try:
        vue = Table('vue_matrice_complete', metadata, autoload_with=session.bind)
        if noms_zones:
            query = select(vue).where(func.lower(vue.c.nom_origine).in_([nom.lower() for nom in noms_zones]))
        else:
            query = select(vue).order_by(vue.c.nombre_total_somme_vehicule.desc()).limit(11)
        result = session.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

    finally:
        session.close()


def pivot_vehicule_count_od(noms_zones=None):
    df = get_vehicule_count_od(noms_zones)
    if df.empty:
        return df
    df_pivot = df.pivot_table(
        index=['origine', 'destination'],
        columns='typevehicule',
        values='nombre',
        fill_value=0
    )
    df_pivot['nombre_total_somme_vehicule'] = df_pivot.sum(axis=1)
    df_pivot.sort_values(by='nombre_total_somme_vehicule', ascending=False, inplace=True)

    df_pivot.reset_index(inplace=True)

    return df_pivot





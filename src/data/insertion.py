from src.data.database import get_session
import json
import random
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import datetime

def insert_zones(geojson_path):
    session = get_session()

    try:
        # Charger le fichier GeoJSON
        with open(geojson_path, 'r') as f:
            geojson_dict = json.load(f)

        zones = []
        for feature in geojson_dict['features']:
            zone_name = feature['properties'].get('ensemble_1', 'Inconnu')
            ensemble_d = feature['properties'].get('ensemble d', '')
            identifiant_commune = f"{ensemble_d}_{zone_name}"
            zones.append({
                "nom": zone_name,
                "identifiant_commune": identifiant_commune
            })

        # Convertir en DataFrame pour l'insertion
        zones_df = pd.DataFrame(zones)

        # Assurez-vous que les colonnes sont du bon type
        zones_df['nom'] = zones_df['nom'].astype(str)
        zones_df['identifiant_commune'] = zones_df['identifiant_commune'].astype(str, errors='ignore')

        # Insérer les données dans la table ZONES
        zones_df.to_sql('zones', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(zones)} zones ont été insérées dans la table ZONES.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Une erreur est survenue lors de l'insertion dans la base de données : {str(e)}")
        raise
    except Exception as e:
        session.rollback()
        print(f"Une erreur inattendue est survenue : {str(e)}")
        raise
    finally:
        session.close()

def insert_random_population():
    session = get_session()
    try:
        # Créer un DataFrame pour les données de population
        population_data = []

        # Récupérer tous les IDZONE de la table zones
        result = session.execute(text("SELECT id FROM zones"))
        idzones = [row[0] for row in result]  # Accéder aux éléments du tuple par leur index

        # Récupérer toutes les tranches d'âge de la table tranche_age
        result = session.execute(text("SELECT id FROM tranche_age"))
        tranche_ages = [row[0] for row in result]  # Accéder aux éléments du tuple par leur index

        # Générer des données de population pour chaque zone et chaque tranche d'âge
        for idzone in idzones:
            for tranche_age_id in tranche_ages:
                feminine = random.randint(100, 1000)  # Générer un nombre aléatoire pour la population féminine
                masculine = random.randint(100, 1000)  # Générer un nombre aléatoire pour la population masculine
                population_data.append({
                    "id_zone": idzone,
                    "id_tranche_age": tranche_age_id,
                    "population_masculine": masculine,
                    "population_feminine": feminine,
                    "annee": datetime.datetime.now().year
                })

        # Convertir en DataFrame pour l'insertion
        population_df = pd.DataFrame(population_data)

        # Insérer les données dans la table POPULATION
        population_df.to_sql('population', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(population_data)} enregistrements de population ont été insérés dans la table POPULATION.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Une erreur est survenue lors de l'insertion dans la base de données : {str(e)}")
        raise
    except Exception as e:
        session.rollback()
        print(f"Une erreur inattendue est survenue : {str(e)}")
        raise
    finally:
        session.close()

# def insert_population(xlsx_path):
#     try:
#         # Lire le fichier Excel
#         population_df = pd.read_excel(xlsx_path)
#
#         # Vérifier et adapter les colonnes si nécessaire
#         population_df['idpopulation'] = population_df['idpopulation'].astype(str)
#         population_df['idzone'] = population_df['idzone'].astype(str)
#         population_df['feminine'] = population_df['feminine'].astype(int)
#         population_df['masculine'] = population_df['masculine'].astype(int)
#
#         # Insérer les données dans la table POPULATION
#         with get_engine().connect() as connection:
#             population_df.to_sql('population', connection, if_exists='append', index=False)
#
#         print(f"{len(population_df)} enregistrements ont été insérés dans la table POPULATION.")
#
#     except SQLAlchemyError as e:
#         print(f"Une erreur est survenue lors de l'insertion dans la base de données : {str(e)}")
#     except Exception as e:
#         print(f"Une erreur inattendue est survenue : {str(e)}")

def insert_matriceOD():
    session = get_session()  # Fonction qui doit retourner une session SQLAlchemy
    try:
        # Récupérer tous les ID de zones et types de véhicules
        idzones = [row[0] for row in session.execute(text("SELECT id FROM zones"))]
        idvehicules = [row[0] for row in session.execute(text("SELECT id FROM types_vehicules"))]

        matrice_od_data = []

        for _ in range(20):  # Insérer 20 enregistrements fictifs
            id_origine = random.choice(idzones)
            id_destination = random.choice(idzones)
            while id_origine == id_destination:  # Assurez-vous que l'origine et la destination ne sont pas identiques
                id_destination = random.choice(idzones)

            id_type_vehicule = random.choice(idvehicules)
            nombre = random.randint(1, 100)  # Générer un nombre aléatoire de déplacements

            matrice_od_data.append({
                "id_origine": id_origine,
                "id_destination": id_destination,
                "id_type_vehicule": id_type_vehicule,
                "nombre": nombre
            })

        # Convertir en DataFrame pour l'insertion
        matrice_od_df = pd.DataFrame(matrice_od_data)

        # Insérer les données dans la table matrice_od
        matrice_od_df.to_sql('matrice_od', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(matrice_od_data)} enregistrements ont été insérés dans la table matrice_od.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Une erreur est survenue lors de l'insertion dans la base de données : {str(e)}")
        raise
    except Exception as e:
        session.rollback()
        print(f"Une erreur inattendue est survenue : {str(e)}")
        raise
    finally:
        session.close()

def insert_vehicules():
    session = get_session()
    try:
        # Liste des types de véhicules à insérer
        vehicules = [
            {"id": 1, "nom_type": "Voiture"},
            {"id": 2, "nom_type": "Moto"},
            {"id": 3, "nom_type": "Bus"},
        ]

        # Convertir en DataFrame pour l'insertion
        vehicules_df = pd.DataFrame(vehicules)

        # Insérer les données dans la table TYPEVEHICULE
        vehicules_df.to_sql('types_vehicules', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(vehicules)} types de véhicules ont été insérés dans la table TYPEVEHICULE.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Une erreur est survenue lors de l'insertion dans la base de données : {str(e)}")
        raise
    except Exception as e:
        session.rollback()
        print(f"Une erreur inattendue est survenue : {str(e)}")
        raise
    finally:
        session.close()

def insert_activite():
    session = get_session()
    try:
        activites = ["Commerciale", "Industrielle", "Résidentielle", "Agricole", "Touristique"]
        activite_data = [{"nom_activite": act} for act in activites]

        activite_df = pd.DataFrame(activite_data)

        # Insérer les données dans la table 'activite'
        activite_df.to_sql('activite', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(activite_data)} activités ont été insérées dans la table activite.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table activite : {str(e)}")
        raise
    finally:
        session.close()

def insert_zone_activite():
    session = get_session()
    try:
        # Récupérer tous les ID de zones et d'activités
        idzones = [row[0] for row in session.execute(text("SELECT id FROM zones"))]
        idactivites = [row[0] for row in session.execute(text("SELECT id FROM activite"))]

        zone_activite_data = []

        for _ in range(20):
            id_zone = random.choice(idzones)
            id_activite = random.choice(idactivites)
            pourcentage = round(random.uniform(10, 100), 2)  # Générer un pourcentage aléatoire entre 10 et 100

            zone_activite_data.append({
                "id_zone": id_zone,
                "id_activite": id_activite,
                "pourcentage": pourcentage
            })

        zone_activite_df = pd.DataFrame(zone_activite_data)

        # Insérer les données dans la table 'zone_activite'
        zone_activite_df.to_sql('zone_activite', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(zone_activite_data)} enregistrements ont été insérés dans la table zone_activite.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table zone_activite : {str(e)}")
        raise
    finally:
        session.close()

def insert_menage():
    session = get_session()
    try:
        annee_courante = datetime.datetime.now().year

        # Récupérer tous les ID des zones et typologies modales
        idzones = [row[0] for row in session.execute(text("SELECT id FROM zones"))]
        id_typologies_modales = [row[0] for row in session.execute(text("SELECT id FROM typologie_modale"))]

        menage_data = []

        for _ in range(20):
            id_zone = random.choice(idzones)
            annee = random.choice(range(annee_courante - 5, annee_courante + 1))  # Années de données
            id_typologie_modale = random.choice(id_typologies_modales)  # Sélectionner aléatoirement une typologie modale
            total_menages = random.randint(50, 5000)  # Nombre aléatoire de ménages
            taille_moyenne_menage = round(random.uniform(2.5, 6.0), 2)  # Taille moyenne des ménages
            vehicules_par_menage = round(random.uniform(0.5, 3.0), 2)  # Nombre moyen de véhicules par ménage

            menage_data.append({
                "id_zone": id_zone,
                "annee": annee,
                "id_typologie_modale": id_typologie_modale,
                "total_menages": total_menages,
                "taille_moyenne_menage": taille_moyenne_menage,
                "vehicules_par_menage": vehicules_par_menage
            })

        menage_df = pd.DataFrame(menage_data)

        # Insérer les données dans la table 'menage'
        menage_df.to_sql('menage', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(menage_data)} enregistrements ont été insérés dans la table menage.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table menage : {str(e)}")
        raise
    finally:
        session.close()

def insert_revenu():
    session = get_session()
    try:
        annee_courante = datetime.datetime.now().year
        idzones = [row[0] for row in session.execute(text("SELECT id FROM zones"))]

        revenu_data = []

        for _ in range(20):
            id_zone = random.choice(idzones)
            annee = random.choice(range(annee_courante - 5, annee_courante + 1))  # Années de données
            revenu_moyen = round(random.uniform(15000, 80000), 2)  # Revenu moyen aléatoire
            revenu_median = round(random.uniform(10000, 70000), 2)  # Revenu médian aléatoire
            taux_pauvrete = round(random.uniform(5.0, 40.0), 2)  # Taux de pauvreté aléatoire

            revenu_data.append({
                "id_zone": id_zone,
                "annee": annee,
                "revenu_moyen": revenu_moyen,
                "revenu_median": revenu_median,
                "taux_pauvrete": taux_pauvrete
            })

        revenu_df = pd.DataFrame(revenu_data)

        # Insérer les données dans la table 'revenu'
        revenu_df.to_sql('revenu', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(revenu_data)} enregistrements ont été insérés dans la table revenu.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table revenu : {str(e)}")
        raise
    finally:
        session.close()

def insert_emploi():
    session = get_session()
    try:
        annee_courante = datetime.datetime.now().year
        idzones = [row[0] for row in session.execute(text("SELECT id FROM zones"))]

        emploi_data = []

        for _ in range(20):
            id_zone = random.choice(idzones)
            annee = random.choice(range(annee_courante - 5, annee_courante + 1))  # Années de données
            taux_chomage = round(random.uniform(5.0, 25.0), 2)  # Taux de chômage aléatoire
            taux_participation = round(random.uniform(50.0, 75.0), 2)  # Taux de participation aléatoire

            emploi_data.append({
                "id_zone": id_zone,
                "annee": annee,
                "taux_chomage": taux_chomage,
                "taux_participation": taux_participation,
            })

        emploi_df = pd.DataFrame(emploi_data)

        # Insérer les données dans la table 'emploi'
        emploi_df.to_sql('emploi', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(emploi_data)} enregistrements ont été insérés dans la table emploi.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table emploi : {str(e)}")
        raise
    finally:
        session.close()

def insert_hierarchie_fonctionnelle():
    session = get_session()
    try:
        niveaux = ["primary", "secondary", "tertiary"]
        hierarchie_data = [{"nom_niveau": niveau} for niveau in niveaux]

        hierarchie_df = pd.DataFrame(hierarchie_data)

        # Insérer les données dans la table 'hierarchie_fonctionnelle'
        hierarchie_df.to_sql('hierarchie_fonctionnelle', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(hierarchie_data)} enregistrements ont été insérés dans la table hierarchie_fonctionnelle.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table hierarchie_fonctionnelle : {str(e)}")
        raise
    finally:
        session.close()

def insert_routes_from_geojson_with_hierarchy(geojson_path):
    session = get_session()
    try:
        # Charger le fichier GeoJSON
        with open(geojson_path, 'r') as f:
            geojson_dict = json.load(f)

        # Exécuter la requête pour obtenir le mapping de la hiérarchie fonctionnelle
        result = session.execute(text("SELECT id, nom_niveau FROM hierarchie_fonctionnelle"))

        # Créer un dictionnaire de mapping entre 'nom_niveau' et 'id'
        hierarchie_mapping = {row[1]: row[0] for row in result}  # row[1] est 'nom_niveau', row[0] est 'id'

        route_data = []

        # Parcourir les features du GeoJSON pour extraire les informations nécessaires
        for feature in geojson_dict['features']:
            id_OSM = feature['properties'].get('osm_id')
            nom_niveau = feature['properties'].get('highway')
            id_hierarchie = hierarchie_mapping.get(nom_niveau)

            # Ajouter les données à la liste si les conditions sont remplies
            if id_OSM is not None and id_hierarchie is not None:
                route_data.append({
                    "id_hierarchie": id_hierarchie,
                    "id_osm": id_OSM
                })

        # Convertir la liste en DataFrame pour l'insertion dans la base de données
        route_df = pd.DataFrame(route_data)

        # Insérer les données dans la table 'route'
        route_df.to_sql('route', session.bind, if_exists='append', index=False)

        # Valider les changements
        session.commit()
        print(f"{len(route_data)} enregistrements ont été insérés dans la table route.")

    except SQLAlchemyError as e:
        # Rollback en cas d'erreur SQL
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table route : {str(e)}")
        raise

    except Exception as e:
        # Rollback en cas d'erreur générale
        session.rollback()
        print(f"Erreur inattendue : {str(e)}")
        raise

    finally:
        # Fermer la session
        session.close()

def insert_flux_trafic():
    session = get_session()
    try:
        idroute = [row[0] for row in session.execute(text("SELECT id FROM route"))]
        idmodes = [row[0] for row in session.execute(text("SELECT id FROM typologie_modale"))]
        idperiodes = [row[0] for row in session.execute(text("SELECT id FROM periodes_temps"))]

        flux_data = []

        for _ in range(20):
            id_origine = random.choice(idroute)
            id_destination = random.choice(idroute)
            while id_origine == id_destination:
                id_destination = random.choice(idroute)
            id_mode = random.choice(idmodes)
            id_periode_temps = random.choice(idperiodes)
            volume = random.randint(50, 1000)
            date = datetime.datetime.now().date()
            vitesse_moyenne = round(random.uniform(30.0, 120.0), 2)
            temps_de_trajet = round(random.uniform(5.0, 60.0), 2)
            distance = round(random.uniform(1.0, 100.0), 2)

            flux_data.append({
                "id_departed": id_origine,
                "id_arrived": id_destination,
                "id_typologie_modale": id_mode,
                "id_periode_temps": id_periode_temps,
                "volume": volume,
                "date": date,
                "vitesse_moyenne": vitesse_moyenne,
                "temps_de_trajet": temps_de_trajet,
                "distance": distance
            })

        flux_df = pd.DataFrame(flux_data)

        # Insérer les données dans la table 'flux_trafic'
        flux_df.to_sql('flux_trafic', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(flux_data)} enregistrements ont été insérés dans la table flux_trafic.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table flux_trafic : {str(e)}")
        raise
    finally:
        session.close()

def insert_debit_vitesse():
    session = get_session()
    try:
        idroutes = [row[0] for row in session.execute(text("SELECT id FROM route"))]
        debit_vitesse_data = []

        for _ in range(20):
            id_route = random.choice(idroutes)
            vitesse_moyenne = round(random.uniform(30.0, 120.0), 2)
            vitesse_maximale = round(random.uniform(80.0, 130.0), 2)
            vitesse_minimale = round(random.uniform(10.0, 50.0), 2)
            debit_trafic = round(random.uniform(100.0, 10000.0), 2)
            date_observation = datetime.datetime.now()

            debit_vitesse_data.append({
                "id_route": id_route,
                "vitesse_moyenne": vitesse_moyenne,
                "vitesse_maximale": vitesse_maximale,
                "vitesse_minimale": vitesse_minimale,
                "debit_trafic": debit_trafic,
                "date_observation": date_observation
            })

        debit_vitesse_df = pd.DataFrame(debit_vitesse_data)

        # Insérer les données dans la table 'debit_vitesse'
        debit_vitesse_df.to_sql('debit_vitesse', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(debit_vitesse_data)} enregistrements ont été insérés dans la table debit_vitesse.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table debit_vitesse : {str(e)}")
        raise
    finally:
        session.close()

def insert_iri():
    session = get_session()
    try:
        idroutes = [row[0] for row in session.execute(text("SELECT id FROM route"))]

        iri_data = []

        for _ in range(20):
            id_route = random.choice(idroutes)
            valeur_iri = round(random.uniform(1.0, 10.0), 2)  # IRI values usually range from 1 to 10 m/km
            date_observation = datetime.datetime.now()

            iri_data.append({
                "id_route": id_route,
                "valeur_iri": valeur_iri,
                "date_observation": date_observation
            })

        iri_df = pd.DataFrame(iri_data)

        # Insérer les données dans la table 'iri'
        iri_df.to_sql('iri', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(iri_data)} enregistrements ont été insérés dans la table iri.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table iri : {str(e)}")
        raise
    finally:
        session.close()

def insert_typologie_modale():
    session = get_session()
    try:
        modes_transport = [
            {"nom_mode": "Bus", "description": "Transport en commun par bus", "vitesse_moyenne": 40.0, "capacite": 50},
            {"nom_mode": "Vélo", "description": "Transport individuel par vélo", "vitesse_moyenne": 15.0, "capacite": 1},
            {"nom_mode": "Voiture", "description": "Transport individuel ou partagé par voiture", "vitesse_moyenne": 60.0, "capacite": 5},
            {"nom_mode": "Tramway", "description": "Transport en commun par tramway", "vitesse_moyenne": 25.0, "capacite": 200},
            {"nom_mode": "Train", "description": "Transport longue distance par train", "vitesse_moyenne": 100.0, "capacite": 500},
            {"nom_mode": "Marche", "description": "Déplacement à pied", "vitesse_moyenne": 5.0, "capacite": 1}
        ]

        typologie_modale_df = pd.DataFrame(modes_transport)

        # Insérer les données dans la table 'typologie_modale'
        typologie_modale_df.to_sql('typologie_modale', session.bind, if_exists='append', index=False)

        session.commit()
        print(f"{len(modes_transport)} enregistrements ont été insérés dans la table typologie_modale.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion dans la table typologie_modale : {str(e)}")
        raise
    finally:
        session.close()
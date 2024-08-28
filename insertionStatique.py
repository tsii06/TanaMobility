from src.data.insertion import *
regionale = r"data/Zonage_interne_externe_PMUD.geojson"
route = r"data/Antananarivo_voiries_primaires-secondaires-tertiaire.geojson"
insert_zones(regionale)
insert_random_population()
insert_vehicules()
insert_matriceOD()
insert_activite()
insert_zone_activite()
insert_hierarchie_fonctionnelle()
insert_typologie_modale()
insert_routes_from_geojson_with_hierarchy(route)
insert_menage()
insert_revenu()
insert_emploi()
insert_flux_trafic()
insert_iri()
insert_debit_vitesse()
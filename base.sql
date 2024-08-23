CREATE database mobilite;
/c mobilite;

CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,  -- Nom de la zone géographique
    id_OSM VARCHAR(50),
    identifiant_commune VARCHAR(50) NOT NULL
);

CREATE TABLE periodes_temps (
    id SERIAL PRIMARY KEY,
    nom_periode VARCHAR(255) NOT NULL  -- Nom de la période (ex : "Matin", "Soir")
);

insert into periodes_temps values(default,'matin'),(default,'soir');

CREATE TABLE types_vehicules (
    id SERIAL PRIMARY KEY,
    nom_type VARCHAR(255) NOT NULL  -- Nom du type de véhicule (ex : "Voiture", "Bus")
);



CREATE TABLE typologie_modale (
    id SERIAL PRIMARY KEY,
    nom_mode VARCHAR(255) NOT NULL,  -- Nom du mode de transport (ex : "Bus", "Vélo")
    description TEXT,  -- Description du mode de transport
    vitesse_moyenne DECIMAL(5, 2) NOT NULL,  -- Vitesse moyenne en km/h
    capacite INTEGER NOT NULL -- Capacité moyenne (ex : nombre de passagers pour un bus)
);

CREATE TABLE tranche_age (
    id SERIAL PRIMARY KEY,  
    tranche VARCHAR(50) NOT NULL,  -- Description de la tranche d'âge (ex: "0-5 ans")
    age_min INTEGER NOT NULL,  -- Âge minimum de la tranche d'âge
    age_max INTEGER NOT NULL   -- Âge maximum de la tranche d'âge
);
INSERT INTO tranche_age (tranche, age_min, age_max)
VALUES 
('0-14 ans', 0, 14),  -- Enfants et adolescents
('15-24 ans', 15, 24),  -- Jeunes (adolescents et jeunes adultes)
('25-64 ans', 25, 64),  -- Population active (adulte)
('65 ans et plus', 65, 150);  

CREATE TABLE population (
    id SERIAL PRIMARY KEY,
    id_zone INTEGER REFERENCES zones(id),  -- Référence à la zone géographique
    id_tranche_age INTEGER NOT NULL REFERENCES tranche_age(id),  -- Référence à la tranche d'âge
    annee INTEGER NOT NULL,  -- Année de la donnée de population
    population_masculine INTEGER NOT NULL,  -- Nombre d'hommes dans la zone
    population_feminine INTEGER NOT NULL,  -- Nombre de femmes dans la zone
    UNIQUE(annee)
);



CREATE TABLE activite (
    id SERIAL PRIMARY KEY,
    nom_activite VARCHAR(255) NOT NULL  -- Nom de l'activité (ex : "Commerciale", "Industrielle")
);

CREATE TABLE zone_activite (
    id SERIAL PRIMARY KEY,
    id_zone INTEGER REFERENCES zones(id),  -- Référence à la zone géographique
    id_activite INTEGER REFERENCES activite(id),  -- Référence à l'activité
    pourcentage DECIMAL(5, 2) NOT NULL CHECK (pourcentage >= 0 AND pourcentage <= 100)  -- Importance de l'activité dans la zone en pourcentage
);

CREATE TABLE menage (
    id SERIAL PRIMARY KEY,
    id_zone INTEGER REFERENCES zones(id),  -- Référence à la zone géographique
    annee INTEGER NOT NULL,  -- Année de la donnée statistique
    id_typologie_modale INTEGER REFERENCES typologie_modale(id), -- Référence à la typologie modale
    total_menages INTEGER NOT NULL,  -- Nombre total de ménages dans la zone
    taille_moyenne_menage DECIMAL(4, 2) NOT NULL,  -- Taille moyenne des ménages (nombre moyen de personnes par ménage)
    vehicules_par_menage DECIMAL(4, 2) NOT NULL -- Nombre moyen de véhicules par ménage
);


CREATE TABLE revenu (
    id SERIAL PRIMARY KEY,
    id_zone INTEGER REFERENCES zones(id),  -- Référence à la zone géographique
    annee INTEGER NOT NULL,  -- Année de la donnée statistique
    revenu_moyen DECIMAL(10, 2) NOT NULL,  -- Revenu moyen des ménages dans la zone
    revenu_median DECIMAL(10, 2) NOT NULL,  -- Revenu médian des ménages dans la zone
    taux_pauvrete DECIMAL(5, 2) NOT NULL  -- Taux de pauvreté (pourcentage de ménages sous le seuil de pauvreté)
);

CREATE TABLE emploi (
    id SERIAL PRIMARY KEY,
    id_zone INTEGER REFERENCES zones(id),  -- Référence à la zone géographique
    annee INTEGER NOT NULL,  -- Année de la donnée statistique
    taux_chomage DECIMAL(5, 2) NOT NULL,  -- Taux de chômage dans la zone
    taux_participation DECIMAL(5, 2) NOT NULL  -- Taux de participation à la force de travail
);

CREATE TABLE matrice_od (
    id SERIAL PRIMARY KEY,
    id_origine INTEGER REFERENCES zones(id),  -- Référence à la zone d'origine
    id_destination INTEGER REFERENCES zones(id),  -- Référence à la zone de destination
    id_type_vehicule INTEGER REFERENCES types_vehicules(id),  -- Référence au type de véhicule
    nombre INTEGER NOT NULL  -- Nombre de déplacements pour cette combinaison
);

CREATE TABLE hierarchie_fonctionnelle (
    id SERIAL PRIMARY KEY,
    nom_niveau VARCHAR(255) NOT NULL  -- Nom de la hiérarchie (ex : "Autoroute", "Route Principale", "Route Secondaire")
);

CREATE TABLE route(
   id SERIAL PRIMARY KEY,
   id_hierarchie INTEGER REFERENCES hierarchie_fonctionnelle(id),
   id_OSM VARCHAR(50)
);

CREATE TABLE flux_trafic (
    id SERIAL PRIMARY KEY,
    id_departed INTEGER REFERENCES route(id),  -- Référence à la zone d'origine
    id_arrived INTEGER REFERENCES route(id),  -- Référence à la zone de destination
    id_typologie_modale INTEGER REFERENCES typologie_modale(id),  -- Référence au mode de transport
    id_periode_temps INTEGER REFERENCES periodes_temps(id),  -- Référence à la période de temps (ex : "Matin", "Soir")
    volume INTEGER NOT NULL,  -- Volume de trafic (nombre de véhicules ou de piétons)
    date DATE NOT NULL,  -- Date de l'enregistrement
    vitesse_moyenne DECIMAL(5, 2),  -- Vitesse moyenne du flux de trafic (en km/h)
    temps_de_trajet DECIMAL(5, 2),  -- Temps de trajet moyen (en minutes)
    distance DECIMAL(10, 2)  -- Distance entre les zones (en kilomètres)
);

CREATE TABLE debit_vitesse (
    id SERIAL PRIMARY KEY,
    id_route INTEGER REFERENCES route(id),  -- Référence à la zone géographique
    vitesse_moyenne DECIMAL(5, 2) NOT NULL,  -- Vitesse moyenne observée (en km/h)
    vitesse_maximale DECIMAL(5, 2) NOT NULL,  -- Vitesse maximale autorisée (en km/h)
    vitesse_minimale DECIMAL(5, 2) NOT NULL,  -- Vitesse minimale observée (en km/h)
    debit_trafic DECIMAL(10, 2) NOT NULL,  -- Débit de trafic (nombre de véhicules/heure)
    date_observation TIMESTAMP NOT NULL  -- Date et heure de l'observation
);

CREATE TABLE iri (
    id SERIAL PRIMARY KEY,
    id_route INTEGER REFERENCES route(id),  -- Référence à la zone géographique
    valeur_iri DECIMAL(6, 2) NOT NULL,  -- Valeur de l'IRI (Indice de Rugosité Internationale) en m/km
    date_observation TIMESTAMP NOT NULL  -- Date et heure de l'observation
);


-- view --
CREATE OR REPLACE VIEW population_view AS 
   SELECT 
       p.id_zone,
       z.nom AS nom,
       z.identifiant_commune,
       SUM(p.population_masculine) AS population_masculine_totale,
       SUM(p.population_feminine) AS population_feminine_totale,
       SUM(p.population_masculine + p.population_feminine) AS population_totale
   FROM 
       population p
   JOIN 
       zones z ON p.id_zone = z.id
   GROUP BY 
       p.id_zone, z.nom,z.identifiant_commune;

CREATE VIEW revenu_view AS
   SELECT
       r.id AS revenu_id,
       r.annee,
       r.revenu_moyen,
       r.revenu_median,
       r.taux_pauvrete,
       z.nom AS zone_nom,
       z.identifiant_commune
   FROM
       revenu r
   JOIN
       zones z ON r.id_zone = z.id;




CREATE VIEW population_par_tranche_age AS
   SELECT 
       ta.tranche, 
       SUM(p.population_masculine) AS population_masculine_totale, 
       SUM(p.population_feminine) AS population_feminine_totale
   FROM 
       population p
   JOIN 
       tranche_age ta ON p.id_tranche_age = ta.id
   GROUP BY 
       ta.tranche
   ORDER BY 
       ta.age_min;


CREATE VIEW vue_productions_attractions AS
   SELECT 
       z.id AS zone_id,
       z.identifiant_commune AS zone_nom,
       COALESCE(SUM(CASE WHEN m.id_origine = z.id THEN m.nombre ELSE 0 END), 0) AS total_productions,
       COALESCE(SUM(CASE WHEN m.id_destination = z.id THEN m.nombre ELSE 0 END), 0) AS total_attractions,
       COALESCE(SUM(CASE WHEN m.id_origine = z.id THEN m.nombre ELSE 0 END), 0) +
       COALESCE(SUM(CASE WHEN m.id_destination = z.id THEN m.nombre ELSE 0 END), 0) AS total_volume
   FROM 
       zones z
   LEFT JOIN 
       matrice_od m ON z.id = m.id_origine OR z.id = m.id_destination
   GROUP BY 
       z.id, z.identifiant_commune;



CREATE VIEW vue_nombre_vehicules_par_zone AS
SELECT 
    z.id AS zone_id,
    z.identifiant_commune AS zone_nom,
    tv.id AS type_vehicule_id,
    tv.nom_type AS type_vehicule,
    SUM(mo.nombre) AS nombre_total
FROM 
    zones z
LEFT JOIN 
    matrice_od mo ON z.id = mo.id_origine OR z.id = mo.id_destination
LEFT JOIN 
    types_vehicules tv ON mo.id_type_vehicule = tv.id
GROUP BY 
    z.id, z.identifiant_commune, tv.id, tv.nom_type;

CREATE TABLE zone_vehicules (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES zones(id),  -- Référence à l'ID de la zone
    type_vehicule_id INTEGER REFERENCES types_vehicules(id)  -- Référence à l'ID du type de véhicule
);

-- Insérer les combinaisons de chaque zone avec chaque type de véhicule
INSERT INTO zone_vehicules (zone_id, type_vehicule_id)
SELECT z.id AS zone_id, tv.id AS type_vehicule_id
FROM zones z
CROSS JOIN types_vehicules tv;


-- Création de la table résultante si nécessaire
CREATE or REPLACE view resultat_jointure AS
SELECT
    zv.zone_id,
    z.identifiant_commune AS zone_nom,
    zv.type_vehicule_id,
    tv.nom_type AS type_vehicule,
    COALESCE(SUM(mo.nombre), 0) AS nombre_total
FROM
    zone_vehicules zv
LEFT JOIN
    zones z ON zv.zone_id = z.id
LEFT JOIN
    types_vehicules tv ON zv.type_vehicule_id = tv.id
LEFT JOIN
    matrice_od mo ON zv.zone_id = mo.id_origine AND zv.type_vehicule_id = mo.id_type_vehicule
GROUP BY
    zv.zone_id,
    z.identifiant_commune,
    zv.type_vehicule_id,
    tv.nom_type
ORDER BY
    zv.zone_id;  -- Tri par nom de la zone

CREATE VIEW vue_matrice AS
SELECT
    mo.id,
    mo.id_origine,
    zo.identifiant_commune AS nom_origine,
    mo.id_destination,
    zd.identifiant_commune AS nom_destination,
    mo.id_type_vehicule,
    mo.nombre
FROM
    matrice_od mo
JOIN
    zones zo ON mo.id_origine = zo.id
JOIN
    zones zd ON mo.id_destination = zd.id;



CREATE VIEW vue_matrice_od AS
SELECT 
    nom_origine,
    nom_destination,
    sum(nombre) AS nombre_deplacements,
    (SELECT SUM(nombre) 
     FROM vue_matrice
     WHERE vue_matrice.nom_origine = v.nom_origine) AS somme_totale_par_origine
FROM 
    vue_matrice v
GROUP BY 
    nom_origine, nom_destination;


CREATE VIEW congestion AS
WITH total_volume AS (
    SELECT
        id_departed AS route_id,
        SUM(volume) AS total_volume
    FROM
        flux_trafic
    GROUP BY
        id_departed
    
    UNION ALL
    
    SELECT
        id_arrived AS route_id,
        SUM(volume) AS total_volume
    FROM
        flux_trafic
    GROUP BY
        id_arrived
)
SELECT
    tv.route_id,
    r.id_osm,
    SUM(tv.total_volume) AS total_traffic_volume
FROM
    total_volume tv
JOIN
    route r ON tv.route_id = r.id
GROUP BY
    tv.route_id, r.id_osm
ORDER BY
    total_traffic_volume DESC;

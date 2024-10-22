# TanaMobility

Visualisation et Modélisation des Flux de Transport à Antananarivo.

## Description

TanaMobility est une plateforme interactive, développée en utilisant Dash et Python, dédiée à la modélisation et à la visualisation des flux de transport à Antananarivo, Madagascar. En s'appuyant sur des données géospatiales et des outils avancés de visualisation, TanaMobility offre une compréhension approfondie des mouvements de population, des dynamiques de trafic, et des infrastructures de transport.

![Capture d'ecran du site](assets/image/ecran.png)


## Structure du Projet

- **.prompts/** : Contient des fichiers ou des données associées aux prompts utilisés dans le projet.
  
- **assets/** : Contient les ressources statiques utilisées par l'application.
  - **image/** : Dossier pour les images utilisées dans l'application.
  - **style.css** : Feuille de style CSS pour le design de l'application.

- **data/** : Contient les jeux de données utilisés pour l'analyse et la modélisation.
  - **Antananarivo_voieries_primaires-secondaires-tutr...** : Fichier géospatial contenant les données sur les voies de circulation.
  - **Zonage_interne_externe_PMUD.geojson** : Fichier GeoJSON avec les zones internes et externes pour le PMUD.

- **environement/** : Fichiers de configuration pour l'environnement Python.
  - **requirements.txt** : Liste des dépendances Python nécessaires au projet.

- **src/** : Contient le code source de l'application.
  - **callbacks/** : Scripts pour les callbacks utilisés dans l'application Dash.
  - **components/** : Composants réutilisables pour la construction de l'interface utilisateur.
  - **data/** : Scripts de traitement des données.
  - **figure/** : Scripts pour la création de graphiques et visualisations.
  - **pages/** : Différentes pages de l'application.
  - **test/** : Scripts de test pour vérifier la fonctionnalité du code.

- **app.py** : Point d'entrée principal de l'application Flask/Dash.
- **wsgi.py** : Script pour déployer l'application avec un serveur WSGI.

## Prérequis

- Python 3.x
- pip
- Dash
- Gunicorn
- PostgreSQL

## Modules Utilisés

- **Dash** : Framework pour créer des interfaces utilisateur analytiques.
- **Pandas** : Manipulation et analyse des données.
- **Plotly** : Visualisation interactive des données.
- **Gunicorn** : Serveur WSGI pour déployer l'application.
- **Psycopg2** : Adaptateur PostgreSQL pour Python, utilisé pour interagir avec la base de données PostgreSQL.
- **GeoPandas** : Extension de Pandas pour la manipulation de données géospatiales.

## Configuration de la Base de Données

Ce projet utilise une base de données PostgreSQL pour stocker et gérer les données de trafic et de mobilité. Suivez les étapes ci-dessous pour configurer la base de données :
- Copier le script dans le fichier sql: **base.sql** et executez pour la creation du base de donnée, des tables et des views.
- Configurer les paramètres de connexion dans le fichier **data/database.py** en changeant le mot de passe et le nom d'utilisateur


## Installation

Clonez ce repository et installez les dépendances nécessaires :

```bash
git clone https://github.com/tsii06/TanaMobility.git
cd TanaMobility
pip install -r environement/requirements.txt
```

## Utilisation
-Executer le fichier **insertionStatique.py** dans le racine du projet pour faire de inserer des données statiques dans le base de donnée. Assurez-vous que les paramètres de connexion est bien configuré

-Pour lancer l'application en local :
```bash
python app.py
```
-Pour déployer l'application sur un serveur WSGI :
```bash
python wsgi.py
```

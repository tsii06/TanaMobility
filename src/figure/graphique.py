import numpy as np
from dash import dcc, html, dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from src.data.traitement_data_spatiale import loadPopulationCarte
from src.data.traitement_data_visualisation import get_volume_deplacements, \
    get_nombre_vehicules_par_zone, get_od_count, get_population

# Chargement des données
gdf_merged = loadPopulationCarte()

# Ce fonction permet de genere un graphique de densite
def generate_graph_density():
    components = []
    df_population = get_population()
    fig_bar = go.Figure(data=[
        go.Bar(
            name='Hommes',
            x=df_population['tranche'],
            y=df_population['population_masculine_totale'],
            marker_color='blue',
            text=df_population['population_masculine_totale'],
            textposition='auto'
        ),
        go.Bar(
            name='Femmes',
            x=df_population['tranche'],
            y=df_population['population_feminine_totale'],
            marker_color='pink',
            text=df_population['population_feminine_totale'],
            textposition='auto'
        )
    ])
    fig_bar.update_layout(
        barmode='group',
        title='Distribution de la population masculine et féminine par tranche d\'âge',
        xaxis_title='Tranche d\'âge',
        yaxis_title='Population',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="Légende"),
        margin=dict(l=50, r=50, t=100, b=50)
    )
    components.append(dcc.Graph(id='graph-densite', figure=fig_bar, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
        'scrollZoom': False
    }))

    return html.Div([
        html.Div([
            html.I(className='fas fa-chart-pie', style={'margin-right': '1rem', 'font-size': '1.5rem'}),
            html.H3("Densité de population", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0},
                    id="title-Densité de population"),
            # Ajout de l'icône d'information pour le Popover
            html.Span(
                html.I(className='fas fa-info-circle', style={'margin-left': '0.5rem', 'font-size': '1rem'}),
                id='info-icon-population',  # ID correspondant pour le Popover
                style={'cursor': 'pointer'}
            ),
            # Ajout du Popover avec l'ID correspondant à l'icône d'information
            dbc.Popover(
                [
                    dbc.PopoverHeader("Détails sur la Visualisation"),
                    dbc.PopoverBody([
                        "Cette visualisation montre la distribution de la population masculine et féminine par tranche d'âge.",
                        html.Br(),
                        "Source de données : AGETIPA.",
                        html.Br(),
                        html.A("Cliquez ici pour plus de détails", href="https://www.exemple.com/details_population", target="_blank", style={'color': '#007bff'})
                    ])
                ],
                id="popover-population",  # ID unique pour le Popover
                target='info-icon-population',  # Cible l'icône d'information
                trigger='hover',  # Affiche le popover au survol
                placement='right',
                style={'font-size': '0.8rem', 'max-width': '200px'}
            )
        ], className='custom-div'),
        *components
    ])


def generate_graph_deplacement(noms_zones=None):
    components = []
    df_deplacement = get_volume_deplacements(noms_zones)

    fig_bar = go.Figure(data=[
        go.Bar(
            name='Productions',
            y=df_deplacement['zone_nom'],  # Nom des zones sur l'axe y
            x=df_deplacement['total_productions'],  # Volume sur l'axe x
            marker_color='rgba(31, 119, 180, 0.8)',
            text=df_deplacement['total_productions'],  # Ajout du texte sur les barres
            textposition='auto',  # Position automatique du texte
            orientation='h'  # Barres horizontales
        ),
        go.Bar(
            name='Attractions',
            y=df_deplacement['zone_nom'],  # Nom des zones sur l'axe y
            x=df_deplacement['total_attractions'],  # Volume sur l'axe x
            marker_color='rgba(255, 127, 14, 0.8)',  # Orange vif avec transparence
            text=df_deplacement['total_attractions'],  # Ajout du texte sur les barres
            textposition='auto',  # Position automatique du texte
            orientation='h'  # Barres horizontales
        ),
        go.Bar(
            name='Volume Total',
            y=df_deplacement['zone_nom'],  # Nom des zones sur l'axe y
            x=df_deplacement['total_volume'],  # Volume total sur l'axe x
            marker_color='rgba(44, 160, 44, 0.8)',  # Vert vif avec transparence
            text=df_deplacement['total_volume'],  # Ajout du texte sur les barres
            textposition='auto',  # Position automatique du texte
            orientation='h'  # Barres horizontales
        )
    ])

    # Mise à jour du layout du graphique
    fig_bar.update_layout(
        barmode='stack',  # Les barres sont empilées par zone
        xaxis_title='Volume de déplacements',  # Volume sur l'axe x
        yaxis_title='Zone',  # Nom des zones sur l'axe y
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="Type de Volume"),
        margin=dict(l=50, r=50, t=100, b=50),
        yaxis=dict(autorange="reversed")  # Inverser l'ordre des zones pour aligner avec l'image fournie
    )

    # Ajout du graphique aux composants
    components.append(dcc.Graph(id='deplacement-graph', figure=fig_bar, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
        'scrollZoom': False
    }))

    # Retourner le Div contenant le titre et le graphique
    return html.Div([
        html.Div([
            html.I(className='fas fa-chart-bar', style={'margin-right': '3rem', 'font-size': '1.5rem'}),
            html.H3("Volume des Déplacements", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0},
                    id="title-Volume de Déplacements"),
            html.Span(
                html.I(className='fas fa-info-circle', style={'margin-left': '0.5rem', 'font-size': '1rem'}),
                id='info-icon-deplacement',  # ID correspondant pour le Popover
                style={'cursor': 'pointer'}
            ),
            # Ajout du Popover avec l'ID correspondant à l'icône d'information
            dbc.Popover(
                [
                    dbc.PopoverHeader("Détails sur la Visualisation"),
                    dbc.PopoverBody([
                        "Cette visualisation montre le volume de déplacements par zone.",
                        html.Br(),
                        "Source de données : AGETIPA.",
                        html.Br(),
                        html.A("Cliquez ici pour plus de détails", href="https://www.exemple.com/details_deplacements", target="_blank", style={'color': '#007bff'})
                    ])
                ],
                id="popover-deplacement",  # ID unique pour le Popover
                target='info-icon-deplacement',  # Cible l'icône d'information
                trigger='hover',  # Affiche le popover au survol
                placement='right',
                style={'font-size': '0.8rem', 'max-width': '200px'}
            )
        ], className='custom-div'),
        *components
    ])


def generate_graph_vehicules(noms_zones=None):
    df_vehicules = get_nombre_vehicules_par_zone(noms_zones)

    components = []

    # Si une seule zone est sélectionnée, on crée un pie chart pour cette zone
    if noms_zones and len(noms_zones) == 1:
        zone_nom = noms_zones[0]
        zone_nom = zone_nom.lower()  # Transformation du nom de la zone en minuscule (ou majuscule si vous préférez)

        # Filtrer les données pour la zone sélectionnée
        df_zone = df_vehicules[df_vehicules['zone_nom'].str.lower() == zone_nom]
        df_zone = df_zone[df_zone['nombre_total'] > 0]  # Exclure les valeurs nulles ou égales à 0

        fig_pie = go.Figure(data=[
            go.Pie(
                labels=df_zone['type_vehicule'],
                values=df_zone['nombre_total'],
                textinfo='label+percent',
                insidetextorientation='radial'
            )
        ])

        fig_pie.update_layout(
            title=f"Répartition des types de véhicules dans la zone {zone_nom.capitalize()}",
            margin=dict(l=50, r=50, t=100, b=50)
        )

        components.append(dcc.Graph(id='vehicules-pie-chart', figure=fig_pie, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
            'scrollZoom': False
        }))

    else:
        fig_bar = go.Figure()

        # Calculer les pourcentages pour chaque type de véhicule par zone
        df_totals = df_vehicules.groupby('zone_nom')['nombre_total'].sum().reset_index()
        df_totals.rename(columns={'nombre_total': 'total_vehicules'}, inplace=True)
        df_vehicules = df_vehicules.merge(df_totals, on='zone_nom')
        df_vehicules['pourcentage'] = df_vehicules['nombre_total'] / df_vehicules['total_vehicules'] * 100

        for type_vehicule in df_vehicules['type_vehicule'].unique():
            df_type = df_vehicules[df_vehicules['type_vehicule'] == type_vehicule]

            fig_bar.add_trace(go.Bar(
                name=type_vehicule,
                y=df_type['zone_nom'],  # Nom des zones sur l'axe y
                x=df_type['pourcentage'],  # Pourcentage sur l'axe x
                text=df_type['pourcentage'].round(2).astype(str) + '%',  # Ajout du texte en pourcentages sur les barres
                textposition='auto',  # Position automatique du texte
                orientation='h'  # Barres horizontales
            ))

        # Mise à jour du layout du bar chart empilé
        fig_bar.update_layout(
            barmode='stack',  # Empiler les barres
            title='Répartition des types de véhicules par zone (en %)',
            xaxis_title='Pourcentage de véhicules',
            yaxis_title='Zone',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(title="Type de Véhicule"),
            margin=dict(l=50, r=50, t=100, b=50),
            yaxis=dict(autorange="reversed"),
            xaxis=dict(range=[0, 100])  # Plage de l'axe x de 0 à 100 %
        )

        components.append(dcc.Graph(id='vehicules-bar-chart', figure=fig_bar, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
            'scrollZoom': False
        }))

    # Retourner le Div contenant le titre et le graphique
    return html.Div([
        html.Div([
            html.I(className='fas fa-chart-pie', style={'margin-right': '1rem', 'font-size': '1.5rem'}),
            html.H3("Répartition des Véhicules", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0},
                    id="title-Repartition-Vehicules"),
            html.Span(
                html.I(className='fas fa-info-circle', style={'margin-left': '0.5rem', 'font-size': '1rem'}),
                id='info-icon-repartition',  # ID correspondant pour le Popover
                style={'cursor': 'pointer'}
            ),
            # Ajout du Popover avec l'ID correspondant à l'icône d'information
            dbc.Popover(
                [
                    dbc.PopoverHeader("Détails sur la Visualisation"),
                    dbc.PopoverBody([
                        "Cette visualisation montre la répartition des types de véhicules par zone.",
                        html.Br(),
                        "Source de données : AGETIPA.",
                        html.Br(),
                        html.A("Cliquez ici pour plus de détails", href="https://www.exemple.com/details_vehicules", target="_blank", style={'color': '#007bff'})
                    ])
                ],
                id="popover-repartition",  # ID unique pour le Popover
                target='info-icon-repartition',  # Cible l'icône d'information
                trigger='hover',  # Affiche le popover au survol
                placement='right',
                style={'font-size': '0.8rem', 'max-width': '200px'}
            )
        ], className='custom-div'),
        *components
    ])


def generate_sankey_diagram(noms_zones=None):
    df_matrice = get_od_count(noms_zones)

    # Créer une liste unique des zones pour les nœuds
    zones = list(pd.concat([df_matrice['nom_origine'], df_matrice['nom_destination']]).unique())

    # Créer des indices pour les zones
    zone_indices = {zone: i for i, zone in enumerate(zones)}

    sources = [zone_indices[zone] for zone in df_matrice['nom_origine']]
    targets = [zone_indices[zone] for zone in df_matrice['nom_destination']]
    values = df_matrice['somme_totale_par_origine']

    # Créer les couleurs pour les nœuds
    node_colors = ['#1f77b4' if i < len(df_matrice['nom_origine'].unique()) else '#ff7f0e' for i in range(len(zones))]

    # Créer le diagramme de Sankey avec deux colonnes
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=zones,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=[f"rgba(31, 119, 180, {value/sum(values):.2f})" for value in values]  # Assigner des couleurs avec opacité variable selon la valeur
        )
    ))

    fig_sankey.update_layout(
        title_text="Flux de Déplacements entre Zones",
        font_size=10
    )

    # Retourner le Div contenant le titre et le graphique
    return html.Div([
        html.Div([
            html.I(className='fas fa-chart-line', style={'margin-right': '3rem', 'font-size': '1.5rem'}),
            html.H3("Flux de Déplacements entre Zones", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0},
                    id="title-Flux-Deplacements"),
            html.Span(
                html.I(className='fas fa-info-circle', style={'margin-left': '0.5rem', 'font-size': '1rem'}),
                id='info-icon-matrice',  # ID correspondant pour le Popover
                style={'cursor': 'pointer'}
            ),
            # Ajout du Popover avec l'ID correspondant à l'icône d'information
            dbc.Popover(
                [
                    dbc.PopoverHeader("Détails sur la Visualisation"),
                    dbc.PopoverBody([
                        "Cette visualisation montre les flux de déplacements entre les zones.",
                        html.Br(),
                        "Source de données : AGETIPA.",
                        html.Br(),
                        html.A("Cliquez ici pour plus de détails", href="https://www.exemple.com/details_sankey", target="_blank", style={'color': '#007bff'})
                    ])
                ],
                id="popover-matrice",  # ID unique pour le Popover
                target='info-icon-matrice',  # Cible l'icône d'information
                trigger='hover',  # Affiche le popover au survol
                placement='right',
                style={'font-size': '0.8rem', 'max-width': '200px'}
            )
        ], className='custom-div'),
        dcc.Graph(id='sankey-diagram', figure=fig_sankey, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
            'scrollZoom': False
        })
    ])

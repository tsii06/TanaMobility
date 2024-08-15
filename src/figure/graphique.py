from dash import dcc,html,dash_table
import pandas as pd
import plotly.graph_objects as go
from src.data.traitement import loadPopulationCarte, load_data_population_bar_chart, get_volume_deplacements, \
    get_nombre_vehicules_par_zone

# Chargement des données
gdf_merged = loadPopulationCarte()
def generate_graph_density(clickData):
    components = []

    # Charger les données pour le bar chart
    df_population = load_data_population_bar_chart()

    # Créer le bar chart avec des styles supplémentaires
    fig_bar = go.Figure(data=[
        go.Bar(
            name='Hommes',
            x=df_population['tranche'],
            y=df_population['population_masculine_totale'],
            marker_color='blue',
            text=df_population['population_masculine_totale'],  # Ajout du texte sur les barres
            textposition='auto'  # Position automatique du texte
        ),
        go.Bar(
            name='Femmes',
            x=df_population['tranche'],
            y=df_population['population_feminine_totale'],
            marker_color='pink',
            text=df_population['population_feminine_totale'],  # Ajout du texte sur les barres
            textposition='auto'  # Position automatique du texte
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
    components.append(dcc.Graph(id='graph-densite',figure=fig_bar,config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
            'scrollZoom': False
        }))

    return html.Div([
        html.Div([
            html.I(className='fas fa-chart-pie', style={'margin-right': '3rem', 'font-size': '1.5rem'}),
            html.H3("Densité de population", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0}, id="title-Densité de population")
        ], className='custom-div'),
        *components
    ])


def generate_graph_deplacement(noms_zones=None):
    components = []

    # Charger les données pour le bar chart en utilisant la fonction `get_volume_deplacements`
    df_deplacement = get_volume_deplacements(noms_zones)

    # Créer le bar chart avec des barres empilées
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
        title='Zones le plus de volume de deplaacement',
        xaxis_title='Volume de déplacements',  # Volume sur l'axe x
        yaxis_title='Zone',  # Nom des zones sur l'axe y
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="Type de Volume"),
        margin=dict(l=50, r=50, t=100, b=50),
        yaxis=dict(autorange="reversed")  # Inverser l'ordre des zones pour aligner avec l'image fournie
    )

    # Ajout du graphique aux composants
    components.append(dcc.Graph(id='deplacement-graph',figure=fig_bar, config={
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
                    id="title-Volume de Déplacements")
        ], className='custom-div'),
        *components
    ])

def generate_graph_vehicules(noms_zones=None):
    df_vehicules = get_nombre_vehicules_par_zone(noms_zones)

    components = []

    # Si une seule zone est sélectionnée, on crée un pie chart pour cette zone
    if noms_zones and len(noms_zones) == 1:
        zone_nom = noms_zones[0]
        df_zone = df_vehicules[df_vehicules['zone_nom'] == zone_nom]

        fig_pie = go.Figure(data=[
            go.Pie(
                labels=df_zone['type_vehicule'],
                values=df_zone['nombre_total'],
                textinfo='label+percent',
                insidetextorientation='radial'
            )
        ])

        # Mise à jour du layout du graphique
        fig_pie.update_layout(
            title=f"Répartition des types de véhicules dans la zone {zone_nom}",
            margin=dict(l=50, r=50, t=100, b=50)
        )

        components.append(dcc.Graph(id='vehicules-pie-chart', figure=fig_pie, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toImage', 'zoom2d', 'pan2d'],
            'scrollZoom': False
        }))

    else:
        # Si plusieurs zones sont sélectionnées, on peut faire un bar chart empilé
        fig_bar = go.Figure()

        for type_vehicule in df_vehicules['type_vehicule'].unique():
            df_type = df_vehicules[df_vehicules['type_vehicule'] == type_vehicule]

            fig_bar.add_trace(go.Bar(
                name=type_vehicule,
                y=df_type['zone_nom'],  # Nom des zones sur l'axe y
                x=df_type['nombre_total'],  # Nombre total sur l'axe x
                text=df_type['nombre_total'],  # Ajout du texte sur les barres
                textposition='auto',  # Position automatique du texte
                orientation='h'  # Barres horizontales
            ))

        fig_bar.update_layout(
            barmode='stack',  # Empiler les barres
            title='Répartition des types de véhicules par zone',
            xaxis_title='Nombre de véhicules',
            yaxis_title='Zone',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(title="Type de Véhicule"),
            margin=dict(l=50, r=50, t=100, b=50),
            yaxis=dict(autorange="reversed")
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
            html.I(className='fas fa-chart-pie', style={'margin-right': '3rem', 'font-size': '1.5rem'}),
            html.H3("Répartition des Véhicules", style={'display': 'inline-block', 'textAlign': 'center', 'margin': 0},
                    id="title-Repartition-Vehicules")
        ], className='custom-div'),
        *components
    ])
from dash import dcc, html
import plotly.graph_objects as go

import dash_bootstrap_components as dbc

from src.data.traitement_data_visualisation import pivot_vehicule_count_od


def deplacement():
    df = pivot_vehicule_count_od()

    # Contenu à retourner
    content = []

    # Boucler sur chaque combinaison unique origine-destination
    for (origine, destination), group in df.groupby(['origine', 'destination']):
        trajet = f"{origine} -> {destination}"  # Utiliser la flèche bidirectionnelle
        distance = " 500 m"  # Exemple de distance statique, remplacez par votre distance dynamique si nécessaire

        # Créer une figure Plotly pour le trajet courant
        fig = go.Figure()

        # Ajouter les barres empilées pour chaque type de véhicule
        for typevehicule in ['Bus', 'Moto', 'Voiture']:
            if typevehicule in group.columns:
                pourcentage_deplacement = (group[typevehicule].sum() / group['nombre_total_somme_vehicule'].iloc[
                    0]) * 100 if group['nombre_total_somme_vehicule'].iloc[0] > 0 else 0
                fig.add_trace(go.Bar(
                    y=[trajet],
                    x=[pourcentage_deplacement],
                    text=[f"{pourcentage_deplacement:.1f}%"],  # Afficher les pourcentages sur les barres
                    textposition='inside',  # Positionner le texte à l'intérieur des barres
                    name=typevehicule,
                    orientation='h',
                ))

        # Mettre à jour la disposition de la figure pour enlever les axes et étiquettes
        fig.update_layout(
            barmode='stack',
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            xaxis_showticklabels=False,
            yaxis_showticklabels=False,
            showlegend=False,  # Cacher la légende pour un affichage plus propre
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            height=50,  # Hauteur totale du graphique
            margin=dict(l=0, r=0, t=0, b=0),  # Supprimer les marges du graphique
            autosize=True  # Utiliser tout l'espace disponible dans le conteneur
        )

        # Ajouter le graphique et le total des véhicules au contenu Dash, avec display flex
        content.append(
            html.Div([

                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4(trajet, style={'margin': '0', 'font-weight': 'normal', 'font-size': '16px'}),
                            html.P(distance, style={'margin': '0', 'font-weight': 'bold', 'font-size': '24px'})
                        ])
                    ], width=4, style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}),
                    dbc.Col([
                        dcc.Graph(figure=fig, config={'displayModeBar': False})  # Supprimer la barre de mode
                    ], width=8, style={'padding-left': '20px'})  # Espacement entre le graphique et le texte
                ], align='center')
            ], style={
                'padding': '15px',  # Espacement interne
            })
        )

    return html.Div(
        content,
        style={
            'background-color': '#f9f9f9',  # Couleur de fond gris clair
            'border-radius': '8px',  # Coins arrondis
            'margin': '30px',  # Espace entre les divs
            'padding': '30px',
            'display': 'flex',
            'flex-direction': 'column',
            'justify-content': 'center'
        },

    )
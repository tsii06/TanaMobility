from dash import html

from src.figure.graphique import generate_graph_deplacement, generate_graph_vehicules, generate_sankey_diagram


def detail_zone(zone):
    zone = [zone]
    return html.Div([
        html.Div([
            html.H3(f"Details for {zone}"),
            generate_graph_deplacement(zone),
            generate_graph_vehicules(zone),
            generate_sankey_diagram(zone)
        ])
    ])


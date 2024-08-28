from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    return html.Div([
        # Titre principal
        html.H2("PROFIL DE LA POPULATION", className="mb-2"),

        # Section Population par tranches d'âge
        html.Div([
            html.Div("Population par tranches d'âge", className="mb-2"),
            dbc.ButtonGroup([
                dbc.Button('Ensemble', id='ensemble-btn', outline=True, color="secondary"),
                dbc.Button('Hommes', id='hommes-btn', outline=True, color="secondary"),
                dbc.Button('Femmes', id='femmes-btn', outline=True, color="secondary"),
            ], className="btn-group"),
        ], className="mb-2"),

        # Section Classes d'âge
        html.Div([
            html.Div("Classes d'âge", className="mb-2"),
            dbc.ButtonGroup([
                dbc.Button('-14 ans', id='moins-14-btn', outline=True, color="secondary"),
                dbc.Button('15-29 ans', id='15-29-btn', outline=True, color="secondary"),
                dbc.Button('30-44 ans', id='30-44-btn', outline=True, color="secondary"),
            ], className="btn-group"),
            dbc.ButtonGroup([
                dbc.Button('44-60 ans', id='44-60-btn', outline=True, color="secondary"),
                dbc.Button('60+ ans', id='60-plus-btn', outline=True, color="secondary"),
            ], className="btn-group-row"),
        ], className="mb-2"),

    ], className="sidebar")
from dash import Input, Output, html
from src.figure.legende import generate_legend

def register_legend_callback(app):
    @app.callback(
        [Output('population-legend', 'children'),
         Output('segment-legend', 'children'),
         Output('route-legend', 'children'),
         Output('density-legend', 'children')],
        [Input('selected-thematiques', 'data')]
    )
    def update_legends(selected_thematiques):
        # Initialiser les légendes à "N/A" par défaut
        population_legend = html.Div()
        segment_legend = html.Div()
        route_legend = html.Div()
        density_legend = html.Div()

        # Vérifier si selected_thematiques n'est pas None et est itérable
        if selected_thematiques:
            if 'densite' in selected_thematiques:
                couleurs = ['#FFFFB2', '#FED976', '#FEB24C', '#FD8D3C',
                            '#D7301F']
                valeurs = ['0 - 1,000 habitants', '1,001 - 10,000 habitants', '10,001 - 50,000 habitants',
                           '50,001 - 100,000 habitants', '100,001+ habitants']
                population_legend = generate_legend('Population',couleurs, valeurs,'densite-legend')

            if 'segment' in selected_thematiques:
                couleurs = ['#440154', '#3B528B', '#21918C', '#5EC962', '#FDE725']
                valeurs = ['4500-7500', '7500-10000', '10000-15000', '15000-20000', '20000+']
                segment_legend = generate_legend('Volume de deplacement',couleurs, valeurs,'segment-legend')

        return population_legend, segment_legend, route_legend, density_legend

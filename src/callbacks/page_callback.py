from dash import Output, Input
from src.pages.home import layout as home_layout
from src.pages.about import layout as about_layout
from src.pages.contact import layout as contact_layout
from dash import html
def page_callback(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/about':
            return about_layout()
        elif pathname == '/contact':
            return contact_layout()
        elif pathname and pathname.startswith('/details/'):
            zone_id = pathname.split('/details/')[1]
            return html.Div([
                html.H3(f"Details for {zone_id}"),
                # Ajoutez ici plus d'informations détaillées sur la localisation
            ])
        else:
            return home_layout(app)
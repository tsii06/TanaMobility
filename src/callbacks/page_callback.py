from dash import Output, Input

from src.pages.detail_zone import detail_zone
from src.pages.home import layout as home_layout
from src.pages.about import layout as about_layout
from src.pages.contact import layout as contact_layout

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
            return detail_zone(zone_id)
        else:
            return home_layout(app)



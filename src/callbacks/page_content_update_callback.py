from dash import Output, Input

from src.pages.detail_zone import detail_zone
from src.pages.home import layout as home_layout
from src.pages.reference import reference
from src.pages.scenario import scenario


def page_callback(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/selection':
            return detail_zone()
        elif pathname == '/scenario':
            return scenario()
        elif pathname == '/reference':
            return reference()
        elif pathname and pathname.startswith('/details'):
            return detail_zone()
        else:
            return home_layout(app)



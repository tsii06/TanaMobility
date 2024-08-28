from dash import html, Dash, dcc

def graph(app: Dash):
    return html.Div([
        html.Div(id='graph-content', children=[
            html.Div(id='densite',),
            html.Div(id='typologie', ),
            html.Div(id='finances',),
            html.Div(id='matrice',),
            html.Div(id='dd', )

        ]),
        dcc.Store(id='clicked-zones', data=[]),
    ],
    className='scroll-style'
    ),



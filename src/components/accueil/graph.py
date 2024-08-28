from dash import html, Dash, dcc

def graph(app: Dash):
    return html.Div([
        html.Div(id='graph-content', children=[
            html.Div(id='densite',),
            html.Div(id='typologie', ),
            html.Div(id='volumes',),
            html.Div(id='matrice',),

        ]),
        dcc.Store(id='clicked-zones', data=[]),
    ],
    className='scroll-style'
    ),



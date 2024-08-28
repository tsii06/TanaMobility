from dash import html,dcc

def create_header():
    return html.Div(
        id="header",
        children=[
            html.Div(
                id="section-navigation",
                children=[
                    html.Span('DESCRIPTION DU TERRITOIRE', className='section-nav-item', id='description', n_clicks=0),
                    html.Span('OFFRE DE TRANSPORT', className='section-nav-item', id='offre_transport', n_clicks=0),
                    html.Span('PRATIQUES DE DÉPLACEMENT', className='section-nav-item', id='pratiques_deplacement', n_clicks=0),
                ],
                className='section-nav'
            ),
            html.Div(id='content', className='content')
        ]
    )
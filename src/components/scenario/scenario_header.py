from dash import html,dcc

def create_header_scenario():
    return html.Div(
        id="header",
        children=[
            html.Div(
                children=[
                    html.Span('SIMULATION', className='section-nav-item', id='simulation', n_clicks=0),
                    html.Span('COMPARAISON ', className='section-nav-item', id='comparaison', n_clicks=0),
                ],
                className='section-nav'
            ),
        ]
    )
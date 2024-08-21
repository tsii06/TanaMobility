from dash import dcc, html, Dash, Input, Output

def create_map(app: Dash):

    return html.Div(
        children=[
            dcc.Graph(
                id='map',
                config={
                    'displayModeBar': False
                },
                style={'width': '100%', 'height': 'calc(80vh - 60px)'}
            ),
            html.Div(
                id='legend',
                children=[
                    html.H4('Trafic/Road Segment' , className='legend-div'), # Ajout du titre
                    html.Div(
                        children=[
                            html.Span(
                                style={
                                    'background-color': '#FFFFB2',
                                    'display': 'inline-block',
                                    'width': '20px',
                                    'height': '20px',
                                    'margin-right': '10px',
                                    'border': '1px solid black',
                                    'border-radius': '50%',
                                }
                            ),
                            html.Span('1900 - 5000')
                        ],
                        className='legend-attribut-div'
                    ),
                    html.Div(
                        children=[
                            html.Span(
                                style={
                                    'background-color': '#FECC5C',
                                    'display': 'inline-block',
                                    'width': '20px',
                                    'height': '20px',
                                    'margin-right': '10px',
                                    'border': '1px solid black',
                                    'border-radius': '50%',
                                }
                            ),
                            html.Span('5000 - 7500')
                        ],
                        className='legend-attribut-div'
                    ),
                    html.Div(
                        children=[
                            html.Span(
                                style={
                                    'background-color': '#FD8D3C',
                                    'display': 'inline-block',
                                    'width': '20px',
                                    'height': '20px',
                                    'margin-right': '10px',
                                    'border': '1px solid black',
                                    'border-radius': '50%',
                                }
                            ),
                            html.Span('7500 - 15300')
                        ],
                        className='legend-attribut-div'
                    ),
                    html.Div(
                        children=[
                            html.Span(
                                style={
                                    'background-color': '#E31A1C',
                                    'display': 'inline-block',
                                    'width': '20px',
                                    'height': '20px',
                                    'margin-right': '10px',
                                    'border': '1px solid black',
                                    'border-radius': '50%',
                                }
                            ),
                            html.Span('15400 - 50000')
                        ],
                        className='legend-attribut-div'
                    ),
                ],
                style={'height': '20vh', 'padding': '10px', 'background-color': 'rgb(226 227 229 / 42%)', 'overflow-y': 'auto'}
            )

        ],
        style={'display': 'flex', 'flex-direction': 'column', 'height': '100vh'}
    )

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Exemple de données de flux de transport
data = {
    'Heure': ['6:00', '7:00', '8:00', '9:00', '10:00', '16:00', '17:00', '18:00', '19:00'],
    'Volume de Trafic': [100, 300, 500, 400, 200, 300, 600, 500, 300]
}
df_traffic = pd.DataFrame(data)

# Exemple de données géospatiales pour la carte de chaleur
data_geo = {
    'Route': ['Route1', 'Route1', 'Route2', 'Route2', 'Route3', 'Route3'],
    'Latitude': [-18.8792, -18.8802, -18.9156, -18.9166, -18.8992, -18.9002],
    'Longitude': [47.5079, 47.5089, 47.5361, 47.5371, 47.5237, 47.5247],
    'Nombre d\'Intermédiaires': [100, 150, 200, 250, 50, 75]
}
df_geo = pd.DataFrame(data_geo)



# Créer l'application Dash
app = dash.Dash(__name__)

# Disposition de l'application
app.layout = html.Div([
    html.H1("Modélisation des Flux de Transport"),

    html.H2("Carte de Chaleur des Routes à Antananarivo"),
    dcc.Graph(id='heatmap'),

    html.H2("Trafic Horaire"),
    dcc.Graph(id='traffic-chart'),

    dcc.Slider(
        id='slider',
        min=df_geo['Nombre d\'Intermédiaires'].min(),
        max=df_geo['Nombre d\'Intermédiaires'].max(),
        value=df_geo['Nombre d\'Intermédiaires'].min(),
        marks={str(n): str(n) for n in df_geo['Nombre d\'Intermédiaires'].unique()},
        step=None
    )
])


# Callback pour mettre à jour la carte de chaleur
@app.callback(
    Output('heatmap', 'figure'),
    [Input('slider', 'value')]
)
def update_heatmap(value):
    filtered_df = df_geo[df_geo['Nombre d\'Intermédiaires'] >= value]
    fig = px.density_mapbox(filtered_df, lat='Latitude', lon='Longitude', z='Nombre d\'Intermédiaires', radius=10,
                            center=dict(lat=-18.8792, lon=47.5079), zoom=12,
                            mapbox_style="open-street-map")
    fig.update_layout(title="Carte de Chaleur des Routes à Antananarivo")
    return fig


# Callback pour afficher le graphique de trafic horaire
@app.callback(
    Output('traffic-chart', 'figure'),
    [Input('slider', 'value')]
)
def update_traffic_chart(value):
    # Filtrer les données en figure de la valeur du slider
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_traffic['Heure'], y=df_traffic['Volume de Trafic'],
                             mode='lines+markers', name='Volume de Trafic'))
    fig.update_layout(title='Trafic Horaire', xaxis_title='Heure', yaxis_title='Volume de Trafic')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

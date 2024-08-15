import dash
from dash import html, dcc
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Exemple de données pour les flèches
data = [
    {'zone': 'Zone 1', 'latitude': 34.0522, 'longitude': -118.2437, 'voiture': 10, 'moto': 5, 'bus': 2},
    {'zone': 'Zone 2', 'latitude': 40.7128, 'longitude': -74.0060, 'voiture': 20, 'moto': 15, 'bus': 5},
    {'zone': 'Zone 3', 'latitude': 51.5074, 'longitude': -0.1276, 'voiture': 30, 'moto': 10, 'bus': 8}
]

# Préparer les traces pour les points représentant les diagrammes circulaires
circle_traces = []
for row in data:
    pie_chart = f"""
        <div style="position: absolute; left: 0; top: 0;">
            <svg width="50" height="50">
                <circle cx="25" cy="25" r="20" fill="green" stroke="none" stroke-width="0" />
                <text x="25" y="25" text-anchor="middle" fill="white" font-size="20" font-family="Arial" dy=".3em">{row['voiture']}</text>
            </svg>
        </div>
    """
    circle_traces.append(go.Scattermapbox(
        lat=[row['latitude']],
        lon=[row['longitude']],
        mode='markers+text',
        marker=dict(size=10, color='rgba(0,0,0,0)'),
        text=[pie_chart],
        hoverinfo='text',
        hovertext=f"Zone: {row['zone']}<br>Voiture: {row['voiture']}<br>Moto: {row['moto']}<br>Bus: {row['bus']}",
        textposition='middle center',
        textfont=dict(size=14, color='black')
    ))

# Préparer les traces pour les lignes de flux
line_traces = []
flows = [
    {'start_lat': 34.0522, 'start_lon': -118.2437, 'end_lat': 40.7128, 'end_lon': -74.0060, 'flux': 100},
    {'start_lat': 40.7128, 'start_lon': -74.0060, 'end_lat': 51.5074, 'end_lon': -0.1276, 'flux': 200}
]
for row in flows:
    line = go.Scattermapbox(
        lat=[row['start_lat'], row['end_lat']],
        lon=[row['start_lon'], row['end_lon']],
        mode='lines',
        line=dict(width=2, color='blue'),
        hoverinfo='text',
        text=f"Flux: {row['flux']}"
    )
    line_traces.append(line)

# Créer la carte
fig = go.Figure()

# Ajouter les traces de diagrammes circulaires
for trace in circle_traces:
    fig.add_trace(trace)

# Ajouter les lignes de flux
for trace in line_traces:
    fig.add_trace(trace)

# Configuration de la carte
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=39, lon=-98),
        zoom=3
    ),
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0)
)

# Layout de l'application Dash
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

from dash import dcc, html, Dash
import plotly.graph_objects as go

# Initialiser l'application Dash
app = Dash(__name__)

# Données pour le graphique Sankey
nodes = ["West", "East", "South", "Central", "Technology", "Office Supplies", "Furniture"]
sources = [0, 1, 2, 3, 0, 1, 2, 3]
targets = [4, 4, 4, 4, 5, 5, 5, 6]
values = [8, 4, 2, 8, 4, 4, 2, 8]

# Couleurs pour chaque nœud
node_colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494"]

# Couleurs pour chaque flux (utiliser la même couleur que le nœud source)
link_colors = [node_colors[src] for src in sources]

# Création du graphique Sankey
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color=node_colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors  # Assigner la couleur des flux selon les nœuds sources
    ))])

fig.update_layout(title_text="Sankey Diagram with Node and Link Colors", font_size=10)

# Disposition de l'application Dash
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

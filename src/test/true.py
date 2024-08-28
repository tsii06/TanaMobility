from pyproj import Proj, Transformer

# Définir les paramètres de la projection UTM
utm_proj = Proj(proj='utm', zone=38, ellps='WGS84', datum='WGS84', units='m', no_defs=True)
latlon_proj = Proj(proj='latlong', datum='WGS84')

# Décalage de la projection (netOffset)
net_offset_x = 751064.25
net_offset_y = 2106749.38

utm_coords = [
    (11353.35 + net_offset_x, 22778.59 + net_offset_y),
    (11351.92 + net_offset_x, 22778.81 + net_offset_y),
    (11351.09 + net_offset_x, 22778.49 + net_offset_y),
    (771123.918307, 2119975.6658679997)
]

# Créer un transformeur pour convertir les coordonnées
transformer = Transformer.from_proj(utm_proj, latlon_proj)
latlon_coords = [transformer.transform(x, y) for x, y in utm_coords]
# Coordonnées UTM à convertir (appliquer le décalage)


# Convertir les coordonnées UTM en latitude/longitude


# Afficher les coordonnées converties
# for coord in latlon_coords:
#     print(f"Longitude: {coord[0]}, Latitude: {coord[1]}")

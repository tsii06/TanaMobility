import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Exemple de données
data = {
    'Densité_Population': [5000, 8000, 6000, 7000, 4000],
    'Volume_Trafic': [15000, 30000, 20000, 25000, 12000]
}
df = pd.DataFrame(data)

# Graphique de dispersion
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Densité_Population', y='Volume_Trafic', s=100, color='blue', edgecolor="w", linewidth=1)
plt.title('Corrélation entre Densité de Population et Volume de Trafic')
plt.xlabel('Densité de Population (habitants/km²)')
plt.ylabel('Volume de Trafic (véhicules/jour)')
plt.grid(True)
plt.show()

# Exemple de données
data = {
    'Densité_Population': [5000, 8000, 6000, 7000, 4000],
    'Volume_Trafic': [15000, 30000, 20000, 25000, 12000],
    'Revenu_Moyen': [2500, 3200, 2900, 3100, 2700],
    'Distance_Deplacement': [5, 8, 6, 7, 4]
}
df = pd.DataFrame(data)

# Matrice de corrélation
corr_matrix = df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matrice de Corrélation')
plt.show()

# Graphique de dispersion avec ligne de régression
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Densité_Population', y='Volume_Trafic', scatter_kws={'s':100}, line_kws={'color':'red'})
plt.title('Corrélation entre Densité de Population et Volume de Trafic avec Ligne de Régression')
plt.xlabel('Densité de Population (habitants/km²)')
plt.ylabel('Volume de Trafic (véhicules/jour)')
plt.grid(True)
plt.show()

# Exemple de données avec une troisième variable
data = {
    'Densité_Population': [5000, 8000, 6000, 7000, 4000],
    'Volume_Trafic': [15000, 30000, 20000, 25000, 12000],
    'Revenu_Moyen': [2500, 3200, 2900, 3100, 2700]
}
df = pd.DataFrame(data)

# Graphique en bulles
plt.figure(figsize=(10, 6))
plt.scatter(df['Densité_Population'], df['Volume_Trafic'], s=df['Revenu_Moyen']*10, alpha=0.5, c='blue', edgecolors='w', linewidth=1)
plt.title('Corrélation entre Densité de Population et Volume de Trafic avec Taille des Bulles représentant le Revenu Moyen')
plt.xlabel('Densité de Population (habitants/km²)')
plt.ylabel('Volume de Trafic (véhicules/jour)')
plt.grid(True)
plt.show()

from mpl_toolkits.mplot3d import Axes3D

# Graphique en nuage de points 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['Densité_Population'], df['Volume_Trafic'], df['Revenu_Moyen'], c='blue', s=100)

ax.set_title('Nuage de Points 3D')
ax.set_xlabel('Densité de Population')
ax.set_ylabel('Volume de Trafic')
ax.set_zlabel('Revenu Moyen')
plt.show()

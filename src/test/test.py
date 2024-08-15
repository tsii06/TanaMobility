# Exemple fictif d'analyse par type d'activités
import pandas as pd
from scipy.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt
data = {
    'Type_Activité': ['Résidentiel', 'Commercial', 'Industriel', 'Mixte', 'Rural'],
    'Utilisation_VP': [60, 20, 40, 50, 70],
    'Utilisation_TC': [30, 70, 50, 40, 20],
    'Utilisation_Moto': [10, 10, 10, 10, 10]
}

df = pd.DataFrame(data)

# Visualisation des différentes typologies modales
plt.figure(figsize=(12, 6))
sns.barplot(x='Type_Activité', y='Utilisation_VP', data=df, label='VP', color='blue')
sns.barplot(x='Type_Activité', y='Utilisation_TC', data=df, label='TC', color='green', alpha=0.5)
sns.barplot(x='Type_Activité', y='Utilisation_Moto', data=df, label='Moto', color='red', alpha=0.3)
plt.legend()
plt.title('Typologie Modale des Offres par Type d\'Activité')
plt.xlabel('Type d\'Activité')
plt.ylabel('Utilisation (%)')
plt.show()

data = {
    'Zone': ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'],
    'Densité_Population': [5000, 8000, 6000, 7000, 4000],
    'Volume_Trafic': [15000, 30000, 20000, 25000, 12000]
}

df = pd.DataFrame(data)

# Calcul de la corrélation de Pearson
corr, _ = pearsonr(df['Densité_Population'], df['Volume_Trafic'])
print(f"Coefficient de corrélation de Pearson: {corr}")

# Visualisation de la corrélation
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Densité_Population', y='Volume_Trafic')
plt.title('Corrélation entre Densité de Population et Volume de Trafic')
plt.xlabel('Densité de Population (habitants/km²)')
plt.ylabel('Volume de Trafic (véhicules/jour)')
plt.show()

# Données de hiérarchie fonctionnelle et débit/vitesse
data = {
    'Hiérarchie': ['Autoroute', 'Route principale', 'Route secondaire'],
    'Débit': [5000, 3000, 1000],
    'Vitesse': [100, 60, 40]
}

df = pd.DataFrame(data)

# Visualisation du débit/vitesse par hiérarchie fonctionnelle
fig, ax1 = plt.subplots(figsize=(10, 6))

ax2 = ax1.twinx()
sns.barplot(x='Hiérarchie', y='Débit', data=df, ax=ax1, color='blue')
sns.lineplot(x='Hiérarchie', y='Vitesse', data=df, ax=ax2, color='red', marker='o')

ax1.set_xlabel('Hiérarchie Fonctionnelle')
ax1.set_ylabel('Débit (véhicules/h)', color='blue')
ax2.set_ylabel('Vitesse (km/h)', color='red')
plt.title('Débit et Vitesse par Hiérarchie Fonctionnelle')
plt.show()


# Données de revenu moyen et distance moyenne de déplacement
data = {
    'Zone': ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'],
    'Revenu_Moyen': [2500, 3200, 2900, 3100, 2700],
    'Distance_Deplacement': [5, 8, 6, 7, 4]
}

df = pd.DataFrame(data)

# Calcul de la corrélation de Pearson
corr, _ = pearsonr(df['Revenu_Moyen'], df['Distance_Deplacement'])
print(f"Coefficient de corrélation de Pearson: {corr}")

# Visualisation de la corrélation
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Revenu_Moyen', y='Distance_Deplacement')
plt.title('Corrélation entre Revenu Moyen et Distance Moyenne de Déplacement')
plt.xlabel('Revenu Moyen (euros)')
plt.ylabel('Distance Moyenne de Déplacement (km)')
plt.show()


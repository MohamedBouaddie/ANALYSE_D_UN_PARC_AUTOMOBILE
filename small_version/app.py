
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Lecture du fichier Excel
file_path = "voitures.xlsx" 
df = pd.read_excel(file_path)
df.head()



# Conversion des colonnes en tableaux NumPy
marques = df["Marque"].to_numpy()
kilometrages = df["Kilométrage"].to_numpy()
consommations = df["Consommation(L/100km)"].to_numpy()

# --- Moyenne des kilomètres ---
moyenne_km = np.mean(kilometrages)
print("Moyenne des kilomètres :", moyenne_km)

# --- Moyenne de consommation ---
moyenne_conso = np.mean(consommations)
print("Moyenne de consommation :", moyenne_conso)

# --- Voitures dont le kilométrage est supérieur à la moyenne ---
indices_sup_moyenne = np.where(kilometrages > moyenne_km)[0]

print("Voitures avec kilométrage supérieur à la moyenne :")
for i in indices_sup_moyenne:
    print(f"{marques[i]} → {kilometrages[i]} km, {consommations[i]} L/100km")




# --- Diagramme : consommation moyenne par marque ---
marques_uniques, nb_voitures = np.unique(marques, return_counts=True)
conso_moyenne_par_marque = []
for marque in marques_uniques:
    conso_moyenne_par_marque.append(np.mean(consommations[marques == marque]))

plt.figure(figsize=(8,5))
plt.bar(marques_uniques, conso_moyenne_par_marque)
plt.title("Consommation moyenne des voitures par marque")
plt.xlabel("Marque")
plt.ylabel("Consommation moyenne (L/100 km)")
plt.tight_layout()
plt.show()




# --- Diagramme : kilométrage moyen par marque ---
km_moyen_par_marque = []
for marque in marques_uniques:
    km_moyen_par_marque.append(np.mean(kilometrages[marques == marque]))

plt.figure(figsize=(8,5))
plt.bar(marques_uniques, km_moyen_par_marque)
plt.title("Kilométrage moyen des voitures par marque")
plt.xlabel("Marque")
plt.ylabel("Kilométrage moyen (km)")
plt.tight_layout()
plt.show()

# Analyse d’un parc automobile (Excel → NumPy/Pandas/Matplotlib)

Ce mini-projet analyse un fichier Excel `data.xlsx` contenant des informations sur des voitures (marque, kilométrage, consommation).  
Il calcule des statistiques simples et génère des graphiques pour comparer les marques.

---

## 🎯 Objectifs

À partir de `data.xlsx`, le script permet de :

- Lire les données depuis Excel avec **Pandas**
- Convertir les colonnes en tableaux **NumPy**
- Calculer :
  - la **moyenne des kilométrages**
  - la **moyenne des consommations**
- Afficher la liste des voitures dont le **kilométrage est supérieur à la moyenne**
- Générer 2 graphiques (**Matplotlib**) :
  - **consommation moyenne par marque**
  - **kilométrage moyen par marque**

---

## 📁 Project Structure

```bash
analyse-parc-automobile/
│-- main.py            # Script principal (analyse + graphiques)
│-- data.xlsx      # Données Excel (dataset)
│-- requirements.txt   # Dépendances Python
│-- README.md          # Documentation
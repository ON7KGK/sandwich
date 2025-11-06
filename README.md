# Gestion des Sandwichs

Application web pour gérer les commandes de sandwichs quotidiennes et suivre les paiements.

## Fonctionnalités

- **Page de commande** : Sélection de sandwichs avec affichage des ingrédients et prix
- **Gestion des personnes** : Possibilité d'ajouter plusieurs personnes à une commande
- **Suivi des paiements** : Marquer les commandes comme payées ou non payées
- **Historique** : Consultation des commandes des 15 derniers jours
- **Statistiques** : Vue d'ensemble des montants payés, non payés et totaux
- **Filtres** : Recherche par nom de personne et par statut de paiement

## Installation

1. Installez Python 3.8 ou supérieur

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement

1. Démarrez le serveur :
```bash
python main.py
```

2. Ouvrez votre navigateur à l'adresse :
```
http://localhost:5000
```

## Utilisation

### Commander des sandwichs

1. Allez sur l'onglet "Commander"
2. Cliquez sur les sandwichs que vous souhaitez commander
3. Entrez le(s) nom(s) des personne(s) (séparés par des virgules si plusieurs)
4. Ajoutez un commentaire si nécessaire (ex: "sans oignons")
5. Cochez "Déjà payé" si le paiement a été effectué
6. Cliquez sur "Valider la commande"

### Consulter l'historique

1. Allez sur l'onglet "Historique"
2. Consultez les statistiques en haut de page
3. Utilisez les filtres pour rechercher des commandes spécifiques
4. Marquez les commandes comme payées/non payées
5. Supprimez les commandes si nécessaire

## Structure de la base de données

L'application utilise SQLite avec les tables suivantes :

- **sandwichs** : Liste des sandwichs disponibles avec leurs ingrédients et prix
- **commandes** : Historique de toutes les commandes avec statut de paiement

## Technologies utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML, CSS, JavaScript (Vanilla)
- **Base de données** : SQLite
- **API** : REST API avec JSON

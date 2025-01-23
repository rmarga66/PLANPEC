# PLANPEC

**PLANPEC** est une application Flask pour gérer et optimiser une tournée de patients. 

## Fonctionnalités
- Ajouter un patient avec son adresse.
- Récupérer les coordonnées GPS de l'adresse via une API gratuite.
- Lister les patients et leur état (visité ou non).
- Marquer une visite comme effectuée.

## Installation

1. Clonez le projet :

2. Créez un environnement virtuel et activez-le :

3. Installez les dépendances :

4. Lancez l'application :

L'application est accessible à `http://127.0.0.1:5000`.

## Endpoints

- **Ajouter un patient** : `POST /add_patient`
- Données requises : `{ "name": "John Doe", "address": "10 rue de Rivoli, Paris" }`

- **Lister les patients** : `GET /list_patients`

- **Marquer un patient visité** : `POST /mark_visited/<id>`

## Dépendances
- Flask
- Requests

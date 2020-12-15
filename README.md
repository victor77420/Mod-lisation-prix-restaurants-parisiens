# Projet de fin de semestre (Python pour le Data Scientist) : "Qu'est-ce qui détermine le prix d'un repas dans un restaurant Parisien ?"

## Présentation de notre sujet

Dans ce projet, nous allons étudier les déterminants du prix d'un repas dans un restaurant situé à Paris. Pour cela, nous allons procéder en plusieurs étapes.

  - Récupération des données : nous partons d'un jeu de données contenant les informations de base de restaurants en France (nom, numéro d'immatriculation, adresse...) issu de SalesDorado. Nous complétons d'abord ce jeu de données par diverses informations géographiques sur les communes de localisation des restaurants. Puis nous nous restreignons aux restaurants parisiens, et scrappons des données de plusieurs sites pour compléter cette base de données : TripAdvisor, Societe.com et PagesJaunes.
  - Analyse descriptive et représentation graphique : on confronte graphiquement différentes variables au prix, et en déduit leur impact sur le prix d'un repas en restaurant parisien. 
  - Modélisation : on va faire des régressions linéaires du prix sur certianes de nos diverses variables explicatives qu'on aura sélectionné, pour voir si le prix peut s'expliquer linéairement par d'autres variables. Puis on réalise une ACP et un clustering. 

## Organisation du repository

- [LE FICHIER DES DONNÉES BRUTES ISSU DE SALESDORADO]

- [LE FICHIER DE DONNÉES A LA FIN DU SCRAPPING]

- Untitled1.ipynb : notebook final du projet en trois partiels (scrapping, analyse descriptive et modéliation).

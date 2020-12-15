# Projet de fin de semestre (Python pour le Data Scientist) : "Qu'est-ce qui détermine le prix d'un repas dans un restaurant Parisien ?"

## Présentation de notre sujet

Dans ce projet, nous allons étudier les déterminants du prix d'un repas dans un restaurant situé à Paris. Pour cela, nous allons procéder en plusieurs étapes.

  - Récupération des données : nous partons d'un jeu de données contenant les informations de base de restaurants en France (nom, numéro d'immatriculation, adresse...) issu de SalesDorado. Nous complétons d'abord ce jeu de données par diverses informations géographiques sur les communes de localisation des restaurants. Puis nous nous restreignons aux restaurants parisiens, et scrappons des données de plusieurs sites pour compléter cette base de données : TripAdvisor, Societe.com et PagesJaunes.
  - Analyse descriptive et représentation graphique : on confronte graphiquement différentes variables au prix, et en déduit leur impact sur le prix d'un repas en restaurant parisien. 
  - Modélisation : on va faire des régressions linéaires du prix sur certaines de nos diverses variables explicatives qu'on aura sélectionné, pour voir si le prix peut s'expliquer linéairement par d'autres variables. Puis on réalise une ACP et un clustering. 

## Organisation du repository

- tablefinalisee.csv : la table obtenue à la fin de la partie 1 et de nos scrappings 

- partie1_recuperation_des_donnees.ipynb : première partie du projet

- partie2_analyse_descriptive.ipynb : deuxième partie du sujet

- partie3_modelisation.ipynb : troisième partie du projet

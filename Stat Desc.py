#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:48:21 2020

@author: victorhuynh
"""

import matplotlib.pyplot as plt
import seaborn as sns

parisiens = pd.read_csv('/Users/victorhuynh/Documents/ENSAE/ENSAE 2A/2A S1/PDS/Projet/victoire.csv', sep = ";")

df = parisiens.groupby('Catégorie de prix').aggregate({'name':'count'}).reset_index()
df = df.rename(columns={'name': 'Nombre de restaurants'})
sns.catplot(x='Catégorie de prix', y='Nombre de restaurants', edgecolor="black", data=df,kind = "bar", color = "cyan")

##Quelques tendances
        
#Moyenne de note globale par catégorie de prix
parisiens = parisiens[parisiens['Note Globale'] != 'NR']
parisiens = parisiens[parisiens['Note Globale'] != 'Non renseigné']

parisiens['Note Globale'] = parisiens['Note Globale'].str.replace(",", ".").astype(float)
parisiens.groupby('Catégorie de prix').aggregate({'Note Globale' : 'mean'})

#Moyenne du nombre d'avis par catégorie de prix

parisiens['Nombre avis'] = parisiens['Nombre avis'].astype(int)
df = parisiens.groupby('Catégorie de prix').aggregate({'Nombre avis' : 'mean'}).reset_index()
df = df.rename(columns={'Nombre avis': "Nombre moyen d'avis"})
sns.catplot(x='Catégorie de prix', y="Nombre moyen d'avis", edgecolor="black", data=df,kind = "bar", color = "yellow")

#Moyenne de note de cuisine par catégorie de prix

parisiens_avec_note_cuisine = parisiens[parisiens['Note de cuisine'] != 'Non renseigné']
parisiens_avec_note_cuisine = parisiens_avec_note_cuisine.astype({'Note de cuisine' : 'float'})
parisiens_avec_note_cuisine.groupby('Catégorie de prix').aggregate({'Note de cuisine' : 'mean'})

#Moyenne de note de service par catégorie de prix

parisiens_avec_note_service = parisiens[parisiens['Note de service'] != 'Non renseigné']
parisiens_avec_note_service = parisiens_avec_note_service.astype({'Note de service' : 'float'})
parisiens_avec_note_service.groupby('Catégorie de prix').aggregate({'Note de service' : 'mean'})

#Moyenne de note QP par catégorie de prix

parisiens_avec_note_QP = parisiens[parisiens['Note qualité-prix'] != 'Non renseigné']
parisiens_avec_note_QP = parisiens_avec_note_QP.astype({'Note qualité-prix' : 'float'})
parisiens_avec_note_QP.groupby('Catégorie de prix').aggregate({'Note qualité-prix' : 'mean'})

#Moyenne de note d'ambiance par catégorie de prix

parisiens_avec_note_ambiance = parisiens[parisiens['Note ambiance'] != 'Non renseigné']
parisiens_avec_note_ambiance = parisiens_avec_note_ambiance.astype({'Note ambiance' : 'float'})
parisiens_avec_note_ambiance.groupby('Catégorie de prix').aggregate({'Note ambiance' : 'mean'})

##On va prendre une catégorie de prix par une, et représenter le pourcentage de restaurants par arrondissement dans cette catégorie de prix

parisiens_cheap = parisiens[parisiens['Catégorie de prix'] == 'faible'].reset_index(drop = True)
parisiens_average = parisiens[parisiens['Catégorie de prix'] == 'moyen'].reset_index(drop = True)
parisiens_expensive = parisiens[parisiens['Catégorie de prix'] == 'élevé'].reset_index(drop = True)

#On compte le nombre de restaurants par arrondissement
from matplotlib.ticker import MultipleLocator
effectif_total_par_arr = parisiens.groupby('arr').aggregate({'arr' : 'count'})['arr']

#On compte le nombre de restaurants "cheap" par arrondissement et on trace leur fréquence par arrondissement
effectif_cheap = parisiens_cheap.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_cheap = range(1,21)
ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_cheap,effectif_cheap/effectif_total_par_arr, color = "#ABEBC6", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)

#On compte le nombre de restaurants "average" par arrondissement et on trace leur fréquence par arrondissement
effectif_average = parisiens_average.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_average = range(1,21)
ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_average,effectif_average/effectif_total_par_arr, color = "#F0B27A", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)

#On compte le nombre de restaurants "expensive" par arrondissement et on trace leur fréquence par arrondissement
effectif_expensive = parisiens_expensive.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_expensive = range(1,21)
ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_expensive,effectif_expensive/effectif_total_par_arr, color = "#EC7063", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)
        
##Etude de la variable "Prix moyen" pour avoir les idées plus claires avec des prix en chiffres

#Etudions le prix moyen d'un restaurant par arrondissement

df = parisiens.groupby('arr').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'arr' : 'Arrondissement'})
sns.catplot(x='Arrondissement', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "pink")

#Traçons l'évolution du prix d'un restaurant en fonction de l'année de sa créaton

df = parisiens.groupby('foundingYear').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'foundingYear' : 'Année de création'})
sns.lineplot(x='Année de création', y='Prix moyen', data=df, color = "green")

#Voyons le prix d'un restaurant selon le style de nourriture

df = parisiens.groupby('Style de nourriture').aggregate({'Prix moyen' : 'mean'}).reset_index()
g = sns.catplot(x='Style de nourriture', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "orange")
g.set_xticklabels(rotation=90) #Pour ne pas que les intitulés se chevauchent

#Comparons taille d'entreprise d'un restaurant et prix moyen du repas dans ce restaurant

df = parisiens.groupby('categorySize').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'categorySize' : 'Taille du restaurant'})
sns.catplot(x='Taille du restaurant', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "blue")











## INUTILE On l'a replacé autre part : le bout de code pour obtenir la variable 'Prix moyen'

parisiens_test4 = parisiens_test3[parisiens_test3['Fourchette de prix'].str.contains('€')].reset_index(drop=True)
parisiens_test4['Fourchette prix inf'] = 'Non renseigné'
parisiens_test4['Fourchette prix sup'] = 'Non renseigné'

#On récupère la borne supérieure et la borne inférieure de la variable 'Fourchette de prix'
for k in range(parisiens_test4.shape[0]):
    i = 0
    carac = parisiens_test4['Fourchette de prix'][k][0]
    while carac != '€':
        i = i+1
        carac = parisiens_test4['Fourchette de prix'][k][i]
    j = i
    carac = parisiens_test4['Fourchette de prix'][k][i+1] #Pour que carac ne soit plus égal à '€'
    while carac != '€':
        i = i+1
        carac = parisiens_test4['Fourchette de prix'][k][i]
    parisiens_test4['Fourchette prix inf'][k] = parisiens_test4['Fourchette de prix'][k][0:j]
    parisiens_test4['Fourchette prix sup'][k] = parisiens_test4['Fourchette de prix'][k][j+4:i]

#On convertit ces bornes en 'int'
    
parisiens_test4 = parisiens_test4[parisiens_test4['Fourchette prix sup'] != '23\xa0243'].reset_index(drop = True)
#On fait cela pour enlever une ligne délirante où la fourchette de prix supérieure vaut '23\xa0243'

parisiens_test4 = parisiens_test4.astype({'Fourchette prix inf' : 'int64','Fourchette prix sup' : 'int64'})
parisiens_test4['Prix moyen'] = (parisiens_test4['Fourchette prix inf'] + parisiens_test4['Fourchette prix sup']) / 2

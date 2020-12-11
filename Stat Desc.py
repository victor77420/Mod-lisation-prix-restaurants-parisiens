#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:48:21 2020

@author: victorhuynh
"""

import matplotlib.pyplot as plt
import seaborn as sns


parisiens_test2 = pd.read_excel('parisiens_test2_avec_note.xlsx')

parisiens_test3 = parisiens_test2.copy()
parisiens_test3 = parisiens_test3.drop('Style de nourriture', axis=1)
parisiens_test3 = parisiens_test3.drop('index', axis=1)
parisiens_test3 = parisiens_test3.drop('Unnamed: 0', axis=1)
parisiens_test3 = parisiens_test3.drop('level_0', axis=1)
parisiens_test3 = parisiens_test3.drop('Unnamed: 0.1', axis=1)
parisiens_test3 = parisiens_test3.astype({'Catégorie de prix':'str'})
parisiens_test3 = parisiens_test3[parisiens_test3['Catégorie de prix'].str.contains('€')].reset_index(drop = True)

df = parisiens_test3.groupby('Catégorie de prix').aggregate({'name':'count'}).reset_index()
df = df.rename(columns={'name': 'Effectif'})
sns.catplot(x='Catégorie de prix', y='Effectif', edgecolor="black", data=df,kind = "bar", color = "cyan")

##Quelques tendances
        
#Moyenne de note globale par catégorie de prix

parisiens_test3['Note Globale'] = parisiens_test3['Note Globale'].str.replace(",", ".").astype(float)
parisiens_test3.groupby('Catégorie de prix').aggregate({'Note Globale' : 'mean'})

#Moyenne de nombre d'avis par catégorie de prix

parisiens_test3['Nombre avis'] = parisiens_test3['Nombre avis'].astype(int)
parisiens_test3.groupby('Catégorie de prix').aggregate({'Nombre avis' : 'mean'})

#Moyenne de note de cuisine par catégorie de prix

parisiens_avec_note_cuisine = parisiens_test3[parisiens_test3['Note de cuisine'] != 'Non renseigné']
parisiens_avec_note_cuisine = parisiens_avec_note_cuisine.astype({'Note de cuisine' : 'float'})
parisiens_avec_note_cuisine.groupby('Catégorie de prix').aggregate({'Note de cuisine' : 'mean'})

#Moyenne de note de service par catégorie de prix

parisiens_avec_note_service = parisiens_test3[parisiens_test3['Note de service'] != 'Non renseigné']
parisiens_avec_note_service = parisiens_avec_note_service.astype({'Note de service' : 'float'})
parisiens_avec_note_service.groupby('Catégorie de prix').aggregate({'Note de service' : 'mean'})

#Moyenne de note QP par catégorie de prix

parisiens_avec_note_QP = parisiens_test3[parisiens_test3['Note qualité-prix'] != 'Non renseigné']
parisiens_avec_note_QP = parisiens_avec_note_QP.astype({'Note qualité-prix' : 'float'})
parisiens_avec_note_QP.groupby('Catégorie de prix').aggregate({'Note qualité-prix' : 'mean'})

#Moyenne de note d'ambiance par catégorie de prix

parisiens_avec_note_ambiance = parisiens_test3[parisiens_test3['Note ambiance'] != 'Non renseigné']
parisiens_avec_note_ambiance = parisiens_avec_note_ambiance.astype({'Note ambiance' : 'float'})
parisiens_avec_note_ambiance.groupby('Catégorie de prix').aggregate({'Note ambiance' : 'mean'})

##On va prendre une catégorie de prix par une, et représenter le pourcentage de restaurants par arrondissement dans cette catégorie de prix

parisiens_cheap = parisiens_test3[parisiens_test3['Catégorie de prix'] == "['€']"].reset_index(drop = True)
parisiens_average = parisiens_test3[parisiens_test3['Catégorie de prix'] == "['€€-€€€']"].reset_index(drop = True)
parisiens_expensive = parisiens_test3[parisiens_test3['Catégorie de prix'] == "['€€€€']"].reset_index(drop = True)

from matplotlib.ticker import MultipleLocator
effectif_total_par_arr = parisiens_test3.groupby('arr').aggregate({'arr' : 'count'})['arr']

effectif_cheap = parisiens_cheap.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_cheap = range(1,21)

ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_cheap,effectif_cheap/effectif_total_par_arr, color = "#ABEBC6", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)
        
effectif_average = parisiens_average.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_average = range(1,21)

ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_average,effectif_average/effectif_total_par_arr, color = "#F0B27A", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)
        
effectif_expensive = parisiens_expensive.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_expensive = range(1,21)

ax = plt.axes()
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_expensive,effectif_expensive/effectif_total_par_arr, color = "#EC7063", edgecolor="black",linewidth=1, ecolor = "green",capsize = 10)
        
##Etude de la variable "Fourchette de prix" pour avoir les idées plus claires avec des prix en chiffres

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

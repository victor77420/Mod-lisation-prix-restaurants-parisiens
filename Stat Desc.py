#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:48:21 2020

@author: victorhuynh
"""

# On importe trois modules qui vont nous servir pour réaliser des graphiques.
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# On importe la base de données qu'on a construite via scrapping
parisiens = pd.read_csv('/Users/victorhuynh/Documents/ENSAE/ENSAE 2A/2A S1/PDS/Projet/table_finale.csv', sep = ";")

parisiens_avec_prix = parisiens[parisiens['Prix moyen'].notna()] 
# On crée un dataframe secondaire où l'on retire tous les restaurants pour lequels on n'a pas de 
# valeur quantitative : il nous servira à certaines étapes
display(parisiens_avec_prix.sort_values('Prix moyen').tail(5))
# Pour visualiser si on a des valeurs aberrantes

parisiens = parisiens.drop([10879,1675,12166], axis=0).reset_index(drop = True)
parisiens_avec_prix = parisiens_avec_prix.drop([10879,1675,12166], axis=0).reset_index(drop = True)
#On retire les lignes des restaurants ayant des prix moyens aberrants, qui risquent de fausser nos graphiques

df = parisiens.groupby('Catégorie de prix').aggregate({'name':'count'}).reset_index()
df = df.rename(columns={'name': 'Nombre de restaurants'})
sns.catplot(x='Catégorie de prix', y='Nombre de restaurants', edgecolor="black", data=df,kind = "bar", color = "cyan")

parisiens.describe()
#Le prix moyen du restaurant Parisien est de 33.60€, avec un écart-type de 102.36€. Cela semble élevé, et peut s'expliquer par le fait qu'il y a beaucoup 
#de restaurants très chers parmi les restaurants dont on connaît le prix moyen dans notre base. Le prix médian, 22€ semble déjà plus raisonnable.

##Quelques tendances
        
#Moyenne de note globale par catégorie de prix
parisiens['Note Globale'] = parisiens['Note Globale'].str.replace(",", ".").astype(float)

df = parisiens.groupby('Catégorie de prix').aggregate({'Note Globale' : 'mean'}).reset_index()
df = df.rename(columns={'Note Globale': 'Note globale moyenne'})
sns.catplot(x='Catégorie de prix', y='Note globale moyenne', edgecolor="black", data=df,kind = "bar", color = "brown")

#Moyenne du nombre d'avis par catégorie de prix

df = parisiens.groupby('Catégorie de prix').aggregate({'Nombre avis' : 'mean'}).reset_index()
df = df.rename(columns={'Nombre avis': "Nombre moyen d'avis"})
sns.catplot(x='Catégorie de prix', y="Nombre moyen d'avis", edgecolor="black", data=df,kind = "bar", color = "yellow")

#Moyenne de note de cuisine par catégorie de prix

parisiens.groupby('Catégorie de prix').aggregate({'Note de cuisine' : 'mean'})

#Moyenne de note de service par catégorie de prix

parisiens.groupby('Catégorie de prix').aggregate({'Note de service' : 'mean'})

#Moyenne de note QP par catégorie de prix

parisiens.groupby('Catégorie de prix').aggregate({'Note qualité-prix' : 'mean'})

#Moyenne de note d'ambiance par catégorie de prix

parisiens.groupby('Catégorie de prix').aggregate({'Note ambiance' : 'mean'})

##On va prendre une catégorie de prix par une, et représenter le pourcentage de restaurants par arrondissement dans cette catégorie de prix

#On crée des DataFrames regroupant chaque catégorie de prix
parisiens_cheap = parisiens[parisiens['Catégorie de prix'] == 'faible'].reset_index(drop = True)
parisiens_average = parisiens[parisiens['Catégorie de prix'] == 'moyen'].reset_index(drop = True)
parisiens_expensive = parisiens[parisiens['Catégorie de prix'] == 'élevé'].reset_index(drop = True)

#On compte le nombre de restaurants par arrondissement
effectif_total_par_arr = parisiens.groupby('arr').aggregate({'arr' : 'count'})['arr']

#On importe une fonction qui nous permettra de choisir les graduations des axes dans nos graphes
from matplotlib.ticker import MultipleLocator


#On compte le nombre de restaurants "cheap" par arrondissement et on trace leur fréquence par arrondissement
effectif_cheap = parisiens_cheap.groupby('arr').aggregate({'arr' : 'count'})['arr']
#On compte par arrondissement le nombre de restaurants bon marché
arrondissements_cheap = range(1,21)

ax = plt.axes()
plt.xlabel("Arrondissement")
plt.ylabel("% de restaurants bon marché dans cet arrondissement")
ax.xaxis.set_major_locator(MultipleLocator(1)) 
#Sert à choisir une graduation de 1, afin de représenter clairement chaque arrondissement
plt.bar(arrondissements_cheap,effectif_cheap/effectif_total_par_arr, color = "#ABEBC6", 
                                                                     edgecolor="black",
                                                                     linewidth=1, 
                                                                     ecolor = "green",
                                                                     capsize = 10)

# Représentation du nombre de restaurants émeraudes par arrondissement 
df = parisiens.rename(columns = {'arr' : 'Arrondissement', 'nb_emeraudes' : 'Nombre de restaurants émeraudes'})
sns.catplot(x='Arrondissement', y='Nombre de restaurants émeraudes', edgecolor="black", data=df, kind = "bar", color = "cyan")

#Versions cartographiques de ces graphiques :

arrondissements = gpd.read_file("https://opendata.paris.fr/explore/dataset/arrondissements/download/?format=geojson&timezone=Europe/Berlin&lang=fr")
# Fond de carte des arrondissements parisiens trouvé sur internet
arrondissements['l_ar'] = arrondissements['l_ar'].str.extract('(\d+)').astype(int)
arrondissements = arrondissements.rename(columns = {'l_ar' : 'arr'})
# On recode la colonne 'l_ar' représentant l'arrondissement pour pouvoir faire une fusion avec notre
# base de données ensuite.

df = parisiens_cheap.groupby('arr').aggregate({'name' : 'count'}).reset_index()
# Par arrondissement, on compte le nombre de restaurants dans la base "cheap"
df2 = parisiens.groupby('arr').aggregate({'name' : 'count'}).reset_index()
# Par arrondissement, on compte le nombre de restaurants dans la base de données entière
df['name'] = df['name']/df2['name']
# Ici, df est donc un dataframe qui recense par arrondissement le pourcentage de restaurants chers

arrondissements.merge(df, how='inner').plot(column = 'name',
                                            legend = True, 
                                            legend_kwds={'label': "Pourcentage de restaurants bon marché par arrondissement", 
                                                         'orientation': "horizontal"})

df = parisiens.drop_duplicates(subset = ['arr'])
# On garde juste un restaurant par arrondissement pour avoir le nombre de restaurants émeraudes
# par arrondissement.

arrondissements.merge(df, how='inner').plot(column = 'nb_emeraudes',
                                            legend = True, 
                                            legend_kwds={'label': "Nombre de restaurants émeraudes par arrondissement", 
                                                         'orientation': "horizontal"})


#On compte le nombre de restaurants "average" par arrondissement et on trace leur fréquence par arrondissement
effectif_average = parisiens_average.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_average = range(1,21)

ax = plt.axes()
plt.xlabel("Arrondissement")
plt.ylabel("% de restaurants modérés dans cet arrondissement")
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_average,effectif_average/effectif_total_par_arr, color = "#F0B27A", 
                                                                         edgecolor="black",
                                                                         linewidth=1, 
                                                                         ecolor = "green",
                                                                         capsize = 10)

#On compte le nombre de restaurants "expensive" par arrondissement et on trace leur fréquence par arrondissement
effectif_expensive = parisiens_expensive.groupby('arr').aggregate({'arr' : 'count'})['arr']
arrondissements_expensive = range(1,21)

ax = plt.axes()
plt.xlabel("Arrondissement")
plt.ylabel("% de restaurants chers dans cet arrondissement")
ax.xaxis.set_major_locator(MultipleLocator(1))
plt.bar(arrondissements_expensive,effectif_expensive/effectif_total_par_arr, color = "#EC7063", 
                                                                             edgecolor="black",
                                                                             linewidth=1, 
                                                                             ecolor = "green",
                                                                             capsize = 10)

#Ce dernier graphique est semblable au graphique représentant le niveau de vie selon l'arrondissement : donc plus un arrondissement est riche, plus il a de restaurants chers

sns.catplot(x='arr', y='Niveau de vie Commune', edgecolor="black", data=parisiens, kind = "bar", color = "grey")

#Versions cartographiques de ces graphiques :

df = parisiens_expensive.groupby('arr').aggregate({'name' : 'count'}).reset_index()

df2 = parisiens.groupby('arr').aggregate({'name' : 'count'}).reset_index()
# Par arrondissement, on compte le nombre de restaurants dans la base de données entière
df['name'] = df['name']/df2['name']
# Ici, df est donc un dataframe qui recense par arrondissement le pourcentage de restaurants chers

# Par arrondissement on compte le nombre de restaurants dans la base "expensive"
arrondissements.merge(df, how='inner').plot(column = 'name',
                                            cmap='OrRd',
                                            legend = True, 
                                            legend_kwds={'label': "Pourcentage de restaurants chers par arrondissement", 
                                                         'orientation': "horizontal"})

df = parisiens.drop_duplicates(subset = ['arr'])
# On garde juste un restaurant par arrondissement pour avoir le niveau de vie par arrondissement.

arrondissements.merge(df, how='inner').plot(column = 'Niveau de vie Commune',
                                            cmap='OrRd',
                                            legend = True, 
                                            legend_kwds={'label': "Niveau de vie par arrondissement", 
                                                         'orientation': "horizontal"})

        
##Etude de la variable "Prix moyen" pour avoir les idées plus claires avec des prix en chiffres

#Etudions le prix moyen d'un restaurant par arrondissement

df = parisiens.groupby('arr').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'arr' : 'Arrondissement'})
sns.catplot(x='Arrondissement', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "pink")

#Traçons l'évolution du prix d'un restaurant en fonction de l'année de sa créaton

df = parisiens.groupby('foundingYear').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'foundingYear' : 'Année de création'})
sns.lineplot(x='Année de création', y='Prix moyen', data=df, color = "green")
#On choisit ici le lineplot pour représenter la continuité dans le temps

#Voyons le prix d'un restaurant selon le style de nourriture

df = parisiens.groupby('Style de nourriture').aggregate({'Prix moyen' : 'mean'}).reset_index()
g = sns.catplot(x='Style de nourriture', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "orange")
g.set_xticklabels(rotation=90) #Pour ne pas que les intitulés se chevauchent

#Les catégories suivantes ont été attribuées à tort à de nombreux restaurants : on refait le même graphique que le précédent mais sans ces catégories
df = parisiens[parisiens['Style de nourriture'] != 'Asiatique']
df = df[df['Style de nourriture'] != 'Japonaise']
df = df[df['Style de nourriture'] != 'Cantonaise']
df = df[df['Style de nourriture'] != 'Espagnole']
df = df.groupby('Style de nourriture').aggregate({'Prix moyen' : 'mean'}).reset_index()
g = sns.catplot(x='Style de nourriture', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "orange")
g.set_xticklabels(rotation=90) #Pour ne pas que les intitulés se chevauchent

#Comparons taille d'entreprise d'un restaurant et prix moyen du repas dans ce restaurant

df = parisiens.groupby('categorySize').aggregate({'Prix moyen' : 'mean'}).reset_index()
df = df.rename(columns = {'categorySize' : 'Taille du restaurant'})
sns.catplot(x='Taille du restaurant', y='Prix moyen', edgecolor="black", data=df, kind = "bar", color = "blue")

##On commente les coefficients de corrélation de plusieurs variables avec 'Prix moyen'

parisiens.corr()['Prix moyen'].reset_index()
#Les coefficients sont très petits mais leurs signes sont en accord avec les résultats tirés des graphiques précédents. 







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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 19:17:41 2020

@author: victorhuynh
"""

### But : obtenir les liens des pages TripAdvisor de plein de restaurants Parisiens

import urllib
from urllib import request
import bs4
import pandas as pd

#On prend l'URL de la page de recueil des restaurants Parisiens de TripAdvisor
url = 'https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html'
request_text = request.urlopen(url).read()
page = bs4.BeautifulSoup(request_text, "lxml")

#Les liens qui nous intéressent sont contenues dans les "divs" dont la classe est la suivante (parfois il faut ajouter un espace après "widget" pour que ça marche)
data = page.find_all('div', {"class":"react-container component-widget"})

#En visualisant le contenu de "data", on se rend compte que les liens sont contenus dans les "a" 
ls = data[2].contents[0].find_all('a')

#On récupère tous les liens 
restaurants_index = {i:  {'url': 'https://www.tripadvisor.fr' + ls[i]['href']} for i in range(len(ls))}

#Début de la création du DataFrame
data = {'Nom':  ['First value'],
        'Adresse': ['First value'],
        'Type de service': ['First value'],
        'Style de nourriture': ['First value'],
        'Note globale': ['First value'],
        'Catégorie de prix': ['First value'],
        'Fourchette de prix': ['First value'],
        'Note de cuisine': ['First value'],
        'Note de service': ['First value'],
        'Note qualité-prix': ['First value'],
        'Note ambiance': ['First value']}
df = pd.DataFrame (data, columns = ['Nom','Adresse','Type de service','Style de nourriture','Note globale','Catégorie de prix','Fourchette de prix','Note de cuisine','Note de service','Note qualité-prix','Note ambiance'])

#Pour chaque lien, on va récupérer les informations du restaurant associé
for i in range(0,len(restaurants_index)):
  url = restaurants_index[i]['url']
  request_text = request.urlopen(url).read()
  page = bs4.BeautifulSoup(request_text, "lxml")

  if page.find_all('div',{"id":"taplc_top_info_0"}) != []:
    nom = page.find_all('div',{"id":"taplc_top_info_0"})[0].find_all('h1')[0].contents
  else:
    nom = "Non renseigné"

  #Si ça ne marche pas, retirer l'espace après "'page'"
  if page.find_all('div',{'class':'page '}) != []:
    divs = page.find('div',{'class':'page '})
    infos = divs.find_all('a')
    adresse = infos[7].contents
    service = infos[5].contents
    style = infos[6].contents
    note = infos[1].contents[0]['title'][0:3]
    prix = infos[3].contents
  else:
    adresse = "Non renseigné"
    service = "Non renseigné"
    style = "Non renseigné"
    note = "Non renseigné"
    prix = "Non renseigné"

  if page.find_all('div',{"class":"_1XLfiSsv"}) != []:
    infos2 = page.find_all('div',{"class":"_1XLfiSsv"})
    fourchette_prix = infos2[0].contents[0]
  else:
    fourchette_prix = "Non renseigné"

  if page.find_all('span',{"class":"_377onWB-"}) != []:
    infos3 = page.find_all('span',{"class":"_377onWB-"})
    note_cuisine = int(infos3[0].contents[0]['class'][1][7:])/10
    note_service = int(infos3[1].contents[0]['class'][1][7:])/10
    note_QP = int(infos3[2].contents[0]['class'][1][7:])/10
  #Boucle "if" car pas tous les restaurants ont la note d'ambiance
    if len(infos3) == 4:
      note_ambiance = int(infos3[3].contents[0]['class'][1][7:])/10
    else:
      note_ambiance = "Non renseigné"
  else:
    note_cuisine = "Non renseigné"
    note_service = "Non renseigné"
    note_QP = "Non renseigné"
    note_ambiance = "Non renseigné"

  df = df.append({'Nom':  nom, 'Adresse': adresse, 'Type de service': service, 'Style de nourriture': style, 'Note globale': note, 'Catégorie de prix': prix, 'Fourchette de prix': fourchette_prix, 'Note de cuisine': note_cuisine, 'Note de service': note_service, 'Note qualité-prix': note_QP, 'Note ambiance': note_ambiance}, ignore_index=True)

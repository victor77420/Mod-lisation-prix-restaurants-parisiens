#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 20:14:33 2020

@author: victorhuynh
"""

### SCRAPPING DE LA NOTE ET DU PRIX A L'AIDE DE TRIPADVISOR

import urllib
from urllib import request
import bs4
import pandas as pd
import re

#"parisiens" désigne le dataframe des restaurants parisiens

i = 0
parisiens['Style de nourriture'] = 'Non renseigné'
parisiens['Note Globale'] = "Non renseigné"
parisiens['Catégorie de prix'] = "Non renseigné
parisiens['Fourchette de prix'] = "Non renseigné"
parisiens['Note de cuisine'] = "Non renseigné"
parisiens['Note de service'] = "Non renseigné"
parisiens['Note qualité-prix'] = "Non renseigné"
parisiens['Note ambiance'] = "Non renseigné"
parisiens['Nombre avis'] = "Non renseigné"

#Pour chaque lien, on va récupérer les informations du restaurant associé
for lien in parisiens['Lien TripAdvisor']:
  url = parisiens['Lien TripAdvisor'][i]
  request_text = request.urlopen(url).read()
  page = bs4.BeautifulSoup(request_text, "lxml")

  #Si ça ne marche pas, retirer l'espace après "'page'"
  if page.find_all('div',{'class':'page '}) != []:
    divs = page.find('div',{'class':'page '})
    infos = divs.find_all('a')
    parisiens['Style de nourriture'][i] = infos[6].contents
    parisiens['Note Globale'][i] = infos[1].contents[0]['title'][0:3]
    parisiens['Catégorie de prix'][i] = infos[3].contents

  if page.find_all('div',{"class":"_1XLfiSsv"}) != []:
    infos2 = page.find_all('div',{"class":"_1XLfiSsv"})
    parisiens['Fourchette de prix'][i] = infos2[0].contents[0]

  if page.find_all('span',{"class":"_377onWB-"}) != []:
    infos3 = page.find_all('span',{"class":"_377onWB-"})
    parisiens['Note de cuisine'][i] = int(infos3[0].contents[0]['class'][1][7:])/10
    parisiens['Note de service'][i] = int(infos3[1].contents[0]['class'][1][7:])/10
    parisiens['Note qualité-prix'][i] = int(infos3[2].contents[0]['class'][1][7:])/10
  #Boucle "if" car pas tous les restaurants ont la note d'ambiance
    if len(infos3) == 4:
      parisiens['Note ambiance'][i] = int(infos3[3].contents[0]['class'][1][7:])/10 
  i = i + 1
  
  if page.find('span',{"class":"_3Wub8auF"}) != []:
    parisiens['Nombre avis'][i] = re.sub("[^0-9]", "", page.find('span',{"class":"_3Wub8auF"}).text) #ça sert à ne garder que les chiffres

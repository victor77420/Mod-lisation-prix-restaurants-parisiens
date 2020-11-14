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

#On prend l'URL d'un restaurant sur tripadvisor

url = "https://www.tripadvisor.fr/Restaurant_Review-g187147-d6575305-Reviews-Il_Etait_Un_Square-Paris_Ile_de_France.html"
request_text = request.urlopen(url).read()
page = bs4.BeautifulSoup(request_text, "lxml")

#On extrait les informations sur ce restaurant

nom = page.find_all('div',{"id":"taplc_top_info_0"})[0].find_all('h1')[0].contents

#Si ça ne marche pas, retirer l'espace après "'page'"
divs = page.find('div',{'class':'page '})
infos = divs.find_all('a')
adresse = infos[7].contents
service = infos[5].contents
style = infos[6].contents
note = infos[1].contents[0]['title'][0:3]
prix = infos[3].contents

if page.find_all('div',{"class":"_1XLfiSsv"}) == []:
  infos2 = page.find_all('div',{"class":"_1XLfiSsv"})
  fourchette_prix = infos2[0].contents[0]
else:
  fourchette_prix = NaN

infos3 = page.find_all('span',{"class":"_377onWB-"})
note_cuisine = int(infos3[0].contents[0]['class'][1][7:])/10
note_service = int(infos3[1].contents[0]['class'][1][7:])/10
note_QP = int(infos3[2].contents[0]['class'][1][7:])/10
#Boucle "if" car pas tous les restaurants ont la note d'ambiance
if len(infos3) == 4:
  note_ambiance = int(infos3[3].contents[0]['class'][1][7:])/10
else:
  note_ambiance = NaN

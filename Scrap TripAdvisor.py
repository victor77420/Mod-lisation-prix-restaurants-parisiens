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

#On prend l'URL de la page de recueil des restaurants Parisiens de TripAdvisor
url = 'https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html'
request_text = request.urlopen(url).read()
page = bs4.BeautifulSoup(request_text, "lxml")

#Les liens qui nous intéressent sont contenues dans les "divs" dont la classe est la suivante (parfois il faut ajouter un espace après "widget" pour que ça marche):
data = page.find_all('div', {"class":"react-container component-widget"})

#En visualisant le contenu de "data", on se rend compte que les liens sont contenus dans les "a" :
ls = data[2].contents[0].find_all('a')

#On récupère tous les liens :
restaurants_index = {i:  {'url': 'https://www.tripadvisor.fr' + ls[i]['href']} for i in range(len(ls))}

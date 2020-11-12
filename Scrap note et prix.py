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

#On extrait la note moyenne sur 5 attribuée à ce restaurant, et la fourchette de prix estimée

note = page.find_all('div')[102].find_all('div')[11].find_all('svg')[0]['aria-label'][0:3]
prix = page.find_all('div')[102].find_all('span')[15].find_all('a')[0].contents[0]

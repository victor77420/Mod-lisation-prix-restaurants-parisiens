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
import re

url = 'https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html'
request_text = request.urlopen(url).read()
page = bs4.BeautifulSoup(request_text, "lxml")

data = page.find('script', text = re.compile('window.__WEB_CONTEXT__'))
#On obtient un "script" avec plein d'infos sur plein de restaurants dont les liens TripAdvisor, les noms... mais je ne sais pas comment les extraire 
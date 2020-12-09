#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 19:17:41 2020

@author: victorhuynh
"""

### But : obtenir les liens des pages TripAdvisor 

import pandas as pd

!pip install selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
!pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome(ChromeDriverManager().install())
query = 'test pour se débarrasser du cookie' 
browser.get('https://www.google.fr/')
search = browser.find_element_by_name('q')
search.send_keys(query)
search.send_keys(Keys.RETURN)
WebDriverWait(browser,15).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://consent.google.com']")))
WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='introAgreeButton']"))).click() 

for i in range(nombre_parisiens): 
    query = str(parisiens['name'][i]) + ' ' + 'restaurant paris tripadvisor' 
    browser.get('https://www.google.fr/')
    search = browser.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)
    try:
        browser.find_element(By.XPATH, '(//h3)[1]/../../a').click()
        parisiens['Lien TripAdvisor'][i] = browser.current_url 
        continue
    except NoSuchElementException:
        pass
    i = i + 1 #Je crois que cette ligne ne sert à rien
    
parisiens_test = pd.DataFrame.copy(parisiens) #J'ai créé des copies pour la jouer safe mais on pourra remplacer les tests par "parisien" à la fin
    
 #Certains restos ont eu comme lien le lien d'une review en particulier : le code suivant permet de trouver la page globale de ces restos
 for i in range(nombre_parisiens): 
    if "https://www.tripadvisor.fr/ShowUserReviews" in parisiens_test['Lien TripAdvisor'][i]:
        url = parisiens_test['Lien TripAdvisor'][i]
        request_text = request.urlopen(url).read()
        page = bs4.BeautifulSoup(request_text, "lxml")        
        if page.find_all('span',{'class':'altHeadInline'}) != []:
            span = page.find('span',{'class':'altHeadInline'})
            if span.find('a')['href'] != []:
                href = span.find('a')['href']
                parisiens_test['Lien TripAdvisor'][i] = 'https://www.tripadvisor.fr' + href

#On ne garde que les restaurants dont le lien est bien une page tripadvisor : on en a 14 000 environ
parisiens_test2 = parisiens_test[parisiens_test['Lien TripAdvisor'].str.contains('https://www.tripadvisor.fr/Restaurant_Review')].reset_index()

import urllib
from urllib import request
import bs4
import pandas as pd
import re

parisiens_test2['Style de nourriture'] = 'Non renseigné'
parisiens_test2['Note Globale'] = "Non renseigné"
parisiens_test2['Catégorie de prix'] = "Non renseigné"
parisiens_test2['Fourchette de prix'] = "Non renseigné"
parisiens_test2['Note de cuisine'] = "Non renseigné"
parisiens_test2['Note de service'] = "Non renseigné"
parisiens_test2['Note qualité-prix'] = "Non renseigné"
parisiens_test2['Note ambiance'] = "Non renseigné"
parisiens_test2['Nombre avis'] = "Non renseigné"

#Pour chaque lien, on va récupérer les informations du restaurant associé
for i in range(14830):
  url = parisiens_test2['Lien TripAdvisor'][i]
  request_text = request.urlopen(url).read()
  page = bs4.BeautifulSoup(request_text, "lxml")

  #Si ça ne marche pas, retirer l'espace après "'page'"
  if page.find_all('div',{'class':'page '}) != []:
    divs = page.find('div',{'class':'page '})
    infos = divs.find_all('a')
    parisiens_test2['Style de nourriture'][i] = infos[6].contents
    parisiens_test2['Note Globale'][i] = infos[1].contents[0]['title'][0:3]
    parisiens_test2['Catégorie de prix'][i] = infos[3].contents

  if page.find_all('div',{"class":"_1XLfiSsv"}) != []:
    infos2 = page.find_all('div',{"class":"_1XLfiSsv"})
    parisiens_test2['Fourchette de prix'][i] = infos2[0].contents[0]

  if page.find_all('span',{"class":"_377onWB-"}) != []:
    infos3 = page.find_all('span',{"class":"_377onWB-"})
    parisiens_test2['Note de cuisine'][i] = int(infos3[0].contents[0]['class'][1][7:])/10
    if len(infos3) == 2:
        parisiens_test2['Note de service'][i] = int(infos3[1].contents[0]['class'][1][7:])/10
    #Boucle "if" car pas tous les restaurants ont la note de qualité prix
    if len(infos3) == 3:
        parisiens_test2['Note qualité-prix'][i] = int(infos3[2].contents[0]['class'][1][7:])/10
    #Boucle "if" car pas tous les restaurants ont la note d'ambiance
    if len(infos3) == 4:
      parisiens_test2['Note ambiance'][i] = int(infos3[3].contents[0]['class'][1][7:])/10 
    
  if page.find('span',{"class":"_3Wub8auF"}) != []:
    parisiens_test2['Nombre avis'][i] = re.sub("[^0-9]", "", page.find('span',{"class":"_3Wub8auF"}).text) #ça sert à ne garder que les chiffres











#ON OUBLIE TEMPORAIREMENT CETTE PARTIE

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

#Il y a beaucoup de duplicates, il faut les supprimer
df_propre = df.loc[df.astype(str).drop_duplicates().index]
df_propre.reset_index()

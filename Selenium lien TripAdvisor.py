# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 10:43:22 2020

@author: VICTOR
"""

### But : à partir du nom du restaurant, trouver son lien TripAdvisor 

import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

query = 'naritake page tripadvisor' #Exemple avec le restaurant "Naritake"

browser = webdriver.Chrome('C:/Users/HUYNHKHAM VICTOR/Documents/Python Scripts/chromedriver.exe')
browser.get('https://www.google.fr/')

search = browser.find_element_by_name('q')
search.send_keys(query)
search.send_keys(Keys.RETURN)

WebDriverWait(browser,10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://consent.google.com']")))
WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='introAgreeButton']"))).click() 
    
browser.find_element(By.XPATH, '(//h3)[1]/../../a').click()
browser.current_url #On est censés obtenir le lien TripAdvisor du restaurant

# Exemple avec le capital social sur societe.com + pages jaunes

import bs4
from urllib import request
import selenium
import html5lib

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException


# récupération du capital social : 

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path="C:/Users/GUILLOT Robin/Documents/Robin Ensae/Matières/Python//chromedriver",options=chrome_options)

browser.get('https://www.societe.com/')

liste=["304305519","824490221","306332362","315946814","318906591","319947537","320228919","325621605"]    # on a pris pour l'exemple 8 numéros de siren de restaurants
capital_social=[]

cookie=browser.find_element_by_id("didomi-notice-agree-button").click()                                  # tous les cookies sont visibles par le motif"didomi-notice-agree-button"
                                                                                                         # on clique dessus pour le supprimer
for siren in tqdm(liste):
    
    search_bar = browser.find_element_by_id("input_search")                                             # on recherche sur la page la barre de recherche
    search_bar.send_keys(siren + Keys.ENTER)                                                            # on dit au webdriver de taper le siren du resto puis touche ENTRER
    
    try:
        browser.find_element_by_xpath("//p[@class = 'red' and contains (text(),'Aucune réponse pour cette recherche')]")    # ignorer cette partie( le try +except). Spécifique 
        capital_social.append('NaN')                                                                                        # à societe.com
        continue
        
    except NoSuchElementException:
        pass
        
    try:                                                                                                                   # làpar contre c'est impt : s'il ne trouve pas l'élément
        cap_soc = browser.find_element_by_id('capital-histo-description').text                                             # on lui dit de continuer normalement
        capital_social.append(cap_soc)
        
    except NoSuchElementException:
        capital_social.append('NaN')
            
              
        
print(capital_social)

browser.quit() 



# récupération du prix moyen sur pages jaunes : 

# série d'options pour notre webdriver comme navigation en mode privé, bloquer les pops ups et publicités (mais pas les cookies ...)
options = webdriver.ChromeOptions()
options.add_argument("private")
options.add_argument("--start-maximized");
options.add_argument("--ignore-certificate-errors");
options.add_argument("--disable-popup-blocking");
options.add_argument("--incognito");
options.add_argument("--headless");

browser = webdriver.Chrome(executable_path="C:/Users/GUILLOT Robin/Documents/Robin Ensae/Matières/Python//chromedriver",options=options)

browser.get('https://www.pagesjaunes.fr/activites')

cookie=browser.find_element_by_id("didomi-notice-agree-button").click()                      

# ici on récupère sur tous les resaturants parisiens (faire des boucles de 1000 à chaque fois)

prix_moy=[]


for k in tqdm(range(449,1000)):
    
    nom=parisiens.iloc[k].loc['legalName']
    code_post=parisiens.iloc[k].loc['postalCode']
    
    search_bar_une = browser.find_element_by_id("quoiqui")                                
    search_bar_une.send_keys(nom)
    
    search_bar_deux = browser.find_element_by_id("ou")
    search_bar_deux.send_keys(code_post + Keys.ENTER)
        
    try:
        sleep(0.5)
        donnee = browser.find_element_by_xpath("//div[@class = 'zone-cvi-cviv']/p[1]").text
        prix_moy_1.append(donnee)
        
    except NoSuchElementException:
        prix_moy_1.append('NaN')
        
    search_bar_une_nettoyee = browser.find_element_by_id("quoiqui").clear()
    search_bar_deux_nettoyee = browser.find_element_by_id("ou").clear()
        
            
              
print(prix_moy)

browser.quit() 

# on conserve en mémoire la liste obtenue en l'écrivant dans un fichier de notre ordi : 

fichier=open("C:/Users/GUILLOT Robin/Documents/Robin Ensae/Matières/Python/Données/prix_moyen_449_1000.txt","w")     # indiquer le chemin du fichier et le nommer
fichier.write(str(s))                                                                                             # prix_moy_x_y_.txt où x et y sont les 
fichier.close()                                                                                                   # positions extremes des restos qu' on a scrappé

# On relance la boucle précédente en faisant sur les restos de 1000 à 1500 etc...

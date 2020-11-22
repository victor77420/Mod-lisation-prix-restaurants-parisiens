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

browser.find_element(By.XPATH, '(//h3)[1]/../../a').click()
browser.current_url #On est censés optenir le lien TripAdvisor du restaurant
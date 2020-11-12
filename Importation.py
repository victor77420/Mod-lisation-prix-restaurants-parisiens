#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 20:49:25 2020

@author: victorhuynh
"""

import pandas as pd
!pip install geopandas
import geopandas as gpd

### On importe un fichier de données pré-existant sur les commerces à Paris

df = gpd.read_file('/Users/victorhuynh/Documents/ENSAE/ENSAE 2A/2A S1/PDS/COMMERCE_RESTAURATION_HOTELLERIE.csv')

#On garde uniquement les restaurants

restaurants = df[df['LIBACT'].str.contains('Restaurant')==True]
restaurants = restaurants.reset_index()
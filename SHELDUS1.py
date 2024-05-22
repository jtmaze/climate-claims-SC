#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:54:29 2024

@author: jmaze
"""

# %% 1. Libraries and directories

import pandas as pd
import geopandas as gpd

# %% 2. Read and format SHELDUS

claims = pd.read_csv('./project_data/SC-claimsA.csv', index_col = False)

print(f'{len(claims)} total claims in South Carolina between 1960 and 2022')

claims.drop(columns = ['StateName', 'Fatalities', 'FatalitiesDuration', 'FatalitiesPerCapita'], inplace = True)

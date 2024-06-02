#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 19:00:32 2024

@author: jmaze
"""

# %% 1.0 Libraries and directories

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

from scipy.optimize import curve_fit

os.chdir("/Users/jmaze/Documents/geog590/")

#Read claims data
claims_v2 = pd.read_csv('./project_data/claims_v2.csv')

# %% 2.0 Model RI for Total Annual Storm Damages

storms = claims_v2[claims_v2['hazard_broad'] == 'GeneralStorm'].copy()
#storms = claims_v2.copy()

storms.loc[:, 'property_dmg'] = storms['PropertyDmg(ADJ)'] / 1e6 

storms_years = storms.groupby('Year').agg(
    total_annual_dmg=('property_dmg', 'sum')
).reset_index()

storms_years['rank'] = storms_years['total_annual_dmg'].rank(ascending=False).astype(int)

# Calculate the Return Period = (n+1/m)
def calc_ri(dataframe, year_col, damage_col):
    df = dataframe.copy()
    
    # Rank the years based on the damage column in descending order
    df['rank'] = df[damage_col].rank(ascending=False).astype(int)
    
    # Calculate the number of years in the record
    record_yrs = df[year_col].max() - df[year_col].min()

    # Define the function to calculate Return Interval (RI)
    def ri_calc(row):
        rank = row['rank']
        ri = (record_yrs + 1) / rank
        return ri

    # Apply the function to each row
    df['RI'] = df.apply(ri_calc, axis=1)
    
    return df

    
storms_years = calc_ri(storms_years, 'Year', 'total_annual_dmg')

# %% 2.1 Log fit to t

modeling_domain = np.linspace(1, 100, num=1000)

def log_func(x, a, b):
    return a * np.log(x) + b


def ri_model_fitting(df, ri_col, dmg_col):
    
    model = curve_fit(log_func, df[ri_col], df[dmg_col])
    params = model[0]
    covariance = model[1]

    a_fit, b_fit = params
    
    model_dmg = log_func(modeling_domain, params[0], params[1])
    
    return model_dmg

curve = ri_model_fitting(storms_years, 'RI', 'total_annual_dmg')

plt.scatter(storms_years['RI'], storms_years['total_annual_dmg'], label='Data', color='navy')

# Plot the fitted log curve
plt.plot(modeling_domain, curve, label='Fitted Curve', color='orange')
plt.xlabel('Recurrance Interval (Years)')
plt.ylabel('Inflation adjusted damages ($Million 2022 dollars)', size = 8)
plt.legend(loc='lower right')
plt.show()

# %% 5.0 Model the RI for Per Capita Storm Damages

storms_years_percap = storms.groupby('Year').agg(
    annual_dmg_percap=('PropertyDmgPerCapita', 'sum')
).reset_index()

storms_years_percap = calc_ri(storms_years_percap, 'Year', 'annual_dmg_percap')

curve = ri_model_fitting(storms_years_percap, 'RI', 'annual_dmg_percap')

plt.scatter(storms_years_percap['RI'], storms_years_percap['annual_dmg_percap'], label='Data', color='navy')
plt.plot(modeling_domain, curve, label='Fitted Curve', color='orange')
plt.xlabel('Recurrance Interval (Years)')
plt.ylabel('Per-capita inflation ajusted damages ($)')
plt.legend(loc='lower right')

# %% Evaluate whether inflation adjusted per-capita damages change over time.

modeling_domain = np.linspace(1, 50, num=1000)

early = storms_years_percap[storms_years_percap['Year'] < 1991]
early = early[early['Year'] != 1984]
early = calc_ri(early, 'Year', 'annual_dmg_percap')
curve_early = ri_model_fitting(early, 'RI', 'annual_dmg_percap')

late = storms_years_percap[storms_years_percap['Year'] >= 1991]
late = calc_ri(late, 'Year', 'annual_dmg_percap')
curve_late = ri_model_fitting(late, 'RI', 'annual_dmg_percap')

plt.plot(modeling_domain, curve_early, label='1960-1991', color ='skyblue')
plt.plot(modeling_domain, curve_late, label='1991-2022', color='red')
plt.scatter(early['RI'], early['annual_dmg_percap'], label='Early Data', color='navy')
plt.scatter(late['RI'], late['annual_dmg_percap'], label='Late Data', color='maroon')

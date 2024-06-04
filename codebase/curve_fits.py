#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 19:00:32 2024

@author: jmaze
"""

# %% 1.0 Libraries and directories

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

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

modeling_domain = np.linspace(1, 100, num=1000)

# Log 10 fits much better than numpy's ln() default
def log_func(x, a, b):
    return a * np.log10(x) + b


def ri_model_fitting(df, ri_col, dmg_col):
    model = curve_fit(log_func, df[ri_col].copy(), df[dmg_col].copy())
    params = model[0]
    covariance = model[1]

    a_fit, b_fit = params
    
    model_dmg = log_func(modeling_domain, params[0], params[1])
    
    print(f'covariance = {covariance}')
    print(f'a = {a_fit:.2f} and b = {b_fit:.2f}')
    
    return params, covariance, model_dmg

params, covariance, curve = ri_model_fitting(storms_years, 'RI', 'total_annual_dmg')

# %% 2.1 Visualize RI for Total Annual Storm Damages

a_err = np.sqrt(covariance[0, 0])
b_err = np.sqrt(covariance[1, 1])

# Delta value corresponds to a two z-score
delta = 1.96 * np.sqrt((a_err * np.log(modeling_domain))**2 + b_err**2)

lower_bound = curve - delta
upper_bound = curve + delta

plt.figure(figsize=(8, 10))
plt.scatter(storms_years['RI'], storms_years['total_annual_dmg'], label='Data', color='navy', edgecolor='black')

# Plot the fitted log curve
plt.plot(modeling_domain, curve, label='Fitted Curve', color='orange')
plt.fill_between(modeling_domain, lower_bound, upper_bound, color='orange', alpha=0.25, label='95% CI')
plt.xlabel('Recurrance Interval (Years)', size=16)
plt.ylabel('Storm Damages (Millions of Dollars)', size=16)
plt.legend(loc='lower right')
plt.show()

# %% 2.2 Explore the residuals for Total Annual Storm Damages Model

storms_years['fitted'] = log_func(storms_years['RI'], params[0], params[1])
storms_years['residual'] = np.log10(storms_years['total_annual_dmg']) - np.log10(storms_years['fitted'])

plt.figure(figsize=(8, 10))
# Residuals are really bizare for low RI storms
df_temp = storms_years[storms_years['RI'] > 1.5]
plt.scatter(df_temp['RI'], df_temp['residual'], color='red', edgecolors='black')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.xlim(0, 100)
plt.xlabel('Recurrence Interval (Years)', size=16)
plt.ylabel('Log10 of Residuals', size=16)
plt.show()

# %% 2.3 Evaluate Poisson Distrubution for loss thresholds

poisson_lambdas = []

thresholds = [25, 50, 100, 150]

for value in thresholds:
           
    modeled_RI = 10 ** ((value - params[1]) / params[0])
    modeled100_frequency = 100 / modeled_RI
    poisson_lambdas.append((value, modeled100_frequency))
    
    print(modeled100_frequency)
    
results = []

for i in poisson_lambdas:
    lambda_value = i[1]
    threshold = i[0]
    
    k_values = range(1, 50)
    for k in k_values:
    
        P = ((lambda_value ** k) * math.exp(-lambda_value)) / math.factorial(k)
    
        results.append({'threshold': threshold, 
                        'Lambda': lambda_value, 
                        'k': k, 
                        'P': P
                        })

poission_df = pd.DataFrame(results)

plt.figure(figsize=(10, 6))

# Define a color map
colors = plt.cm.YlOrRd(np.linspace(0.25, 1, len(thresholds)))

for idx, threshold in enumerate(thresholds):
    subset = poission_df[poission_df['threshold'] == threshold]
    plt.plot(subset['k'], 
             subset['P'], 
             marker='o', 
             label=f'${threshold} Million Annual Losses', 
             color=colors[idx],
             markersize = 5,
             markeredgecolor='black')

plt.title('Poisson Probability vs k for Different Thresholds')
plt.xlabel('Number of excedences / 100 years')
plt.ylabel('Poisson Probability (P)')
plt.legend(title='Threshold')
plt.show()
    
# %% 3.0 Model the RI for Per Capita Storm Damages
modeling_domain = np.linspace(1, 100, num=1000)

storms_years_percap = storms.groupby('Year').agg(
    annual_dmg_percap=('PropertyDmgPerCapita', 'sum')
).reset_index()

storms_years_percap = calc_ri(storms_years_percap, 'Year', 'annual_dmg_percap')

params, covariance, curve = ri_model_fitting(storms_years_percap, 'RI', 'annual_dmg_percap')

plt.scatter(storms_years_percap['RI'], storms_years_percap['annual_dmg_percap'], label='Data', color='navy')
plt.plot(modeling_domain, curve, label='Fitted Curve', color='orange')
plt.xlabel('Recurrance Interval (Years)')
plt.ylabel('Per-capita inflation ajusted damages ($)')
plt.legend(loc='lower right')

# %% 4.0 Evaluate whether inflation adjusted per-capita damages change over time.

modeling_domain = np.linspace(1, 50, num=1000)

early = storms_years_percap[storms_years_percap['Year'] < 1991]
#early = early[early['Year'] != 1984]
early = calc_ri(early, 'Year', 'annual_dmg_percap')
params_early, covariance_early, curve_early = ri_model_fitting(early, 'RI', 'annual_dmg_percap')

late = storms_years_percap[storms_years_percap['Year'] >= 1991]
late = calc_ri(late, 'Year', 'annual_dmg_percap')
params_late, covariance_late, curve_late = ri_model_fitting(late, 'RI', 'annual_dmg_percap')

plt.plot(modeling_domain, curve_early, label='pre-1991 model', color ='skyblue')
plt.plot(modeling_domain, curve_late, label='post-1991 model', color='orangered')
plt.scatter(early['RI'], early['annual_dmg_percap'], label='Pre-1991 data', color='blue')
plt.scatter(late['RI'], late['annual_dmg_percap'], label='Post-1991 data', color='orangered')
plt.xlabel('Return Interval')
plt.ylabel('Per-capita inflation adjusted claims ($)')
plt.legend(loc='lower right')

# %% 4.1 Remove the outlier value from 1984

modeling_domain = np.linspace(1, 50, num=1000)

storms_comp = storms_years_percap[storms_years_percap['Year'] != 1984]

early = storms_comp[storms_comp['Year'] < 1991]
early = calc_ri(early, 'Year', 'annual_dmg_percap')
params_early, covariance_early, curve_early = ri_model_fitting(early, 'RI', 'annual_dmg_percap')

late = storms_comp[storms_comp['Year'] >= 1991]
late = calc_ri(late, 'Year', 'annual_dmg_percap')
params_late, covariance_late, curve_late = ri_model_fitting(late, 'RI', 'annual_dmg_percap')

plt.plot(modeling_domain, curve_early, label='pre-1991 model', color ='skyblue')
plt.plot(modeling_domain, curve_late, label='post-1991 model', color='orangered')
plt.scatter(early['RI'], early['annual_dmg_percap'], label='Pre-1991 data', color='blue')
plt.scatter(late['RI'], late['annual_dmg_percap'], label='Post-1991 data', color='orangered')
plt.xlabel('Return Interval')
plt.ylabel('Per-capita inflation adjusted claims ($)')
plt.legend(loc='lower right')

# %% 4.2 Create early Poisson Dataframe

poisson_lambdas = []

thresholds = [250, 500, 750]

for value in thresholds:
           
    modeled_RI = 10 ** ((value - params_early[1]) / params_early[0])
    modeled50_frequency = 50 / modeled_RI
    poisson_lambdas.append((value, modeled50_frequency))
    
    #print(modeled50_frequency)
    
results = []

for i in poisson_lambdas:
    lambda_value = i[1]
    threshold = i[0]
    
    k_values = range(1, 50)
    for k in k_values:
    
        P = ((lambda_value ** k) * math.exp(-lambda_value)) / math.factorial(k)
    
        results.append({'threshold': threshold, 
                        'Lambda': lambda_value, 
                        'k': k, 
                        'P': P
                        })

poission_df_early = pd.DataFrame(results)


# %% 4.3 Create late Poisson Dataframe

poisson_lambdas = []

thresholds = [250, 500, 750]

for value in thresholds:
           
    modeled_RI = 10 ** ((value - params_late[1]) / params_late[0])
    modeled50_frequency = 50 / modeled_RI
    poisson_lambdas.append((value, modeled50_frequency))
 
results = []

for i in poisson_lambdas:
    lambda_value = i[1]
    threshold = i[0]
    
    k_values = range(1, 50)
    for k in k_values:
    
        P = ((lambda_value ** k) * math.exp(-lambda_value)) / math.factorial(k)
    
        results.append({'threshold': threshold, 
                        'Lambda': lambda_value, 
                        'k': k, 
                        'P': P
                        })

poission_df_late = pd.DataFrame(results)

# %% 4.4 Plot and compare PMF functions for pre and post:

fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(8, 6))

# Define color maps correctly
colors_early = plt.cm.Wistia(np.linspace(0, 1, len(thresholds)))
colors_late = plt.cm.Wistia(np.linspace(0, 1, len(thresholds)))

for idx, threshold in enumerate(thresholds):
    subset_early = poission_df_early[poission_df_early['threshold'] == threshold]
    axs[0].plot(subset_early['k'], 
                subset_early['P'], 
                marker='o', 
                label=f'${threshold} Losses', 
                color=colors_early[idx],
                markersize=5,
                markeredgecolor='black')

for idx, threshold in enumerate(thresholds):
    subset_late = poission_df_late[poission_df_late['threshold'] == threshold]
    axs[1].plot(subset_late['k'], 
                subset_late['P'], 
                marker='o', 
                label=f'${threshold} Losses', 
                color=colors_late[idx],
                markersize=5,
                markeredgecolor='black')

# Adding a legend to each subplot
axs[0].legend(title='Threshold (Early)')
axs[1].legend(title='Threshold (Late)')


plt.tight_layout()
plt.show()






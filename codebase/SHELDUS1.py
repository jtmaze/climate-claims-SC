#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:54:29 2024

@author: jmaze
"""

# %% 1.0 Libraries and directories

import pandas as pd
import numpy as np
import os
import geopandas as gpd
import matplotlib.pyplot as plt


os.chdir("/Users/jmaze/Documents/geog590/")

# %% 2.0 Read and format SHELDUS

claims = pd.read_csv('./project_data/SC-claimsA.csv', index_col=False)

# Drop columns which we aren't using
drop_cols = [
    'StateName', 'Fatalities', 'FatalitiesDuration', 'FatalitiesPerCapita', 
    'Glide', 'Injuries', 'InjuriesDuration', 'InjuriesPerCapita', 'PropertyDmgDuration'
]

claims.drop(columns=drop_cols, inplace=True)

# Some of the column names have bad syntax
claims.rename(columns={' Hazard': 'Hazard', ' CountyName': 'CountyName'}, inplace=True)

# For the purpose of this project we'll ignore landslides. Those are predominately 
# geologic, not climate. 
claims = claims[claims['Hazard'] != 'Landslide']

# Some claims amounts are $0, this is useless for many analyses
claims = claims[claims['PropertyDmg(ADJ)'] > 0]

claims.head()

# %% 3.0 Explore the data

hazard_types = claims['Hazard'].unique().tolist()
event_names = claims['EventName'].unique().tolist()
total_dollars = claims['PropertyDmg(ADJ)'].sum()

worst_events = claims.groupby('EventName').agg({
    'PropertyDmg(ADJ)': 'sum'
})

worst_events['percent_all_claims_dollars'] = (
    worst_events['PropertyDmg(ADJ)'] / total_dollars * 100
)

worst_events['millions_dollars'] = worst_events['PropertyDmg(ADJ)'] / 1e6

worst_events.sort_values(
    by='percent_all_claims_dollars', 
    ascending=False, 
    inplace=True
)

worst_events = worst_events.drop(columns=['PropertyDmg(ADJ)'])

worst_events.round(2).head()


# %% 4.0 Plot the claims timeseries

df = claims.groupby('Year').agg({
    'PropertyDmg(ADJ)': 'sum',
    'Year': 'first'})

plt.figure(figsize=(10, 6))
plt.fill_between(df['Year'], df['PropertyDmg(ADJ)']/1e6, color='skyblue', alpha=0.4)
plt.plot(df['Year'], df['PropertyDmg(ADJ)']/1e6, color='Slateblue', alpha=0.6)
plt.title("South Carolina Insurance Claims 1960-2022 (All disasters)")
plt.xlabel("Year")
plt.ylabel("Claims Millions of Dollars")
plt.show()

# %% 4.1 Exclude Hurricane Hugo's impact

claims2 = claims[claims['EventName'] != "Hurricane 1989 Hugo"]

df2 = claims2.groupby('Year').agg({
    'PropertyDmg(ADJ)': 'sum',
    'Year': 'first'})

claims3 = claims[(claims['EventName'] != "Hurricane 1989 Hugo") & (claims['EventName'] != "Drought/Heatwave 1993 Southeast")]
df3 = claims3.groupby('Year').agg({
    'PropertyDmg(ADJ)': 'sum',
    'Year': 'first'})

fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 8))

#First panel Includes Hugo
axs[0].fill_between(df['Year'], df['PropertyDmg(ADJ)']/1e6, color='skyblue', alpha=0.4, label='Hurricane Hugo')
axs[0].plot(df['Year'], df['PropertyDmg(ADJ)']/1e6, color='Slateblue', alpha=0.6)
axs[0].fill_between(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='orange', alpha=0.4, label='1993 Drought')
axs[0].plot(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='red', alpha=0.8)
axs[0].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='lightgreen', alpha=0.7, label='All other disasters')
axs[0].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='darkgreen', alpha=1)
axs[0].set_title("All Events (Showing impact of Hurricane Hugo)")
axs[0].legend()


# Second panel doesn't include Hugo
axs[1].fill_between(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='orange', alpha=0.4)
axs[1].plot(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='red', alpha=0.8)
axs[1].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='lightgreen', alpha=0.7)
axs[1].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='darkgreen', alpha=1)
axs[1].set_title("Excluding Hurricane Hugo but including 1993 Drought")

# Third panel doesn't include Hugo or 1993 Drought
axs[2].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='lightgreen', alpha=0.7)
axs[2].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='darkgreen', alpha=1)
axs[2].set_title("Excluding 1993 Drought & Hurricane Hugo")

#fig.supxlabel('Year', fontsize=16)
fig.supylabel('Claims (Millions of Dollars)', fontsize=16)

plt.tight_layout()
plt.show()

# %% 5.0 Recatagorize the Hazard types 69 is too many

claims_noHugo = claims2.copy()

def hazard_broad_reclass(hazard):
    if 'Winter Weather' in hazard:
        return "WinterWeather"
    
    if 'Heat' in hazard or 'Drought' in hazard or 'Wildfire' in hazard:
        return "Drought/Heat/Wildfire"
    
    if 'Hurricane' in hazard or 'Tropical Storm' in hazard:
        return "Hurricane/TropicalStorm"
    
    if ('Tornado' in hazard or 
        'Severe Storm' in hazard or 
        'Thunder Storm' in hazard or 
        'Hail' in hazard or
        'Wind' in hazard or
        'Flooding' in hazard or
        'Lightning' in hazard): 
        return "GeneralStorm"
    
    else:
        return "Unclassified"


claims_noHugo['hazard_broad'] = claims_noHugo['Hazard'].apply(hazard_broad_reclass)

# Check to ensure reclass as expected. 
reclass = claims_noHugo[['Hazard', 'hazard_broad']].drop_duplicates()

# See how many $ are unclassified
unclass_claims = claims_noHugo['PropertyDmg(ADJ)'][claims_noHugo['hazard_broad'] == 'Unclassified'].sum()
unclass_perc = unclass_claims/total_dollars * 100

# %% 6.0 Plot the distributions of disasters.

winter_weather = claims_noHugo[claims_noHugo['hazard_broad'] == 'WinterWeather'].copy()
drought_heat_wildfire = claims_noHugo[claims_noHugo['hazard_broad'] == 'Drought/Heat/Wildfire'].copy()
hurricanes = claims_noHugo[claims_noHugo['hazard_broad'] == "Hurricane/TropicalStorm"].copy()
generalstorms = claims_noHugo[claims_noHugo['hazard_broad'] == "GeneralStorm"].copy()


fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,10))

colors = ['cyan', 'orange', 'blue', 'green']

axs[0, 0].hist(winter_weather['PropertyDmg(ADJ)']/1e6, bins=15, alpha = 0.7, color=colors[0], edgecolor='black')
axs[0, 0].set_yscale('log')
axs[0, 0].set_title('Winter Weather Damages')

axs[0, 1].hist(drought_heat_wildfire['PropertyDmg(ADJ)']/1e6, bins=40, alpha = 0.7, color=colors[1], edgecolor='black')
axs[0, 1].set_yscale('log')
axs[0, 1].set_title('Drought, Heat & Wildfire Damages')

axs[1, 0].hist(hurricanes['PropertyDmg(ADJ)']/1e6, bins=50, alpha = 0.7, color=colors[2], edgecolor='black')
axs[1, 0].set_yscale('log')
axs[1, 0].set_title('Hurricane and Tropical Storm Damages')

axs[1, 1].hist(generalstorms['PropertyDmg(ADJ)']/1e6, bins=70, alpha = 0.7, color=colors[3], edgecolor='black')
axs[1, 1].set_yscale('log')
axs[1, 1].set_title('General Storms Damages')

x_limits = [0, max(claims_noHugo['PropertyDmg(ADJ)']) / 1e6]
for ax in axs.flat:
    ax.set_xlim(x_limits)
    
fig.supxlabel('Claim Amount (Millions of Dollars)')
fig.supylabel('Occurances of claims (log scale)')

plt.tight_layout()
plt.show()

# %% 6.1 Will the plots look better if the x-axis is rescaled log?

winter_weather['adj_dmg_log10'] = np.log10(winter_weather['PropertyDmg(ADJ)'])
drought_heat_wildfire['adj_dmg_log10'] = np.log10(drought_heat_wildfire['PropertyDmg(ADJ)'])
hurricanes['adj_dmg_log10'] = np.log10(hurricanes['PropertyDmg(ADJ)'])
generalstorms['adj_dmg_log10'] = np.log10(generalstorms['PropertyDmg(ADJ)'])

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,10))

colors = ['cyan', 'orange', 'blue', 'green']

axs[0, 0].hist(winter_weather['adj_dmg_log10'], bins=15, alpha = 0.7, color=colors[0], edgecolor='black')
#axs[0, 0].set_yscale('log')
axs[0, 0].set_title('Winter Weather Damages')

axs[0, 1].hist(drought_heat_wildfire['adj_dmg_log10'], bins=40, alpha = 0.7, color=colors[1], edgecolor='black')
#axs[0, 1].set_yscale('log')
axs[0, 1].set_title('Drought, Heat & Wildfire Damages')

axs[1, 0].hist(hurricanes['adj_dmg_log10'], bins=50, alpha = 0.7, color=colors[2], edgecolor='black')
#axs[1, 0].set_yscale('log')
axs[1, 0].set_title('Hurricane and Tropical Storm Damages')

axs[1, 1].hist(generalstorms['adj_dmg_log10'], bins=70, alpha = 0.7, color=colors[3], edgecolor='black')
#axs[1, 1].set_yscale('log')
axs[1, 1].set_title('General Storms Damages')
    
fig.supxlabel('Claim Amount (Millions of Dollars)')
fig.supylabel('Occurances of claims (log scale)')

plt.tight_layout()
plt.show()

# %% Some other stuff






















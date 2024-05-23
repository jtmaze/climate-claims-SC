#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:54:29 2024

@author: jmaze
"""

# %% 1.0 Libraries and directories

import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt

# %% 2.0 Read and format SHELDUS

claims = pd.read_csv('./project_data/SC-claimsA.csv', index_col=False)

# Drop columns which we aren't using
drop_cols = [
    'StateName', 'Fatalities', 'FatalitiesDuration', 'FatalitiesPerCapita', 
    'Glide', 'Injuries', 'InjuriesDuration', 'InjuriesPerCapita', 'PropertyDmgDuration'
]


claims.drop(columns=drop_cols, inplace=True)
# Some of the column names have bad syntax
claims.rename(columns={' Hazard': 'Hazard'}, inplace=True)

claims.head()

# %% 3.0 Explore the data

hazard_types = claims['Hazard'].unique().tolist()
event_names = claims['EventName'].unique().tolist()
total_dollars = claims['PropertyDmg(ADJ)'].sum()

worst_events = claims.groupby('EventName').agg({
    'PropertyDmg(ADJ)': 'sum'})

worst_events['percent_all_claims_dollars'] = worst_events['PropertyDmg(ADJ)']/total_dollars * 100
worst_events.sort_values(by='percent_all_claims_dollars', ascending=False, inplace=True)

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
axs[0].fill_between(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='lightgreen', alpha=0.4, label='1993 Drought')
axs[0].plot(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='darkgreen', alpha=0.8)
axs[0].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='orange', alpha=0.7, label='All other disasters')
axs[0].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='red', alpha=1)
axs[0].set_title("All Events (Showing impact of Hurricane Hugo)")
axs[0].legend()


# Second panel doesn't include Hugo
axs[1].fill_between(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='lightgreen', alpha=0.4)
axs[1].plot(df2['Year'], df2['PropertyDmg(ADJ)']/1e6, color='darkgreen', alpha=0.8)
axs[1].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='orange', alpha=0.7)
axs[1].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='red', alpha=1)
axs[1].set_title("Excluding Hurricane Hugo but including 1993 Drought")

# Third panel doesn't include Hugo or 1993 Drought
axs[2].fill_between(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='orange', alpha=0.7)
axs[2].plot(df3['Year'], df3['PropertyDmg(ADJ)']/1e6, color='red', alpha=1)
axs[2].set_title("Excluding 1993 Drought & Hurricane Hugo")

#fig.supxlabel('Year', fontsize=16)
fig.supylabel('Claims (Millions of Dollars)', fontsize=16)

plt.tight_layout()
plt.show()

# %% Plot the distribution of claims data

plt.figure(figsize=(10, 6))
plt.hist(temp['PropertyDmg(ADJ)']/1e6, bins=100, edgecolor='black')
plt.yscale('log')
plt.ylabel('Number of Claims (log scale)')
plt.xlabel('Claim Amount (Millions of Dollars)')
plt.show()



























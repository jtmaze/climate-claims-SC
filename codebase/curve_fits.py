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

os.chdir("/Users/jmaze/Documents/geog590/")

# %% 2.0 Read claims data

claims_v2 = pd.read_csv('./project_data/claims_v2.csv')
storms = claims_v2[claims_v2['hazard_broad'] == 'GeneralStorm']
#storms = claims_v2.copy()

storms_dates = storms.groupby(['StartDate', 'EndDate']).agg(
    total_cnty_dmg=('PropertyDmg(ADJ)', 'sum'), 
    num_counties=('CountyName', 'nunique'),
    counties_list=('CountyName', lambda x: x.unique().tolist())
).reset_index()

storms_dates['total_cnty_dmg'] = storms_dates['total_cnty_dmg'] / 1e6


# %% 3.0

# Convert 'StartDate' to datetime
storms_dates['StartDate'] = pd.to_datetime(storms_dates['StartDate'])

# Filter the data
storms_early = storms_dates[storms_dates['StartDate'] < '1991-01-01']
storms_late = storms_dates[storms_dates['StartDate'] > '1991-01-01']

# Create subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))  # Adjust figsize for better spacing

# Plot histogram for storms_early
ax1.hist(storms_early['total_cnty_dmg'], bins=40, edgecolor='black')
ax1.set_yscale('log')
ax1.set_title('Storms Before 1991')

# Plot histogram for storms_late
ax2.hist(storms_late['total_cnty_dmg'], bins=40, color='orange', edgecolor='black')
ax2.set_yscale('log')
ax2.set_title('Storms After 1991')

plt.tight_layout()
plt.show()

# %% 4.0 Try curve fitting

# Fit a Log-Normal distribution to the data
shape, loc, scale = stats.lognorm.fit(storms_dates['total_cnty_dmg'], floc=0)
print(f"Fitted parameters: shape={shape}, loc={loc}, scale={scale}")

# Generate a range of values over which to evaluate the PDF
x = np.linspace(storms_dates['total_cnty_dmg'].min() + 0.25, storms_dates['total_cnty_dmg'].max(), 1000)
fitted_pdf = stats.lognorm.pdf(x, shape, loc, scale)

# %% 5.0

fig, ax = plt.subplots(figsize=(8, 8))

hist_data, bins, _ = plt.hist(storms_dates['total_cnty_dmg'], bins=50, edgecolor='black', density=False)

# Calculate the bin width
bin_width = bins[1] - bins[0]

# Scale the PDF by the number of data points and the bin width
scaled_pdf = fitted_pdf * len(storms_dates['total_cnty_dmg']) * bin_width

# Plot the scaled PDF
ax.plot(x, scaled_pdf, 'r-', lw=2, label='Fitted Log-Normal PDF')


# Set y-axis to logarithmic scale (uncomment if needed)
ax.set_yscale('log')



plt.show()

# %%

# Fit a Gamma distribution to the data
alpha, loc, beta = stats.gamma.fit(storms_dates['total_cnty_dmg'], floc=0)
print(f"Fitted parameters: alpha={alpha}, loc={loc}, beta={beta}")

# Generate a range of values over which to evaluate the PDF
x = np.linspace(storms_dates['total_cnty_dmg'].min(), storms_dates['total_cnty_dmg'].max(), 1000)
fitted_pdf = stats.gamma.pdf(x, alpha, loc, beta)

# Plot the histogram of the data
plt.hist(storms_dates['total_cnty_dmg'], bins=50, edgecolor='black', density=True, alpha=0.6)

# Plot the fitted Gamma PDF
plt.plot(x, fitted_pdf, 'r-', lw=2, label='Fitted Gamma PDF')

# Set y-axis to logarithmic scale (uncomment if needed)
# plt.yscale('log')

plt.xlabel('Total County Damage')
plt.ylabel('Density')
plt.yscale('log')
plt.title('Fitting a Gamma Distribution')
plt.legend()
plt.show()

# %%


# Assuming storms_dates['total_cnty_dmg'] is your data

# Fit a Pareto distribution to the data
b, loc, scale = stats.pareto.fit(storms_dates['total_cnty_dmg'], floc=0)
print(f"Fitted Pareto parameters: b={b}, loc={loc}, scale={scale}")

# Generate a range of values over which to evaluate the PDF
x = np.linspace(storms_dates['total_cnty_dmg'].min() + 1, storms_dates['total_cnty_dmg'].max()+ 10, 1000)
fitted_pdf_pareto = stats.pareto.pdf(x, b, loc, scale)

# Plot the histogram and the fitted PDF
fig, ax = plt.subplots(figsize=(8, 8))

hist_data, bins, _ = ax.hist(storms_dates['total_cnty_dmg'], bins=50, edgecolor='black', density=False)

# Calculate the bin width
bin_width = bins[1] - bins[0]

# Scale the PDF by the number of data points and the bin width
scaled_pdf_pareto = fitted_pdf_pareto * len(storms_dates['total_cnty_dmg']) * bin_width

# Plot the scaled PDF
ax.plot(x, scaled_pdf_pareto, 'r-', lw=2, label='Fitted Pareto PDF')

# Set y-axis to logarithmic scale
ax.set_yscale('log')

# Add legend
ax.legend()


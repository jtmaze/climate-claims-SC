# Evaluating Disaster Insurance Claims in South Carolina
#### James Maze

---
### Summary: 
This project explores the spatiotemporal patterns for disaster insurance claims in South Carolina (SC) between 1960 and 2022. The scope focuses on climate hazards within the broader context of climate attribution. As an ambitious step further, I will attempt relating these claims patterns to climate data. 

### Problem statement:
Insurance costs is the prominent climate impact experienced by wealthy economically mobile people, who witness minimal physical danger relative to vulnerable poorer groups. In recent years, there's been contentious debate about skyrocketing premiums, and insurers entirely stepping away from the riskiest geographies. Given this context, I want to examine the extent of increasing disaster claims and attempt attribution with climate trends.

### Datasets used:  
1. **Spatial Hazards Events and Losses Database US** -- (SHELDUS) curated by the Arizona State Center for Emergency Management and Homeland Security. (<http://macdown.uranusjr.com>). Only South Carolina data is free, which limited my project scope. Data from other states is quite expensive!   
2. **County level census data** -- Created by the U.S. Census 5-year American Community Survey (<https://www.census.gov/data/developers/data-sets/acs-5year.html>), but accessed with the census API (<https://github.com/datamade/census>). Since counties have vastly different population sizes, I'll likely need to adjust the hazards data on a per-capita basis. There is also potential for a compelling demographic story within the insurance claims. 
3. **ERA5-Land Reanalysis data (To be continued)** -- Produced by the European Center for Medium-Range Weather Forecasts (ECMWF) by combining model data with observations. (<https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview>) I will utilize this data for attributing disaster claims to real climate events/trends.  **I did not have time for this step given a limited timeline in a class project. I hope to continue at a later date**

### Python libraries required:
* geopandas
* census
* scipy

### Planned methods and approaches:
1. Exploratory analysis of the SHELDUS. Produce claims timeseries for inflation adjusted dollars by disaster type, create-county level choropleth maps of per-capita losses for different disasters.
2. When applicable, conduct frequency/return period analysis (i.e. $ of claims expected for a 1/X year event). I would love to see some clean Poisson Distributions!
3. Based on results from steps 1. & 2., attempt attribution of insurance trends to climatic trends in ERA5 data. This is a lofty goal. **I did not have time for this step given a limited timeline in a class project. I hope to continue at a later date**

### Expected outcomes:
* Determine which types of disaster insurance claims are most common in each county. 
* Assess whether disaster claims have increased overtime. If there's been an increase in claims, where is the increase most pronounced? 
* Establish a connection between disaster claims and ERA5 climate data. Has there been a concomitant increase in disaster claims with changing climate?

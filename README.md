# Evaluating Disaster Insurance Claims in South Carolina
#### James Maze

---
### Summary: 
This project explores the spatiotemporal paterns for disaster insurance claims in South Carolina (SC) between 1960 and 2022. The scope foccuses on climate hazards within the broader context of climate attribution. As an ambitous step further, I will attempt relating these claims patterns to climate data. 

### Problem statement:
Insurance costs are the most palpable climate impact experienced by wealthy econmically mobile people, who experience much less physical danger compared to vunerable groups. In recent years, there's been contentious debate about skyrocketing premiums, and insurers entirely stepping away from the riskiest geographies. Given this context, I want to examine the extent of increasing disaster claims and attempt attribution with climate trends.

### Datasets used:  
1. **Spatial Hazards Events and Losses Database US** -- (SHELDUS) currated by the Arizona State Center for Emergency Management and Homeland Security. (<http://macdown.uranusjr.com>). Only South Carolina data is free, which limited my project scope. Data from other states is quite expensive!   
2. **County level census data** -- Created by the U.S. Census 5-year American Comunity Survey (<https://www.census.gov/data/developers/data-sets/acs-5year.html>), but accessed with the census API (<https://github.com/datamade/census>). Since counties have vastly different population sizes, I'll likely need to adjust the hazards data on a per-capita basis. There is also potential for a compelling demographic story within the insurance claims. 
3. **ERA5-Land Reanalysis data** -- Produced by the European Center for Medium-Range Weather Forecasts (ECMWF) by combining model data with observations. (<https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview>) I will utilize this data for attributing disaster claims to real climate events/trends.

### Python libraries required:
* geopandas
* census
* rasterio 
* More packages TBD

### Planned methods and approaches:
1. Exploratory analysis of the SHELDUS data. Produce claims timeseries for inflation adjusted dollars and by disaster type, create county level chloropleth maps of per-capita losses for different disasters.
2. When applicable, conduct frequency/return period analysis (i.e. $ of claims expected a 1/X year event). Would love to see some clean Poisson Distributions!
3. Based on results from steps 1. & 2., attempt attribution of insurance trends to climatic trends. 

### Expected outcomes:
* Find which types of disaster insurance claims are most comon in each county. 
* Determine whether disaster claims have increased overtime. If there's been an increase in claims, where is the increase most pronounced? 
* Establish a connection between disaster claims and ERA5 climate data. Has there been a concomitant increase in disaster claims with changing climate?

### References:
1. "Too hot to insure – avoiding the insurability tipping point" (<https://www.bis.org/fsi/publ/insights54.htm>)
2. 
 
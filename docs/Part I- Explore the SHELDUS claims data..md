# Part I: Explore the SHELDUS claims data.

### Libraries required

```python
import pandas as pd
import census
import geopandas

import matplotlib.pyplot as plt

```

### Step 1: Read the claims data

```python
claims = pd.read_csv('./project_data/SC-claimsA.csv', index_col=False)

# Drop columns which we aren't using
drop_cols = [
    'StateName', 'Fatalities', 'FatalitiesDuration', 'FatalitiesPerCapita', 
    'Glide', 'Injuries', 'InjuriesDuration', 'InjuriesPerCapita', 'PropertyDmgDuration'
]
claims.drop(columns=drop_cols, inplace=True)

# Some of the column names have bad syntax
claims.rename(columns={' Hazard': 'Hazard'}, inplace=True)
```

```
test a codecell
```





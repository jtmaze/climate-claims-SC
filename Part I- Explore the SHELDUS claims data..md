# Part I: Explore the SHELDUS claims data.

### Libraries required

```python
import pandas as pd
import census
import geopandas

```

### Step 1: Read the claims data

```python
claims = pd.read_csv('./project_data/SC-claimsA.csv', index_col=False)

# A few columns are unecessary
drop_cols = ['StateName', 'Fatalities', 'FatalitiesDuration', 'FatalitiesPerCapita']
claims.drop(columns=drop_cols, inplace=True)
```

```
test a codecell
```





import plotly.express as px

import pandas as pd

# Read data from a csv
_data = pd.read_excel('data.xlsx')
wdata = pd.DataFrame(dict(learning=_data['Learning Rate'], testing=_data['Test Performance'], crime=_data['Crime'],
                          housing=_data['Normalized Housing Price'], farms=_data['FARMS Rate with Multiplier If Applicable'],
                          absence=_data['Absence Rate'], discipline=_data['discipline rate'], prop=_data['Proportion of Revenue Spent on Teachers']))
# tdata = wdata.melt(id_vars='crime')


fig = px.scatter_3d(wdata, x=wdata.learning, y=wdata.testing, z=wdata.prop, color=wdata.crime)
fig.show()

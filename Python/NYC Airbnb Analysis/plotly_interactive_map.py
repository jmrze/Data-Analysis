#!/usr/bin/env python3

import plotly.express as px
import pandas as pd

df = pd.read_csv("/home/james/Documents/analysis/sql/airbnb/AB_NYC_2019.csv")

# borough input

boroughs = list(df['neighbourhood_group'].unique())

boroughs.append('All')

print(boroughs)

print("\n\t{ or alternatively 'All' }")

    # borough input control flow

while True:
    borough = input("\nPlease choose a borough: ")
    if borough in boroughs:
        break
    else:
        print("Choose valid option")

if borough == 'All':
    df_borough = df
else:
    df_borough = df[df['neighbourhood_group'] == borough]

# neighbourhood input

neighbourhoods = list(df_borough['neighbourhood'].unique())

neighbourhoods.append('All')

print(neighbourhoods)

print("\n\t{ or alternatively 'All' }")

    # neighbourhood input control flow

while True:
    neighbourhood = input("\nPlease choose a neighbourhood: ")
    if neighbourhood in neighbourhoods:
        break
    else:
        print("Choose valid option")

if neighbourhood == 'All':
    df_neighbourhood = df_borough
else:
    df_neighbourhood = df_borough[df_borough['neighbourhood'] == neighbourhood]

# colour input

num_vars = df.select_dtypes(include=['number']).columns

num_vars = list(num_vars)

print(num_vars)

while True:
    col_var = input("\nchoose continuous variable for colour: ")
    if col_var in num_vars:
        break
    else:
        print("Choose valid option")

# size input

print(num_vars)

while True:
    size_var = input("\nchoose continuous variable for size: ")
    if size_var in num_vars:
        break
    else:
        print("Choose valid option")

# plotting

df_neighbourhood.dropna(
    # axis=0,
    # how='any',
    # thresh=None,
    # subset=None,
    # inplace=True
)

hover_vars = [col_var, size_var] # chosen variables

cat_vars = ['room_type', 'neighbourhood'] # additional categorical variables for hover info

for var in cat_vars:
    hover_vars.append(var)

color_scale = 'viridis'

fig = px.scatter_map(df_neighbourhood, 
                        lat="latitude", 
                        lon="longitude", 
                        hover_name="name", 
                        hover_data=hover_vars,
                        color=col_var,
                        opacity=0.8,
                        color_continuous_scale=color_scale,
                        range_color=[df_neighbourhood[col_var].min(),
                                     df_neighbourhood[col_var].max()],
                        size=size_var,
                        zoom=11, 
                        height=800,
                        width=1200)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()

fig.write_html('exemplar_plot.html')
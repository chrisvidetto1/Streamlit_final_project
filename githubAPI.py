# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 09:04:56 2020

@author: chris
"""

import pandas
import requests
#from plotly.graph_objects import Bar
#from plotly import offline
import streamlit as st
import plotly.express as px
# Make an API call and store the response in a variable

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)

#Print the value of Status Code to make sure the call was successful
print(f"Status code: {r.status_code}")

# View the API response as a .json
response_dict = r.json()
repo_dicts = response_dict['items']
repo_names, stars = [], []
for repo_dict in repo_dicts:
    repo_names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])
    
# # Make visualization
# data = [{
#     'type':'bar',
#     'x':repo_names,
#     'y':stars,
# }]

# my_layout = {
#     'title': 'Popular Python Projects CV Github',
#     'xaxis':{'title':'Repository'},
#     'yaxis':{'title':'Stars'},
# }

# fig = {'data': data, 'layout': my_layout}
# offline.plot(fig, filename='python_repos.html')
 
    
# Take the results from the API get request above and pass them to streamlit   
    
st.header("Most Popular projects on Github by Star Count")   
df = pandas.DataFrame(stars, repo_names)    
df2 = df.reset_index()
#df2.dtypes
new_cols = ["Repository", "Stars"]
df2.columns = new_cols
fig2 = px.bar(df2, x='Repository', y='Stars')
st.plotly_chart(fig2)

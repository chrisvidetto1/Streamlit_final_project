# -*- coding: utf-8 -*-
#"""
#Created on Fri Dec 11 10:22:10 2020

#@author: chris
"""


TO RUN: 
    streamlit run week13_streamlit.py
"""

### Use pip to install the streamlit package, and plotly

# pip install streamlit
# pip install plotly

### Next we have to import the packages into this kernel

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time


# dataURL = ('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(dataURL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     return data

# Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text("Done! (using st.cache)")


#@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

#@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

#@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title("Chris Videtto's Final Project...")


st.header("The battle of East Cost vs. West Coast!!")

st.subheader("Lets go to the Golden State first...")

# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()

hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
hospitals_calif = df_hospital_2[df_hospital_2['state'] == 'CA']
hospitals_mass = df_hospital_2[df_hospital_2['state'] == 'MA']

hospitals_ca_gps = hospitals_calif['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ca_gps['lon'] = hospitals_ca_gps['lon'].str.strip('(')
hospitals_ca_gps = hospitals_ca_gps.dropna()
hospitals_ca_gps['lon'] = pd.to_numeric(hospitals_ca_gps['lon'])
hospitals_ca_gps['lat'] = pd.to_numeric(hospitals_ca_gps['lat'])
st.map(hospitals_ca_gps)


st.subheader('California Hospital Types')
bar1 = hospitals_calif['hospital_type'].value_counts().reset_index()
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)




st.header("Now, lets take a look on the East Coast...")

hospitals_mass_gps = hospitals_mass['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_mass_gps['lon'] = hospitals_mass_gps['lon'].str.strip('(')
hospitals_mass_gps = hospitals_mass_gps.dropna()
hospitals_mass_gps['lon'] = pd.to_numeric(hospitals_mass_gps['lon'])
hospitals_mass_gps['lat'] = pd.to_numeric(hospitals_mass_gps['lat'])
st.map(hospitals_mass_gps)


st.subheader('Massachussetts Hospital Types')
bar1 = hospitals_mass['hospital_type'].value_counts().reset_index()
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)


st.header("Wow, Massachussetts has alot more Psychiatric hospitals!!")
st.header("Cali has 10.1% psych but Mass has 20.5% of their total hospitals")


#Bar Charts of the costs 
st.title("Now lets take a look at the Total Costs of Healthcare...")


st.title('Costs on the West Coast...')


inpatient_CA = df_inpatient_2[df_inpatient_2['provider_state'] == 'CA']
total_inpatient_count1 = sum(inpatient_CA['total_discharges'])


costs = inpatient_CA.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_CA.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)

st.header("For the West Coast it looks like Stanford Health Care which is part of Stanford Medical School has $8.45 million in total payments")




st.title('Costs on the East Coast...')

inpatient_MA = df_inpatient_2[df_inpatient_2['provider_state'] == 'MA']
total_inpatient_count2 = sum(inpatient_MA['total_discharges'])

costs2 = inpatient_MA.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs2['average_total_payments'] = costs2['average_total_payments'].astype('int64')


costs_medicare2 = inpatient_MA.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare2['average_medicare_payments'] = costs_medicare2['average_medicare_payments'].astype('int64')


costs_sum2 = costs2.merge(costs_medicare2, how='left', left_on='provider_name', right_on='provider_name')
costs_sum2['delta'] = costs_sum2['average_total_payments'] - costs_sum2['average_medicare_payments']


bar32 = px.bar(costs_sum2, x='provider_name', y='average_total_payments')
st.plotly_chart(bar32)



st.header("For the East Coast it looks like Massachussets General Hospital which is part of Harvard Medical School has $7.21 million in Average Total Payments")


st.title("West Cost - Stanford Medical School - $8.45 million (avg. total pymt.)")
st.title("East Cost - Harvard Medical School - $7.21 million (avg. total pymt.)")

st.title("West Coast wins!!")
         
st.title("BUT...Does more revenue mean better quality of care?")

#Timeliness of Care

st.subheader('California - Timelieness of Care')
bar2 = hospitals_calif['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.subheader('Massachussetts - Timelieness of Care')
bar2 = hospitals_mass['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.header('Based on the bar charts above, we can see the majority of hospitals in California and Massachusetts both fall BELOW the National Average')

#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Take a closer look at inpatient data for California and Massachusetts')
st.title("California...")

inpatient_CA = df_inpatient_2[df_inpatient_2['provider_state'] == 'CA']
total_inpatient_count1 = sum(inpatient_CA['total_discharges'])

st.header('Total Count of Discharges from Californias Inpatient Captured: ' )
st.header( str(total_inpatient_count1) )

#Common D/C 

common_dischargesCA = inpatient_CA.groupby('drg_definition')['total_discharges'].sum().reset_index()
orderedCA = common_dischargesCA.sort_values('total_discharges', ascending=False)

st.header("Top 10 DRG's for California")
top10MA = orderedCA.head(10)
st.dataframe(top10MA)


###MASSSSS
st.title("Masschusetts...")


inpatient_MA = df_inpatient_2[df_inpatient_2['provider_state'] == 'MA']
total_inpatient_count2 = sum(inpatient_MA['total_discharges'])

st.header('Total Count of Discharges from Massachusetts Inpatient Captured: ' )
st.header( str(total_inpatient_count2) )

common_dischargesMA = inpatient_MA.groupby('drg_definition')['total_discharges'].sum().reset_index()
orderedMA = common_dischargesMA.sort_values('total_discharges', ascending=False)

st.header("Top 10 DRG's for Massachussets")
top10MA = orderedMA.head(10)
st.dataframe(top10MA)

st.title("According to the tables above the Top 4 Most Common DRGS for California are:")
st.header(" 1.Speticemia")
st.header("2.Major Joint Replacement")
st.header("3. Heart Failure")
st.header(" 4.Septicemia > 96hrs")

st.title("And the Top 4 Most Common DRGS for Massachussets are:")
st.header("1.Speticemia")
st.header("2.Major Joint Replacement")
st.header(" 3.Heart Failure")
st.header(" 4.Esophagitis")



st.title("Discussion")
st.header("Both Standford and Harvard represent the flagship medical universities and their affiliated hospital centers for the West and East Coast. However, there are significant differences between them.")
st.subheader("The health system on the West Coast has almost TWICE as many discharges as the east coast: 503,269 vs. 221,439.")
st.subheader("There are almost TWICE as many psychiatric hospitals on the East Coast")
st.subheader("The total average costs tend to be HIGHER on the West Coast")
st.subheader("The quality of care seems to be below average for the majority of hospitals on both coasts")
st.subheader("The Top 3 most common discharges are the same, but the 4th most common is Septicemia >96hrs on the West Coast, and is Esophagitis on the East Coast")
st.subheader("This is interesting, and potentially could be related to the much colder climates on the east coast in the winter months")
st.subheader("In conclusion, this was an insightful project and helped me develop the tools necessary to present healthcare data in a visually impressive format")
st.subheader("Thanks for reading Professor Hants Williams RN PhD.!!!")
st.write('Sincerely, Chris V :sunglasses:') 
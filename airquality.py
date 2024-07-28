pip install streamlit pandas requests matplotlib seaborn
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to get air quality data
def get_air_quality_data(city):
    api_url = f'http://api.waqi.info/feed/{city}/?token=7db710d39a36c80d6bcfe6e600cb185e8f960240'
    response = requests.get(api_url)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']
    else:
        st.error("Unable to fetch data for the selected city.")
        return None

# Streamlit app
st.title("Air Quality Tracker for Indian Cities")

cities = ["Mumbai", "Chennai", "Delhi", "Hyderabad", "Bangalore"]
city = st.selectbox("Select a city:", cities)

if city:
    data = get_air_quality_data(city)
    if data:
        st.write(f"Air Quality Index (AQI) for {city}: {data['aqi']}")
        
        # Displaying additional information
        st.write("Pollutants:")
        pollutants = data['iaqi']
        pollutants_df = pd.DataFrame(pollutants).T
        st.dataframe(pollutants_df)
        
        # Plotting data
        fig = px.bar(pollutants_df, x=pollutants_df.index, y=0, labels={'x': 'Pollutant', 'y': 'Concentration'})
        st.plotly_chart(fig)

st.write("Note: Data fetched from World Air Quality Index project.")


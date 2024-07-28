import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Function to get current air quality data
def get_air_quality_data(city):
    api_url = f'http://api.waqi.info/feed/{city}/?token=7db710d39a36c80d6bcfe6e600cb185e8f960240'
    response = requests.get(api_url)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']
    else:
        st.error("Unable to fetch data for the selected city.")
        return None

# Function to get historical air quality data
def get_historical_data(city):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)
    api_url = f'http://api.waqi.info/feed/{city}/history/?token=7db710d39a36c80d6bcfe6e600cb185e8f960240'
    response = requests.get(api_url)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']['aqi']
    else:
        st.error("Unable to fetch historical data for the selected city.")
        return None

# Streamlit app
st.title("Air Quality Tracker for Indian Cities")

cities = ["Mumbai", "Chennai", "Delhi", "Hyderabad", "Bangalore"]
city = st.selectbox("Select a city:", cities)

if city:
    data = get_air_quality_data(city)
    historical_data = get_historical_data(city)

    if data:
        st.header(f"Current Air Quality in {city}")

        # Display current AQI
        st.metric(label="Air Quality Index (AQI)", value=data['aqi'])

        # Display additional information
        st.subheader("Current Pollutants")
        pollutants = data['iaqi']
        pollutants_df = pd.DataFrame(pollutants).T
        pollutants_df.columns = ['Concentration']
        st.dataframe(pollutants_df)

        # Plotting pollutant data
        fig = px.bar(pollutants_df, x=pollutants_df.index, y='Concentration', labels={'index': 'Pollutant', 'Concentration': 'Concentration'})
        st.plotly_chart(fig)

        if historical_data:
            st.header(f"Historical Air Quality in {city}")
            historical_df = pd.DataFrame(historical_data).reset_index()
            historical_df.columns = ['Datetime', 'AQI']
            historical_df['Datetime'] = pd.to_datetime(historical_df['Datetime'])

            # Line chart for historical AQI data
            fig = px.line(historical_df, x='Datetime', y='AQI', labels={'Datetime': 'Date', 'AQI': 'Air Quality Index'})
            st.plotly_chart(fig)

            # More detailed pollutant information
            st.subheader("Detailed Pollutant Information")
            pollutants_details = {
                'pm25': 'PM2.5 (Fine Particulate Matter)',
                'pm10': 'PM10 (Respirable Particulate Matter)',
                'no2': 'NO2 (Nitrogen Dioxide)',
                'so2': 'SO2 (Sulfur Dioxide)',
                'o3': 'O3 (Ozone)',
                'co': 'CO (Carbon Monoxide)'
            }
            for pollutant, description in pollutants_details.items():
                if pollutant in pollutants:
                    st.write(f"{description}: {pollutants[pollutant]['v']}")

st.write("Note: Data fetched from World Air Quality Index project.")


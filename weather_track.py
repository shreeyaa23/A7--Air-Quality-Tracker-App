pip install streamlit pandas requests matplotlib seaborn
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
API_KEY = 'your_openweather_api_key'  # Replace with your OpenWeatherMap API key
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    # Add more cities as needed
}

# Function to fetch air quality data
def get_air_quality(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={city["lat"]}&lon={city["lon"]}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

# Streamlit app layout
st.title("Air Quality Monitoring App")

st.sidebar.title("Settings")
city_name = st.sidebar.selectbox("Select a city", list(CITIES.keys()))
city = CITIES[city_name]

air_quality_data = get_air_quality(city, API_KEY)

if "list" in air_quality_data:
    aq_info = air_quality_data["list"][0]
    components = aq_info["components"]

    st.subheader(f"Air Quality in {city_name}")
    st.write(f"PM2.5: {components['pm2_5']} µg/m³")
    st.write(f"PM10: {components['pm10']} µg/m³")
    st.write(f"CO: {components['co']} µg/m³")
    st.write(f"NO: {components['no']} µg/m³")
    st.write(f"NO2: {components['no2']} µg/m³")
    st.write(f"O3: {components['o3']} µg/m³")
    st.write(f"SO2: {components['so2']} µg/m³")
    st.write(f"NH3: {components['nh3']} µg/m³")

    # Visualization
    st.subheader("Air Quality Components Visualization")
    df = pd.DataFrame.from_dict(components, orient='index', columns=['Concentration'])
    fig, ax = plt.subplots()
    sns.barplot(x=df.index, y='Concentration', data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.error("Failed to retrieve data. Please check the API key and try again.")
streamlit run air_quality_app.py

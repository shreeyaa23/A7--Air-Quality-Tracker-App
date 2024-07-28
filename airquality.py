import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Streamlit app
st.set_page_config(page_title="Air Quality Tracker", page_icon=":earth_asia:", layout="wide")

st.sidebar.title("Air Quality Tracker")
st.sidebar.markdown("## Select a city to see its air quality details:")

cities = [
    "Mumbai", "Chennai", "Delhi", "Hyderabad", "Bangalore", "Kolkata", 
    "Ahmedabad", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", 
    "Visakhapatnam", "Bhopal", "Patna", "Ludhiana", "Agra", "Nashik", 
    "Faridabad", "Meerut"
]
city = st.sidebar.selectbox("Select a city:", cities)

if city:
    data = get_air_quality_data(city)
    
    if data:
        st.title(f"Air Quality in {city}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Air Quality Index (AQI)", value=data['aqi'])
            
        with col2:
            st.markdown("### Current Pollutants")
            pollutants = data['iaqi']
            pollutants_df = pd.DataFrame(pollutants).T
            pollutants_df.columns = ['Concentration']
            st.dataframe(pollutants_df)

            fig = px.bar(
                pollutants_df, 
                x=pollutants_df.index, 
                y='Concentration', 
                labels={'index': 'Pollutant', 'Concentration': 'Concentration'},
                color='Concentration',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig)

        st.markdown("### Detailed Pollutant Information")
        pollutants_details = {
            'pm25': 'PM2.5 (Fine Particulate Matter)',
            'pm10': 'PM10 (Respirable Particulate Matter)',
            'no2': 'NO2 (Nitrogen Dioxide)',
            'so2': 'SO2 (Sulfur Dioxide)',
            'o3': 'O3 (Ozone)',
            'co': 'CO (Carbon Monoxide)'
        }
        pollutant_expander = st.expander("Click to see detailed pollutant information")
        with pollutant_expander:
            for pollutant, description in pollutants_details.items():
                if pollutant in pollutants:
                    st.write(f"{description}: {pollutants[pollutant]['v']}")

st.sidebar.markdown("## Note:")
st.sidebar.markdown("Data fetched from World Air Quality Index project.")
st.sidebar.markdown("[Learn more about AQI](https://aqicn.org/faq/)")


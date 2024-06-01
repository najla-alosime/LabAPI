import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

st.title("Player Value Prediction App ⚽")

df = pd.read_csv("https://raw.githubusercontent.com/Sulaiman-F-Alharbi/Use-case-7/main/Data/Categorized_football.csv")
# Assuming football_df is your DataFrame
fig = px.scatter(
    df,
    x='appearance',
    y='current_value',
    color='current_value_category',
    title='Scatter Plot of Appearance vs Current Value',
    labels={'appearance': 'Appearance', 'current_value': 'Current Value'}
)

st.plotly_chart(fig)


leagues = [
        "Premier League and Championship", "EFL", "Bundesliga",
        "La liga","Serie A","Serie B",
        "Ligue 1","Eredivisie","Eerste Divisie",
        "Liga NOS","Premier Liga","Super Lig",
        "TFF","Bundesliga","Brasileiro",
        "MLS","Primera División","Liga MX",
        "DStv","J-League","Saudi Pro League",
        "K-League","A-League"
    ]

# Taking user inputs
appearance = st.slider("Appearance", 0, 300, 10)
minutes_played = st.slider("Minutes Played", 0, 10000, 500)
award = st.selectbox('Award', range(0,93))
goals = st.number_input("Insert a goals", value=None, placeholder="Type a number...")
assists = st.number_input("Insert a assists", value=None, placeholder="Type a number...")
days_injured = st.number_input("Insert a days_injured", value=None, placeholder="Type a number...")
games_injured = st.number_input("Insert a games_injured", value=None, placeholder="Type a number...")
highest_value = st.number_input("Insert a highest_value", value=None, placeholder="Type a number...")

league = st.selectbox(
   "Choose player league",
   leagues,
   index=None,
   placeholder="choose player league...",
)


# Converting the inputs into a JSON format
inputs = {
    
    "appearance": appearance,
    "goals": goals,
    
    "minutes_played": minutes_played, 
    
    "games_injured": games_injured,
    
    "highest_value": highest_value,
    }

# When the user clicks on the button, it will fetch the API
if st.button('Get Prediction'):
    try:
        res = requests.post(
            url="https://use-case-7-8gxt.onrender.com/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(inputs)
        )
        res.raise_for_status()  # Check for HTTP request errors
        st.subheader(f"Prediction result 🚀 = {res.json()}")

    except requests.exceptions.RequestException as e:
        st.error(f"HTTP Request failed: {e}")
    except ValueError as e:
        st.error(f"Failed to parse JSON response: {e}")

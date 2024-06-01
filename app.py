import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

st.title("⚽  Prediction of Player Value  ⚽")

df = pd.read_csv("https://raw.githubusercontent.com/najla-alosime/LabAPI/main/Categorized_football.csv")

# Assuming football_df is your DataFrame
fig = px.scatter(
    df,
    x='appearance',
    y='current_value',
    color='current_value_category_encoded',
    title=' Appearance vs Current Value',
    labels={'appearance': 'Appearance', 'current_value': 'Current Value'}
    
)

st.plotly_chart(fig)




# Taking user inputs
goals = st.number_input("Insert a goals", value=None, placeholder="Type a number...")
highest_value = st.number_input("Insert a highest_value", value=None, placeholder="Type a number...")
games_injured = st.number_input("Insert a games_injured", value=None, placeholder="Type a number...")
minutes_played = st.slider("Minutes Played", 0, 10000, 500)
appearance = st.slider("Appearance", 0, 300, 10)




# Converting the inputs into a JSON format
inputs = {
    'appearance': appearance,
    'goals': goals,
    'minutes_played': minutes_played,
    'games_injured': games_injured,
    'highest_value': highest_value,


    }

# When the user clicks on the button, it will fetch the API
if st.button('Get Prediction'):
   # res=None
    try:
       
        res = requests.post(
            url="https://labapi-4dnd.onrender.com/predict",
            headers={"Content-Type": "application/json"},
            json=inputs
        )
        res.raise_for_status()  # Check for HTTP request errors
        #st.write(res.raw)
        st.subheader(f"Prediction result  = {res.json()}")

    except requests.exceptions.RequestException as e:
        st.error(f"HTTP Request failed: {e })")
    except ValueError as e:
        st.error(f"Failed to parse JSON response: {e}")
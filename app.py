import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
import requests  # Import the requests library
import os


# Function to load a pickle file from a URL
def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

# Load the saved models and scaler from GitHub
bouldering_model_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/main/best_model_rf.pkl'
bouldering_scaler_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/main/scaler.pkl'

bouldering_model = load_pickle_from_url(bouldering_model_url)
bouldering_scaler = load_pickle_from_url(bouldering_scaler_url)

sport_model_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/main/best_model_rf_sport.pkl'
sport_scaler_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/main/scaler_sport.pkl'

sport_model = load_pickle_from_url(sport_model_url)
sport_scaler = load_pickle_from_url(sport_scaler_url)

# Create a sidebar for user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    bmi_score = st.sidebar.number_input('BMI score', min_value=0.0, max_value=50.0, value=25.0)
    max_pullups = st.sidebar.number_input('Max pullups in single go', min_value=0.0, max_value=50.0, value=10.0)
    max_hang_weight = st.sidebar.number_input('Max weight added to hang for 10 seconds from a 20mm edge (kg)', min_value=0.0, max_value=100.0, value=10.0)
    max_pullup_weight = st.sidebar.number_input('Max weight added to a single pullup (kg)', min_value=0.0, max_value=100.0, value=10.0)
    continious = st.sidebar.number_input('Continious hang from 20mm edge (seconds)', min_value=1, max_value=1000, value=30)
    repeaters = st.sidebar.number_input('7:3 hangs on a 20mm edge (total time in seconds)', min_value=1, max_value=1000, value=120)
    exp = st.sidebar.number_input('Climbing experience (years)', min_value=0.0, max_value=50.0, value=5.0)
    days = st.sidebar.number_input('Days climbing outside per month', min_value=1, max_value=30, value=5)


    # Calculate strength-to-weight ratios
    strength_to_weight_pullup = (max_pullups + bmi_score) / bmi_score
    strength_to_weight_maxhang = (max_hang_weight + bmi_score) / bmi_score
    strength_to_weight_weightpull = (max_pullup_weight + bmi_score) / bmi_score

    data = {
        'strength_to_weight_pullup': strength_to_weight_pullup,
        'strength_to_weight_maxhang': strength_to_weight_maxhang,
        'strength_to_weight_weightpull': strength_to_weight_weightpull,
        'continious': continious,
        'repeaters1': repeaters,
        'exp': exp,
        'days': days
    }

    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Apply the same preprocessing used during model training
scaled_features = bouldering_scaler.transform(input_df)
scaled_features_sport = sport_scaler.transform(input_df)

# Mapping functions to produce output in the correct value (e.g. V grade for bouldering and French for sport)
# Bouldering
conversion_map_boulder = {
    "<V3": 1,
    "V3": 2, "V4": 3, "V5": 4,
    "V6": 5, "V7": 6, "V8": 7,
    "V9": 8, "V10": 9, "V11": 10,
    "V12": 11, "V13": 12, "V14": 13,
    "V15": 14, "V16": 15, "I have not pursued bouldering goals outside in the past year": 0
}

# Reverse the conversion_map dictionary to map from numerical grade back to V grade
inverse_conversion_map_v = {v: k for k, v in conversion_map_boulder.items()}

# Now define a function to convert numeric grade to V grade
def convert_numeric_to_v_grade(numeric_grade):
    # Round the numeric grade to the nearest integer
    numeric_grade = round(numeric_grade)

    if numeric_grade in inverse_conversion_map_v:
        return inverse_conversion_map_v[numeric_grade]
    else:
        return "Unknown grade"  # or other string to indicate unknown grade

# Sport climbing   
conversion_map_french = {
    '4c': 1, '5a': 2, '5b': 3, '5c': 4, '6a': 5,
    '6a+': 6, '6b': 7, '6b+': 8, '6c': 9, '6c+': 10, '7a': 11,
    '7a+': 12, '7b': 13, '7b+': 14, '7c': 15, '7c+': 16, '8a': 17,
    '8a+': 18, '8b': 19, '8b+': 20, '8c': 21, '8c+': 22, '9a': 23, '9a+': 24, '0': 0
}

# Reverse the conversion_map dictionary to map from numerical grade back to French grade sport
inverse_conversion_map_f = {v: k for k, v in conversion_map_french.items()}

# Now define a function to convert numeric grade to French grade
def convert_numeric_to_f_grade(numeric_grade):
    # Round the numeric grade to the nearest integer
    numeric_grade = round(numeric_grade)

    if numeric_grade in inverse_conversion_map_f:
        return inverse_conversion_map_f[numeric_grade]
    else:
        return "Unknown grade"  # or other string to indicate unknown grade

# Modeling and predictions to display as output
# Make bouldering predictions
bouldering_prediction = bouldering_model.predict(scaled_features)
bouldering_predicted_grade = convert_numeric_to_v_grade(float(bouldering_prediction[0]))

# Make sport predictions
sport_prediction = sport_model.predict(scaled_features_sport)
sport_predicted_grade = convert_numeric_to_f_grade(float(sport_prediction[0]))

# Display the prediction for bouldering
st.header(f'Predicted Max Boulder Grade: {bouldering_predicted_grade}')
# Display the prediction for sport
st.header(f'Predicted Max Sport Grade: {sport_predicted_grade}')

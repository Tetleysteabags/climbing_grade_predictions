import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
import requests  # Import the requests library
import os

print(os.getcwd())

# Function to load a pickle file from a URL
def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

# Load the saved model and scaler from GitHub
model_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/master/best_model_rf.pkl'
scaler_url = 'https://github.com/Tetleysteabags/climbing_ml_project/raw/master/scaler.pkl'

model = load_pickle_from_url(model_url)
scaler = load_pickle_from_url(scaler_url)

# Create a sidebar for user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    bmi_score = st.sidebar.number_input('BMI Score', min_value=0.0, max_value=50.0, value=25.0)
    max_pullups = st.sidebar.number_input('Max Pullups in single go', min_value=0.0, max_value=50.0, value=10.0)
    max_hang_weight = st.sidebar.number_input('Max weight added to hang for 10 seconds from a 20mm edge (kg)', min_value=0.0, max_value=100.0, value=10.0)
    max_pullup_weight = st.sidebar.number_input('Max weight added to a single pullup (kg)', min_value=0.0, max_value=100.0, value=10.0)
    exp = st.sidebar.number_input('Experience (years)', min_value=0.0, max_value=50.0, value=5.0)
    days = st.sidebar.number_input('Days Climbing outside per month', min_value=1, max_value=30, value=5)

    # Calculate strength-to-weight ratios
    strength_to_weight_pullup = (max_pullups + bmi_score) / bmi_score
    strength_to_weight_maxhang = (max_hang_weight + bmi_score) / bmi_score
    strength_to_weight_weightpull = (max_pullup_weight + bmi_score) / bmi_score

    data = {
        'strength_to_weight_pullup': strength_to_weight_pullup,
        'strength_to_weight_maxhang': strength_to_weight_maxhang,
        'strength_to_weight_weightpull': strength_to_weight_weightpull,
        'exp': exp,
        'days': days
    }

    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Apply the same preprocessing used during model training
scaled_features = scaler.transform(input_df)

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

# Make predictions
prediction = model.predict(scaled_features)
predicted_grade = convert_numeric_to_v_grade(float(prediction[0]))

# Display the prediction
st.header(f'Predicted Max Boulder Grade: {predicted_grade}')

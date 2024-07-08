import requests

urls = [
    "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/best_model_gb_bouldering_newdata.pkl",
    "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/scaler_gb_bouldering_newdata.pkl",
    "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/best_model_rf_sport_newdata.pkl",
    "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/scaler_rf_sport_newdata.pkl"
]

for url in urls:
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")


import pickle

import joblib

filenames = [
    "best_model_gb_bouldering_newdata.pkl",
    "scaler_gb_bouldering_newdata.pkl",
    "best_model_rf_sport_newdata.pkl",
    "scaler_rf_sport_newdata.pkl"
]

for filename in filenames:
    try:
        data = joblib.load(filename)
        print(f"Successfully unpickled {filename}")
    except Exception as e:
        print(f"Error unpickling {filename}: {e}")


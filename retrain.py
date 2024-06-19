import pandas as pd
import joblib
from mongodb import fetch_feedback_data

def retrain_model(model_path, existing_data_path, new_data_path):
    model = joblib.load(model_path)
    existing_data = pd.read_csv(existing_data_path)
    new_feedback_data = pd.read_csv(new_data_path)
    all_data = pd.concat([existing_data, new_feedback_data], ignore_index=True)
    X = all_data.drop('grade', axis=1)
    y = all_data['grade']
    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"Model retrained and saved to {model_path}")

# Paths to your model and data files
bouldering_model_path = 'pkl_files/best_model_rf_bouldering_newdata.pkl'
bouldering_existing_data_path = 'training_data/data_filtered_bouldering_new.csv'
bouldering_new_data_path = 'training_data/new_feedback_bouldering.csv'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=bouldering_new_data_path)

# Retrain the bouldering model
retrain_model(bouldering_model_path, bouldering_existing_data_path, bouldering_new_data_path)

# Similarly, you can retrain the sport model
sport_model_path = 'pkl_files/best_model_rf_sport_newdata.pkl'
sport_existing_data_path = 'training_data/data_filtered_sport_new.csv'
sport_new_data_path = 'training_data/new_feedback_sport.csv'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=sport_new_data_path)

# Retrain the sport model
retrain_model(sport_model_path, sport_existing_data_path, sport_new_data_path)

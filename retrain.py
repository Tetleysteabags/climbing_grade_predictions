import pandas as pd
import joblib
from mongodb import fetch_feedback_data

def check_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

def retrain_model(model_path, existing_data_path, new_data_path, grade_column):
    model = joblib.load(model_path)
    existing_data = pd.read_csv(existing_data_path)
    new_feedback_data = pd.read_csv(new_data_path)
    
    # Concatenate existing data with new feedback data
    all_data = pd.concat([existing_data, new_feedback_data], ignore_index=True)
    
    # Check if required columns exist
    required_columns = ['strength_to_weight_pullup', 'strength_to_weight_maxhang', 'strength_to_weight_weightpull', 
                        'exp', 'continuous', 'repeaters1', grade_column]
    check_columns(all_data, required_columns)
    
    # Separate features and target
    X = all_data.drop(grade_column, axis=1)
    y = all_data[grade_column]
    
    # Retrain the model
    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"Model retrained and saved to {model_path}")

# Paths to your model and data files
bouldering_model_path = "pkl_files/best_model_rf_bouldering_newdata.pkl"
bouldering_existing_data_path = "training_data/data_filtered_bouldering_new.csv"
bouldering_new_data_path = "training_data/new_feedback.csv"
bouldering_grade_column = 'actual_bouldering_grade'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=bouldering_new_data_path)

# Retrain the bouldering model
retrain_model(bouldering_model_path, bouldering_existing_data_path, bouldering_new_data_path, bouldering_grade_column)

# Similarly, you can retrain the sport model
sport_model_path = "pkl_files/best_model_rf_sport_newdata.pkl"
sport_existing_data_path = "training_data/data_filtered_sport_new.csv"
sport_new_data_path = "training_data/new_feedback.csv"
sport_grade_column = 'actual_sport_grade'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=sport_new_data_path)

# Retrain the sport model
retrain_model(sport_model_path, sport_existing_data_path, sport_new_data_path, sport_grade_column)

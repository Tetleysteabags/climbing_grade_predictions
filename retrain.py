import pandas as pd
import joblib
from mongodb import fetch_feedback_data
from grade_conversions import convert_f_grade_to_numeric, convert_v_grade_to_numeric

def check_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in DataFrame: {missing_columns}")
    
def rename_columns(df, old_columns, new_columns):
    for old_col, new_col in zip(old_columns, new_columns):
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
            
def apply_grade_conversions(df):
    if 'max_sport_numeric' in df.columns:
        df['max_sport_numeric'] = df['max_sport_numeric'].apply(convert_f_grade_to_numeric)
    if 'max_boulder_numeric' in df.columns:
        df['max_boulder_numeric'] = df['max_boulder_numeric'].apply(convert_v_grade_to_numeric)

def retrain_model(model_path, existing_data_path, new_data_path, grade_column, all_data_path):
    model = joblib.load(model_path)
    existing_data = pd.read_csv(existing_data_path)
    new_feedback_data = pd.read_csv(new_data_path)
    
    # Rename columns if needed
    rename_columns(existing_data, ['actual_bouldering_grade'], ['max_boulder_numeric'])
    rename_columns(new_feedback_data, ['actual_bouldering_grade'], ['max_boulder_numeric'])
    rename_columns(existing_data, ['actual_sport_grade'], ['max_sport_numeric'])
    rename_columns(new_feedback_data, ['actual_sport_grade'], ['max_sport_numeric'])
    
    # Apply grade conversions
    apply_grade_conversions(new_feedback_data)
    
    # Required columns
    required_columns = ['strength_to_weight_pullup', 'strength_to_weight_maxhang', 'strength_to_weight_weightpull', 
                        'exp', 'continuous', 'repeaters1', grade_column]
    
    # Include only the required columns
    existing_data = existing_data[required_columns]
    new_feedback_data = new_feedback_data[required_columns]
    
    # Concatenate existing data with new feedback data
    all_data = pd.concat([existing_data, new_feedback_data], ignore_index=True)
    
    # Save the concatenated data to a CSV file in the GitHub training_data folder
    all_data.to_csv(all_data_path, index=False)
    print(f"Concatenated data saved to: {all_data_path}")
    
    # Check if required columns exist
    check_columns(all_data, required_columns)

    model = load_pickle_from_url(model_url)
    scaler = load_pickle_from_url(scaler_url)

    # Separate features and target
    X = all_data.drop(grade_column, axis=1)
    y = all_data[grade_column]
    
    # Retrain the model
    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"Model retrained and saved to {model_path}")

# Paths to your model and data files
bouldering_model_path = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/best_model_gb_bouldering_newdata.pkl"
bouldering_scaler_url = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/scaler_gb_bouldering_newdata.pkl"
bouldering_existing_data_path = "training_data/data_filtered_bouldering_new.csv"
bouldering_new_data_path = "training_data/new_feedback.csv"
bouldering_all_data_path = "training_data/all_data_bouldering.csv"
bouldering_grade_column = 'max_boulder_numeric'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=bouldering_new_data_path)

# Retrain the bouldering model
retrain_model(bouldering_model_path, bouldering_existing_data_path, bouldering_new_data_path, bouldering_grade_column, bouldering_all_data_path)

# Similarly, you can retrain the sport model
sport_model_path = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/best_model_rf_sport_newdata.pkl"
sport_scaler_url = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/scaler_rf_sport_newdata.pkl"
sport_existing_data_path = "training_data/data_filtered_sport_new.csv"
sport_new_data_path = "training_data/new_feedback.csv"
sport_all_data_path = "training_data/all_data_sport.csv"
sport_grade_column = 'max_sport_numeric'

# Fetch new feedback data from MongoDB and save to CSV
fetch_feedback_data(save_to_csv=True, csv_path=sport_new_data_path)

# Retrain the sport model
retrain_model(sport_model_path, sport_existing_data_path, sport_new_data_path, sport_grade_column, sport_all_data_path)
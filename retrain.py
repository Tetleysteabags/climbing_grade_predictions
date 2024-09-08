import pandas as pd
import joblib
import pickle
import os
import logging
from mongodb import fetch_feedback_data
from grade_conversions import convert_f_grade_to_numeric, convert_v_grade_to_numeric

logging.basicConfig(level=logging.INFO)

def check_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns in DataFrame: {missing_columns}")
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

def retrain_model(pipeline_path, existing_data_path, new_data_path, grade_column, all_data_path):
    print(f"Loading model pipeline from {pipeline_path}")
    
    with open(pipeline_path, 'rb') as model_file:
        model_pipeline = pickle.load(model_file)

    print(f"Loading existing data from {existing_data_path}")
    existing_data = pd.read_csv(existing_data_path)

    print(f"Loading new feedback data from {new_data_path}")
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
    os.makedirs(os.path.dirname(all_data_path), exist_ok=True)
    all_data.to_csv(all_data_path, index=False)
    print(f"Concatenated data saved to: {all_data_path}")
    
    # Check if required columns exist
    check_columns(all_data, required_columns)

    # Separate features and target
    X = all_data.drop(grade_column, axis=1)
    y = all_data[grade_column]

    # Retrain the model
    model_pipeline.fit(X, y)

    # Save the retrained model
    with open(pipeline_path, 'wb') as model_file:
        pickle.dump(model_pipeline, model_file)
    print(f"Model retrained and saved to {pipeline_path}")

# Paths to your model and data files
bouldering_pipeline_path = "pkl_files/full_pipeline_rf_bouldering.pkl"
bouldering_existing_data_path = "training_data/data_filtered_bouldering_new.csv"
bouldering_new_data_path = "training_data/new_feedback.csv"
bouldering_all_data_path = "training_data/all_data_bouldering.csv"
bouldering_grade_column = 'max_boulder_numeric'

sport_pipeline_path = "pkl_files/full_pipeline_rf_sport.pkl"
sport_existing_data_path = "training_data/data_filtered_sport_new.csv"
sport_new_data_path = "training_data/new_feedback.csv"
sport_all_data_path = "training_data/all_data_sport.csv"
sport_grade_column = 'max_sport_numeric'

# Fetch new feedback data from MongoDB and save to CSV
print("Fetching new feedback data...")
fetch_feedback_data(save_to_csv=True, csv_path=bouldering_new_data_path, is_streamlit=False)

# Check if new feedback data file exists
if os.path.exists(bouldering_new_data_path):
    print(f"New feedback data file exists: {bouldering_new_data_path}")
else:
    print(f"New feedback data file does NOT exist: {bouldering_new_data_path}")

# Retrain the bouldering model
retrain_model(
    bouldering_pipeline_path,
    bouldering_existing_data_path,
    bouldering_new_data_path,
    bouldering_grade_column,
    bouldering_all_data_path
)

# Fetch new feedback data for sport model
print("Fetching new feedback data for sport model...")
fetch_feedback_data(save_to_csv=True, csv_path=sport_new_data_path, is_streamlit=False)

# Check if new feedback data file exists
if os.path.exists(sport_new_data_path):
    print(f"New feedback data file exists: {sport_new_data_path}")
else:
    print(f"New feedback data file does NOT exist: {sport_new_data_path}")

# Retrain the sport model
retrain_model(
    sport_pipeline_path,
    sport_existing_data_path,
    sport_new_data_path,
    sport_grade_column,
    sport_all_data_path
)

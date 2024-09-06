import os
import pymongo
from pymongo import MongoClient, errors
import pandas as pd
import toml
import streamlit as st

def load_local_secrets():
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        print(secrets["mongo"]["conn_str"])
        return secrets["mongo"]["conn_str"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading local secrets: {e}")
        raise

def connect_to_mongodb(is_streamlit=False, is_local=True):
    try:
        if is_streamlit:
            conn_str = st.secrets["mongo"]["conn_str"]
            if not conn_str:
                raise ValueError("MongoDB connection string not found in Streamlit secrets")
        elif is_local:
            conn_str = load_local_secrets()
            if not conn_str:
                raise ValueError("MongoDB connection string not found in local secrets.toml")
        else:
            conn_str = os.getenv("MONGO_CONN_STR")
            if not conn_str:
                raise ValueError("MongoDB connection string not found in environment variables")
        
        print(f"Connecting to MongoDB with connection string: {conn_str}")
        client = pymongo.MongoClient(conn_str)
        db = client.ClimbingGradeFeedback
        collection = db.ClimbingFeedbackStreamlit
        return collection, client
    except pymongo.errors.ConnectionFailure as ce:
        print(f"Connection error: {ce}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def save_feedback(feedback_data, is_streamlit=False):
    """
    Save feedback data to MongoDB.

    Args:
        feedback_data (dict): Feedback data to be saved.
        is_streamlit (bool): Flag indicating if the function is running in a Streamlit environment.
    """
    collection, client = connect_to_mongodb(is_streamlit=is_streamlit)
    try:
        collection.insert_one(feedback_data)
        print("Feedback data saved successfully.")
    except errors.PyMongoError as e:
        print(f"Error saving feedback: {e}")
    finally:
        client.close()

def fetch_feedback_data(save_to_csv=False, csv_path=None, is_streamlit=False):
    """
    Fetch feedback data from MongoDB and optionally save it to a CSV file.

    Args:
        save_to_csv (bool): Flag indicating if the fetched data should be saved to a CSV file.
        csv_path (str): Path to save the CSV file.
        is_streamlit (bool): Flag indicating if the function is running in a Streamlit environment.

    Returns:
        pd.DataFrame: DataFrame containing the fetched feedback data.
    """
    try:
        collection, client = connect_to_mongodb(is_streamlit=is_streamlit)
        print("Fetching data from MongoDB collection...")
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))
        client.close()
        print("Data fetched successfully")
        
        if save_to_csv and csv_path:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            print(f"Data saved to {csv_path}")
        
        return df
    except Exception as e:
        print("Error fetching data from MongoDB:", e)
        return pd.DataFrame()

if __name__ == "__main__":
    # Path to save the feedback data
    feedback_data_path = "training_data/new_feedback.csv"
    fetch_feedback_data(save_to_csv=True, csv_path=feedback_data_path)
    
    if os.path.exists(feedback_data_path):
        print(f"File {feedback_data_path} exists.")
    else:
        print(f"File {feedback_data_path} does NOT exist.")

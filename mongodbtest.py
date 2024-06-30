import os
import pymongo
import pandas as pd
import streamlit as st
import toml

def load_secrets():
    try:
        secrets = st.secrets["mongo"]
        conn_str = secrets["conn_str"]
    except Exception as e:
        print(f"Error loading secrets: {e}")
        raise

def connect_to_mongodb():
    try:
        secrets = st.secrets["mongo"]
        conn_str = secrets["conn_str"]
        client = pymongo.MongoClient(conn_str)
        db = client.ClimbingGradeFeedback
        collection = db.ClimbingFeedbackStreamlit
        return collection, client
    except pymongo.errors.ConnectionError as ce:
        print(f"Connection error: {ce}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def fetch_feedback_data():
    try:
        collection, client = connect_to_mongodb()
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))
        client.close()
        print("Data fetched successfully")
        return df
    except Exception as e:
        print("Error fetching data from MongoDB:", e)
        return pd.DataFrame()

if __name__ == "__main__":
    load_secrets()  # Load secrets from the toml file
    collection, client = connect_to_mongodb()
    print("Connected to MongoDB successfully")
    
    # Fetch data and print DataFrame
    feedback_df = fetch_feedback_data()
    print("Fetched DataFrame:")
    print(feedback_df)

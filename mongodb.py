import pymongo
import pandas as pd
import streamlit as st
import subprocess

import pymongo
import streamlit as st

def connect_to_mongodb():
    """
    Connects to MongoDB and returns the collection and client objects.

    Returns:
        collection (pymongo.collection.Collection): The MongoDB collection object.
        client (pymongo.MongoClient): The MongoDB client object.
    """
    secrets = st.secrets["mongo"]
    conn_str = secrets["conn_str"]
    client = pymongo.MongoClient(conn_str)
    db = client.ClimbingGradeFeedback
    collection = db.ClimbingFeedbackStreamlit
    return collection, client

def fetch_feedback_data(save_to_csv=False, csv_path=None):
    try:
        collection, client = connect_to_mongodb()
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))
        client.close()
        print("Data fetched successfully")
        
        if save_to_csv and csv_path:
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


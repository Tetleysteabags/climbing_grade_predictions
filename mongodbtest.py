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

if __name__ == "__main__":
    load_secrets()  # Load secrets from the toml file
    collection, client = connect_to_mongodb()
    print("Connected to MongoDB successfully")

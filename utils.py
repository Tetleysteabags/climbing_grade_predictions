import pickle
import requests
import pymongo
import streamlit as st
import os

def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

import pymongo

def connect_to_mongodb_st():
    """
    Connects to MongoDB and returns the collection and client objects.

    Returns:
        collection (pymongo.collection.Collection): The MongoDB collection object.
        client (pymongo.MongoClient): The MongoDB client object.
    """
    try:
        conn_str = st.secrets["conn_str"]
        if not conn_str:
            raise ValueError("MongoDB connection string not found in Streamlit secrets")
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



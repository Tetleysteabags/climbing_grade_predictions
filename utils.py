# import pickle
# import requests
# import pymongo
# import streamlit as st

# def load_pickle_from_url(url):
#     response = requests.get(url)
#     return pickle.loads(response.content)

# def connect_to_mongodb():
#     secrets = st.secrets["mongo"]
#     conn_str = secrets["conn_str"]
#     client = pymongo.MongoClient(conn_str)
#     db = client.ClimbingGradeFeedback
#     collection = db.ClimbingFeedbackStreamlit
#     return collection, client

import pickle
import requests
import pymongo
import streamlit as st
import os  # Import os module for file operations

def load_pickle_from_url(url_or_path):
    if url_or_path.startswith("http"):
        response = requests.get(url_or_path)
        return pickle.loads(response.content)
    else:
        with open(url_or_path, "rb") as f:
            return pickle.load(f)

def connect_to_mongodb():
    secrets = st.secrets["mongo"]
    conn_str = secrets["conn_str"]
    client = pymongo.MongoClient(conn_str)
    db = client.ClimbingGradeFeedback
    collection = db.ClimbingFeedbackStreamlit
    return collection, client


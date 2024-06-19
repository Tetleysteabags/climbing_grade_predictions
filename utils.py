import pickle
import requests
import pymongo
import streamlit as st

def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

def connect_to_mongodb():
    secrets = st.secrets["mongo"]
    conn_str = secrets["conn_str"]
    client = pymongo.MongoClient(conn_str)
    db = client.ClimbingGradeFeedback
    collection = db.ClimbingFeedbackStreamlit
    return collection, client



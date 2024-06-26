import pickle
import requests
import pymongo
import streamlit as st
import os

def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

def connect_to_mongodb():
    conn_str = st.secrets["mongo"]["conn_str"]
    client = pymongo.MongoClient(conn_str)
    db = client.ClimbingGradeFeedback
    collection = db.ClimbingFeedbackStreamlit
    return collection, client


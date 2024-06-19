# tests/test_utils.py

import pytest
from utils import load_pickle_from_url, connect_to_mongodb

# Mock objects for testing (you may need to adjust based on your actual setup)
class MockResponse:
    def __init__(self, content):
        self.content = content

def test_load_pickle_from_url(monkeypatch):
    # Mocking requests.get() using monkeypatch
    def mock_get(url):
        return MockResponse(b"mocked pickle content")

    monkeypatch.setattr("requests.get", mock_get)
    
    # Test loading from URL
    result = load_pickle_from_url("http://example.com/mock.pkl")
    assert result == b"mocked pickle content"

def test_connect_to_mongodb(monkeypatch):
    # Mocking st.secrets["mongo"] using monkeypatch
    class MockSecrets:
        mongo = {"conn_str": "mock_connection_string"}
    
    class MockMongoClient:
        def __init__(self, conn_str):
            pass
        
        def __getitem__(self, key):
            return MockSecrets.mongo[key]

    monkeypatch.setattr("streamlit.secrets", MockSecrets)
    monkeypatch.setattr("pymongo.MongoClient", MockMongoClient)

    # Test connection function
    collection, client = connect_to_mongodb()
    assert collection.name == "ClimbingFeedbackStreamlit"


import os
import pymongo
import pymongo.errors
import pandas as pd

def connect_to_mongodb_fetch():
    """
    Connects to MongoDB and returns the collection and client objects.

    Returns:
        collection (pymongo.collection.Collection): The MongoDB collection object.
        client (pymongo.MongoClient): The MongoDB client object.
    """
    try:
        conn_str = os.getenv("CONN_STR")
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

def fetch_feedback_data(save_to_csv=False, csv_path=None):
    try:
        collection, client = connect_to_mongodb_fetch()
        print("Fetching data from MongoDB collection...")
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))
        client.close()
        print("Data fetched successfully")
        
        if save_to_csv and csv_path:
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

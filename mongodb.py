import os
import pymongo
import pandas as pd

def connect_to_mongodb():
    try:
        conn_str = os.getenv("MONGO_CONN_STR")
        if not conn_str:
            raise ValueError("MongoDB connection string not found in environment variables")
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

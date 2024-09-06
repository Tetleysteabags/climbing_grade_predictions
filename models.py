import pandas as pd
import numpy as np
import pickle
import requests

def load_pickle_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return pickle.loads(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error loading pickle file from URL: {e}")
        return None 
    except pickle.UnpicklingError as e:
        print(f"Error unpickling the file: {e}")
        return None

def prepare_input_features(sidebar):
    """
    Prepare input features for climbing ML project.

    Args:
        sidebar: The sidebar object used for user input.

    Returns:
        A pandas DataFrame containing the input features.

    """
    height = sidebar.number_input("Height (cm)", min_value=0, max_value=300, value=175, step=1, key="height")
    weight = sidebar.number_input("Weight (kg)", min_value=0.0, max_value=200.0, value=70.0, step=0.5, key="weight")
    max_pullups = sidebar.number_input("Max pullups in single go", min_value=0, max_value=200, value=10, step=1, key="max_pullups")
    max_hang_weight = sidebar.number_input("Max weight added to hang for 10 seconds from a 20mm edge (kg)", min_value=0.0, max_value=200.0, value=10.0, step=0.1, key="max_hang_weight")
    max_pullup_weight = sidebar.number_input("Max weight added to a single pullup (kg)", min_value=0.0, max_value=200.0, value=10.0, step=0.5, key="max_pullup_weight")
    continuous = sidebar.number_input("Continuous hang from 20mm edge (seconds)", min_value=1, max_value=1000, value=30, step=1, key="continuous")
    repeaters = sidebar.number_input("Hanging from 20mm edge, 7 seconds on, 3 seconds rest (total time in seconds)", min_value=0.0, max_value=1000.0, value=10.0, step=0.1, key="repeaters1")
    exp = sidebar.number_input("Years of climbing experience", min_value=0.0, max_value=70.0, value=5.0, step=0.5, key="exp")
    # days = sidebar.number_input("Number of days spent climbing each month", min_value=0, max_value=31, value=8, step=1, key="days")

    strength_to_weight_pullup = max_pullups / weight
    strength_to_weight_maxhang = (max_hang_weight + weight) / weight
    strength_to_weight_weightpull = (max_pullup_weight + weight) / weight

    data = {
        "strength_to_weight_pullup": strength_to_weight_pullup,
        "strength_to_weight_maxhang": strength_to_weight_maxhang,
        "strength_to_weight_weightpull": strength_to_weight_weightpull,
        "exp": exp,
        # "days": days,
        "continuous": continuous,
        "repeaters1": repeaters
        # "height": height,
        # "weight": weight,
    }

    return pd.DataFrame(data, index=[0])
    # return np.array(list(data.values())).reshape(1, -1)

def get_predictions_with_pipeline(input_df, bouldering_pipeline, sport_pipeline):
    """
    Get predictions for bouldering and sport climbing using the full pipelines.

    Args:
        input_df (pd.DataFrame): The input features.
        bouldering_pipeline: The full pipeline for bouldering.
        sport_pipeline: The full pipeline for sport climbing.

    Returns:
        Tuple: Predicted bouldering and sport climbing grades.
    """
    bouldering_prediction = bouldering_pipeline.predict(input_df)
    sport_prediction = sport_pipeline.predict(input_df)

    return bouldering_prediction[0], sport_prediction[0]



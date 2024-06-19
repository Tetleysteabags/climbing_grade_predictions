# tests/test_models.py

import pytest
import pandas as pd
from models import get_predictions

# Mock objects for testing
class MockModel:
    def predict(self, input_data):
        return [1.5]  # Mocking prediction output

class MockScaler:
    def transform(self, input_data):
        return input_data  # Mocking scaler transform output

def test_get_predictions():
    mock_input_df = pd.DataFrame({
        "strength_to_weight_pullup": [0.14],
        "strength_to_weight_maxhang": [1.5],
        "strength_to_weight_weightpull": [1.8],
        "continuous": [30],
        "exp": [5],
        "days": [8],
        "height": [175],
        "weight": [70],
    })

    mock_bouldering_model = MockModel()
    mock_sport_model = MockModel()
    mock_bouldering_scaler = MockScaler()
    mock_sport_scaler = MockScaler()

    bouldering_prediction, sport_prediction = get_predictions(
        mock_input_df, mock_bouldering_model, mock_bouldering_scaler,
        mock_sport_model, mock_sport_scaler
    )

    assert isinstance(bouldering_prediction, float)
    assert isinstance(sport_prediction, float)

 

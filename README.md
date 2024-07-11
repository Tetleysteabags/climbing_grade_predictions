
# Climbing Grade Predictions

This repository contains tools and data for predicting climbing grades using machine learning.

## Project Structure

- `climbing-performance-metrics-analysis.ipynb`: Jupyter Notebook for performance metrics analysis.
- `main.py`: Main script for the application.
- `models.py`: Handles model creation and training.
- `mongodb.py`: Manages MongoDB interactions.
- `retrain.py`: Script for retraining models.
- `utils.py`: Utility functions.
- `training_data/`: Contains training datasets.
- `pkl_files/`: Stores serialized model files.
- `requirements.txt`: Project dependencies.

## Project info

Can a machine learning model accurately predict sport climbing and bouldering grades based on a user’s strength metrics
- This project aims to determine the variables that most significantly influence climbing performance, and then trains a regression, random forest, and gradient boosting model using these variables
- MLflow is used to keep track of model performance.
- To learn about production, a simple front end is hosted on Streamlit where users can interact with the best performing model
- Users can input their strength metrics, and receive their predicted sport climbing and bouldering grades.
- In order to improve the models over time, users are requested to input their actual max sport climbing and bouldering grades.
- These values are then sent to MongoDB and retrieved to be used in re-training the models.


## Licensing
    
    This repository contains tools and data for predicting climbing grades using machine learning.
    Copyright (C) 2024 T. Georgiou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
# The Impact of Strength Metrics on Climbing Performance

## Overview

In recent years, companies such as Lattice have started using data analytics to inform climbers about their potential weaknesses, aiming to personalize training plans for improved long-term performance. This project aims to build upon that concept by using a dataset from Power Company Climbing, which contains metrics from around 600 self-reported members. I have applied machine learning models to determine the factors that most significantly influence climbing performance and split the data into bouldering and sport climbing as these are two separate aspects of climbing and require different strengths.

The project involved generating a script to pre-process and prepare the data, calculating relationships and coefficients between variables, testing different ML models to find the best performing model, and creating a Streamlit application where users can interact with the model. 

In order to improve the model, users are requested to input their actual max climbing and max sport grades. These actual values are then sent to MongoDB where they are stored to be used in re-training and improving the ML models.

I decided to work on this project as a learning experience where I could understand the entire end to end workflow of a data science project including data preprocessing, model training, predictions and model improvement.


## Usage

Open the Streamlit app in your browser: https://climbing-performance-forecast.streamlit.app/
Use the sidebar to input your climbing stats.
Get instant predictions for your max bouldering and sport climbing grades.
Optionally, input your actual max grades for both categories to help improve the model.

## Features
Machine Learning Models: Random Forest and Gradient Boosting models trained on a dataset from Power Company Climbing.
Real-Time Predictions: Get real-time climbing grade predictions based on various metrics.
User Feedback: Allows users to provide feedback by entering their actual grades, which is then stored in MongoDB for future model improvement.

## Technologies used
Python
Streamlit
MongoDB


Pull requests and feedback are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments
Thanks to Power Company Climbing for providing the dataset.
Inspired by the analytics work done by Lattice.
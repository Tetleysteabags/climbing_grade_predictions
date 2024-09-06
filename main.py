import streamlit as st
import pandas as pd
from mongodb import connect_to_mongodb, save_feedback
from models import get_predictions_with_pipeline, prepare_input_features,load_pickle_from_url
from grade_conversions import convert_numeric_to_v_grade, convert_numeric_to_f_grade

def main():
    """
    A Streamlit application for predicting climbing grades based on user input and collecting feedback.

    The application loads pre-trained machine learning models and scalers, takes user input for climbing stats,
    predicts the maximum bouldering and sport climbing grades, converts the predictions to readable grades,
    displays the predicted grades, and collects feedback from the user.

    The feedback data is stored in a MongoDB database and will be used to improve the model and future predictions.

    Returns:
        None
    """

    # Load models and pipelines
    bouldering_pipeline_url = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/full_pipeline_rf_bouldering.pkl"
    sport_pipeline_url = "https://raw.githubusercontent.com/Tetleysteabags/climbing_grade_predictions/main/pkl_files/full_pipeline_rf_sport.pkl"

    bouldering_pipeline = load_pickle_from_url(bouldering_pipeline_url)
    sport_pipeline = load_pickle_from_url(sport_pipeline_url)
    
    # Sidebar for user input
    st.sidebar.header("Enter your climbing stats")
    input_df = prepare_input_features(st.sidebar)

    # Get predictions using the full pipeline (which includes scaling and prediction)
    bouldering_prediction, sport_prediction = get_predictions_with_pipeline(input_df, bouldering_pipeline, sport_pipeline)
    

    # Convert predictions to readable grades
    bouldering_predicted_grade = convert_numeric_to_v_grade(bouldering_prediction)
    sport_predicted_grade = convert_numeric_to_f_grade(sport_prediction)

    # Display predictions
    # Insert an image
    st.image("https://www.patagonia.com/blog/wp-content/uploads/2020/11/etzel_k_1399_cc_web-1280x720-1.jpg", use_column_width=True)
    st.header("Predicted grades based on your climbing metrics")

    # Regular subheader
    st.markdown("<h5 style='color:white;'>Open the sidebar on the left to input your strength metrics.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:white;'>Please note that these are just predictions and may not be accurate for everyone.</h5>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:grey;'>Boulder Grade: {bouldering_predicted_grade}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:grey;'>Sport Grade: {sport_predicted_grade}</h3>", unsafe_allow_html=True)
    
    # Insert an image
    st.image("https://gripped.com/wp-content/uploads/2022/02/LT11_Jess-Talley_adidasTerrex_BrookeRaboutou_3-1.jpg", use_column_width=True)

    # Feedback section
    st.header("Feedback to improve future predictions")
    # Dropdowns for actual grades
    actual_bouldering_grade = st.selectbox("Enter your actual max bouldering grade:", ["<V3", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16", "I have not pursued bouldering in the past year"])
    actual_sport_grade = st.selectbox("Enter your actual max sport grade:", ["4c", "5a", "5b", "5c", "6a", "6a+", "6b", "6b+", "6c", "6c+", "7a", "7a+", "7b", "7b+", "7c", "7c+", "8a", "8a+", "8b", "8b+", "8c", "8c+", "9a", "9a+", "9b", "9b+", "9c", "I have not pursued sport climbing in the past year"])

    
    # Submit feedback
    if st.button("Submit Feedback"):
        feedback_data = {
            **input_df.to_dict(orient="records")[0],
            "predicted_bouldering_grade": bouldering_predicted_grade,
            "actual_bouldering_grade": actual_bouldering_grade,
            "predicted_sport_grade": sport_predicted_grade,
            "actual_sport_grade": actual_sport_grade
        }
        save_feedback(feedback_data, is_streamlit=True)
        st.success("Thank you for your feedback! This will be used to improve the model and future predictions.")


if __name__ == "__main__":
    main()

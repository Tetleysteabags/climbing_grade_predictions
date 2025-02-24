import pandas as pd
from grade_conversions import convert_v_grade_to_numeric, conversion_map_french, sex_dict, convert_to_french_grade
from sklearn.impute import KNNImputer


def load_and_preprocess_original_data():
    """
    Load the original dataset, drop unnecessary columns, and return the cleaned dataframe.
    """
    # Read the data file using pandas, specifying the encoding
    original_data = pd.read_csv(r'original_data_files/PowerCompanyAssessmentData.csv', encoding="cp1252")

    # Display the first few rows of the dataframe to check everything is in order
    print("Original Data Columns:")
    print(original_data.columns)

    # Drop the "country", "state", and "rock" columns from the dataframe
    data = original_data.drop(columns=["country", "state", "rock"])
    
    # Transform variables from the imperial to the metric system
    data['height'] = data['height'] * 2.54  # convert inches to centimeters
    data['weight'] = data['weight'] * 0.45359237  # convert pounds to kilograms
    data['ohpr'] = data['ohpr'] * 0.45359237  # convert pounds to kilograms
    data['ohll'] = data['ohll'] * 0.45359237  # convert pounds to kilograms
    data['dl'] = data['dl'] * 0.45359237  # convert pounds to kilograms
    data['span'] = data['span'] * 2.54  # convert inches to centimeters
    data['weightedpull'] = data['weightedpull'] * 0.45359237  # convert pounds to kilograms
    data['maxhang'] = data['maxhang'] * 0.45359237  # convert pounds to kilograms
    
    # Convert sex data to numeric using dictionary from above
    data["sex"] = data["sex"].map(sex_dict)

    # Create new variables representing strength-to-weight ratios for different physical activities
    data['strength_to_weight_pullup'] = data['pullup'] / data['weight']
    data['strength_to_weight_weightpull'] = (data['weightedpull'] + data['weight']) / data['weight']
    data['strength_to_weight_maxhang'] = (data['maxhang'] + data['weight']) / data['weight']

    # Coerce any errors during conversion of 'continuous' column to a numeric type to NaN
    data['continuous'] = pd.to_numeric(data['continuous'], errors='coerce')
    
    # Apply max boulder and max sport conversions to the original dataset
    data['max_boulder_numeric'] = data['max_boulder'].apply(convert_v_grade_to_numeric)
    
    print(data['max_sport'].unique())  # Check unique values in the max_sport column

    data['max_sport_french'] = data['max_sport'].apply(convert_to_french_grade)

    # Check which values were not converted properly
    unknown_grades = data[data['max_sport_french'].isna()]['max_sport'].unique()
    print("Unknown Grades:", unknown_grades)

    data['max_sport_numeric'] = data['max_sport_french'].map(conversion_map_french)

    # Print rows where conversion failed
    print(data[data['max_sport_french'].isna()][['max_sport']])
    
    # Print the dataframe again to confirm the columns have been dropped
    print("\nData Columns After Dropping:")
    print(data.columns)

    return data

def load_and_preprocess_new_responses():
    """
    Load the new responses dataset, apply conversions, calculate strength-to-weight ratios,
    and impute missing values for specific columns.
    """
    # Import new CSV file
    new_responses = pd.read_csv('original_data_files/Climbharder #V3 (Responses) - final sheet.csv')

    # Apply the max boulder to max boulder numeric dictionary to the new data
    new_responses['max_boulder_numeric'] = new_responses['max_boulder'].apply(convert_v_grade_to_numeric)
    # Map the French grades to numerical values
    new_responses['max_sport_numeric'] = new_responses['max_sport'].map(conversion_map_french)

    # Convert sex data to numeric using dictionary from above
    new_responses["sex"] = new_responses["sex"].map(sex_dict)

    # Create strength-to-weight ratios
    new_responses['strength_to_weight_pullup'] = new_responses['pullup'] / new_responses['weight']
    new_responses['strength_to_weight_weightpull'] = (new_responses['weightedpull'] + new_responses['weight']) / new_responses['weight']
    new_responses['strength_to_weight_maxhang'] = (new_responses['maxhang'] + new_responses['weight']) / new_responses['weight']

    return new_responses

def add_missing_columns(new_responses, original_data):
    """
    Add missing columns to the new responses dataset to match the columns in the original dataset.

    Parameters:
    new_responses (DataFrame): The cleaned new responses dataset.
    original_data (DataFrame): The cleaned original dataset.

    Returns:
    DataFrame: The new responses dataset with missing columns added (filled with NaN).
    """
    # Identify columns in the original dataset that are missing in the new responses dataset
    missing_columns = set(original_data.columns) - set(new_responses.columns)

    # Add missing columns to the new responses dataset, filled with NaN
    for column in missing_columns:
        new_responses[column] = None

    return new_responses


def merge_datasets(original_data, new_responses):
    """
    Merges the original dataset with the new responses dataset.

    Parameters:
    original_data (DataFrame): The cleaned original dataset.
    new_responses (DataFrame): The cleaned new responses dataset.

    Returns:
    DataFrame: A merged dataframe containing all values from both datasets.
    """
    # Add missing columns to the new responses dataset
    new_responses = add_missing_columns(new_responses, original_data)

    # Perform a full outer join on all columns
    merged_data = pd.concat([original_data, new_responses], ignore_index=True)

    return merged_data


def impute_missing_values(data):
    """
    Impute missing values for specified columns using KNN Imputer.

    Parameters:
    data (DataFrame): The dataset to impute missing values.

    Returns:
    DataFrame: The dataset with imputed values.
    """
    # Define columns to impute
    columns_to_impute = ['strength_to_weight_pullup', 'strength_to_weight_weightpull', 
                         'strength_to_weight_maxhang', 'continuous', 'repeaters1']

    # Impute missing values using KNN Imputer
    imputer = KNNImputer(n_neighbors=5)
    data[columns_to_impute] = imputer.fit_transform(data[columns_to_impute])
    
    return data

def convert_to_french_grade(grade):
    # Example conversion logic
    conversion_map = {
        '5.10a': '6a',
        '5.10b': '6a+',
        '5.10c': '6b',
        # Add more mappings as needed
    }
    return conversion_map.get(grade, 'Unknown')

def main():
    """
    Main function to load and preprocess both datasets.
    """
    # Load and preprocess the original dataset
    original_data_cleaned = load_and_preprocess_original_data()

    # Load and preprocess the new responses dataset
    new_responses_cleaned = load_and_preprocess_new_responses()

    # Display the first few rows of the cleaned datasets
    print("\nCleaned Original Data:")
    print(original_data_cleaned.head())

    print("\nCleaned New Responses Data:")
    print(new_responses_cleaned.head())

    # Merge the datasets
    merged_data = merge_datasets(original_data_cleaned, new_responses_cleaned)

    # Impute missing values in the merged dataset
    merged_data = impute_missing_values(merged_data)

    # Display the first few rows of the merged and imputed dataset
    print("\nMerged and Imputed Data:")
    print(merged_data.head())
    
     # Save the datasets to CSV files
    original_data_cleaned.to_csv('training_data/original_data_cleaned.csv', index=False)
    new_responses_cleaned.to_csv('training_data/new_responses_cleaned.csv', index=False)
    merged_data.to_csv('training_data/merged_data.csv', index=False)

if __name__ == "__main__":
    main()
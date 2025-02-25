import numpy as np
import pandas as pd
import logging

# Bouldering conversion map
conversion_map_boulder = {
    "<V3": 1, "V3": 2, "V4": 3, "V5": 4, "V6": 5, "V7": 6, "V8": 7,
    "V9": 8, "V10": 9, "V11": 10, "V12": 11, "V13": 12, "V14": 13,
    "V15": 14, "V16": 15, "I have not pursued bouldering in the past year": 0
}
inverse_conversion_map_v = {v: k for k, v in conversion_map_boulder.items()}

def convert_numeric_to_v_grade(numeric_grade):
    """
    Converts a numeric grade to a V-grade in climbing.

    Parameters:
    numeric_grade (int): The numeric grade to be converted.

    Returns:
    str: The corresponding V-grade in climbing. If the numeric grade is not found in the conversion map, "Unknown grade" is returned.
    """
    numeric_grade = round(numeric_grade)
    return inverse_conversion_map_v.get(numeric_grade, "Unknown grade")


# define a function to convert V Grade bouldering to numeric
def convert_v_grade_to_numeric(grade):
    if grade in conversion_map_boulder:  # check if the grade is in the conversion map
        return conversion_map_boulder[grade]  # convert the grade to numeric
    else:
        return np.nan  # return NaN for unknown or unclassifiable grades



def convert_to_french_grade(grade):
    conversion_map = {
        "<5.10": "4c",
        "5.10": "5a", "5.10a": "5b", "5.10b": "5c",
        "5.10c": "5c", "5.10d": "6a", "5.11a": "6a",
        "5.11b": "6a+", "5.11c": "6b", "5.11d": "6b+",
        "5.12a": "6c", "5.12b": "6c+", "5.12c": "7a",
        "5.12d": "7a+", "5.13a": "7b", "5.13b": "7b+",
        "5.13c": "7c", "5.13d": "7c+", "5.14a": "8a",
        "5.14b": "8a+", "5.14c": "8b", "5.14d": "8b+",
        "5.15a": "8c", "5.15b": "8c+", "5.15c": "9a",
        "5.15d": "9a+", 
        "I have not pursued sport climbing goals outside in the past year": "0"
    }

    if pd.isnull(grade):  
        return np.nan  

    grade = str(grade).strip()  # Ensure it's a string and remove extra spaces

    # If the grade contains a range (e.g., "5.12a/b", "5.12c/d", "5.10a-b"),
    # take the second/harder grade
    if "/" in grade or "-" in grade:
        grade = grade.split("/")[-1].split("-")[-1].strip()  # Take the last part

    result = conversion_map.get(grade, "Unknown")
    
    print(f"Original: {grade} -> Mapped: {result}")  # Debug output

# convert French grades to numerical values
conversion_map_french = {
    '4c': 1, '5a': 2, '5b': 3, '5c': 4, '6a': 5,
    '6a+': 6, '6b': 7, '6b+': 8, '6c': 9, '6c+': 10, '7a': 11,
    '7a+': 12, '7b': 13, '7b+': 14, '7c': 15, '7c+': 16, '8a': 17,
    '8a+': 18, '8b': 19, '8b+': 20, '8c': 21, '8c+': 22, '9a': 23, '9a+': 24, '0': 0
}

def convert_f_grade_to_numeric(grade):
    # map of V grades to numerical values
    conversion_map_french = {
    '4c': 1, '5a': 2, '5b': 3, '5c': 4, '6a': 5,
    '6a+': 6, '6b': 7, '6b+': 8, '6c': 9, '6c+': 10, '7a': 11,
    '7a+': 12, '7b': 13, '7b+': 14, '7c': 15, '7c+': 16, '8a': 17,
    '8a+': 18, '8b': 19, '8b+': 20, '8c': 21, '8c+': 22, '9a': 23, '9a+': 24, '0': 0
}
    if grade in conversion_map_french:  # check if the grade is in the conversion map
        return conversion_map_french[grade]  # convert the grade to numeric
    else:
        return np.nan  # return NaN for unknown or unclassifiable grades
    

# create dictionaries to map experience, season, and days climbing to numeric values so we can use these if needed in our models
experience_dict = { "< 1 year":1,"<1 year":1,"1-2 years":2,"3-4 years":3,"5-6 years":4,"7-8 years":5,
                   "9-10 years":6, ">10 years":7, "> 10 years":8}
season_dict = {"1-3 months":1,"4-6 months":2,"7-9 months":3,"Year round":4}
days_dict = {'3-4 days per month':3, '5-6 days per month':4, '1-5 days per month':5,
       '7-8 days per month':6, '>10 days per month':7, '>15 days per month':8,
             '9-10 days per month':9, 'I currently do no climb outdoors':1, '15-20':10,}
sex_dict = {'Male':1, 'Female':2, 'Other/Prefer to Not Answer':3,'Other':3,'0':3, 'NaN':3}
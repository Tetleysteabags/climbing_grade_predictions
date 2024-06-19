# Bouldering conversion map
conversion_map_boulder = {
    "<V3": 1, "V3": 2, "V4": 3, "V5": 4, "V6": 5, "V7": 6, "V8": 7,
    "V9": 8, "V10": 9, "V11": 10, "V12": 11, "V13": 12, "V14": 13,
    "V15": 14, "V16": 15, "I have not pursued bouldering goals outside in the past year": 0
}
inverse_conversion_map_v = {v: k for k, v in conversion_map_boulder.items()}

def convert_numeric_to_v_grade(numeric_grade):
    numeric_grade = round(numeric_grade)
    return inverse_conversion_map_v.get(numeric_grade, "Unknown grade")

# Sport climbing conversion map
conversion_map_french = {
    "4c": 1, "5a": 2, "5b": 3, "5c": 4, "6a": 5, "6a+": 6, "6b": 7, "6b+": 8, 
    "6c": 9, "6c+": 10, "7a": 11, "7a+": 12, "7b": 13, "7b+": 14, "7c": 15, 
    "7c+": 16, "8a": 17, "8a+": 18, "8b": 19, "8b+": 20, "8c": 21, "8c+": 22, 
    "9a": 23, "9a+": 24, "0": 0
}
inverse_conversion_map_f = {v: k for k, v in conversion_map_french.items()}

def convert_numeric_to_f_grade(numeric_grade):
    numeric_grade = round(numeric_grade)
    return inverse_conversion_map_f.get(numeric_grade, "Unknown grade")

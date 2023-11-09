import pandas as pd
import json

def dataframe_metadata_to_json(df):
    """
    Analyze a DataFrame and produce a JSON with column names, data types, and allowed type conversions.

    Parameters:
    df (pd.DataFrame): DataFrame to analyze.

    Returns:
    str: JSON string with metadata.
    """
    # Does not exceed the number of rows in the data
    sample_size = min(200, len(df))

    metadata = {
        "columnNames": list(df.columns),
        "datatype": [str(df[col].dtype) for col in df.columns],
        "data": df.head(sample_size).to_dict(orient='records'),
        "type_conversion": {col: possible_conversions(str(df[col].dtype)) for col in df.columns}
    }

    return json.dumps(metadata, indent=2)

def possible_conversions(dtype):
    """
    Allowed data type conversions based on the current data type. For example, string can not be numeric

    Parameters:
    dtype (str): Current data type of a column.

    Returns:
    list: List of possible conversions.
    """
    conversion_map = {
        "int64": ["bool", "string"],
        "float64": ["bool", "string"],
        "object": ["bool", "numeric"],  
        "bool": ["numeric", "string"]
    }
    
    return conversion_map.get(dtype, [])

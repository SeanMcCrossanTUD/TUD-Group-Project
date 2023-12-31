import pandas as pd
import json
import numpy as np

def convert_numpy_to_python(data):
    if isinstance(data, (np.int_, np.intc, np.intp, np.int8,
                         np.int16, np.int32, np.int64, np.uint8,
                         np.uint16, np.uint32, np.uint64)):
        return int(data)
    elif isinstance(data, (np.float_, np.float16, np.float32, np.float64)):
        return float(data) if not np.isnan(data) else None
    elif isinstance(data, (np.ndarray,)):
        return data.tolist()
    elif isinstance(data, dict):
        return {k: convert_numpy_to_python(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_python(item) for item in data]
    else:
        return data

def attempt_convert_to_dates(df):
    """
    Attempts to convert DataFrame fields to dates.

    Parameters:
    df (pd.DataFrame): DataFrame to process.

    Returns:
    pd.DataFrame: DataFrame with converted date fields where possible.
    """
    for col in df.columns:
        try:
            converted_col = pd.to_datetime(df[col], errors='coerce')
            # Check if conversion was successful (non-NaT values should exist)
            if converted_col.notna().any():
                df[col] = converted_col
                print(f"{col} converted to datetime: {e}")
        except Exception as e:
            print(f"Could not convert column {col} to datetime: {e}")
    return df

def dataframe_metadata_to_json(df):
    """
    Analyze a DataFrame and produce a JSON with column names, data types, and allowed type conversions.

    Parameters:
    df (pd.DataFrame): DataFrame to analyze.

    Returns:
    str: JSON string with metadata.
    """
    # Mapping from Python data types to user-friendly types
    type_mapping = {
        'object': 'Text',
        'float64': 'Numeric',
        'int64': 'Numeric',
        'bool': 'Boolean'
    }

    # Does not exceed the number of rows in the data
    sample_size = min(500, len(df))

    df_filtered = df.head(sample_size).fillna(value="")

    data_dict = df_filtered.to_dict(orient='records')

    metadata = {
        "columnNames": list(df.columns),
        "datatype": [type_mapping.get(str(df[col].dtype), str(df[col].dtype)) for col in df.columns],
        "data": data_dict,
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

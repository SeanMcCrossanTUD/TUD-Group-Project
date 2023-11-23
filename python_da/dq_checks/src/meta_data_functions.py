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

    # Convert DataFrame to a format suitable for JSON serialization
    data_dict = df.head(sample_size).applymap(convert_numpy_to_python).to_dict(orient='records')

    metadata = {
        "columnNames": list(df.columns),
        "datatype": [str(df[col].dtype) for col in df.columns],
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

import pandas as pd
import json
import numpy as np
from dq_checks.src.meta_data_functions import dataframe_metadata_to_json, possible_conversions

def test_dataframe_metadata_to_json():
    data = {
        'int_col': [1, 2, 3],
        'float_col': [1.1, 2.2, 3.3],
        'bool_col': [True, False, True],
        'text_col': ['text1', 'text2', 'text3'],
        'mixed_col': ['1text', '2.5', 'three'],
        'missing_col': [1, None, 3]
    }
    df = pd.DataFrame(data)

    # Convert df to JSON for comparison
    actual_metadata_json = dataframe_metadata_to_json(df)

    # Expected metadata
    expected_metadata = {
        "columnNames": ['int_col', 'float_col', 'bool_col', 'text_col', 'mixed_col', 'missing_col'],
        "datatype": ['int64', 'float64', 'bool', 'object', 'object', 'float64'],
        "data": df.head(3).fillna(value="").to_dict(orient='records'),  
        "type_conversion": {
            'int_col': ["bool", "string"],
            'float_col': ["bool", "string"],
            'bool_col': ["numeric", "string"],
            'text_col': ["bool", "numeric"],
            'mixed_col': ["bool", "numeric"],
            'missing_col': ["bool", "string"]
        }
    }

    # Convert expected_metadata to JSON for comparing
    expected_metadata_json = json.dumps(expected_metadata, indent=2)

    # Testing
    assert actual_metadata_json == expected_metadata_json


def test_possible_conversions():
    assert possible_conversions("int64") == ["bool", "string"]
    assert possible_conversions("float64") == ["bool", "string"]
    assert possible_conversions("object") == ["bool", "numeric"]
    assert possible_conversions("bool") == ["numeric", "string"]
    assert possible_conversions("nonexistent_type") == []



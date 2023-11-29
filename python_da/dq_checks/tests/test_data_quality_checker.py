import pandas as pd
import pytest
from dq_checks.src.data_quality_checker import DataQualityChecker

# Sample data for testing
data = {
    'A': [1, 2, None, 4, 1, 5, 5],  
    'B': [None, 2, 3.2, 4, 2, None, None],  
    'C': [1, 2.1, 3, 4, 1, 5, 5],
    'D': ['Cat', 'Dog', 'Cat', 'Cow', None, 'Dog', 'Dog'],
    'E': ['Bike', None, 'Bus', 'Car', None, 'Train', 'Train']
}

expected_data_type_profile = {
    'float64': 3,
    'object': 2
}

# Expected result for missing values count
expected_missing_values_result = {'A': 1, 'B': 3, 'C': 0, 'D': 1, 'E': 2}

# Expected result for number of records count
expected_records_count = 7

# Expected result for duplicate values count
expected_duplicate_values_count = 1  

# Expected result for unique values count in text fields
expected_unique_values_result = {'D': 3, 'E': 4}

# Expected result for number of fields count
expected_fields_count = 5

@pytest.fixture
def checker():
    dataset = pd.DataFrame(data)
    return DataQualityChecker(dataset)


# Test function to check count_missing_values method
def test_count_missing_values(checker):
    assert checker.count_missing_values() == expected_missing_values_result

# Test function to check count_number_of_records method
def test_count_number_of_records(checker):
    assert checker.count_number_of_records() == expected_records_count

# Test function to check count_duplicate_values method
def test_count_duplicate_values(checker):
    assert checker.count_duplicate_values() == expected_duplicate_values_count

# Test function to check count_unique_values_in_text_fields method
def test_count_unique_values_in_text_fields(checker):
    assert checker.count_unique_values_in_text_fields() == expected_unique_values_result

# Test function to check count_number_of_fields method
def test_count_number_of_fields(checker):
    assert checker.count_number_of_fields() == expected_fields_count

# Test function for data_type_profile
def test_data_type_profile(checker):
    assert checker.data_type_profile() == expected_data_type_profile

# Sample data for testing z_score_outliers
outlier_data = {
    'A': [1, 2, 3, 4, 5, 100],  # 100 is an outlier
    'B': [1, 1, 1, 1, 1, 10],   # 10 is an outlier
    'C': [10, 20, 30, 40, 50, -100], # -100 is an outlier
    'D': ['Cat', 'Dog', 'Cat', 'Cow', None, 'Dog'], 
}

# Expected result for z_score_outliers
expected_z_outliers_result = {
    'A': [
        {
            "row": 5,
            "field": 'A',
            "value": 100,
            "z_score": 2.234643427783634,
            "is_outlier": True,
            "threshold": 2
        }
    ],
    'B': [
        {
            "row": 5,
            "field": 'B',
            "value": 10,
            "z_score": 2.23606797749979,  # actual value
            "is_outlier": True,
            "threshold": 2
        }
    ],
    'C': [
        {
            "row": 5,
            "field": 'C',
            "value": -100,
            "z_score": 2.1606731097722345,  # actual value
            "is_outlier": True,
            "threshold": 2
        }
    ]
}

# Expected result for IQR outliers
expected_iqr_outliers_result = {
    'A': [
        {'row': 5, 'field': 'A', 'value': 100, 'is_outlier': True, 'lower_bound': -1.5, 'upper_bound': 8.5}
    ],
    'B': [
        {'row': 5, 'field': 'B', 'value': 10, 'is_outlier': True, 'lower_bound': 1.0, 'upper_bound': 1.0}
    ],
    'C': [
        {'row': 5, 'field': 'C', 'value': -100, 'is_outlier': True, 'lower_bound': -25.0, 'upper_bound': 75.0}
    ]
}

# Fixture to initialize DataQualityChecker with z_data for testing z_score_outliers
@pytest.fixture
def outlier_checker():
    dataset = pd.DataFrame(outlier_data)
    return DataQualityChecker(dataset)

# def test_z_score_outliers(outlier_checker):
#     actual_outliers = outlier_checker.z_score_outliers(threshold=2)
    
#     # Filtering actual_outliers to include only those marked as outliers
#     filtered_actual_outliers = {}
#     for col, outliers in actual_outliers.items():
#         filtered_actual_outliers[col] = [outlier for outlier in outliers if outlier['is_outlier']]

#     assert filtered_actual_outliers == expected_z_outliers_result


# Test function to check iqr_outliers method
def test_iqr_outliers(outlier_checker):
    assert outlier_checker.iqr_outliers(k=1.5) == expected_iqr_outliers_result

# Fixture for a test dataframe
@pytest.fixture
def text_data_dataframe():
    return pd.DataFrame({
        'TextColumn1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL',
                        'MM', 'NN', 'OO', 'PP', 'QQ', 'RR', 'SS', 'TT', 'UU', 'VV', 'WW', 'XX'] + ['YY'] * 10,
        'TextColumn2': ['Alpha', 'Beta', 'Gamma', 'Delta'] * 15
    })

# Test for the unique value frequencies function
def test_count_unique_value_frequencies_in_text_fields(text_data_dataframe):
    dq_checker = DataQualityChecker(text_data_dataframe)
    result = dq_checker.count_unique_value_frequencies_in_text_fields()

    # Test if the function identifies all text fields
    assert set(result['text_fields']) == {'TextColumn1', 'TextColumn2'}

    # Test if the function correctly counts unique values
    assert len(result['value_counts']['TextColumn1']) == 51  # 50 unique values + 'other values'
    assert result['value_counts']['TextColumn1']['YY'] == 10
    assert 'other values' in result['value_counts']['TextColumn1']
    assert result['value_counts']['TextColumn2'] == {'Alpha': 15, 'Beta': 15, 'Gamma': 15, 'Delta': 15}

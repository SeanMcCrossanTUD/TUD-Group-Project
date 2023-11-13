import pandas as pd
import pytest
from dq_checks.src.data_quality_checker import DataQualityChecker

# Sample data for testing
data = {
    'A': [1, 2, None, 4, 1, 5, 5],  
    'B': [None, 2, 3.2, 4, 2, None, None],  
    'C': [1, 2, 3, 4, 1, 5, 5],
    'D': ['Cat', 'Dog', 'Cat', 'Cow', None, 'Dog', 'Dog'],
    'E': ['Bike', None, 'Bus', 'Car', None, 'Train', 'Train']
}

# Expected result for data type profile
expected_data_type_profile = {
    'int64': 3,
    'float64': 1,
    'object': 1
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

# Fixture to initialize DataQualityChecker with sample data
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

# Test function to check z_score_outliers method
def test_z_score_outliers(outlier_checker):
    assert outlier_checker.z_score_outliers(threshold=2) == expected_z_outliers_result

# Test function to check iqr_outliers method
def test_iqr_outliers(outlier_checker):
    assert outlier_checker.iqr_outliers(k=1.5) == expected_iqr_outliers_result


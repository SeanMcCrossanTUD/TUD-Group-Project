import pandas as pd
import pytest
from src.data_quality_checker import DataQualityChecker

# Sample data for testing
data = {
    'A': [1, 2, None, 4, 1, 5, 5],  
    'B': [None, 2, 3, 4, 2, None, None],  
    'C': [1, 2, 3, 4, 1, 5, 5],
    'D': ['Cat', 'Dog', 'Cat', 'Cow', None, 'Dog', 'Dog'],
    'E': ['Bike', None, 'Bus', 'Car', None, 'Train', 'Train']
}


# Expected result for missing values count
expected_missing_values_result = {'A': 1, 'B': 3, 'C': 0, 'D': 1, 'E': 2}

# Expected result for number of records count
expected_records_count = 7

# Expected result for duplicate values count
expected_duplicate_values_count = 1  

# Expected result for unique values count in text fields
expected_unique_values_result = {'D': 3, 'E': 4}

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
import pandas as pd
import pytest
from src.data_quality_checker import DataQualityChecker

# Sample data for testing
data = {
    'A': [1, 2, None, 4],
    'B': [None, 2, 3, 4],
    'C': [1, 2, 3, 4]
}

# Expected result for missing values count
expected_result = {'A': 1, 'B': 1, 'C': 0}

# Fixture to initialize DataQualityChecker with sample data
@pytest.fixture
def checker():
    dataset = pd.DataFrame(data)
    return DataQualityChecker(dataset)

# Test function to check count_missing_values method
def test_count_missing_values(checker):
    assert checker.count_missing_values() == expected_result
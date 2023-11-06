import pandas as pd
import numpy as np
from data_prep import DataPrep  # Replace 'your_module' with the name of your actual module
import pytest

# Sample dataframe for testing
@pytest.fixture
def test_dataframe():
    return pd.DataFrame({
        'A': [1, np.nan, 3, 4, 5],
        'B': [np.nan, 2, 3, 4, np.nan],
        'C': [10, 20, 30, 40, 50]
    })

# Tests for fill_missing_values method
def test_fill_missing_values_mode(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.fill_missing_values('A', method='mode')
    assert result['A'].isnull().sum() == 0
    assert result['A'][1] == 1  # Assuming mode is 1 for column 'A'

def test_fill_missing_values_mean(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.fill_missing_values('A', method='mean')
    assert result['A'].isnull().sum() == 0
    assert result['A'][1] == np.mean([1, 3, 4, 5])

def test_fill_missing_values_median(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.fill_missing_values('A', method='median')
    assert result['A'].isnull().sum() == 0
    assert result['A'][1] == np.median([1, 3, 4, 5])

def test_fill_missing_values_specific(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.fill_missing_values('A', method='specific', specific_value=10)
    assert result['A'].isnull().sum() == 0
    assert result['A'][1] == 10

def test_fill_missing_values_remove(test_dataframe):
    dp = DataPrep(test_dataframe)
    original_len = len(test_dataframe)
    result = dp.fill_missing_values('A', method='remove')
    assert len(result) == original_len - 1

# Tests for remove_outliers method
def test_remove_outliers(test_dataframe):
    # Create a dataframe with a clear outlier
    df = pd.DataFrame({'A': [1, 2, 3, 100, 5]})
    dp = DataPrep(df)
    
    # Store a copy of the original dataframe for comparison
    original_df = dp.dataframe.copy()

    # Apply the remove_outliers method
    dp.remove_outliers(sd=2)  # Assuming 2 SD removes the outlier 100

    # Check if the dataframe has changed after removing outliers
    assert not dp.dataframe.equals(original_df), "Dataframe should have changed after outlier removal"

# Tests for normalize_data method
def test_normalize_data_min_max(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.normalize_data('C', method='min-max')
    min_val, max_val = test_dataframe['C'].min(), test_dataframe['C'].max()
    expected = (test_dataframe['C'] - min_val) / (max_val - min_val)
    pd.testing.assert_series_equal(result['C'], expected, check_dtype=False)


def test_normalize_data_z_score(test_dataframe):
    dp = DataPrep(test_dataframe)
    result = dp.normalize_data('C', method='z-score')
    mean_val, std_val = test_dataframe['C'].mean(), test_dataframe['C'].std()
    expected = (test_dataframe['C'] - mean_val) / std_val
    pd.testing.assert_series_equal(result['C'], expected, check_dtype=False)

# Test successful column renaming
def test_rename_column_success(test_dataframe):
    dp = DataPrep(test_dataframe)
    old_name, new_name = 'A', 'X'
    result = dp.rename_column(old_name, new_name)
    assert new_name in result.columns
    assert old_name not in result.columns

# Test renaming with invalid new name
def test_rename_column_invalid_new_name(test_dataframe):
    dp = DataPrep(test_dataframe)
    old_name, new_name = 'A', 123  # Non-string new name
    with pytest.raises(ValueError):
        dp.rename_column(old_name, new_name)




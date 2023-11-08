import pandas as pd
import numpy as np
import re
from data_prep.src.data_prep import DataPrep 

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

# Fixture for a test dataframe
@pytest.fixture
def text_dataframe():
    return pd.DataFrame({
        'Text': ['Hello@World!', 'Test123', 'No$Special#Characters'],
        'Numbers': [1, 2, 3]
    })

# Test successful removal of special characters
def test_remove_special_characters_success(text_dataframe):
    dp = DataPrep(text_dataframe)
    column_name = 'Text'
    dp.remove_special_characters(column_name)
    assert dp.dataframe[column_name].equals(pd.Series(['HelloWorld', 'Test123', 'NoSpecialCharacters']))

# Test removing special characters from a non-existent column
def test_remove_special_characters_non_existent_column(text_dataframe):
    dp = DataPrep(text_dataframe)
    with pytest.raises(ValueError):
        dp.remove_special_characters('NonExistentColumn')

# Test removing special characters from a non-text column
def test_remove_special_characters_non_text_column(text_dataframe):
    dp = DataPrep(text_dataframe)
    with pytest.raises(ValueError):
        dp.remove_special_characters('Numbers')

# Test removing special characters when no dataframe is loaded
def test_remove_special_characters_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.remove_special_characters('Text')

# Fixture for a test dataframe
@pytest.fixture
def test_dataframe2():
    return pd.DataFrame({
        'Numeric': [1, 2, 3],
        'Text': ['a', 'b', 'c']
    })

# Test successful data type change
def test_change_column_type_success(test_dataframe2):
    dp = DataPrep(test_dataframe2)
    dp.change_column_type('Numeric', 'float')
    assert dp.dataframe['Numeric'].dtype == 'float64'

# Test changing type of non-existent column
def test_change_column_type_non_existent_column(test_dataframe2):
    dp = DataPrep(test_dataframe2)
    with pytest.raises(ValueError):
        dp.change_column_type('NonExistent', 'float')

# Test changing to an invalid data type
def test_change_column_type_invalid_conversion(test_dataframe2):
    dp = DataPrep(test_dataframe2)
    with pytest.raises(Exception):
        dp.change_column_type('Numeric', 'invalid_type')

# Test changing column type when no dataframe is loaded
def test_change_column_type_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.change_column_type('Numeric', 'float')

# Fixture for a test dataframe
@pytest.fixture
def test_dataframe3():
    return pd.DataFrame({
        'Numeric': [1, 2, 3],
        'Text': ['a', 'b', 'c'],
        'Mixed': [1, 'two', 3.0],
        'WithMissing': [1, pd.NA, 3]
    })

# Test changing type with potential data loss (e.g., numeric to string)
def test_change_column_type_with_data_loss(test_dataframe3):
    dp = DataPrep(test_dataframe3)
    dp.change_column_type('Numeric', 'str')
    assert dp.dataframe['Numeric'].dtype == 'object'
    assert all(isinstance(x, str) for x in dp.dataframe['Numeric'])

# Test changing type of column with mixed types
def test_change_column_type_mixed_types(test_dataframe3):
    dp = DataPrep(test_dataframe3)
    with pytest.raises(Exception):
        dp.change_column_type('Mixed', 'int')

# Test changing type of column with missing values
def test_change_column_type_with_missing_values(test_dataframe3):
    dp = DataPrep(test_dataframe3)
    # Replace pd.NA with np.nan for float conversion
    dp.dataframe['WithMissing'] = dp.dataframe['WithMissing'].replace({pd.NA: np.nan})
    dp.change_column_type('WithMissing', 'float')
    assert dp.dataframe['WithMissing'].dtype == 'float64'

# Test changing type to a complex type (datetime)
def test_change_column_type_to_datetime():
    df = pd.DataFrame({
        'Date': ['2021-01-01', '2021-01-02', '2021-01-03']
    })
    dp = DataPrep(df)
    dp.change_column_type('Date', 'datetime64[ns]')
    assert dp.dataframe['Date'].dtype == 'datetime64[ns]'
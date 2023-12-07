import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

# Fixture for a test dataframe
@pytest.fixture
def test_dataframe4():
    return pd.DataFrame({
        'Text': ['  hello  ', 'world', '  pandas  '],
        'Mixed': ['  text ', 123, pd.NA],
        'Numeric': [1, 2, 3]
    })

# Test successful trimming of whitespace
def test_trim_whitespace_success(test_dataframe4):
    dp = DataPrep(test_dataframe4)
    dp.trim_whitespace('Text')
    assert dp.dataframe['Text'].equals(pd.Series(['hello', 'world', 'pandas']))

# Test trimming whitespace from a non-existent column
def test_trim_whitespace_non_existent_column(test_dataframe4):
    dp = DataPrep(test_dataframe4)
    with pytest.raises(ValueError):
        dp.trim_whitespace('NonExistentColumn')

# Test trimming whitespace from a non-text column
def test_trim_whitespace_non_text_column(test_dataframe4):
    dp = DataPrep(test_dataframe4)
    with pytest.raises(ValueError):
        dp.trim_whitespace('Numeric')

# Test trimming whitespace when no dataframe is loaded
def test_trim_whitespace_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.trim_whitespace('Text')

# Fixture for a test dataframe
@pytest.fixture
def test_dataframe5():
    return pd.DataFrame({
        'Categorical': pd.Categorical(['apple', 'banana', 'apple']),
        'Object': ['cat', 'dog', 'cat'],
        'Numeric': [1, 2, 3],
        'WithMissing': pd.Categorical(['apple', pd.NA, 'banana'])
    })

# Test successful label encoding on categorical column
def test_label_encode_categorical(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    dp.label_encode('Categorical')
    assert dp.dataframe['Categorical'].dtype == 'int8'

# Test successful label encoding on object column
def test_label_encode_object(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    dp.label_encode('Object')
    assert dp.dataframe['Object'].dtype == 'int8'

# Test label encoding on non-existent column
def test_label_encode_non_existent_column(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    with pytest.raises(ValueError):
        dp.label_encode('NonExistent')

# Test label encoding on non-categorical column
def test_label_encode_non_categorical_column(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    with pytest.raises(ValueError):
        dp.label_encode('Numeric')

# Test label encoding when no dataframe is loaded
def test_label_encode_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.label_encode('Categorical')

# Test label encoding with missing values
def test_label_encode_with_missing_values(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    dp.label_encode('WithMissing')
    assert dp.dataframe['WithMissing'].dtype == 'int8'

# Test label encoding on already encoded column
def test_label_encode_already_encoded(test_dataframe5):
    dp = DataPrep(test_dataframe5)
    dp.label_encode('Categorical')
    with pytest.raises(Exception):
        dp.label_encode('Categorical')  # Attempting to encode again


 # Fixture for a test dataframe
@pytest.fixture
def test_dataframe6():
    return pd.DataFrame({
        'Numeric': [1, 2, 3, 4, 5],
        'Text': ['a', 'b', 'c', 'd', 'e']
    })

# Test if binning is a success
def test_bin_numeric_to_categorical_success(test_dataframe6):
    dp = DataPrep(test_dataframe6)
    bins = [0, 2, 5]  # Define bins
    dp.bin_numeric_to_categorical('Numeric', bins)

    # Check if the new column is created and is categorical
    assert pd.api.types.is_categorical_dtype(dp.dataframe['Numeric_binned'].dtype)
    # Check if the labels are correctly assigned
    assert set(dp.dataframe['Numeric_binned'].cat.categories) == {'0-2', '2-5'}

# Test binning on non-existent column
def test_bin_numeric_to_categorical_non_existent_column(test_dataframe6):
    dp = DataPrep(test_dataframe6)
    with pytest.raises(ValueError):
        dp.bin_numeric_to_categorical('NonExistent', [0, 1])

# Test binning on non-numeric column
def test_bin_numeric_to_categorical_non_numeric_column(test_dataframe6):
    dp = DataPrep(test_dataframe6)
    with pytest.raises(ValueError):
        dp.bin_numeric_to_categorical('Text', [0, 1])

# Test binning when no dataframe is loaded
def test_bin_numeric_to_categorical_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.bin_numeric_to_categorical('Numeric', [0, 1])

# Test incorrect bins specification (not a list)
def test_bin_numeric_to_categorical_incorrect_bins(test_dataframe6):
    dp = DataPrep(test_dataframe6)
    with pytest.raises(ValueError):
        dp.bin_numeric_to_categorical('Numeric', 'incorrect')

# Test incorrect bins specification (too few bins)
def test_bin_numeric_to_categorical_few_bins(test_dataframe6):
    dp = DataPrep(test_dataframe6)
    with pytest.raises(ValueError):
        dp.bin_numeric_to_categorical('Numeric', [0])


# Fixture for a test dataframe
@pytest.fixture
def test_dataframe7():
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })

# Test successful removal of columns
def test_remove_columns_success(test_dataframe7):
    dp = DataPrep(test_dataframe7)
    dp.remove_columns(['A', 'B'])
    assert 'A' not in dp.dataframe.columns and 'B' not in dp.dataframe.columns

# Test removal of non-existent column
def test_remove_columns_non_existent(test_dataframe7):
    dp = DataPrep(test_dataframe7)
    with pytest.raises(ValueError):
        dp.remove_columns(['D'])

# Test removal when no dataframe is loaded
def test_remove_columns_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.remove_columns(['A'])

# Test invalid columns list (not a list)
def test_remove_columns_invalid_input(test_dataframe7):
    dp = DataPrep(test_dataframe7)
    with pytest.raises(ValueError):
        dp.remove_columns('A')  # Passing a string instead of a list

# Test removing non-existent and existing columns together
def test_remove_columns_mixed_existence(test_dataframe7):
    dp = DataPrep(test_dataframe7)
    with pytest.raises(ValueError):
        dp.remove_columns(['A', 'D'])  # 'A' exists, but 'D' does not

# Fixture for a test dataframe
@pytest.fixture
def datetime_dataframe():
    return pd.DataFrame({
        'Datetime': pd.to_datetime(['2021-01-01 10:00:00', '2021-06-15 15:30:25'])
    })

# Test successful extraction of components
def test_extract_datetime_components_success(datetime_dataframe):
    dp = DataPrep(datetime_dataframe)
    dp.extract_datetime_components('Datetime', ['year', 'month', 'day'])
    assert 'Datetime_year' in dp.dataframe.columns
    assert 'Datetime_month' in dp.dataframe.columns
    assert 'Datetime_day' in dp.dataframe.columns
    assert dp.dataframe['Datetime_year'].iloc[0] == 2021
    assert dp.dataframe['Datetime_month'].iloc[1] == 'June'
    assert dp.dataframe['Datetime_day'].iloc[0] == 'Friday'

# Test extraction from non-existent column
def test_extract_datetime_components_non_existent_column(datetime_dataframe):
    dp = DataPrep(datetime_dataframe)
    with pytest.raises(ValueError):
        dp.extract_datetime_components('NonExistent', ['year'])

# Test extraction from non-datetime column
def test_extract_datetime_components_non_datetime_column(datetime_dataframe):
    datetime_dataframe['NotDatetime'] = [1, 2]
    dp = DataPrep(datetime_dataframe)
    with pytest.raises(ValueError):
        dp.extract_datetime_components('NotDatetime', ['year'])

# Test extraction when no dataframe is loaded
def test_extract_datetime_components_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.extract_datetime_components('Datetime', ['year'])

# Test invalid component specification
def test_extract_datetime_components_invalid_component(datetime_dataframe):
    dp = DataPrep(datetime_dataframe)
    with pytest.raises(ValueError):
        dp.extract_datetime_components('Datetime', ['century'])

# Test extracting multiple components
def test_extract_datetime_components_multiple(datetime_dataframe):
    dp = DataPrep(datetime_dataframe)
    dp.extract_datetime_components('Datetime', ['hour', 'minute', 'second'])
    assert 'Datetime_hour' in dp.dataframe.columns
    assert 'Datetime_minute' in dp.dataframe.columns
    assert 'Datetime_second' in dp.dataframe.columns
    assert dp.dataframe['Datetime_hour'].iloc[0] == 10
    assert dp.dataframe['Datetime_minute'].iloc[1] == 30
    assert dp.dataframe['Datetime_second'].iloc[0] == 0

# Fixture for a test dataframe
@pytest.fixture
def text_dataframe2():
    return pd.DataFrame({
        'Text': ['Hello world', 'Hello Python', 'Goodbye world'],
        'Numeric': [1, 2, 3]
    })

# Test successful substring replacement
def test_replace_substring_success(text_dataframe2):
    dp = DataPrep(text_dataframe2)
    dp.replace_substring('Text', 'world', 'Earth')
    assert dp.dataframe['Text'].equals(pd.Series(['Hello Earth', 'Hello Python', 'Goodbye Earth']))

# Test replacement in non-existent column
def test_replace_substring_non_existent_column(text_dataframe2):
    dp = DataPrep(text_dataframe2)
    with pytest.raises(ValueError):
        dp.replace_substring('NonExistent', 'world', 'Earth')

# Test replacement in non-text column
def test_replace_substring_non_text_column(text_dataframe2):
    dp = DataPrep(text_dataframe2)
    with pytest.raises(ValueError):
        dp.replace_substring('Numeric', '1', 'One')

# Test replacement when no dataframe is loaded
def test_replace_substring_no_dataframe():
    dp = DataPrep(None)  # No dataframe loaded
    with pytest.raises(ValueError):
        dp.replace_substring('Text', 'world', 'Earth')


# Test no occurrence of substring
def test_replace_substring_no_occurrence(text_dataframe):
    dp = DataPrep(text_dataframe.copy())
    original_text = dp.dataframe['Text'].copy()
    dp.replace_substring('Text', 'universe', 'galaxy')

    # Ensure no changes were made to the dataframe as 'universe' doesn't exist in 'Text'
    pd.testing.assert_series_equal(dp.dataframe['Text'], original_text)

# Fixture for a test dataframe
@pytest.fixture
def numeric_dataframe():
    np.random.seed(0)
    return pd.DataFrame(np.random.rand(10, 4), columns=['A', 'B', 'C', 'D'])

# Test successful PCA application
def test_apply_pca_success(numeric_dataframe):
    dp = DataPrep(numeric_dataframe)
    dp.apply_pca(['A', 'B', 'C', 'D'])
    assert 'principal_component_1' in dp.dataframe.columns

# Test PCA with non-existent columns
def test_apply_pca_non_existent_column(numeric_dataframe):
    dp = DataPrep(numeric_dataframe)
    with pytest.raises(ValueError):
        dp.apply_pca(['X', 'Y'])

# Test PCA specifying number of components
def test_apply_pca_specified_components(numeric_dataframe):
    dp = DataPrep(numeric_dataframe)
    n_components = 2
    dp.apply_pca(['A', 'B', 'C', 'D'], n_components=n_components)
    assert len([col for col in dp.dataframe.columns if 'principal_component' in col]) == n_components

# Test PCA when no dataframe is loaded
def test_apply_pca_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.apply_pca(['A', 'B'])

# Test PCA on non-numeric columns
def test_apply_pca_non_numeric_columns():
    df = pd.DataFrame({
        'A': ['a', 'b', 'c', 'd'],
        'B': ['e', 'f', 'g', 'h']
    })
    dp = DataPrep(df)
    with pytest.raises(Exception):
        dp.apply_pca(['A', 'B'])



# Fixture for a test dataframe
@pytest.fixture
def text_dataframe3():
    return pd.DataFrame({
        'DateStr': ['2021-01-01', '2021-01-02', '2021-01-03'],
        'DateTime': pd.date_range(start='1/1/2021', periods=3, freq='D')
    })

# Test successful date-time parsing with known format
def test_parse_datetime_success(text_dataframe3):
    dp = DataPrep(text_dataframe3)
    # Ensure the date format matches the format of the date strings in 'DateStr'
    # Assuming 'DateStr' contains dates in 'YYYY-MM-DD' format
    dp.parse_datetime('DateStr', datetime_format='%Y-%m-%d')
    assert pd.api.types.is_datetime64_any_dtype(dp.dataframe['DateStr'])


# Test inferring date-time format
def test_parse_datetime_infer_format(text_dataframe3):
    dp = DataPrep(text_dataframe3)
    dp.parse_datetime('DateStr')
    assert pd.api.types.is_datetime64_any_dtype(dp.dataframe['DateStr'])

# Test parsing with non-existent column
def test_parse_datetime_non_existent_column(text_dataframe3):
    dp = DataPrep(text_dataframe3)
    with pytest.raises(ValueError):
        dp.parse_datetime('NonExistent')

# Test parsing when no dataframe is loaded
def test_parse_datetime_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.parse_datetime('DateStr')

# Test parsing with incorrect date-time format
def test_parse_datetime_incorrect_format(text_dataframe3):
    dp = DataPrep(text_dataframe3)
    with pytest.raises(Exception):
        dp.parse_datetime('DateStr', datetime_format='%d-%m-%Y')

# Test parsing non-date-time data
def test_parse_datetime_non_datetime_data():
    df = pd.DataFrame({'NotDateTime': ['a', 'b', 'c']})
    dp = DataPrep(df)
    dp.parse_datetime('NotDateTime')
    # Check if parsing resulted in NaT (not a time) values due to coercion
    assert all(pd.isna(dp.dataframe['NotDateTime']))

    # Fixture for a test dataframe
@pytest.fixture
def text_dataframe4():
    return pd.DataFrame({
        'Text': ['Hello World', 'goodbye moon', 'Python Programming'],
        'Numeric': [1, 2, 3]
    })

# Test successful text case adjustment for each case format
@pytest.mark.parametrize("case_format,expected", [
    ('upper', ['HELLO WORLD', 'GOODBYE MOON', 'PYTHON PROGRAMMING']),
    ('lower', ['hello world', 'goodbye moon', 'python programming']),
    ('title', ['Hello World', 'Goodbye Moon', 'Python Programming'])
])
def test_adjust_text_case_success(text_dataframe4, case_format, expected):
    dp = DataPrep(text_dataframe4)
    dp.adjust_text_case('Text', case_format)
    assert dp.dataframe['Text'].tolist() == expected

# Test adjustment with non-existent column
def test_adjust_text_case_non_existent_column(text_dataframe4):
    dp = DataPrep(text_dataframe4)
    with pytest.raises(ValueError):
        dp.adjust_text_case('NonExistent', 'upper')

# Test adjustment in non-text column
def test_adjust_text_case_non_text_column(text_dataframe4):
    dp = DataPrep(text_dataframe4)
    with pytest.raises(ValueError):
        dp.adjust_text_case('Numeric', 'upper')

# Test adjustment when no dataframe is loaded
def test_adjust_text_case_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.adjust_text_case('Text', 'upper')

# Test invalid case format
def test_adjust_text_case_invalid_format(text_dataframe4):
    dp = DataPrep(text_dataframe4)
    with pytest.raises(ValueError):  # Expecting a ValueError, not a generic Exception
        dp.adjust_text_case('Text', 'invalid_format')

# Fixture for a test dataframe
@pytest.fixture
def text_dataframe5():
    return pd.DataFrame({
        'Text': ['This is a sample sentence.', 'Another example sentence with stop words.', 'Text with no stopwords'],
        'Numeric': [1, 2, 3]
    })

# Test successful stop word removal
def test_remove_stopwords_success(text_dataframe5):
    dp = DataPrep(text_dataframe5)
    dp.remove_stopwords('Text')
    assert 'is' not in dp.dataframe['Text'].iloc[1]

# Test removal with non-existent column
def test_remove_stopwords_non_existent_column(text_dataframe5):
    dp = DataPrep(text_dataframe5)
    with pytest.raises(ValueError):
        dp.remove_stopwords('NonExistent')

# Test removal in non-text column
def test_remove_stopwords_non_text_column(text_dataframe5):
    dp = DataPrep(text_dataframe5)
    with pytest.raises(ValueError):
        dp.remove_stopwords('Numeric')

# Test removal when no dataframe is loaded
def test_remove_stopwords_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.remove_stopwords('Text')


#Try a different language
def test_remove_stopwords_different_language(text_dataframe5):
    try:
        # Download Spanish stop words, if not already present
        nltk.download('stopwords', quiet=True)

        dp = DataPrep(text_dataframe5)
        dp.remove_stopwords('Text', language='spanish')
        # Add an appropriate assertion here based on your test data
    except LookupError:
        pytest.skip("NLTK stop words for Spanish not available.")

# Fixture for a test dataframe
@pytest.fixture
def categorical_dataframe():
    return pd.DataFrame({
        'Category': ['A', 'A', 'B', 'C', 'C', 'C', 'D', 'E', 'F', 'G']
    })

def test_collapse_rare_categories_success(categorical_dataframe):
    dp = DataPrep(categorical_dataframe)
    dp.collapse_rare_categories('Category', 20.0)
    assert set(dp.dataframe['Category'].unique()) == {'A', 'C', 'Other'}


# Test collapse with non-existent column
def test_collapse_rare_categories_non_existent_column(categorical_dataframe):
    dp = DataPrep(categorical_dataframe)
    with pytest.raises(ValueError):
        dp.collapse_rare_categories('NonExistent', 5.0)

# Test collapse in non-categorical column
def test_collapse_rare_categories_non_categorical_column(categorical_dataframe):
    dp = DataPrep(pd.DataFrame({'Numeric': [1, 2, 3, 4]}))
    with pytest.raises(ValueError):
        dp.collapse_rare_categories('Numeric', 5.0)

# Test collapse when no dataframe is loaded
def test_collapse_rare_categories_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.collapse_rare_categories('Category', 5.0)

def test_collapse_rare_categories_different_thresholds(categorical_dataframe):
    dp = DataPrep(categorical_dataframe)
    dp.collapse_rare_categories('Category', 30.0)
    assert 'Other' in dp.dataframe['Category'].unique()

# Test when no categories are rare
def test_collapse_rare_categories_no_rare(categorical_dataframe):
    dp = DataPrep(categorical_dataframe)
    dp.collapse_rare_categories('Category', 1.0)  # Setting a low threshold so no category is rare
    assert 'Other' not in dp.dataframe['Category'].unique()


# Fixture for a test dataframe
@pytest.fixture
def text_dataframe6():
    return pd.DataFrame({
        'Text': ['This is a sample sentence.', 'Another example sentence.', '', pd.NA],
        'Numeric': [1, 2, 3, 4]
    })

# Test successful text tokenization
def test_tokenize_text_success(text_dataframe):
    # Assuming the first row of 'Text' in text_dataframe is "Hello @World!"
    dp = DataPrep(text_dataframe)
    dp.tokenize_text('Text')

    # Adjust expected tokens based on the actual content of the first row in your dataframe
    expected_tokens = ['Hello', '@', 'World', '!']
    assert dp.dataframe['Text'].iloc[0] == expected_tokens

# Test tokenization with non-existent column
def test_tokenize_text_non_existent_column(text_dataframe6):
    dp = DataPrep(text_dataframe6)
    with pytest.raises(ValueError):
        dp.tokenize_text('NonExistent')

# Test tokenization in non-text column
def test_tokenize_text_non_text_column(text_dataframe6):
    dp = DataPrep(text_dataframe6)
    with pytest.raises(ValueError):
        dp.tokenize_text('Numeric')

# Test tokenization when no dataframe is loaded
def test_tokenize_text_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.tokenize_text('Text')

# Fixture for a test dataframe
@pytest.fixture
def text_dataframe7():
    df = pd.DataFrame({
        'Text': ['This is a sample sentence.', 'Another example.', '12345', '', pd.NA],
        'Numeric': [1, 2, 3, 4, 5]
    })
    df['Text'] = df['Text'].astype('string')  # Cast to string type explicitly
    return df

# Test successful regex replace operation
def test_apply_regex_replace(text_dataframe7):
    dp = DataPrep(text_dataframe7)
    dp.apply_regex('Text', r'\b\w{6}\b', 'word')  # Replaces 6-letter words with 'word'
    assert dp.dataframe['Text'].iloc[0] == 'This is a word sentence.'

# Test regex with non-existent column
def test_apply_regex_non_existent_column(text_dataframe7):
    dp = DataPrep(text_dataframe7)
    with pytest.raises(ValueError):
        dp.apply_regex('NonExistent', r'\d+', operation='replace')

# Test regex in non-text column
def test_apply_regex_non_text_column(text_dataframe7):
    dp = DataPrep(text_dataframe7)
    with pytest.raises(ValueError):
        dp.apply_regex('Numeric', r'\d+', operation='replace')

# Test regex when no dataframe is loaded
def test_apply_regex_no_dataframe():
    dp = DataPrep(None)
    with pytest.raises(ValueError):
        dp.apply_regex('Text', r'\d+', operation='replace')

# Test invalid regex operation
def test_apply_regex_invalid_operation(text_dataframe7):
    dp = DataPrep(text_dataframe7)
    with pytest.raises(ValueError):  # Expecting ValueError for invalid operation
        dp.apply_regex('Text', r'\b\w+\b', operation='invalid_operation')
        
def test_apply_regex_empty_or_null_values(text_dataframe7):
    dp = DataPrep(text_dataframe7)
    dp.apply_regex('Text', r'\d+', operation='replace')
    assert dp.dataframe['Text'].iloc[3] == '' and pd.isna(dp.dataframe['Text'].iloc[4])
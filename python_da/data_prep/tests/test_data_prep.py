import pandas as pd
import numpy as np
from data_prep.src.data_prep import DataPrep

# Test: fill_missing_values() method
def test_fill_missing_values():
    data = {'A': [1, 2, np.nan, 4], 'B': [5, np.nan, np.nan, 8]}
    df = pd.DataFrame(data)
    dp = DataPrep(df)

    # Fill with mode
    dp.fill_missing_values('A', 'mode')
    assert dp.dataframe['A'].tolist() == [1, 2, 1, 4]

    # Fill with mean
    dp.fill_missing_values('B', 'mean')
    assert dp.dataframe['B'].tolist() == [5, 6.5, 6.5, 8]

# Test: remove_duplicates() method
def test_remove_duplicates():
    data = {'A': [1, 1, 2, 2, 3], 'B': [5, 5, 6, 7, 8]}
    df = pd.DataFrame(data)
    dp = DataPrep(df)

    dp.remove_duplicates()
    assert len(dp.dataframe) == 4

# Test: remove_z_score_outliers() method
def test_remove_z_score_outliers():
    data = {'A': [1, 2, 3, 100], 'B': [5, 6, 7, 500]}
    df = pd.DataFrame(data)
    dp = DataPrep(df)

    dp.remove_z_score_outliers(2.5)
    assert pd.isna(dp.dataframe.loc[3, 'A'])
    assert pd.isna(dp.dataframe.loc[3, 'B'])

# Test: remove_iqr_outliers() method
def test_remove_iqr_outliers():
    data = {'A': [1, 2, 3, 100], 'B': [5, 6, 7, 500]}
    df = pd.DataFrame(data)
    dp = DataPrep(df)

    dp.remove_iqr_outliers(1.5)
    assert pd.isna(dp.dataframe.loc[3, 'A'])
    assert pd.isna(dp.dataframe.loc[3, 'B'])



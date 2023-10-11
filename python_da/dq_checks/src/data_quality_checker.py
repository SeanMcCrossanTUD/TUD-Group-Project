import pandas as pd
import numpy as np
from scipy import stats


class DataQualityChecker:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def count_number_of_records(self) -> int:
        return len(self.dataset)
        
    def count_missing_values(self) -> dict:
        missing_values = self.dataset.isnull().sum()
        return missing_values.to_dict()
    
    def count_duplicate_values(self) -> int:
        return self.dataset.duplicated().sum()

    def count_unique_values_in_text_fields(self) -> dict:
        unique_values = {}
        for col in self.dataset.columns:
            if self.dataset[col].dtype == 'object':  # Checking if the col is a text field
                unique_count = self.dataset[col].nunique()  # Counting number of unique values
                unique_values[col] = unique_count
        return unique_values

    def count_number_of_fields(self) -> int:
        return len(self.dataset.columns)

    def z_score_outliers(self, threshold: float = 3.0) -> dict:
        """
        This function identifies and returns the outliers in the dataset based on the z-score method.
    
        Parameters:
        threshold (float): The z-score threshold to identify outliers. Default is 3.0.
    
        Returns:
        dict: A dictionary containing detailed information about each outlier, including:
            - row: The index of the outlier in the dataset.
            - field: The column name where the outlier is located.
            - value: The actual value of the outlier.
            - z_score: The z-score of the outlier.
            - is_outlier: Always True, as we are filtering by the threshold.
            - threshold: The threshold used to determine the outlier.
          
        Instantiate the DataQualityChecker class with a pd.DataFrame and call the z_score_outliers method to get the outliers in the dataset based on the z-score method.

        Thresholds:
            - 1.0 means approximately 68% of the data falls within 1 standard deviation (1 z-score) of the mean.
            - 1.0 means approximately 95% of the data falls within 2 standard deviation (2 z-score) of the mean.
            - 3.0 means approximately 99.7% of the data falls within 3 standard deviation (2 z-score) of the mean.
    
        Example:
        ```
        checker = DataQualityChecker(dataset)
        outliers = checker.z_score_outliers(threshold=3.0)
        ```
        """
        outliers = {}
        for col in self.dataset.select_dtypes(include=[np.number]).columns: # Only works on numeric columns
            col_values = self.dataset[col].dropna().reset_index(drop=True)  # FIXED: Resetting index after dropping NaN values - had to reset index
            z_scores = np.abs(stats.zscore(col_values))
            outlier_indices = np.where(z_scores > threshold)
        
            # Extracting detailed information for each outlier
            outlier_info = [
                {
                    "row": col_values.index[idx],  # Getting the original index of the outlier
                    "field": col,
                    "value": col_values.iloc[idx],
                    "z_score": z_scores[idx],
                    "is_outlier": True,  # Will always be true currently. 
                    "threshold": threshold  # The threshold used to determine the outlier
                }
                for idx in outlier_indices[0]
            ]
            if outlier_info:  # Adding to the result only if there are outliers for the column
                outliers[col] = outlier_info
                
        return outliers

    def iqr_outliers(self, k: float = 1.5) -> dict:
        """
        This function identifies and returns the outliers in the dataset based on the IQR method.

        Parameters:
        k (float): The coefficient used to determine the bounds for the outliers. Default is 1.5.

        Returns:
        dict: A dictionary containing detailed information about each outlier, including:
            - row: The index of the outlier in the dataset.
            - field: The column name where the outlier is located.
            - value: The actual value of the outlier.
            - is_outlier: Always True, as we are filtering by the IQR bounds.
            - lower_bound: The lower bound used to determine the outlier.
            - upper_bound: The upper bound used to determine the outlier.

        Example:
        ```
        checker = DataQualityChecker(dataset)
        outliers = checker.iqr_outliers(k=1.5)
        ```

        Explanation:
        The IQR method calculates the range between the first quartile (25th percentile) and the third quartile (75th percentile) of the data. Outliers are then identified as values that fall outside of this range extended by a factor of k.
        """
        outliers = {}
        for col in self.dataset.select_dtypes(include=[np.number]).columns: # Only works on numeric columns
            col_values = self.dataset[col].dropna().reset_index(drop=True)
            Q1 = col_values.quantile(0.25)
            Q3 = col_values.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - k * IQR
            upper_bound = Q3 + k * IQR

            # Extracting detailed information for each outlier
            outlier_info = [
                {
                    "row": idx,
                    "field": col,
                    "value": value,
                    "is_outlier": True,
                    "lower_bound": lower_bound,
                    "upper_bound": upper_bound
                }
                for idx, value in col_values.iteritems()
                if value < lower_bound or value > upper_bound
            ]
            if outlier_info:  
                outliers[col] = outlier_info

        return outliers
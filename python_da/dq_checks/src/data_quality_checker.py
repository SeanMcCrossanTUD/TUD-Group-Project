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
            if self.dataset[col].dtype == 'object': 
                unique_count = self.dataset[col].nunique() 
                unique_values[col] = unique_count
        return unique_values

    def count_number_of_fields(self) -> int:
        return len(self.dataset.columns)
    
    def data_type_profile(self) -> dict:
        data_type_count = {}
        for col in self.dataset.columns:
            dtype = str(self.dataset[col].dtype)
            data_type_count[dtype] = data_type_count.get(dtype, 0) + 1
        return data_type_count

    def z_score_outliers(self, threshold: float = 3.0) -> dict:
        """
        Identifies and returns information about all values in the dataset,
        indicating which ones are outliers based on the z-score method.
        """
        result = {"fields": [], "outliers": {}}
        for col in self.dataset.select_dtypes(include=[np.number]).columns:
            result["fields"].append(col)

            # Drop NaN values and reset index to align with original dataset
            col_values = self.dataset[col].dropna().reset_index(drop=True)
            original_indices = self.dataset[col].dropna().index

            if not col_values.empty:
                z_scores = np.abs(stats.zscore(col_values))
                z_score_map = dict(zip(original_indices, z_scores))

                result["outliers"][col] = [
                    {
                        "row": original_idx,
                        "field": col,
                        "value": self.dataset.at[original_idx, col],
                        "z_score": z_score_map.get(original_idx),
                        "is_outlier": bool(z_score_map.get(original_idx, 0) > threshold),
                        "threshold": threshold
                    }
                    for original_idx in original_indices
                ]
            else:
                result["outliers"][col] = []

        return result

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

    def count_unique_value_frequencies_in_text_fields(self, max_unique_values=50) -> dict:
        result = {'text_fields': [], 'value_counts': {}}

        for col in self.dataset.select_dtypes(include='object').columns:
            result['text_fields'].append(col)
            value_counts = self.dataset[col].value_counts()

            if len(value_counts) > max_unique_values:
                # Keep the top 'max_unique_values' values and sum the counts of the rest
                top_values = value_counts.head(max_unique_values)
                other_count = value_counts.iloc[max_unique_values:].sum()
                value_counts = top_values.append(pd.Series({'other values': other_count}))

            result['value_counts'][col] = value_counts.to_dict()

        return result
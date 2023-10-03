import pandas as pd

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
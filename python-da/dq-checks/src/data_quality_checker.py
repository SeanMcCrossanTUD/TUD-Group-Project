import pandas as pd

class DataQualityChecker:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def count_number_of_records(self) -> int:
        return len(self.dataset)
        
    def count_missing_values(self) -> dict:
        missing_values = self.dataset.isnull().sum()
        return missing_values.to_dict()
import pandas as pd
import numpy as np
from scipy import stats


# Class to encapsulate data cleaning functionalities
class DataPrep:

    def __init__(self, dataset: pd.DataFrame):
        self.dataframe = dataset

    # def load_dataframe(self, file_path):
    #     # Check if the file path is valid from OS
    #     if not os.path.exists(file_path):
    #         raise FileNotFoundError(f'File {file_path} not found')
    #     try:
    #         # Try to load the file as a CSV
    #         dataframe = pd.read_csv(file_path)
    #         # Check if the dataframe is empty or incorrectly formatted (CSV only now)
    #         if dataframe.empty:
    #             raise ValueError(f'File {file_path} is empty or not in the correct format')
    #         return dataframe
    #     except pd.errors.ParserError as e:
    #         # Handle CSV parsing errors
    #         raise ValueError(f'Failed to parse {file_path} as a CSV file: {e}')
    #     except Exception as e:
    #         # Catch any other exceptions that may occur
    #         raise Exception(f'An unexpected error occurred: {e}')

    def fill_missing_values(self, column_name, method='mode'):
        # Check if a dataframe is loaded or raise error
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')
        
        # Check if the specified column exists in the dataframe or raise error
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')
        
        # Check if there are any missing values in the specified column or just return df
        if self.dataframe[column_name].isnull().sum() == 0:
            print(f'No missing values found in column {column_name}. Returning original dataframe.')
            return self.dataframe
        
        if method not in ['mode', 'mean', 'median', 'interpolate']:
            raise ValueError(f'Invalid method: {method}. Supported methods are "mode", "mean", "median", "interpolate".')


        #Try-excpet block containing different functionalities for specific keywords
        try:
            if method == 'mode':
                fill_value = self.dataframe[column_name].mode()[0]
            elif method == 'mean':
                fill_value = self.dataframe[column_name].mean()
            elif method == 'median':
                fill_value = self.dataframe[column_name].median()
            elif method == 'interpolate':
                self.dataframe[column_name].interpolate(inplace=True)
                return self.dataframe
            
            # Fill missing values in the dataframe
            self.dataframe[column_name].fillna(fill_value, inplace=True)
        except Exception as e:
            raise Exception(f'An error occurred while filling missing values: {e}')

        return self.dataframe
    

    # Removes duplicate rows from the dataframe. Limited functionality for now, aim to add more 
    def remove_duplicates(self):
        
        #File check
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Remove duplicates using pandas drop_duplicates method
        initial_rows = len(self.dataframe)
        self.dataframe.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.dataframe)

        print(f'Removed {removed_rows} duplicate rows.')
        return self.dataframe
    
    def remove_z_score_outliers(self, threshold: float = 3.0) -> None:
    
        #This function removes or modifies the outliers in the dataframe based on the z-score method.
        
        # Iterate over each numeric column in the dataframe
        for col in self.dataframe.select_dtypes(include=[np.number]).columns:
            # Exclude null values from the column
            col_values = self.dataframe[col].dropna()
            
            # Calculate the z-scores for each value in the column
            z_scores = np.abs(stats.zscore(col_values))
            
            # Identify indices of the values where the z-score is greater than the given threshold
            outlier_indices = np.where(z_scores > threshold)

            # Replace the outliers in the dataframe with NaN
            self.dataframe.loc[self.dataframe.index[outlier_indices], col] = np.nan

    def remove_iqr_outliers(self, k: float = 1.5) -> None:
    
         #This function removes or modifies the outliers in the dataframe based on the IQR method.
    
        # Iterate over each numeric column in the dataframe
        for col in self.dataframe.select_dtypes(include=[np.number]).columns:
            # Exclude null values from the column
            col_values = self.dataframe[col].dropna()
            
            # Calculate the first and third quartiles of the column values
            Q1 = col_values.quantile(0.25)
            Q3 = col_values.quantile(0.75)
            
            # Compute the Interquartile Range (IQR)
            IQR = Q3 - Q1

            # Calculate the bounds for outliers using the provided coefficient, k
            lower_bound = Q1 - k * IQR
            upper_bound = Q3 + k * IQR

            # Replace the values outside the bounds (outliers) in the dataframe with NaN
            self.dataframe.loc[(self.dataframe[col] < lower_bound) | (self.dataframe[col] > upper_bound), col] = np.nan

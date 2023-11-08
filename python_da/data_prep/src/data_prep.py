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



    # Function 1.
    def fill_missing_values(self, column_name, method='mode', specific_value=None):
        """
        Fills missing values in a specified column using various methods.

        Args:
        column_name (str): The name of the column to fill missing values in.
        method (str): The method to use for filling missing values. Options are 'remove', 'mode', 'median', 'mean', or 'specific'.
        specific_value (numeric, optional): A specific numeric value to use for filling missing values. This is used only if method='specific'.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Return if no missing values are found
        if self.dataframe[column_name].isnull().sum() == 0:
            print(f'No missing values found in column {column_name}. Returning original dataframe.')
            return self.dataframe

        if method not in ['remove', 'mode', 'mean', 'median', 'specific']:
            raise ValueError(f'Invalid method: {method}. Supported methods are "remove", "mode", "mean", "median", "specific".')

        try:
            if method == 'remove':
                self.dataframe.dropna(subset=[column_name], inplace=True)
            elif method == 'mode':
                fill_value = self.dataframe[column_name].mode()[0]
                self.dataframe[column_name].fillna(fill_value, inplace=True)
            elif method == 'mean':
                fill_value = self.dataframe[column_name].mean()
                self.dataframe[column_name].fillna(fill_value, inplace=True)
            elif method == 'median':
                fill_value = self.dataframe[column_name].median()
                self.dataframe[column_name].fillna(fill_value, inplace=True)
            elif method == 'specific':
                if specific_value is None or not isinstance(specific_value, (int, float)):
                    raise ValueError('A specific numeric value must be provided for the "specific" method.')
                self.dataframe[column_name].fillna(specific_value, inplace=True)
        except Exception as e:
            raise Exception(f'An error occurred while filling missing values: {e}')

        return self.dataframe
    
    # Function 2.
    def remove_outliers(self, sd: float = 3.0) -> None:
        """
        Removes or modifies the outliers in the dataframe based on the specified standard deviation.

        Args:
        sd (float): The number of standard deviations to use for defining an outlier. 
                    Defaults to 3.0.

        """

        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Iterate over each numeric column in the dataframe
        for col in self.dataframe.select_dtypes(include=[np.number]).columns:
            # Exclude null values from the column
            col_values = self.dataframe[col].dropna()
            
            # Calculate the mean and standard deviation for the column
            mean, std = col_values.mean(), col_values.std()
            
            # Define the upper and lower bounds for outliers
            lower_bound = mean - sd * std
            upper_bound = mean + sd * std

            # Replace the outliers in the dataframe with NaN
            self.dataframe.loc[(self.dataframe[col] < lower_bound) | (self.dataframe[col] > upper_bound), col] = np.nan


    # Function 3.
    def normalize_data(self, column_name, method='min-max'):
        """
        Normalizes the data in the specified column using either min-max scaling or z-score normalization.

        Args:
        column_name (str): The name of the column to normalize.
        method (str): The normalization method to use. Options are 'min-max' or 'z-score'.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Normalization process
        try:
            if method == 'min-max':
                min_val = self.dataframe[column_name].min()
                max_val = self.dataframe[column_name].max()
                self.dataframe[column_name] = (self.dataframe[column_name] - min_val) / (max_val - min_val)
            elif method == 'z-score':
                mean_val = self.dataframe[column_name].mean()
                std_val = self.dataframe[column_name].std()
                self.dataframe[column_name] = (self.dataframe[column_name] - mean_val) / std_val
            else:
                raise ValueError('Invalid method. Supported methods are "min-max" and "z-score".')
        except Exception as e:
            raise Exception(f'An error occurred while normalizing data: {e}')

        return self.dataframe


 #Function 4.
    def rename_column(self, old_name, new_name):
        """
        Renames a column in the DataFrame.

        Args:
        old_name (str): The current name of the column.
        new_name (str): The new name for the column. Must be a string.

        Raises:
        ValueError: If new_name is not a string.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Ensure that new_name is a string
        if not isinstance(new_name, str):
            raise ValueError('new_name must be a string')

        # Check if the old column name exists
        if old_name not in self.dataframe.columns:
            raise ValueError(f'Column name {old_name} not found in dataframe')

        # Perform the renaming
        try:
            self.dataframe.rename(columns={old_name: new_name}, inplace=True)
        except Exception as e:
            raise Exception(f'An error occurred while renaming the column: {e}')

        return self.dataframe

    

import pandas as pd
import numpy as np
from scipy import stats
import re
from sklearn.decomposition import PCA

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

    def remove_duplicates(self):
        self.dataframe = self.dataframe.drop_duplicates()
        return self.dataframe

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

    
    #Function 5.
    def remove_special_characters(self, column_name):
        """
        Removes special characters from a text column in the DataFrame.

        Args:
        column_name (str): The name of the column from which to remove special characters.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Check if the column data type is string
        if not pd.api.types.is_string_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a text column.')

        # Perform the removal of special characters
        try:
            self.dataframe[column_name] = self.dataframe[column_name].apply(lambda x: re.sub(r'[^A-Za-z0-9 ]+', '', x) if isinstance(x, str) else x)
        except Exception as e:
            raise Exception(f'An error occurred while removing special characters: {e}')

        return self.dataframe
    
     #Function 6
    def change_column_type(self, column_name, new_type):
        """
        Changes the data type of a specified column in the DataFrame.

        Args:
        column_name (str): The name of the column to change the data type of.
        new_type: The new data type for the column. This should be a valid pandas data type.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Perform the data type change
        try:
            self.dataframe[column_name] = self.dataframe[column_name].astype(new_type)
        except Exception as e:
            raise Exception(f'An error occurred while changing the data type of the column: {e}')

        return self.dataframe
    
    #Function 7
    def trim_whitespace(self, column_name):
        """
        Trims leading and trailing whitespace from a text column in the DataFrame.

        Args:
        column_name (str): The name of the text column to trim whitespace from.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Ensure that the column is of text type
        if not pd.api.types.is_string_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a text column.')

        # Perform the trimming of whitespace
        try:
            self.dataframe[column_name] = self.dataframe[column_name].str.strip()
        except Exception as e:
            raise Exception(f'An error occurred while trimming whitespace: {e}')

        return self.dataframe
    
     #Function 8
    def label_encode(self, column_name):
        """
        Performs label encoding on a specified categorical column in the DataFrame,
        replacing each unique category with a numerical value.

        Args:
        column_name (str): The name of the column to be label encoded.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Ensure that the column is categorical
        if not pd.api.types.is_categorical_dtype(self.dataframe[column_name]) and not pd.api.types.is_object_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a categorical column.')

        # Perform label encoding
        try:
            # Convert the column to category if it's not already
            if not pd.api.types.is_categorical_dtype(self.dataframe[column_name]):
                self.dataframe[column_name] = self.dataframe[column_name].astype('category')

            # Assign numerical labels
            self.dataframe[column_name] = self.dataframe[column_name].cat.codes
        except Exception as e:
            raise Exception(f'An error occurred while performing label encoding: {e}')

        return self.dataframe
    
     #Function 9
    def bin_numeric_to_categorical(self, column_name, bins, labels=None):
        """
        Converts a numeric column into categorical by binning values into specified ranges.

        Args:
        column_name (str): The name of the numeric column to convert.
        bins (list): The edges defining the bins. Should be a list of numbers.
        labels (list, optional): A list of labels for the bins. Length should be one less than the bins.

        Raises:
        ValueError: If the bins or labels are not correctly specified.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Ensure the column is numeric
        if not pd.api.types.is_numeric_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a numeric column.')

        # Perform the binning
        try:
            self.dataframe[column_name] = pd.cut(self.dataframe[column_name], bins, labels=labels)
        except Exception as e:
            raise Exception(f'An error occurred while binning the column: {e}')

        return self.dataframe
    
     #Function 10
    def remove_columns(self, columns_to_remove):
        """
        Removes specified columns from the DataFrame.

        Args:
        columns_to_remove (list): A list of column names to be removed from the DataFrame.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Ensure that columns_to_remove is a list
        if not isinstance(columns_to_remove, list):
            raise ValueError('columns_to_remove should be a list of column names.')

        # Check if the specified columns exist
        for col in columns_to_remove:
            if col not in self.dataframe.columns:
                raise ValueError(f'Column name {col} not found in dataframe')

        # Remove the specified columns
        try:
            self.dataframe.drop(columns=columns_to_remove, inplace=True)
        except Exception as e:
            raise Exception(f'An error occurred while removing columns: {e}')

        return self.dataframe
    
    #Function 11
    def extract_datetime_components(self, column_name, components):
        """
        Extracts specified datetime components from a datetime column in the DataFrame,
        converting month to text representation and replacing 'weekday' with 'day'.

        Args:
        column_name (str): The name of the datetime column.
        components (list): A list of components to extract. Valid options are 'year', 'month', 'day', 'hour', 'minute', 'second'.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Ensure the column is a datetime type
        if not pd.api.types.is_datetime64_any_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a datetime column.')

        # Extract the specified components
        for component in components:
            if component not in ['year', 'month', 'day', 'hour', 'minute', 'second']:
                raise ValueError(f'Invalid component: {component}. Valid components are year, month, day, hour, minute, second.')

            try:
                if component == 'year':
                    self.dataframe[f'{column_name}_year'] = self.dataframe[column_name].dt.year
                elif component == 'month':
                    self.dataframe[f'{column_name}_month'] = self.dataframe[column_name].dt.strftime('%B')
                elif component == 'day':
                    # 'day' now refers to the day of the week
                    self.dataframe[f'{column_name}_day'] = self.dataframe[column_name].dt.strftime('%A')
                elif component == 'hour':
                    self.dataframe[f'{column_name}_hour'] = self.dataframe[column_name].dt.hour
                elif component == 'minute':
                    self.dataframe[f'{column_name}_minute'] = self.dataframe[column_name].dt.minute
                elif component == 'second':
                    self.dataframe[f'{column_name}_second'] = self.dataframe[column_name].dt.second
            except Exception as e:
                raise Exception(f'An error occurred while extracting {component}: {e}')

        return self.dataframe
    
 #Function 12
    def replace_substring(self, column_name, old_substring, new_substring):
        """
        Replaces a specified substring with a new substring in a text column of the DataFrame.

        Args:
        column_name (str): The name of the text column in which to replace the substring.
        old_substring (str): The substring to be replaced.
        new_substring (str): The new substring to replace the old substring.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified column exists
        if column_name not in self.dataframe.columns:
            raise ValueError(f'Column name {column_name} not found in dataframe')

        # Ensure that the column is of text type
        if not pd.api.types.is_string_dtype(self.dataframe[column_name]):
            raise ValueError(f'Column {column_name} is not a text column.')

        # Perform the replacement
        try:
            self.dataframe[column_name] = self.dataframe[column_name].str.replace(old_substring, new_substring, regex=False)
        except Exception as e:
            raise Exception(f'An error occurred while replacing substring: {e}')

        return self.dataframe
    
#Function 13
    def apply_pca(self, columns, n_components=None):
        """
        Performs principal component analysis (PCA) on specified columns.

        Args:
        columns (list): List of column names to apply PCA to.
        n_components (int, optional): Number of principal components to keep. 
                                      If None, all components are kept.
        """

        # Check if a dataframe is loaded
        if self.dataframe is None:
            raise ValueError('Dataframe is not loaded. Provide a file_path to load dataframe.')

        # Check if the specified columns exist
        for col in columns:
            if col not in self.dataframe.columns:
                raise ValueError(f'Column name {col} not found in dataframe')

        # Extract the specified columns
        data_subset = self.dataframe[columns]

        # Apply PCA
        try:
            pca = PCA(n_components=n_components)
            principal_components = pca.fit_transform(data_subset)
            
            # Create a DataFrame with principal components
            pc_df = pd.DataFrame(data=principal_components, 
                                 columns=[f'principal_component_{i+1}' for i in range(principal_components.shape[1])])
            
            # Drop original columns and concatenate the principal components
            self.dataframe = pd.concat([self.dataframe.drop(columns, axis=1), pc_df], axis=1)
        except Exception as e:
            raise Exception(f'An error occurred while performing PCA: {e}')

        return self.dataframe

    

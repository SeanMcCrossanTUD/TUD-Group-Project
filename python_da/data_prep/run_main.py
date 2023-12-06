import os
import logging
import time
import json
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from data_prep.src.data_prep import DataPrep
from data_prep.azure_package.src.azure_functions import (download_blob_csv_data,
                                                download_blob_json_data,
                                                upload_result_excel_to_azure,
                                                download_blob_excel_data,
                                                upload_result_csv_to_azure,
                                                receive_message_from_queue)

# Set up logging
logger = logging.getLogger('data-prep')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'pyconfigurations', 'azure_config.json')



with open(CONFIG_PATH, 'r') as file:
    config = json.load(file)

SERVICE_BUS_CONNECTION_STRING = config["SERVICE_BUS_CONNECTION_STRING"]
SERVICE_BUS_QUEUE_NAME = config["SERVICE_BUS_QUEUE_2_NAME"]
connection_string = config["AZURE_CONNECTION_STRING"]
RULES_CONTAINER = config["RULES_CONTAINER"]

if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_data_input = config["DATA_INPUT_CONTAINER"]

def validate_inputs(dataset, json_config):
    if not isinstance(dataset, pd.DataFrame):
        raise ValueError("Dataset must be a pandas DataFrame.")
    if not isinstance(json_config, dict):
        raise ValueError("Configuration must be a dictionary.")

def handle_outlier_management(prep, json_config):
    for outlier_management in json_config.get('outlier_management', []):
        for col, details in outlier_management.items():
            if pd.api.types.is_numeric_dtype(prep.dataframe[col]):
                sd = int(details['method'].split('-')[0].strip())
                logger.info(f"Removing outliers in column: {col} using {sd} SD method")
                prep.remove_outliers(col, sd)
                logger.info(f"Outliers removed from column: {col}")


def handle_missing_value_imputation(prep, json_config):
    for imputation in json_config.get('missing_value_imputation', []):
        for col, details in imputation.items():
            method = details['method'].lower()
            prep.fill_missing_values(col, method=method)
            logger.info(f"Missing values handled in column: {col}")

def handle_renaming_and_dropping_columns(prep, json_config):
    # Renaming columns
    renamed_columns = {}
    for renaming in json_config.get('rename_column_name', []):
        for old_name, new_name in renaming.items():
            prep.rename_column(old_name, new_name)
            renamed_columns[old_name] = new_name
            logger.info(f"Renamed column {old_name} to {new_name}")

    # Update columns_kept list with new names
    columns_to_keep = set(json_config.get('columns_kept', []))
    for old_name, new_name in renamed_columns.items():
        if old_name in columns_to_keep:
            columns_to_keep.remove(old_name)
            columns_to_keep.add(new_name)

    # Identify columns that have been binned
    binned_columns = [col for col in prep.dataframe.columns if col.endswith('_binned')]
    columns_to_keep.update(binned_columns)

    # Dropping columns
    columns_to_remove = [col for col in prep.dataframe.columns if col not in columns_to_keep]
    if columns_to_remove:
        prep.remove_columns(columns_to_remove)
        logger.info(f"Dropped columns: {', '.join(columns_to_remove)}")



def apply_transformations(prep, json_config):

    for col in prep.dataframe.columns:
        # Trim whitespace in text columns
        if col in json_config.get('trim_whitespace', []) and pd.api.types.is_string_dtype(prep.dataframe[col]):
            prep.trim_whitespace(col)
            logger.info(f"Trimmed whitespace in column: {col}")

        # Remove special characters in text columns
        if col in json_config.get('remove_special_characters', []) and pd.api.types.is_string_dtype(prep.dataframe[col]):
            prep.remove_special_characters(col)
            logger.info(f"Removed special characters in column: {col}")

        # Normalize data in numeric columns
        for normalization in json_config.get('normalize_data', []):
            if col in normalization and pd.api.types.is_numeric_dtype(prep.dataframe[col]):
                method = normalization[col]['method']['types']
                prep.normalize_data(col, method)
                logger.info(f"Normalized data in column: {col} using method: {method}")

        # Remove stopwords in text columns
        if col in json_config.get('remove_stopwords', []) and pd.api.types.is_string_dtype(prep.dataframe[col]):
            prep.remove_stopwords(col)
            logger.info(f"Removed stopwords in column: {col}")

        # Label encoding in categorical columns
        if col in json_config.get('label_encoding', []) and pd.api.types.is_string_dtype(prep.dataframe[col]):
            prep.label_encode(col)
            logger.info(f"Label encoded column: {col}")

        # Numerical column binning in numeric columns
        for binning_config in json_config.get('numerical_column_binning', []):
            if col in binning_config and pd.api.types.is_numeric_dtype(prep.dataframe[col]):
                bins = sorted(binning_config[col])
                prep.bin_numeric_to_categorical(col, bins)
                logger.info(f"Binned numeric column: {col} into categories")

        # Text case adjustment in text columns
        for adjustment in json_config.get('textcase_adjustment', []):
            if col in adjustment and pd.api.types.is_string_dtype(prep.dataframe[col]):
                case_format = adjustment[col].lower()
                prep.adjust_text_case(col, case_format)
                logger.info(f"Adjusted text case in column: {col} to {case_format}")

        # Substring replacement in text columns
        for replacement in json_config.get('replace_substring', []):
            if col in replacement and pd.api.types.is_string_dtype(prep.dataframe[col]):
                for old_substring, new_substring in replacement[col].items():
                    prep.replace_substring(col, old_substring, new_substring)
                    logger.info(f"Replaced substring in column: {col}")

        # Collapse rare categories in categorical columns
        for collapse_config in json_config.get('collapse_rare_categories', []):
            if col in collapse_config:
                threshold = float(collapse_config[col])
                if pd.api.types.is_string_dtype(prep.dataframe[col]):
                    prep.collapse_rare_categories(col, threshold_percentage=threshold)
                    logger.info(f"Collapsed rare categories in column: {col} with threshold: {threshold}")

        # Datetime parsing
        for datetime_config in json_config.get('standard_datetime_format', []):
            if col in datetime_config:
                format = datetime_config[col]
                prep.parse_datetime(col, datetime_format=format)
                logger.info(f"Parsed datetime in column: {col} with format: {format}")

        # Regular expression operations
        for regex_operation in json_config.get('regular_expression_operations', []):
            if col in regex_operation:
                pattern = regex_operation[col].get("pattern")
                replace_with = regex_operation[col].get("replaceWith", "")
                prep.apply_regex(col, regex_pattern=pattern, replacement_string=replace_with, operation="replace")
                logger.info(f"Applied regex operation on column: {col}")

        # Text tokenization
        for text_tokenisation in json_config.get('text_tokenisation', []):
            if col in text_tokenisation and pd.api.types.is_string_dtype(prep.dataframe[col]):
                prep.tokenize_text(col)
                logger.info(f"Tokenized text in column: {col}")

        # Column type conversion
        for conversion in json_config.get('column_type_conversion', []):
            if col in conversion and conversion[col] == "Text" and pd.api.types.is_string_dtype(prep.dataframe[col]):
                prep.change_column_type(col, 'object')
                logger.info(f"Changed data type of column {col} to Text (object)")

def apply_configured_transformations(json_config, dataset):
    try:
        logger.info("Begin column transformations")
        prep = DataPrep(dataset)

        # Validate inputs
        validate_inputs(dataset, json_config)

        # Handle outlier management first
        handle_outlier_management(prep, json_config)

        # Handle missing values second
        handle_missing_value_imputation(prep, json_config)

        # Apply other transformations
        apply_transformations(prep, json_config)

        # Handle renaming and dropping columns towards the end
        handle_renaming_and_dropping_columns(prep, json_config)

        logger.info("Transformed dataset")
        return prep.dataframe

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise






def apply_dataset_cleaning(dataset: pd.DataFrame, config_path: str) -> pd.DataFrame:
    """
    Apply dataset-wide cleaning actions based on the JSON configuration.

    Parameters:
    dataset (pd.DataFrame): The dataset to clean.
    config_path (str): Path to the JSON configuration file.

    Returns:
    pd.DataFrame: The cleaned dataset.
    """
    if not isinstance(dataset, pd.DataFrame):
        logging.error('Provided dataset is not a pandas DataFrame')
        raise TypeError('Expected dataset to be a pandas DataFrame')

    try:
        # Load JSON configuration
        with open(config_path, 'r') as file:
            config = json.load(file)

        prep = DataPrep(dataset)

        # Remove duplicates
        if config.get('remove_duplicates', {}).get('option') == 'yes':
            logging.info('Removing duplicates from the dataset')
            prep.remove_duplicates()

        # Apply PCA
        pca_config = config.get('apply_pca', {})
        if pca_config:
            columns = pca_config.get('columns', [])
            n_components = pca_config.get('n_components')
            if n_components is not None:
                n_components = int(n_components)  # Convert to integer if it's not None
            logging.info('Applying PCA on specified columns')
            prep.apply_pca(columns, n_components)

        logging.info('Dataset cleaning actions applied successfully')
        return prep.dataframe

    except FileNotFoundError:
        logging.error(f'Configuration file {config_path} not found')
        raise
    except json.JSONDecodeError:
        logging.error(f'Error parsing JSON from {config_path}')
        raise
    except Exception as e:
        logging.error(f'Error occurred during dataset cleaning: {e}')
        raise e
        

def main(test_iterations=None):
    counter = 0

    while True:
        # If test_iterations is set and counter has reached it, break the loop
        if test_iterations and counter >= test_iterations:
            break

        # Check Azure queue for a new message
        try:
            time.sleep(5)
            msg = receive_message_from_queue(SERVICE_BUS_CONNECTION_STRING, SERVICE_BUS_QUEUE_NAME)
            logger.info(msg)
            if msg is not None:
                logger.info('Received a new message, processing...')
                cleaned_msg = str(msg).replace("'", "\"")
                message_content = json.loads(cleaned_msg)

                filename = message_content.get('rawurl', 'Unknown Filename') 
                json_file_name = message_content.get('jsonFilename', 'Unknown Filename')
                jobID = message_content.get('jobID', 'Unknown JobID')

                # Download JSON rules file
                json_rules_string = download_blob_json_data(connection_string, json_file_name, RULES_CONTAINER)
                json_rules = json.loads(json_rules_string) if json_rules_string else None

                file_extension = os.path.splitext(filename)[1].lower()
                if file_extension == '.csv':
                    data = download_blob_csv_data(connection_string, filename)
                    logger.info(f'CSV data downloaded for {filename}')
                elif file_extension == '.xlsx' or file_extension == '.xls':
                    data = download_blob_excel_data(connection_string, filename)
                    logger.info(f'Excel data downloaded for {filename}')
                else:
                    logger.error(f'Invalid file type for {filename}. Only CSV and Excel files are supported.')
                    continue

                result = apply_configured_transformations(json_config=json_rules, dataset=data)
                
                if file_extension == '.csv':
                    upload_result_csv_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'CSV result uploaded for {filename}')
                elif file_extension == '.xlsx' or file_extension == '.xls':
                    upload_result_excel_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'Excel result uploaded for {filename}')
                
                logger.info('Clean data uploaded in data prep')
            else:
                logger.info('No new messages. Waiting for next check...')
            

        except AzureError as ae:
            logger.error(f"AzureError: {str(ae)}")
        except pd.errors.EmptyDataError as ede:
            logger.error(f"Pandas EmptyDataError: {str(ede)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()


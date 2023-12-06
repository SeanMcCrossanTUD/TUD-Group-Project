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


def apply_configured_transformations(json_config, dataset):
    try:
        logger.info(f"Begin column transformations")
        prep = DataPrep(dataset)

        # Parse JSON configuration
       # config = json.loads(json_config)
        config = json_config

        # Remove columns not in columns_kept
        columns_kept = config.get('columns_kept', [])
        columns_to_remove = [col for col in dataset.columns if col not in columns_kept]
        if columns_to_remove:
            prep.remove_columns(columns_to_remove)
            logger.info(f"Removed columns: {columns_to_remove}")

            # Apply renaming of column names
        for renaming_config in config.get('rename_column_name', []):
            for old_name, new_name in renaming_config.items():
                prep.rename_column(old_name, new_name)
                logger.info(f"Renamed column {old_name} to {new_name}")

        # Apply transformations based on column data type
        for col in dataset.columns:
            # Check and apply trim whitespace
            if col in config.get('trim_whitespace', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.trim_whitespace(col)
                logger.info(f"Trimmed whitespace in column: {col}")

            # Check and apply removal of special characters
            if col in config.get('remove_special_characters', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.remove_special_characters(col)
                logger.info(f"Removed special characters in column: {col}")

            # Apply normalization on numeric columns
            for normalization in config.get('normalize_data', []):
                if col in normalization and pd.api.types.is_numeric_dtype(dataset[col]):
                    method = normalization[col]['method']['types']
                    prep.normalize_data(col, method)
                    logger.info(f"Normalized data in column: {col} using method: {method}")

            # Apply missing value imputation
            for imputation in config.get('missing_value_imputation', []):
                if col in imputation:
                    method = imputation[col]['method'].lower()
                    prep.fill_missing_values(col, method=method)
                    logger.info(f"Filled missing values in column: {col} using method: {method}")

            # Apply removal of stopwords on text columns
            if col in config.get('remove_stopwords', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.remove_stopwords(col)
                logger.info(f"Removed stopwords in column: {col}")

            # Apply label encoding on categorical columns
            if col in config.get('label_encoding', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.label_encode(col)
                logger.info(f"Label encoded column: {col}")

            # Apply numerical column binning
            for binning in config.get('numerical_column_binning', []):
                if col in binning and pd.api.types.is_numeric_dtype(dataset[col]):
                    bins = sorted(binning[col])  # Sort the bins
                    prep.bin_numeric_to_categorical(col, bins)
                    logger.info(f"Binned numeric column: {col} into categories")

            # Apply text case adjustment
            for adjustment in config.get('textcase_adjustment', []):
                for col, case_format in adjustment.items():
                    if pd.api.types.is_string_dtype(dataset[col]):
                        prep.adjust_text_case(col, case_format.lower())
                        logger.info(f"Adjusted text case in column: {col} to {case_format}")

            # Apply substring replacement
            for replacement in config.get('replace_substring', []):
                for col, substrings in replacement.items():
                    if pd.api.types.is_string_dtype(dataset[col]):
                        for old_substring, new_substring in substrings.items():
                            prep.replace_substring(col, old_substring, new_substring)
                            logger.info(f"Replaced substring in column: {col}")

            # Apply rare categories collapse
            for collapse_config in config.get('collapse_rare_categories', []):
                for col, threshold in collapse_config.items():
                    threshold = float(threshold)
                    if pd.api.types.is_categorical_dtype(dataset[col]) or pd.api.types.is_object_dtype(dataset[col]):
                        prep.collapse_rare_categories(col, threshold_percentage=threshold)
                        logger.info(f"Collapsed rare categories in column: {col} with threshold: {threshold}")

            # Apply datetime parsing
            for datetime_config in config.get('standard_datetime_format', []):
                for col, format in datetime_config.items():
                    prep.parse_datetime(col, datetime_format=format)
                    logger.info(f"Parsed datetime in column: {col} with format: {format}")

            # Apply regular expression operations
            for regex_operation in config.get('regular_expression_operations', []):
                col = regex_operation.get("columnName")
                pattern = regex_operation.get("pattern")
                replace_with = regex_operation.get("replaceWith", "")
                prep.apply_regex(col, regex_pattern=pattern, replacement_string=replace_with, operation="replace")
                logger.info(f"Applied regex operation on column: {col}")

            # Apply text tokenization
            for text_tokenisation in config.get('text_tokenisation', []):
                if pd.api.types.is_string_dtype(dataset[col]):
                    prep.tokenize_text(col)
                    logger.info(f"Tokenized text in column: {col}")

        logger.info(f"Transformed dataset")

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


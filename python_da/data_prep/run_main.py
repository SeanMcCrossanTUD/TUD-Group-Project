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

if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_data_input = config["DATA_INPUT_CONTAINER"]


def apply_transformations(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations to the dataset using the functionalities defined in the DataPrep class.
    Parameters:
    dataset (pd.DataFrame): The dataset to transform.
    Returns:
    pd.DataFrame: The transformed dataset.
    """
    if not isinstance(dataset, pd.DataFrame):
        logging.error('Provided dataset is not a pandas DataFrame')
        raise TypeError('Expected dataset to be a pandas DataFrame')
    try:
        prep = DataPrep(dataset)
        prep.remove_duplicates()
    except Exception as e:
        logging.error(f'Error occurred during transformation: {e}')
        raise e

    logging.info('Data transformations applied successfully')
    return prep.dataframe


def apply_col_specific_transformations(dataset: pd.DataFrame, config_path: str) -> pd.DataFrame:
    """
    Apply column-specific transformations to the dataset based on the JSON configuration.

    Parameters:
    dataset (pd.DataFrame): The dataset to transform.
    config_path (str): Path to the JSON configuration file.

    Returns:
    pd.DataFrame: The transformed dataset.
    """
    if not isinstance(dataset, pd.DataFrame):
        logging.error('Provided dataset is not a pandas DataFrame')
        raise TypeError('Expected dataset to be a pandas DataFrame')

    try:
        # Load JSON configuration
        with open(config_path, 'r') as file:
            config = json.load(file)

        prep = DataPrep(dataset)

        # Fill missing values
        for col, params in config.get('fill_missing_values', {}).items():
            prep.fill_missing_values(col, method=params['method'], specific_value=params.get('specific_value'))

        # Normalize data
        for col, params in config.get('normalize_data', {}).items():
            prep.normalize_data(col, method=params['method'])

        # Remove special characters
        for col in config.get('remove_special_characters', []):
            prep.remove_special_characters(col)

        # Trim whitespace
        for col in config.get('trim_whitespace', []):
            prep.trim_whitespace(col)

        # Change column type
        for col, params in config.get('change_column_type', {}).items():
            prep.change_column_type(col, new_type=params['new_type'])

        # Label encode
        for col in config.get('label_encode', []):
            prep.label_encode(col)

        # Bin numeric to categorical
        for col, params in config.get('bin_numeric_to_categorical', {}).items():
            prep.bin_numeric_to_categorical(col, bins=params['bins'], labels=params.get('labels'))

        # Extract datetime components
        for col, params in config.get('extract_datetime_components', {}).items():
            prep.extract_datetime_components(col, components=params['components'])

        # Replace substring
        for col, params in config.get('replace_substring', {}).items():
            prep.replace_substring(col, old_substring=params['old_substring'], new_substring=params['new_substring'])

        # Parse datetime
        for col, params in config.get('parse_datetime', {}).items():
            prep.parse_datetime(col, datetime_format=params['datetime_format'])

        # Adjust text case
        for col, params in config.get('adjust_text_case', {}).items():
            prep.adjust_text_case(col, case_format=params['case_format'])

        # Remove stopwords
        for col, params in config.get('remove_stopwords', {}).items():
            prep.remove_stopwords(col, language=params['language'])

        # Collapse rare categories
        for col, params in config.get('collapse_rare_categories', {}).items():
            prep.collapse_rare_categories(col, threshold_percentage=params['threshold_percentage'])

        # Remove columns
        for col in config.get('remove_columns', {}).get('columns_to_remove', []):
            prep.remove_column(col)

        logging.info('Column-specific transformations applied successfully')
        return prep.dataframe

    except FileNotFoundError:
        logging.error(f'Configuration file {config_path} not found')
        raise
    except json.JSONDecodeError:
        logging.error(f'Error parsing JSON from {config_path}')
        raise
    except Exception as e:
        logging.error(f'Error occurred during column-specific transformation: {e}')
        raise e



def main(test_iterations=None):
    counter = 0

    while True:
        # If test_iterations is set and counter has reached it, break the loop
        if test_iterations and counter >= test_iterations:
            break

        # Check Azure queue for a new message
        try:
            msg = receive_message_from_queue(SERVICE_BUS_CONNECTION_STRING, SERVICE_BUS_QUEUE_NAME)
            logger.info(msg)
            if msg is not None:
                logger.info('Received a new message, processing...')
                cleaned_msg = str(msg).replace("'", "\"")
                message_content = json.loads(cleaned_msg)

                filename = message_content.get('rawurl', 'Unknown Filename') 
                jobID = message_content.get('jobID', 'Unknown JobID')

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

                result = apply_transformations(data)
                
                if file_extension == '.csv':
                    upload_result_csv_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'CSV result uploaded for {filename}')
                elif file_extension == '.xlsx' or file_extension == '.xls':
                    upload_result_excel_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'Excel result uploaded for {filename}')
                
                logger.info('Clean data uploaded in data prep')
            else:
                logger.info('No new messages. Waiting for next check...')
            
            time.sleep(600)  # waits for 60 seconds before checking again

        except AzureError as ae:
            logger.error(f"AzureError: {str(ae)}")
        except pd.errors.EmptyDataError as ede:
            logger.error(f"Pandas EmptyDataError: {str(ede)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()


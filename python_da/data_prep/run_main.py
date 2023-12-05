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
            logging.info(f"Filling missing values for {col}")
            prep.fill_missing_values(col, method=params['method'], specific_value=params.get('specific_value'))

        # Normalize data
        for col, params in config.get('normalize_data', {}).items():
            logging.info(f"Normalizing data for {col}")
            prep.normalize_data(col, method=params['method'])

        # Remove special characters
        for col in config.get('remove_special_characters', []):
            logging.info(f"Removing special characters from {col}")
            prep.remove_special_characters(col)

        # Trim whitespace
        for col in config.get('trim_whitespace', []):
            logging.info(f"Trimming whitespace in {col}")
            prep.trim_whitespace(col)

        # Change column type
        for col, params in config.get('change_column_type', {}).items():
            logging.info(f"Changing column type for {col}")
            prep.change_column_type(col, new_type=params['new_type'])

        # Label encode
        for col in config.get('label_encode', []):
            logging.info(f"Label encoding {col}")
            prep.label_encode(col)

        # Bin numeric to categorical
        for col, params in config.get('bin_numeric_to_categorical', {}).items():
            logging.info(f"Binning numeric data to categorical for {col}")
            prep.bin_numeric_to_categorical(col, bins=params['bins'], labels=params.get('labels'))

        # Extract datetime components
        for col, params in config.get('extract_datetime_components', {}).items():
            logging.info(f"Extracting datetime components for {col}")
            prep.extract_datetime_components(col, components=params['components'])

        # Replace substring
        for col, params in config.get('replace_substring', {}).items():
            logging.info(f"Replacing substring in {col}")
            prep.replace_substring(col, old_substring=params['old_substring'], new_substring=params['new_substring'])

        # Parse datetime
        for col, params in config.get('parse_datetime', {}).items():
            logging.info(f"Parsing datetime for {col}")
            prep.parse_datetime(col, datetime_format=params['datetime_format'])

        # Adjust text case
        for col, params in config.get('adjust_text_case', {}).items():
            logging.info(f"Adjusting text case for {col}")
            prep.adjust_text_case(col, case_format=params['case_format'])

        # Remove stopwords
        for col, params in config.get('remove_stopwords', {}).items():
            logging.info(f"Removing stopwords from {col}")
            prep.remove_stopwords(col, language=params['language'])

        # Collapse rare categories
        for col, params in config.get('collapse_rare_categories', {}).items():
            logging.info(f"Collapsing rare categories in {col}")
            prep.collapse_rare_categories(col, threshold_percentage=params['threshold_percentage'])

        # Remove columns
        for col in config.get('remove_columns', {}).get('columns_to_remove', []):
            logging.info(f"Removing column {col}")
            prep.remove_column(col)

        logging.info('All column-specific transformations applied successfully')
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
            msg = receive_message_from_queue(SERVICE_BUS_CONNECTION_STRING, SERVICE_BUS_QUEUE_NAME)
            logger.info(msg)
            if msg is not None:
                logger.info('Received a new message, processing...')
                cleaned_msg = str(msg).replace("'", "\"")
                message_content = json.loads(cleaned_msg)

                filename = message_content.get('rawurl', 'Unknown Filename') 
                json_file_name = message_content.get('rawurl', 'Unknown Filename')
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

                result = apply_col_specific_transformations(data, json_rules)
                
                if file_extension == '.csv':
                    upload_result_csv_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'CSV result uploaded for {filename}')
                elif file_extension == '.xlsx' or file_extension == '.xls':
                    upload_result_excel_to_azure(result, connection_string, jobID, filename)
                    logger.info(f'Excel result uploaded for {filename}')
                
                logger.info('Clean data uploaded in data prep')
            else:
                logger.info('No new messages. Waiting for next check...')
            
            time.sleep(5)  # waits for 5 seconds before checking again

        except AzureError as ae:
            logger.error(f"AzureError: {str(ae)}")
        except pd.errors.EmptyDataError as ede:
            logger.error(f"Pandas EmptyDataError: {str(ede)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()


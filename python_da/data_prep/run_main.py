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


def main():
    while True:
        try:
            logger.info('Checking for new messages...')

            # Receiving a message from the queue to get a new blob or file for processing.
            msg = receive_message_from_queue(SERVICE_BUS_CONNECTION_STRING, SERVICE_BUS_QUEUE_NAME)
            logger.info(msg)
            
            logger.info(msg)
            if msg is not None:
                logger.info('Received a new message, processing...')
                cleaned_msg = str(msg).replace("'", "\"")
                message_content = json.loads(cleaned_msg)

                filename = message_content.get('rawurl', 'Unknown Filename') 
                jobID = message_content.get('jobID', 'Unknown JobID')                

                data = download_blob_csv_data(connection_string=connection_string, container_name=container_name_data_input, file_name=filename)
                result = apply_transformations(data)
                upload_result_csv_to_azure(result, connection_string=connection_string, job_id=jobID, file_name=filename)
                
                logger.info('Clean data uploaded in data prep')
            else:
                logger.info('No new messages. Waiting for next check...')
            
            # Wait for a while before checking again, to not overwhelm your resources.
            time.sleep(600)  # waits for 60 seconds before checking again

        except AzureError as ae:
            logger.error(f"AzureError: {str(ae)}")
        except pd.errors.EmptyDataError as ede:
            logger.error(f"Pandas EmptyDataError: {str(ede)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()


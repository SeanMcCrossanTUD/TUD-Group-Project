import os
import io
import logging
from flask import Flask, jsonify
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from .data_prep import DataPrep


# Set up logging
logger = logging.getLogger('data-prep')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

connection_string = os.getenv('AZURE_CONNECTION_STRING')
if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_csv = "csv"

@app.route('/health', methods=['GET'])
def health_check():
    """
    Serves as a health check endpoint for the application.
    If it returns a 200 then we know that the application is working as expected.
    """
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    }), 200


def download_blob_csv_data():
    """
    Downloads the CSV from Azure Blob Storage, converts it into a Pandas DataFrame, and returns it.

    This function initializes a BlobServiceClient using the connection credenitals, retrieves the blob client for a specific
    container, and lists all blobs within that container. For now we assume only one blob in the container
    (May be subject to change) and retrieves it's name.
    The function then downloads this blob, decodes the CSV data from it, and reads this data into
    a Pandas DataFrame which is then returned.

    Logging and error handling is utilized to provide information about the process
    and to provide specific errors. 

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the CSV data downloaded from Azure Blob Storage.

    Raises:
        AzureError: If there is an Azure-specific error while trying to download the blob data.
        Exception: For general exceptions that might occur while trying to download the blob data.
    """

    try:
        logger.info('Initializing BlobServiceClient')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name_csv)
        blob_list = container_client.list_blobs()
        blob_name = next(blob_list).name  # Assumes only one blob

        logger.info(f'Downloading CSV data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client(container_name_csv, blob_name)
        blob_data = blob_client.download_blob()
        csv_data = blob_data.readall().decode('utf-8')
        data = pd.read_csv(io.StringIO(csv_data))

        return data

    except AzureError as ae:
        logger.error(f"AzureError while downloading blob data: {str(ae)}")
        raise ae 
    except Exception as e:
        logger.error(f"Unexpected error while downloading blob data: {str(e)}")
        raise e 


def upload_result_csv_to_azure(result):
    
    # Get the current time in epoch format and convert it to a string
    timestamp = str(int(time.time()))
    
    # Define the name of the result blob with the epoch timestamp
    result_blob_name = f'clean_data_{timestamp}.csv'
    
    # Define the name of the container to upload the result
    result_container_name = 'flaskapi2output'
    
    try:
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get the blob client for the result
        blob_client = blob_service_client.get_blob_client(result_container_name, result_blob_name)
        
        # Upload the result df to Azure Blob Storage
        blob_client.upload_blob(result.to_csv(index=False), overwrite=True)
        logger.info(f'Successfully uploaded {result_blob_name} to {result_container_name} in Azure Blob Storage')
    
    except AzureError as ae:
        logger.error(f"AzureError while uploading result to Azure Blob Storage: {str(ae)}")
        raise ae 
    except Exception as e:
        logger.error(f"Unexpected error while uploading result to Azure Blob Storage: {str(e)}")
        raise e 


def apply_transformations(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations to the dataset using the functionalities defined in the DataPrep class.
    Parameters:
    dataset (pd.DataFrame): The dataset to transform.
    Returns:
    pd.DataFrame: The transformed dataset.
    """
    # Ensure dataset is of the right type
    if not isinstance(dataset, pd.DataFrame):
        logging.error('Provided dataset is not a pandas DataFrame')
        raise TypeError('Expected dataset to be a pandas DataFrame')
    try:
        # Initialize DataPrep with the dataset
        prep = DataPrep(dataset)

        # Remove duplicate rows
        prep.remove_duplicates()

    except Exception as e:
        logging.error(f'Error occurred during transformation: {e}')
        raise e
    # If everything went fine, log the successful transformation
    logging.info('Data transformations applied successfully')
    # Return the transformed dataset
    return prep.dataframe

@app.route('/data-prep', methods=['GET'])
def data_quality_check():
    try:
        logger.info('Running Data Prep module!')
        data = download_blob_csv_data()
        result = apply_transformations(data)

        # Upload the result to Azure Blob Storage
        upload_result_csv_to_azure(result)

        return 'Clean data uploaded in data prep'

    except AzureError as ae:
        logger.error(f"AzureError: {str(ae)}")
        return jsonify({'error': str(ae), 'type': 'AzureError'}), 500
    except pd.errors.EmptyDataError as ede:
        logger.error(f"Pandas EmptyDataError: {str(ede)}")
        return jsonify({'error': str(ede), 'type': 'EmptyDataError'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e), 'type': str(type(e).__name__)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

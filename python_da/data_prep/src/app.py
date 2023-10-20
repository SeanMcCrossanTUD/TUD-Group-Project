import os
import io
import logging
from flask import Flask, jsonify
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from .data_prep import DataPrep
from azure_package.src.azure_functions import (download_blob_csv_data, 
                                            upload_result_csv_to_azure,
                                            send_message_to_queue,
                                            receive_message_from_queue)

# Set up logging
logger = logging.getLogger('data-prep')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

# Load configuration from JSON file
with open('python_da/pyconfigurations/azure_config.json', 'r') as file:
    config = json.load(file)

SERVICE_BUS_CONNECTION_STRING = config["SERVICE_BUS_CONNECTION_STRING"]
SERVICE_BUS_QUEUE_NAME = config["SERVICE_BUS_QUEUE_1_NAME"]
connection_string = config["AZURE_CONNECTION_STRING"]

if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_data_input = config["DATA_INPUT_CONTAINER"]

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


 # Define an endpoint accessible via the GET method
@app.route('/data-prep', methods=['GET']) 
def data_prep():
    try:
        # Log the initiation of the data preparation process
        logger.info('Running Data Prep module!')

        # Download CSV data from a storage
        data = download_blob_csv_data(connection_string=connection_string, container_name=container_name_data_input)

        # Apply transformations to the downloaded data
        result = apply_transformations(data)

        # Upload the transformed result to Azure Blob Storage
        upload_result_csv_to_azure(result,connection_string=connection_string)

        # Send a message to the queue after uploading
        send_message_to_queue("Clean data uploaded.", service_bus_connection_string=SERVICE_BUS_CONNECTION_STRING)
        
        # Return a success message if everything goes well
        return 'Clean data uploaded in data prep'

    # Handle Azure-specific errors
    except AzureError as ae:
        logger.error(f"AzureError: {str(ae)}")
        return jsonify({'error': str(ae), 'type': 'AzureError'}), 500

    # Handle cases where the CSV data is empty
    except pd.errors.EmptyDataError as ede:
        logger.error(f"Pandas EmptyDataError: {str(ede)}")
        return jsonify({'error': str(ede), 'type': 'EmptyDataError'}), 500

    # Handle all other unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e), 'type': str(type(e).__name__)}), 500

#run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Start the app with debugging enabled on port 5000


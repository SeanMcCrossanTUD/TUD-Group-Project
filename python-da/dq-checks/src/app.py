import os
import io
import logging
from flask import Flask, jsonify
import json
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from .data_quality_checker import DataQualityChecker

# Set up logging
logger = logging.getLogger('data-quality-check')
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

container_name = "csv"

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
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        blob_name = next(blob_list).name  # Assumes only one blob

        logger.info(f'Downloading CSV data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
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


def perform_data_quality_checks(data):
    """
    Perform data quality checks on the given data.

    Parameters:
    data (pd.DataFrame): The data on which to perform data quality checks.

    Returns:
    dict: A dictionary containing the results of the data quality checks.
    """
    checker = DataQualityChecker(data)
    try:
        number_of_records = int(checker.count_number_of_records())
        logger.info(f'Successfully retrieved number_of_records: {number_of_records}')
    except KeyError as e:
        logger.error(f"KeyError accessing count_number_of_records: {e}")
        raise
    
    try:
        number_of_fields = int(checker.count_number_of_fields())
        logger.info(f'Successfully retrieved number_of_fields: {number_of_fields}')
    except KeyError as e:
        logger.error(f"KeyError accessing count_number_of_fields: {e}")
        raise
    
    try:
        number_of_duplicate_values = int(checker.count_duplicate_values())
        logger.info(f'Successfully retrieved number_of_duplicate_values: {number_of_duplicate_values}')
    except KeyError as e:
        logger.error(f"KeyError accessing count_duplicate_values: {e}")
        raise
    
    try:
        missing_values = checker.count_missing_values()
        logger.info(f'Successfully retrieved missing_values: {missing_values}')
    except KeyError as e:
        logger.error(f"KeyError accessing count_missing_values: {e}")
        raise
    
    try:
        unique_values = checker.count_unique_values_in_text_fields()
        logger.info(f'Successfully retrieved unique_values: {unique_values}')
    except KeyError as e:
        logger.error(f"KeyError accessing count_unique_values_in_text_fields: {e}")
        raise
    
    try:
        z_score_outliers = checker.z_score_outliers()
        logger.info(f'Successfully retrieved z_score_outliers')
    except KeyError as e:
        logger.error(f"KeyError accessing z_score_outliers: {e}")
        raise
    
    try:
        iqr_outliers = checker.iqr_outliers()
        logger.info(f'Successfully retrieved iqr_outliers')
    except KeyError as e:
        logger.error(f"KeyError accessing iqr_outliers: {e}")
        raise
    
    # Combine the results into a dictionary
    result = {
        'number_of_records': number_of_records,
        'number_of_fields': number_of_fields,
        'number_of_duplicate_values': number_of_duplicate_values,
        'missing_values': missing_values,
        'unique_values_in_text_fields': unique_values,
        'z_score_outliers': z_score_outliers,
        'iqr_outliers': iqr_outliers
    }

    return result

def save_results_to_json(result):
    
    result_path = "/Users/seanmccrossan/group_project/TUD-Group-Project/python-da/results"
    # Create the directory if it does not exist
    os.makedirs(result_path, exist_ok=True)
    
    # Define the name of the result file
    result_file = os.path.join(result_path, 'data_quality_result.json')
    
    # Write the result into a JSON file
    with open(result_file, 'w') as outfile:
        json.dump(result, outfile, indent=4)


@app.route('/data-quality-check', methods=['GET'])
def data_quality_check():
    try:
        logger.info('Running Data Profile module!')
        data = download_blob_csv_data()
        result = perform_data_quality_checks(data)
        # Save the result to a JSON file
        save_results_to_json(result)
        return jsonify(result), 200

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



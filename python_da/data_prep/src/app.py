import json
import os
import logging
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient

# Set up logging
logger = logging.getLogger('data-quality-prep')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set your Azure connection string here
connection_string = os.getenv('AZURE_CONNECTION_STRING')

def download_blob_json_data():
    """
    Downloads the JSON from Azure Blob Storage, converts it into a Python dictionary, and returns it.

    This function initializes a BlobServiceClient using the connection credentials, retrieves the blob client for a specific
    container (dataprofileoutput), and lists all blobs within that container. For now, we assume only one blob in the container
    (may be subject to change) and retrieves its name.
    The function then downloads this blob, decodes the JSON data from it, and converts this data into
    a Python dictionary which is then returned.

    Logging and error handling is utilized to provide information about the process
    and to provide specific errors. 

    Returns:
        dict: A Python dictionary containing the JSON data downloaded from Azure Blob Storage.

    Raises:
        AzureError: If there is an Azure-specific error while trying to download the blob data.
        Exception: For general exceptions that might occur while trying to download the blob data.
    """

    try:
        logger.info('Initializing BlobServiceClient')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client('dataprofileoutput')
        blob_list = container_client.list_blobs()
        blob_name = next(blob_list).name  # Assumes only one blob

        logger.info(f'Downloading JSON data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client('dataprofileoutput', blob_name)
        blob_data = blob_client.download_blob()
        json_data = blob_data.readall().decode('utf-8')
        data = json.loads(json_data)

        return data

    except AzureError as ae:
        logger.error(f"AzureError while downloading blob data: {str(ae)}")
        raise ae 
    except Exception as e:
        logger.error(f"Unexpected error while downloading blob data: {str(e)}")
        raise e 


def convert_outliers_dict_to_dataframe(outliers_dict):
    """
    Converts the dictionary of outliers into a Pandas DataFrame.

    Parameters:
    outliers_dict (dict): The dictionary of outliers (z_scores_outliers_method).

    Returns:
    pd.DataFrame: A Pandas DataFrame containing the outliers information.
    """
    # Flatten the nested dictionaries and create a list of all outlier info
    all_outliers = []
    for col, outlier_info_list in outliers_dict.items():
        all_outliers.extend(outlier_info_list)

    # Convert the list of outlier info dictionaries into a Pandas DataFrame
    outliers_df = pd.DataFrame(all_outliers)

    return outliers_df
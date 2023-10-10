import json
import os
import logging
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient
from .data_prep import DataPrep

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

        # Fill missing values (demonstrated for one column 'example_column' using mode)
        # You can expand or loop through columns as needed
        if 'example_column' in dataset.columns:
            prep.fill_missing_values('example_column', method='mode')
        else:
            logging.warning("'example_column' is not found in the dataset")

        # Remove duplicate rows
        prep.remove_duplicates()

        # Remove outliers based on z-score
        prep.remove_z_score_outliers()

        # Remove outliers based on IQR
        prep.remove_iqr_outliers()

    except Exception as e:
        logging.error(f'Error occurred during transformation: {e}')
        raise e

    # If everything went fine, log the successful transformation
    logging.info('Data transformations applied successfully')
    
    # Return the transformed dataset
    return prep.dataframe




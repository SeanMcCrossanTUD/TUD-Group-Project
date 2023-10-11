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

def convert_outliers_dict_to_dataframe(outliers_dict):
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
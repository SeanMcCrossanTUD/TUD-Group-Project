import os
import logging
from flask import Flask, jsonify
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError

from .data_quality_checker import DataQualityChecker
from .data_profiling_visuals import DataProfilingVisuals
from azure_package.src.azure_functions import (download_blob_csv_data, 
                                            upload_results_to_azure,
                                            upload_image_to_azure, 
                                            send_message_to_queue,
                                            receive_message_from_queue)

# Set up logging
logger = logging.getLogger('data-quality-check')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://fab5-mq.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=/i79GR2PUSm8IuWFqlgqCHP9BJ2+QYPm0+ASbDU8pRM='
SERVICE_BUS_QUEUE_NAME = 'q1'

connection_string = os.getenv('AZURE_CONNECTION_STRING')
if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_images = "imagesoutput"

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


def run_visuals_and_upload(data_quality_checker, connection_string, container_name_images):
    visuals = DataProfilingVisuals(data_quality_checker)

    # Define the methods to run and the corresponding blob names
    methods_and_blob_names = [
        (visuals.plot_missing_values, 'missing_values_plot'),
        (visuals.plot_unique_values_in_text_fields, 'unique_values_plot'),
        (visuals.plot_outlier_table, 'outlier_table'),
        (visuals.plot_outlier_scatter, 'outlier_scatter')
    ]

    # Run methods and upload images to Azure
    for method, blob_name_template in methods_and_blob_names:
        img_data = method()
        if img_data is not None:  # Check if the method returned image data
            timestamp = str(int(time.time()))
            blob_name = f'{blob_name_template}_{timestamp}.png'    
            upload_image_to_azure(img_data, blob_name, connection_string, container_name_images)



@app.route('/data-quality-check', methods=['GET'])
def data_quality_check():
    try:
        logger.info('Running Data Profile module!')
        data = download_blob_csv_data(connection_string=connection_string)
        result = perform_data_quality_checks(data)

        # Upload the result to Azure Blob Storage
        upload_results_to_azure(result, connection_string=connection_string)

        # Send a message to the queue after uploading
        send_message_to_queue("Data quality check complete json results uploaded.", service_bus_connection_string=SERVICE_BUS_CONNECTION_STRING)


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

@app.route('/data-profiling-images', methods=['GET'])
def data_profiling_images():
    try:
        logger.info('Running Data Profiling Images module!')
        
        # Download CSV data from Azure Blob Storage and convert it to a Pandas DataFrame
        data = download_blob_csv_data(connection_string=connection_string)
        
        # Initialize the DataQualityChecker with the downloaded data
        data_quality_checker = DataQualityChecker(data)
        
        # Run visuals and upload images to Azure Blob Storage
        run_visuals_and_upload(data_quality_checker, connection_string, container_name_images)

        send_message_to_queue("Data profile visuals created plots uploaded.", service_bus_connection_string=SERVICE_BUS_CONNECTION_STRING)
        
        return jsonify({'status': 'success', 'message': 'Data profiling images generated and uploaded successfully'}), 200

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



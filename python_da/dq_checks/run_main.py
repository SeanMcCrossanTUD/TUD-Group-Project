import os
import logging
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError

from dq_checks.src.data_quality_checker import DataQualityChecker
from dq_checks.src.data_profiling_visuals import DataProfilingVisuals
from dq_checks.azure_package.src.azure_functions import (
    download_blob_csv_data, 
    upload_results_to_azure,
    upload_meta_to_azure_data_preview,
    upload_image_to_azure,
    receive_message_from_queue
)
from dq_checks.src.meta_data_functions import dataframe_metadata_to_json
print("Current Directory:", os.getcwd())
print("Directory Contents:", os.listdir('.'))


# Set up logging
logger = logging.getLogger('data-quality-check')
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
SERVICE_BUS_QUEUE_NAME = config["SERVICE_BUS_QUEUE_1_NAME"]
connection_string = config["AZURE_CONNECTION_STRING"]

if connection_string is None:
    raise Exception("Failed to get connection string from environment variable")

container_name_images = config["IMAGE_OUTPUT_CONTAINER"]
container_name_data_input = config["DATA_INPUT_CONTAINER"]

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

def meta_data_to_blob(df):

    try:
        
        metadata_json = dataframe_metadata_to_json(df)
        logger.info("Meta data to json")
        return metadata_json

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
        

def run_visuals_and_upload(data_quality_checker, connection_string, container_name_images, jobId):
    visuals = DataProfilingVisuals(data_quality_checker)

    # Define the methods to run and the corresponding blob names
    methods_and_blob_names = [
        (visuals.plot_missing_values, 'missing_values_plot'),
        (visuals.plot_unique_values_in_text_fields, 'unique_values_plot'),
        (visuals.plot_outlier_table, 'outlier_table'),
        (visuals.plot_outlier_scatter, 'outlier_scatter')
    ]
    
    container_name_images = f'{container_name_images}/{jobId}'
    # Run methods and upload images to Azure
    for method, blob_name_template in methods_and_blob_names:
        img_data = method()
        if img_data is not None:  # Check if the method returned image data
            blob_name = f'{blob_name_template}.png'  
            upload_image_to_azure(img_data, blob_name, connection_string, container_name_images)

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
                
                filename = message_content.get('filename', 'Unknown Filename') 
                jobID = message_content.get('jobID', 'Unknown JobID')

                data = download_blob_csv_data(connection_string=connection_string, file_name=filename, container_name=container_name_data_input)
                logger.info(f'Download data complete for: {filename} - {jobID}')

                meta_data_result = meta_data_to_blob(df=data)
                logger.info(f'Meta data for Data Preview complete for: {filename} - {jobID}')

                upload_meta_to_azure_data_preview(meta_data_result, connection_string=connection_string, job_id=jobID)
                logger.info(f'Meta data for data preview uploaded for: {filename} - {jobID}')

                result = perform_data_quality_checks(data)
                logger.info(f'Data Quality checks complete for: {filename} - {jobID}')

                upload_results_to_azure(result, connection_string=connection_string, job_id=jobID)
                logger.info(f'Data Quality checks uploaded for: {filename} - {jobID}')

                data_quality_checker = DataQualityChecker(data)
                run_visuals_and_upload(data_quality_checker, connection_string, container_name_images,jobID)
                logger.info(f'Data profile images created and uploaded: {filename} - {jobID}')

                logger.info(f'Data profile images nessage sent to service bus queue: {filename} - {jobID}')
                time.sleep(6000)

                # Increment the counter
                counter += 1

        except AzureError as ae:
            logger.error(f"AzureError for {filename}: {str(ae)}")
        except pd.errors.EmptyDataError as ede:
            logger.error(f"Pandas EmptyDataError for {filename}: {str(ede)}")
        except Exception as e:
            logger.error(f"Unexpected error for {filename}: {str(e)}")


if __name__ == '__main__':
    main()
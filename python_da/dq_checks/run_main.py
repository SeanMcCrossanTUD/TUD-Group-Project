import os
import logging
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError
import numpy as np

from dq_checks.src.data_quality_checker import DataQualityChecker
from dq_checks.src.data_profiling_visuals import DataProfilingVisuals
from dq_checks.src.data_quality_evaluator import AdvancedDataQualityEvaluator
from dq_checks.azure_package.src.azure_functions import (
    download_blob_csv_data,
    download_blob_excel_data, 
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
OUTLIER_OUTPUT_CONTAINER = config["OUTLIER_OUTPUT_CONTAINER"]
DATA_QUALITY_SCORE_CONTAINER = config["DATA_QUALITY_SCORE_CONTAINER"]
BUBBLE_CHART_CONTAINER = config["BUBBLE_CHART_CONTAINER"]

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
        data_type_profile_count = checker.data_type_profile()
        logger.info(f'Successfully retrieved data_type_profile_count: {data_type_profile_count}')
    except KeyError as e:
        logger.error(f"KeyError accessing data_type_profile_count: {e}")
        raise
    
    
    # Combine the results into a dictionary
    result = {
        'number_of_records': number_of_records,
        'number_of_fields': number_of_fields,
        'number_of_duplicate_values': number_of_duplicate_values,
        'missing_values': missing_values,
        'data_type_profile': data_type_profile_count,
        'unique_values_in_text_fields': unique_values
    }

    return result

def run_outliers_result(data, threshold=3.0):
    # Certain charts become unusbale if the data is too much.
    if len(data) > 5000:
        data_sample = data.sample(n=5000, random_state=42)
    else:
        data_sample = data

    checker = DataQualityChecker(data_sample)
    outliers_result = checker.z_score_outliers(threshold)

    return outliers_result

def run_count_unique_values(data, max_unique_values=24):
    # Drop rows with NaN values in text columns
    text_columns = data.select_dtypes(include='object').columns
    data_cleaned = data.dropna(subset=text_columns)

    # Instantiate DataQualityChecker with the cleaned data
    checker = DataQualityChecker(data_cleaned)
    unique_values_result = checker.count_unique_value_frequencies_in_text_fields(max_unique_values)

    return unique_values_result


def calculate_overall_quality(data):
    """
    Calculate the overall data quality score based on completeness, uniqueness, consistency, and readability.

    Parameters:
    data (pd.DataFrame): The data on which to perform data quality evaluation.

    Returns:
    dict: A dictionary containing the individual scores and the overall quality score as a percentage.
    """
    quality_results = {}

    try:
        evaluator = AdvancedDataQualityEvaluator(data)
        logger.info("Data quality evaluator initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing data quality evaluator: {e}")
        raise

    try:
        completeness_score = evaluator.completeness()
        quality_results['completeness_score'] = completeness_score
        logger.info(f"Successfully calculated completeness score: {completeness_score}")
    except Exception as e:
        logger.error(f"Error calculating completeness score: {e}")
        raise

    try:
        uniqueness_score = evaluator.uniqueness()
        quality_results['uniqueness_score'] = uniqueness_score
        logger.info(f"Successfully calculated uniqueness score: {uniqueness_score}")
    except Exception as e:
        logger.error(f"Error calculating uniqueness score: {e}")
        raise

    try:
        consistency_score = evaluator.consistency()
        quality_results['consistency_score'] = consistency_score
        logger.info(f"Successfully calculated consistency score: {consistency_score}")
    except Exception as e:
        logger.error(f"Error calculating consistency score: {e}")
        raise

    try:
        readability_scores = [evaluator.readability(col) for col in evaluator.df.columns if evaluator.df[col].dtype == 'object']
        average_readability = np.mean(readability_scores) if readability_scores else 1
        quality_results['average_readability'] = average_readability
        logger.info(f"Successfully calculated average readability score: {average_readability}")
    except Exception as e:
        logger.error(f"Error calculating readability scores: {e}")
        raise

    try:
        overall_score = (completeness_score + uniqueness_score + consistency_score + average_readability) / 4
        quality_results['overall_score'] = overall_score * 100
        logger.info(f"Successfully calculated overall quality score: {overall_score}")
    except Exception as e:
        logger.error(f"Error calculating overall quality score: {e}")
        raise
    try:
        if overall_score >= 80:
            colour_score = "Green"
        elif 60 <= overall_score < 80:
            colour_score = "Yellow"
        elif 40 <= overall_score < 60:
            colour_score = "Orange" 
        else:
            colour_score = "Red"
    
        quality_results['color'] = colour_score
        logger.info(f"Successfully calculated colour score: {colour_score}")
    except Exception as e:
        logger.error(f"Error calculating colour scheme: {e}")
        raise


    return quality_results

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
        time.sleep(30)
        logger.info("sleep finished")
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

                file_extension = os.path.splitext(filename)[1].lower()
                if file_extension in ['.xlsx', '.xls']:
                    data = download_blob_excel_data(connection_string=connection_string, file_name=filename, container_name=container_name_data_input)
                elif file_extension == '.csv':
                    data = download_blob_csv_data(connection_string=connection_string, file_name=filename, container_name=container_name_data_input)
                else:
                    logger.error(f'Unsupported file format for file: {filename}. Only CSV and Excel files are supported.')
                    continue  # Skip to the next iteration

                meta_data_result = meta_data_to_blob(df=data)
                logger.info(f'Meta data for Data Preview complete for: {filename} - {jobID}')

                upload_meta_to_azure_data_preview(meta_data_result, connection_string=connection_string, job_id=jobID)
                logger.info(f'Meta data for data preview uploaded for: {filename} - {jobID}')

                result = perform_data_quality_checks(data)
                logger.info(f'Data Quality checks complete for: {filename} - {jobID}')

                upload_results_to_azure(result, connection_string=connection_string, job_id=jobID)
                logger.info(f'Data Quality checks uploaded for: {filename} - {jobID}')

                outlier_result = run_outliers_result(data=data, threshold=3.0)

                # Upload the result to Azure Blob Storage
                upload_results_to_azure(outlier_result, connection_string, jobID, OUTLIER_OUTPUT_CONTAINER)
                logger.info("Z-score outliers analysis results uploaded successfully for  {filename} - {jobID}")

                dq_score = calculate_overall_quality(data=data)
                logger.info("Overall quality score calculated")

                upload_results_to_azure(dq_score, connection_string, jobID, DATA_QUALITY_SCORE_CONTAINER)
                logger.info("Data quality score results uploaded successfully for  {filename} - {jobID}")

                unique_values_count = run_count_unique_values(data=data, max_unique_values=24)
                logger.info("Number of unique values counted")

                upload_results_to_azure(unique_values_count, connection_string, jobID, BUBBLE_CHART_CONTAINER)
                logger.info("Number of unique results uploaded successfully for  {filename} - {jobID}")

                #logger.info(f'Data profile images nessage sent to service bus queue: {filename} - {jobID}')
                logger.info("Data profile success")
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
import os
import io
import logging
import json
import time
import pandas as pd
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from data_prep.rds_sql_package.src.rds_sql_functions import update_rds_data_profile, update_rds_data_clean

# Set up logging
logger = logging.getLogger('azure-package')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def download_blob_csv_data(connection_string, file_name, container_name="csv"):
    """Download CSV data from Azure Blob Storage.

    Args:
    - connection_string (str): The Azure connection string.
    - container_name (str, optional): Name of the Azure blob container. Defaults to 'csv'.

    Returns:
    - pd.DataFrame: DataFrame containing downloaded CSV data.
    """

    try:
        logger.info('Initializing BlobServiceClient')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_name = file_name

        if blob_name is None:
            logger.error('No blobs found in container')
            raise Exception('No blobs found in the container')

        logger.info(f'Downloading CSV data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        blob_data = blob_client.download_blob()
        csv_data = blob_data.readall().decode('utf-8')

        if not csv_data.strip():
            logger.warning("Downloaded CSV data is empty or contains only whitespace. No acceptable data.")
            return None

        data = pd.read_csv(io.StringIO(csv_data))
        return data

    except AzureError as ae:
        logger.error(f"AzureError while downloading blob data: {str(ae)}")
        raise ae
    except Exception as e:
        logger.error(f"Unexpected error while downloading blob data: {str(e)}")
        raise e

def download_blob_json_data(connection_string, file_name, container_name="rules"):
    """Download JSON data from Azure Blob Storage.

    Args:
    - connection_string (str): The Azure connection string.
    - container_name (str, optional): Name of the Azure blob container. Defaults to 'rules'.

    Returns:
    - str: JSON string containing the downloaded data.
    """

    try:
        logger.info('Initializing BlobServiceClient')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_name = file_name

        if not blob_name:
            logger.error('No blobs found in container')
            raise Exception('No blobs found in the container')

        logger.info(f'Downloading JSON data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob()
        json_data = blob_data.readall().decode('utf-8')

        if not json_data:
            logger.warning("Downloaded JSON data is empty or contains only whitespace. No acceptable data.")
            return None

        return json_data

    except Exception as e:
        logger.error(f"Error downloading blob data: {e}")
        raise

def download_blob_excel_data(connection_string, file_name, container_name="csv"):
    """Download Excel data from Azure Blob Storage.

    Args:
    - connection_string (str): The Azure connection string.
    - container_name (str, optional): Name of the Azure blob container. Defaults to 'excel'.

    Returns:
    - pd.DataFrame: DataFrame containing downloaded Excel data.
    """

    try:
        logger.info('Initializing BlobServiceClient')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_name = file_name

        if not blob_name:
            logger.error('No blobs found in container')
            raise Exception('No blobs found in the container')

        logger.info(f'Downloading Excel data from Azure Blob Storage: {blob_name}')
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        blob_data = blob_client.download_blob().readall()

        if not blob_data:
            logger.warning("Downloaded Excel data is empty. No acceptable data.")
            return None

        data = pd.read_excel(io.BytesIO(blob_data))
        return data

    except AzureError as ae:
        logger.error(f"AzureError while downloading blob data: {str(ae)}")
        raise ae
    except Exception as e:
        logger.error(f"Unexpected error while downloading blob data: {str(e)}")
        raise e

def upload_results_to_azure(data, connection_string, job_id, result_container_name='dataprofileoutput'):
    """Upload data as a JSON to Azure Blob Storage.

    Args:
    - data (dict): The data to be uploaded.
    - connection_string (str): The Azure connection string.
    - result_container_name (str, optional): Name of the Azure blob container for results. Defaults to 'dataprofileoutput'.
    """

    result_json = json.dumps(data, indent=4)
    timestamp = str(int(time.time()))
    result_blob_name = f'data_quality_result_{timestamp}.json'
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(result_container_name, result_blob_name)
        blob_client.upload_blob(result_json, overwrite=True)

        update_rds_data_profile(result_blob_name, job_id)
        logger.info(f'Successfully uploaded {result_blob_name} to {result_container_name} in Azure Blob Storage')

    except AzureError as ae:
        logger.error(f"AzureError while uploading result to Azure Blob Storage: {str(ae)}")
        raise ae
    except Exception as e:
        logger.error(f"Unexpected error while uploading result to Azure Blob Storage: {str(e)}")
        raise e

def upload_image_to_azure(img_data, blob_name, connection_string, container_name_images):
    """Upload image data to Azure Blob Storage.

    Args:
    - img_data (bytes): The image data to be uploaded.
    - blob_name (str): Name of the blob for the image.
    - connection_string (str): The Azure connection string.
    - container_name_images (str): Name of the Azure blob container for images.
    
    Returns:
    - str: Name of the uploaded blob.
    """

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name_images, blob_name)
        blob_client.upload_blob(img_data, overwrite=True)
        logger.info(f'Successfully uploaded {blob_name} to {container_name_images} in Azure Blob Storage')
        return blob_name

    except Exception as e:
        logger.error(f"Error while uploading image to Azure Blob Storage: {str(e)}")
        raise e

def upload_result_csv_to_azure(result, connection_string, job_id, file_name):
    """Upload a DataFrame as a CSV to Azure Blob Storage.

    Args:
    - result (pd.DataFrame): The DataFrame to be uploaded.
    - connection_string (str): The Azure connection string.
    """
    
    
    result_blob_name = f'data_polish_{file_name}'
    # result_blob_name = f'data_polish_{file_name.split(".")[0]}'
    
    # Define the name of the container to upload the result
    result_container_name = 'output'
    
    try:
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get the blob client for the result
        blob_client = blob_service_client.get_blob_client(result_container_name, result_blob_name)
        
        # Upload the result df to Azure Blob Storage
        blob_client.upload_blob(result.to_csv(index=False), overwrite=True)
        logger.info(f'Successfully uploaded {result_blob_name} to {result_container_name} in Azure Blob Storage')
        update_rds_data_clean(result_blob_name, job_id)
    
    except AzureError as ae:
        logger.error(f"AzureError while uploading result to Azure Blob Storage: {str(ae)}")
        raise ae 
    except Exception as e:
        logger.error(f"Unexpected error while uploading result to Azure Blob Storage: {str(e)}")
        raise e 

def upload_result_excel_to_azure(result, connection_string, job_id, file_name):
    """Upload a DataFrame as an Excel file to Azure Blob Storage.

    Args:
    - result (pd.DataFrame): The DataFrame to be uploaded.
    - connection_string (str): The Azure connection string.
    - job_id (str): The job ID associated with the upload.
    - file_name (str): The file name to be used in Azure Blob Storage.
    """
    
    result_blob_name = f'data_polish_{file_name}'
    # result_blob_name = f'data_polish_{file_name.split(".")[0]}'
    
    # Define the name of the container to upload the result
    result_container_name = 'output'
    
    # Convert DataFrame to Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result.to_excel(writer, index=False)
        writer.save()
    output.seek(0)
    
    try:
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get the blob client for the result
        blob_client = blob_service_client.get_blob_client(container=result_container_name, blob=result_blob_name)
        
        # Upload the Excel file to Azure Blob Storage
        blob_client.upload_blob(output, overwrite=True)
        logger.info(f'Successfully uploaded {result_blob_name} to {result_container_name} in Azure Blob Storage')
        
        # Update RDS with the blob name and job id after successful upload
        update_rds_data_clean(result_blob_name, job_id)
    
    except AzureError as ae:
        logger.error(f"AzureError while uploading result to Azure Blob Storage: {str(ae)}")
        raise ae 
    except Exception as e:
        logger.error(f"Unexpected error while uploading result to Azure Blob Storage: {str(e)}")
        raise e

def send_message_to_queue(job_id, filename, process, message, service_bus_connection_string, service_bus_queue_name='q1'):
    """Send a message to Azure Service Bus queue.

    Args:
    - job_id (str): The job ID associated with the process.
    - filename (str): The name of the file being processed.
    - process (str): The process being performed (e.g., "Data quality check").
    - message (str): The main message or result.
    - service_bus_connection_string (str): The Azure Service Bus connection string.
    - service_bus_queue_name (str, optional): Name of the Service Bus queue. Defaults to 'q1'.
    """

    # Constructing the JSON message body
    message_body = json.dumps({
        "jobID": job_id,
        "filename": filename,
        "process": process,
        "message": message
    })

    try:
        with ServiceBusClient.from_connection_string(service_bus_connection_string) as client:
            with client.get_queue_sender(queue_name=service_bus_queue_name) as sender:
                message = ServiceBusMessage(message_body)
                sender.send_messages(message)
                logger.info(f"Sent message to queue: {message_body}")

    except Exception as e:
        logger.error(f"Error sending message to queue: {str(e)}")
        raise e

def receive_message_from_queue(service_bus_connection_string, service_bus_queue_name='q1'):
    """Receive and log messages from Azure Service Bus queue.

    Args:
    - service_bus_connection_string (str): The Azure Service Bus connection string.
    - service_bus_queue_name (str, optional): Name of the Service Bus queue. Defaults to 'q1'.
    
    Returns:
    dict or None: The received message as a dictionary or None if no message is received.
    """

    try:
        with ServiceBusClient.from_connection_string(service_bus_connection_string) as client:
            with client.get_queue_receiver(queue_name=service_bus_queue_name, max_wait_time=5) as receiver:
                # Get the first message
                msg = next(receiver, None)
                if msg:
                    # Parse the message body as JSON
                    message_content = json.loads(str(msg))
                    logger.info(f"Received message from queue: {message_content}")
                    receiver.complete_message(msg)
                    return message_content  # Return the parsed message content

    except Exception as e:
        logger.error(f"Error receiving message from queue: {str(e)}")
        raise e

    return None  # Return None if no message was received



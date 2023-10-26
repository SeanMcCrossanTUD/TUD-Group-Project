import pymysql
import json
import logging

# Set up logging
logger = logging.getLogger('rds-sql-package')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load configuration from JSON file
with open('python_da/pyconfigurations/sql_config.json', 'r') as file:
    config = json.load(file)

RDS_HOST = config["RDS_HOST"]
RDS_PORT = config["RDS_PORT"]
RDS_DB_NAME = config["RDS_DB_NAME"]
RDS_USER = config["RDS_USER"]
RDS_PASSWORD = config["RDS_PASSWORD"]
RDS_TABLE = config["RDS_TABLE"]
RDS_COLUMN_DATA_PROFILE = config["RDS_COLUMN_DATA_PROFILE"]
RDS_COLUMN_DATA_CLEAN = config["RDS_COLUMN_DATA_CLEAN"]

def update_rds_data_profile(filename, job_id):
    """Updates a filename in the AWS RDS table based on job_id."""
    connection = None
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            port=int(RDS_PORT),
            db=RDS_DB_NAME,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = connection.cursor()

        # Construct the update query
        update_query = f"UPDATE {RDS_TABLE} SET {RDS_COLUMN_DATA_PROFILE} = %s WHERE jobid = %s;"
        
        cursor.execute(update_query, (filename, job_id))
        connection.commit()

    except Exception as e:
        logger.error(f"Error while updating RDS: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_rds_data_clean(filename, job_id):
    """Updates a filename in the AWS RDS table based on job_id."""
    connection = None
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            port=int(RDS_PORT),
            db=RDS_DB_NAME,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = connection.cursor()

        # Construct the update query
        update_query = f"UPDATE {RDS_TABLE} SET {RDS_COLUMN_DATA_CLEAN} = %s WHERE jobid = %s;"
        
        cursor.execute(update_query, (filename, job_id))
        connection.commit()

    except Exception as e:
        logger.error(f"Error while updating RDS: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()

def select_all_from_rds():
    """Fetches all records from the AWS RDS table."""
    connection = None
    results = []
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            port=int(RDS_PORT),
            db=RDS_DB_NAME,
            user=RDS_USER,
            password=RDS_PASSWORD
        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        select_query = f"SELECT * FROM {RDS_TABLE};"
        cursor.execute(select_query)
        
        results = cursor.fetchall()

        # Log the results
        for result in results:
            logger.info(f"Retrieved record: {result}")

    except Exception as e:
        logger.error(f"Error while fetching from RDS: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

    return results

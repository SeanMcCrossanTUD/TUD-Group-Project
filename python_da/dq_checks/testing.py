import argparse
import pandas as pd
from dq_checks.src.data_quality_checker import DataQualityChecker
import logging
import json
import os
import numpy as np

# Configure logging
logger = logging.getLogger('data-quality-check')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class NumpyEncoder(json.JSONEncoder):
    """ Custom JSON encoder for NumPy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# Usage example
def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, cls=NumpyEncoder, ensure_ascii=False, indent=4)

def perform_data_quality_checks(data, output_dir="output"):


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
    
    try:
        z_score_outliers = checker.z_score_outliers()
        logger.info(f'Successfully retrieved z_score_outliers')
    except KeyError as e:
        logger.error(f"KeyError accessing z_score_outliers: {e}")
        raise

    os.makedirs(output_dir, exist_ok=True)


    write_to_json({'number_of_records': number_of_records}, os.path.join(output_dir, 'number_of_records.json'))


    write_to_json({'number_of_fields': number_of_fields}, os.path.join(output_dir, 'number_of_fields.json'))


    write_to_json({'number_of_duplicate_values': number_of_duplicate_values}, os.path.join(output_dir, 'number_of_duplicate_values.json'))


    write_to_json({'missing_values': missing_values}, os.path.join(output_dir, 'missing_values.json'))


    write_to_json({'data_type_profile': data_type_profile_count}, os.path.join(output_dir, 'data_type_profile.json'))


    write_to_json({'unique_values_in_text_fields': unique_values}, os.path.join(output_dir, 'unique_values_in_text_fields.json'))



    outlier_result = {
        "fields": list(z_score_outliers.keys()),
        "outliers": z_score_outliers
    }
    write_to_json(outlier_result, os.path.join(output_dir, 'z_score_outliers.json'))

    # If you had more checks, you would continue the pattern here...

    return {
        'status': 'Data quality checks completed and results written to JSON files.'
    }

def main():
    parser = argparse.ArgumentParser(description="Run Data Quality Checks on a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file to analyze.")
    parser.add_argument("-o", "--output", default="output", help="Output directory for JSON results.")
    
    args = parser.parse_args()

    # Read the CSV file
    try:
        data = pd.read_csv(args.csv_file)
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        return

    # Perform data quality checks
    try:
        result = perform_data_quality_checks(data, output_dir=args.output)
        print(result)
    except Exception as e:
        logger.error(f"Error during data quality checks: {e}")

if __name__ == "__main__":
    main()

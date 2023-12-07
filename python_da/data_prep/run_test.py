import json
import pandas as pd
from data_prep.src.data_prep import DataPrep
import logging
# Set up logging
logger = logging.getLogger('data-prep')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
def apply_configured_transformations(json_config, dataset_path, output_path):
    # Load dataset
    dataset = pd.read_csv(dataset_path)
    prep = DataPrep(dataset)

    # Parse JSON configuration
    config = json.loads(json_config)

    # Remove columns not in columns_kept
    columns_kept = config.get('columns_kept', [])
    columns_to_remove = [col for col in dataset.columns if col not in columns_kept]
    prep.remove_columns(columns_to_remove)

    # Apply transformations based on column data type
    for col in dataset.columns:
        # Trim whitespace in text columns
        if col in config.get('trim_whitespace', []) and pd.api.types.is_string_dtype(dataset[col]):
            prep.trim_whitespace(col)

        # Remove special characters in text columns
        if col in config.get('remove_special_characters', []) and pd.api.types.is_string_dtype(dataset[col]):
            prep.remove_special_characters(col)

        # Normalize data in numeric columns
        for normalization in config.get('normalize_data', []):
            if col in normalization and pd.api.types.is_numeric_dtype(dataset[col]):
                method = normalization[col]['method']['types']
                prep.normalize_data(col, method)

        # Fill missing values
        for imputation in config.get('missing_value_imputation', []):
            if col in imputation:
                method = imputation[col]['method']
                method = method.lower()
                prep.fill_missing_values(col, method=method)

        # Remove stopwords in text columns
        if col in config.get('remove_stopwords', []) and pd.api.types.is_string_dtype(dataset[col]):
            prep.remove_stopwords(col)

        # Label encoding in categorical columns
        if col in config.get('label_encoding', []) and pd.api.types.is_categorical_dtype(dataset[col]):
            prep.label_encode(col)

        # Numerical column binning in numeric columns
        for binning in config.get('numerical_column_binning', []):
            if col in binning and pd.api.types.is_numeric_dtype(dataset[col]):
                bins = sorted(binning[col])  # Sort the bins
                prep.bin_numeric_to_categorical(col, bins)

    # Adjust text case in text columns
    for adjustment in config.get('textcase_adjustment', []):
        for col, case_format in adjustment.items():
            case_format = case_format.lower()
            if pd.api.types.is_string_dtype(dataset[col]):
                prep.adjust_text_case(col, case_format)

    # Replace substring in text columns
    for replacement in config.get('replace_substring', []):
        for col, substrings in replacement.items():
            if pd.api.types.is_string_dtype(dataset[col]):
                for old_substring, new_substring in substrings.items():
                    prep.replace_substring(col, old_substring, new_substring)

    # Collapse rare categories in categorical columns
    for col in config.get('collapse_rare_categories', []):
        if pd.api.types.is_categorical_dtype(dataset[col]):
            prep.collapse_rare_categories(col, threshold_percentage=5.0)
    
        # Rename column names
    for renaming in config.get('rename_column_name', []):
        for old_name, new_name in renaming.items():
            prep.rename_column(old_name, new_name)
    
        # Standard datetime format parsing
    for datetime_config in config.get('standard_datetime_format', []):
        for col, format in datetime_config.items():
            prep.parse_datetime(col, datetime_format=format)

    # Regular expression operations
    for regex_operation in config.get('regular_expresion_operations', []):
        col = regex_operation.get("columnName")
        method = regex_operation.get("method")
        pattern = regex_operation.get("pattern")
        replace_with = regex_operation.get("replaceWith", "")

        if method == "Replace":
            prep.apply_regex(col, regex_pattern=pattern, replacement_string=replace_with, operation="replace")

    # Collapse rare categories
    for collapse_config in config.get('collapse_rare_caregories', []):
        for col, threshold in collapse_config.items():
            threshold = float(threshold)  # Convert threshold to float
            prep.collapse_rare_categories(col, threshold_percentage=threshold)

    # Text tokenization
    for text_tokenisation in config.get('text_tokenisation', []):
        prep.tokenize_text(text_tokenisation)
    

    prep.dataframe.to_csv(output_path, index=False)

# Initialize logger
logger = logging.getLogger(__name__)

def apply_configured_transformations(json_config, dataset_path, output_path):
    try:
        # Load dataset
        dataset = pd.read_csv(dataset_path)
        logger.info(f"Dataset loaded from {dataset_path}")
        prep = DataPrep(dataset)

        # Parse JSON configuration
        config = json.loads(json_config)

        # Remove columns not in columns_kept
        columns_kept = config.get('columns_kept', [])
        columns_to_remove = [col for col in dataset.columns if col not in columns_kept]
        if columns_to_remove:
            prep.remove_columns(columns_to_remove)
            logger.info(f"Removed columns: {columns_to_remove}")

        # Apply transformations based on column data type
        for col in dataset.columns:
            # Check and apply trim whitespace
            if col in config.get('trim_whitespace', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.trim_whitespace(col)
                logger.info(f"Trimmed whitespace in column: {col}")

            # Check and apply removal of special characters
            if col in config.get('remove_special_characters', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.remove_special_characters(col)
                logger.info(f"Removed special characters in column: {col}")

            # Apply normalization on numeric columns
            for normalization in config.get('normalize_data', []):
                if col in normalization and pd.api.types.is_numeric_dtype(dataset[col]):
                    method = normalization[col]['method']['types']
                    prep.normalize_data(col, method)
                    logger.info(f"Normalized data in column: {col} using method: {method}")

            # Apply missing value imputation
            for imputation in config.get('missing_value_imputation', []):
                if col in imputation:
                    method = imputation[col]['method'].lower()
                    prep.fill_missing_values(col, method=method)
                    logger.info(f"Filled missing values in column: {col} using method: {method}")

            # Apply removal of stopwords on text columns
            if col in config.get('remove_stopwords', []) and pd.api.types.is_string_dtype(dataset[col]):
                prep.remove_stopwords(col)
                logger.info(f"Removed stopwords in column: {col}")

            # Apply label encoding on categorical columns
            if col in config.get('label_encoding', []) and pd.api.types.is_categorical_dtype(dataset[col]):
                prep.label_encode(col)
                logger.info(f"Label encoded column: {col}")

            # Apply numerical column binning
            for binning in config.get('numerical_column_binning', []):
                if col in binning and pd.api.types.is_numeric_dtype(dataset[col]):
                    bins = sorted(binning[col])  # Sort the bins
                    prep.bin_numeric_to_categorical(col, bins)
                    logger.info(f"Binned numeric column: {col} into categories")

            # Apply text case adjustment
            for adjustment in config.get('textcase_adjustment', []):
                for col, case_format in adjustment.items():
                    if pd.api.types.is_string_dtype(dataset[col]):
                        prep.adjust_text_case(col, case_format.lower())
                        logger.info(f"Adjusted text case in column: {col} to {case_format}")

            # Apply substring replacement
            for replacement in config.get('replace_substring', []):
                for col, substrings in replacement.items():
                    if pd.api.types.is_string_dtype(dataset[col]):
                        for old_substring, new_substring in substrings.items():
                            prep.replace_substring(col, old_substring, new_substring)
                            logger.info(f"Replaced substring in column: {col}")

            # Apply rare categories collapse
            for collapse_config in config.get('collapse_rare_categories', []):
                for col, threshold in collapse_config.items():
                    threshold = float(threshold)
                    if pd.api.types.is_categorical_dtype(dataset[col]) or pd.api.types.is_object_dtype(dataset[col]):
                        prep.collapse_rare_categories(col, threshold_percentage=threshold)
                        logger.info(f"Collapsed rare categories in column: {col} with threshold: {threshold}")

            # Apply datetime parsing
            for datetime_config in config.get('standard_datetime_format', []):
                for col, format in datetime_config.items():
                    prep.parse_datetime(col, datetime_format=format)
                    logger.info(f"Parsed datetime in column: {col} with format: {format}")

            # Apply regular expression operations
            for regex_operation in config.get('regular_expression_operations', []):
                col = regex_operation.get("columnName")
                pattern = regex_operation.get("pattern")
                replace_with = regex_operation.get("replaceWith", "")
                prep.apply_regex(col, regex_pattern=pattern, replacement_string=replace_with, operation="replace")
                logger.info(f"Applied regex operation on column: {col}")

            # Apply text tokenization
            for text_tokenisation in config.get('text_tokenisation', []):
                if pd.api.types.is_string_dtype(dataset[col]):
                    prep.tokenize_text(col)
                    logger.info(f"Tokenized text in column: {col}")

        # Save the transformed dataset
        prep.dataframe.to_csv(output_path, index=False)
        logger.info(f"Transformed dataset saved to {output_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

# Example usage
json_config = '''{
    "columns_kept": [
        "ID",
        "name",
        "category",
        "main_category",
        "currency",
        "deadline",
        "goal",
        "launched",
        "pledged",
        "state",
        "backers",
        "country",
        "usd pledged",
        "usd_pledged_real",
        "usd_goal_real"
    ],
    "trim_whitespace": [
        "name"
    ],
    "remove_special_characters": [],
    "normalize_data": [
        {
            "usd_goal_real": {
                "method": {
                    "types": "min-max"
                }
            }
        }
    ],
    "outlier_management": [
        {
            "usd_pledged_real": {
                "method": {
                    "types": "2 - SD"
                }
            }
        }
    ],
    "missing_value_imputation": [
        {
            "ID": {
                "method": "Remove"
            }
        }
    ],
    "remove_stopwords": [],
    "label_encoding": [
        "main_category"
    ],
    "numerical_column_binning": [
        {
            "usd pledged": [
                1,
                100,
                1000,
                10000,
                100000
            ]
        }
    ],
    "rename_column_name": [
        {
            "name": "FULLNAME"
        }
    ],
    "textcase_adjustment": [
        {
            "name": "Upper"
        }
    ],
    "replace_substring": [
        {
            "country": {
                "US": "IE"
            }
        }
    ],
    "column_type_conversion": [
        {
            "currency": "Text"
        }
    ],
    "text_tokenisation": [],
    "collapse_rare_caregories": [
        {
            "category": "20"
        }
    ],
    "standard_datetime_format": [
        {
            "deadline": "%Y-%m-%d"
        }
    ],
    "regular_expresion_operations": [
        {
            "columnName": "launched",
            "method": "Replace",
            "pattern": "5-[0-9]+",
            "replaceWith": "/"
        }
    ]
}'''
dataset_path = '/Users/seanmccrossan/Downloads/dirty_startup_dataset.csv'
output_path = '/Users/seanmccrossan/group_project/TUD-Group-Project/Project supporting Artifacts/test_data/data_clean_result.csv'

# At the end of your script, call the function with both dataset_path and output_path
apply_configured_transformations(json_config, dataset_path, output_path)



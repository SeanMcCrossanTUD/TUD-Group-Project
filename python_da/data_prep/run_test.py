import json
import pandas as pd
from data_prep.src.data_prep import DataPrep

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

    # Save the transformed dataset
    prep.dataframe.to_csv(output_path, index=False)

# Example usage
json_config = '''{
  "columns_kept": [
      "ID",
      "name",
      "category",
      "currency",
      "main_category",
      "goal",
      "launched",
      "pledged",
      "state",
      "country",
      "usd pledged",
      "usd_pledged_real"
  ],
  "trim_whitespace": [
      "ID",
      "currency",
      "name"
  ],
  "remove_special_characters": [
      "ID",
      "currency",
      "name"
  ],
  "normalize_data": [
      {
          "currency": {
              "method": {
                  "types": "min-max"
              }
          }
      },
      {
          "usd pledged": {
              "method": {
                  "types": "min-max"
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
  "remove_stopwords": [
      "ID",
      "country"
  ],
  "label_encoding": [
      "category"
  ],
  "numerical_column_binning": [
      {
          "usd_pledged_real": [
              1000,
              10000,
              100000,
              1,
              1000000
          ]
      }
  ],
  "rename_column_name": [
      {
          "currency": "PAYMENT_CURRENCY"
      },
      {
          "main_category": "NEW_CATEGORY"
      }
  ],
  "textcase_adjustment": [
      {
          "ID": "upper"
      },
      {
          "currency": "upper"
      }
  ],
  "replace_substring": [
      {
          "ID": {
              "10": "X"
          }
      }
  ]
}'''
dataset_path = '/Users/seanmccrossan/Downloads/dirty_startup_dataset.csv'
output_path = '/Users/seanmccrossan/group_project/TUD-Group-Project/Project supporting Artifacts/test_data/data_clean_result.csv'

# At the end of your script, call the function with both dataset_path and output_path
apply_configured_transformations(json_config, dataset_path, output_path)



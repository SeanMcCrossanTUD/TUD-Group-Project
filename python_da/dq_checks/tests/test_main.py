import json
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from dq_checks import run_main

def test_main():
    # Mock receive_message_from_queue to return a sample message
    sample_message = json.dumps({
        "filename": "sean_sample_file.csv",
        "jobID": "12345"
    })

    # Mock the Azure and other services
    with patch('dq_checks.run_main.receive_message_from_queue', return_value=sample_message) as mock_receive:
        with patch('dq_checks.run_main.download_blob_csv_data', return_value=pd.DataFrame()):
            with patch('dq_checks.run_main.perform_data_quality_checks', return_value={...}):
                with patch('dq_checks.run_main.upload_results_to_azure', return_value=None):
                    with patch('dq_checks.run_main.send_message_to_queue', return_value=None):
                        with patch('dq_checks.run_main.DataQualityChecker', MagicMock()):
                            with patch('dq_checks.run_main.run_visuals_and_upload', return_value=None):
                                run_main.main(test_iterations=1)

    mock_receive.assert_called()

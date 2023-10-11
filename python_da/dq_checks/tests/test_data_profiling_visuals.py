import pandas as pd
import pytest
from unittest import mock
import matplotlib.pyplot as plt
from dq_checks.src.data_quality_checker import DataQualityChecker
from dq_checks.src.data_profiling_visuals import DataProfilingVisuals


# Sample data for testing
data = {
    'A': [1, 2, 3, 4, 5, None, 7, 8, 9, 10],
    'B': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
}
df = pd.DataFrame(data)

# Mocked DataQualityChecker object
dqc = DataQualityChecker(df)
dqc.count_missing_values = mock.Mock(return_value={'A': 1})
dqc.count_unique_values_in_text_fields = mock.Mock(return_value={'B': 10})
dqc.z_score_outliers = mock.Mock(return_value={'A': [{'row': 0, 'field': 'A', 'value': 1, 'z_score': 3.0, 'is_outlier': True, 'threshold': 3.0}]})

# DataProfilingVisuals object
dpv = DataProfilingVisuals(dqc)

def test_plot_missing_values(mocker):
    mocker.patch.object(plt, 'show')
    mocker.patch.object(plt, 'savefig')
    dpv.plot_missing_values()
    assert plt.savefig.call_count == 1, "The plot should be saved as a PNG file"

def test_plot_unique_values_in_text_fields(mocker):
    mocker.patch.object(plt, 'show')
    mocker.patch.object(plt, 'savefig')
    dpv.plot_unique_values_in_text_fields()
    assert plt.savefig.call_count == 1, "The plot should be saved as a PNG file"

def test_plot_outlier_table(mocker):
    mocker.patch.object(plt, 'show')
    mocker.patch.object(plt, 'savefig')
    dpv.plot_outlier_table()
    assert plt.savefig.call_count == 1, "The plot should be saved as a PNG file"

def test_plot_outlier_scatter(mocker):
    mocker.patch.object(plt, 'show')
    mocker.patch.object(plt, 'savefig')
    dpv.plot_outlier_scatter()
    assert plt.savefig.call_count == 1, "The plot should be saved as a PNG file"

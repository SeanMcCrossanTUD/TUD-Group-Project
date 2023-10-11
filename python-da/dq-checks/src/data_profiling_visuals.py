import matplotlib.pyplot as plt
import seaborn as sns
from data_quality_checker import DataQualityChecker 

class DataProfilingVisuals:
    def __init__(self, data_quality_checker: DataQualityChecker):
        self.dqc = data_quality_checker

    def plot_missing_values(self):
        missing_values = self.dqc.count_missing_values()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(missing_values.keys()), y=list(missing_values.values()))
        plt.title('Missing Values per Column')
        plt.xlabel('Columns')
        plt.ylabel('Number of Missing Values')
        plt.xticks(rotation=45)
        plt.show()

    def plot_unique_values_in_text_fields(self):
        unique_values = self.dqc.count_unique_values_in_text_fields()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(unique_values.keys()), y=list(unique_values.values()))
        plt.title('Unique Values in Text Fields')
        plt.xlabel('Text Fields')
        plt.ylabel('Number of Unique Values')
        plt.xticks(rotation=45)
        plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .data_quality_checker import DataQualityChecker


class DataProfilingVisuals:
    def __init__(self, data_quality_checker: DataQualityChecker):
        self.dqc = data_quality_checker

    def plot_missing_values(self, output_file: str = "missing_values_plot.png"):
        missing_values = self.dqc.count_missing_values()
        
        if not missing_values:  # Check if the dictionary is empty
            print("No missing values found.")
            return
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(missing_values.keys()), y=list(missing_values.values()), palette="viridis")
        plt.title('Missing Values per Column', fontsize=16)
        plt.xlabel('Columns', fontsize=14)
        plt.ylabel('Number of Missing Values', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig(output_file)  # Save the plot as a PNG file
        plt.show()

    def plot_unique_values_in_text_fields(self, output_file: str = "unique_values_plot.png"):
        unique_values = self.dqc.count_unique_values_in_text_fields()
        
        if not unique_values:  # Check if the dictionary is empty
            print("No text fields found.")
            return
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(unique_values.keys()), y=list(unique_values.values()), palette="mako")
        plt.title('Unique Values in Text Fields', fontsize=16)
        plt.xlabel('Text Fields', fontsize=14)
        plt.ylabel('Number of Unique Values', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig(output_file)  # Save the plot as a PNG file
        plt.show()

    def plot_outlier_table(self, threshold: float = 3.0, output_file: str = "outlier_table.png"):
        outliers = self.dqc.z_score_outliers(threshold)
        if not outliers:
            print("No outliers found.")
            return
        
        # Convert the outlier information into a DataFrame for visualization
        outlier_data = []
        for col, outlier_info in outliers.items():
            for info in outlier_info:
                outlier_data.append(info)
        
        outlier_df = pd.DataFrame(outlier_data)
        outlier_df = outlier_df.sort_values(by=['z_score'], ascending=False).head(20)  # Select top 20 extreme outliers
        
        # Plot table
        fig, ax = plt.subplots(figsize=(12, 4))  # Adjust size as needed
        ax.axis('off')
        ax.table(cellText=outlier_df.values,
                 colLabels=outlier_df.columns,
                 cellLoc='center', loc='center', colWidths=[0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
        plt.title('Table of Top 20 Extreme Outliers')
        plt.savefig(output_file)  # Save the plot as a PNG file
        plt.show()
        print(f"Plot saved as {output_file}")

    def plot_outlier_scatter(self, threshold: float = 3.0, output_file: str = "outlier_scatter.png"):
        outliers = self.dqc.z_score_outliers(threshold)
        if not outliers:
            print("No outliers found.")
            return
        
        num_plots = len(outliers)
        fig, axs = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots))  # Adjust size as needed
        
        for idx, (col, outlier_info) in enumerate(outliers.items()):
            # Extract rows and values of outliers
            outlier_rows = [info['row'] for info in outlier_info]
            outlier_values = [info['value'] for info in outlier_info]
            
            # Plot scatter with outliers highlighted
            if num_plots > 1:
                ax = axs[idx]
            else:
                ax = axs  # If there's only one subplot, axs is not an array
            ax.scatter(x=self.dqc.dataset.index, y=self.dqc.dataset[col])
            ax.scatter(x=outlier_rows, y=outlier_values, color='red')
            ax.set_title(f'Outliers in {col} (highlighted in red)')
            ax.set_xlabel('Row Index')
            ax.set_ylabel(col)
        
        plt.tight_layout()
        plt.savefig(output_file)  # Save the plot as a PNG file
        plt.show()
        print(f"Plot saved as {output_file}")

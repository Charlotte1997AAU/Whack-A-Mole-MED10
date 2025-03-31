import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import shapiro, kstest


def check_normality(df, channels, large_dataset=False):
    for ch in channels:
        print(f'Checking normality for {ch}...')

        # Histogram & Q-Q Plot
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        sns.histplot(df[ch], kde=True)
        plt.title(f'Histogram - {ch}')

        plt.subplot(1, 2, 2)
        stats.probplot(df[ch], dist="norm", plot=plt)
        plt.title(f'Q-Q Plot - {ch}')

        plt.show()

        # Statistical Tests
        if large_dataset:
            stat, p = kstest(df[ch], 'norm')
            test_name = "Kolmogorov-Smirnov"
        else:
            stat, p = shapiro(df[ch])
            test_name = "Shapiro-Wilk"

        print(f'{test_name} test for {ch}: p-value = {p:.5f}')
        if p < 0.05:
            print(f'--> {ch} is NOT normally distributed\n')
        else:
            print(f'--> {ch} is normally distributed\n')


# Example usage
filepath = f"Data_CleanUp_C/merged_file_pinch_C_cleaned.csv"
df = pd.read_csv(filepath, delimiter=';', skipinitialspace=True)  # Load your dataset with ';' delimiter
channels = [f'EMG{i}' for i in range(1, 9)]  # Adjust column names to match your dataset
check_normality(df, channels, large_dataset=len(df) > 5000)
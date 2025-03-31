import pandas as pd
import scipy.stats as stats

# Example: Load your dataset
filepath = f"Data_CleanUp_C/merged_file_pinch_C_cleaned.csv"
df = pd.read_csv(filepath, delimiter=';', skipinitialspace=True)
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names

# Remove rows where 'ActiveCube' is NaN or empty
df = df[df['ActivatedCube'].notna()]  # Keeps only rows where ActiveCube is not NaN
df = df[df['ActivatedCube'] != '']   # Removes rows where ActiveCube is an empty string

#verify there are no missing values.
missing_values = df['ActivatedCube'].isna().sum()
print(f'Number of missing (NaN) values in ActiveCube: {missing_values}')



# List of EMG channels to test
channels = [f'EMG{i + 1}' for i in range(8)]

# Perform Kruskal-Wallis test for each EMG channel
for ch in channels:
    print(f"Kruskal-Wallis test for {ch}:")

    # Group the data by 'ActiveCube' (representing different cubes)
    grouped = [df[df['ActivatedCube'] == cube][ch] for cube in df['ActivatedCube'].unique()]

    # Perform Kruskal-Wallis test
    h_stat, p_value = stats.kruskal(*grouped)

    # Output the results
    print(f"H-statistic: {h_stat:.4f}, p-value: {p_value:.4f}")

    # Check if the result is statistically significant
    if p_value < 0.05:
        print(f"--> Significant difference found in {ch} based on active cube\n")
    else:
        print(f"--> No significant difference found in {ch} based on active cube\n")

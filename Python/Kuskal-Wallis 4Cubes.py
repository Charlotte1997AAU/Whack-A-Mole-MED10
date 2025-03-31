import pandas as pd
import scipy.stats as stats

# Load your dataset
filepath = f"Data_CleanUp_C/merged_file_pinch_C_cleaned.csv"
df = pd.read_csv(filepath, delimiter=';', skipinitialspace=True)
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names

# Filter out rows where 'ActiveCube' is missing or empty
df = df[df['ActivatedCube'].notna()]  # Keeps only rows where ActiveCube is not NaN
df = df[df['ActivatedCube'] != '']  # Removes rows where ActiveCube is an empty string

# Define the EMG channels to check
channels = [f'EMG{i + 1}' for i in range(8)]  # Adjust according to your columns

# Define cubes to compare
cubes_to_compare = ['Cube 0', 'Cube 4', 'Cube 19', 'Cube 24']


# Loop through each EMG channel and perform the Kruskal-Wallis test
for ch in channels:
    print(f"\nKruskal-Wallis test for {ch}:")

    # Extract the EMG data for the selected cubes
    cube_data = [df[df['ActivatedCube'] == cube][ch] for cube in cubes_to_compare]

    # Perform Kruskal-Wallis test
    if all(len(cube) > 0 for cube in cube_data):  # Check that all groups have data
        h_stat, p_value = stats.kruskal(*cube_data)
        print(f"H-statistic = {h_stat:.4f}, p-value = {p_value:.4f}")

        if p_value < 0.05:
            print(f"--> Significant difference found between the selected cubes based on {ch}\n")
        else:
            print(f"--> No significant difference found between the selected cubes based on {ch}\n")
    else:
        print("--> Not enough data for one or more of the selected cubes.\n")

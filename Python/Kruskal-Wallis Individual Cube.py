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

# Loop through each EMG channel and perform the Kruskal-Wallis test
for ch in channels:
    print(f"\nKruskal-Wallis test for {ch}:")

    # Loop through all cubes (Cube 1 to Cube 25)
    for i in range(1, 26):
        # Get the data for the current cube (e.g., Cube 1, Cube 2, ..., Cube 25)
        cube_data = df[df['ActivatedCube'] == f'Cube {i}'][ch]

        # Perform Kruskal-Wallis test between current cube and the next one
        if i < 25:
            next_cube_data = df[df['ActivatedCube'] == f'Cube {i + 1}'][ch]

            if len(cube_data) > 0 and len(next_cube_data) > 0:  # Check if both groups have data
                h_stat, p_value = stats.kruskal(cube_data, next_cube_data)
                print(f"    Comparing Cube {i} vs Cube {i + 1} on {ch}:")
                print(f"    H-statistic = {h_stat:.4f}, p-value = {p_value:.4f}")

                if p_value < 0.05:
                    print(f"    --> Significant difference found between Cube {i} and Cube {i + 1} on {ch}\n")
                else:
                    print(f"    --> No significant difference found between Cube {i} and Cube {i + 1} on {ch}\n")
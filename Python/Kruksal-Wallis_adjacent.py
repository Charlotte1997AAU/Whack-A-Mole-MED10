import pandas as pd
import scipy.stats as stats

# Load your dataset
filepath = f"Data_CleanUp_C/merged_file_fist_C_cleaned.csv"
df = pd.read_csv(filepath, delimiter=';', skipinitialspace=True)
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces from column names

# Filter out rows where 'ActivatedCube' is missing or empty
df = df[df['ActivatedCube'].notna()]  # Keeps only rows where ActivatedCube is not NaN
df = df[df['ActivatedCube'] != '']  # Removes rows where ActivatedCube is an empty string

# Define the EMG channel to analyze
channel = 'EMG8'

print(f"\nKruskal-Wallis test for {channel}:")

# Define the 5x5 grid based on your numbering system
grid = [
    [4,  9,  14, 19, 24],
    [3,  8,  13, 18, 23],
    [2,  7,  12, 17, 22],
    [1,  6,  11, 16, 21],
    [0,  5,  10, 15, 20]
]

# Function to find neighbors of a given cube
def get_neighbors(cube):
    neighbors = []
    for row in range(5):
        for col in range(5):
            if grid[row][col] == cube:
                # Check all 8 possible neighbors (left, right, up, down, diagonals)
                for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 5 and 0 <= nc < 5:
                        neighbors.append(grid[nr][nc])
                return neighbors
    return []

# Perform Kruskal-Wallis test between each cube and its adjacent neighbors
for cube in range(25):
    cube_label = f'Cube {cube}'
    cube_data = df[df['ActivatedCube'] == cube_label][channel]

    if len(cube_data) == 0:
        continue  # Skip if no data for this cube

    for neighbor in get_neighbors(cube):
        neighbor_label = f'Cube {neighbor}'
        neighbor_data = df[df['ActivatedCube'] == neighbor_label][channel]

        if len(neighbor_data) > 0:
            h_stat, p_value = stats.kruskal(cube_data, neighbor_data)
            print(f"    Comparing {cube_label} vs {neighbor_label} on {channel}:")
            print(f"    H-statistic = {h_stat:.4f}, p-value = {p_value:.4f}")

            if p_value < 0.05:
                print(f"    --> Significant difference found between {cube_label} and {neighbor_label}\n")
            else:
                print(f"    --> No difference found between {cube_label} and {neighbor_label}\n")

import pandas as pd
import os

output_folder = "Data_CleanUp_C"
gesture_files = [
    "merged_file.csv",
    #"Pre-Pilot test C/Unity_fist_C.csv",
    #"Pre-Pilot test C/Unity_Flexion_C.csv",
    #"Pre-Pilot test C/Unity_Pinch_C.csv",
    #"Pre-Pilot test C/Unity_Supination_C.csv",
    #"Pre-Pilot test C/Unity_Pronation_C.csv"
]

# Iterate over the files, load them, strip spaces, and save with a new name
for file in gesture_files:
    # Load the data with the correct delimiter ';'
    df = pd.read_csv(file, delimiter=";", skipinitialspace=True)

    # Step 1: Find the index of the first row where 'State' is 'MVC'
    mvc_index = df[df['State'] == 'MVC'].index[0]

    # Keep all rows from the first 'MVC' row onward
    df = df.iloc[mvc_index:].reset_index(drop=True)

    # Add an 'Index' column starting from 0
    df['Index'] = range(len(df))

    # Move the 'Index' column to the first column position
    df = df[['Index'] + [col for col in df.columns if col != 'Index']]

    # Step 2: Remove rows after the first occurrence where 'GesturesAtempted' == 25 and 'Event' == 'Successful Gesture'
    success_row_index = df[(df['GesturesAtempted'] == 25) & (df['Event'] == 'Successful Gesture')].index

    if not success_row_index.empty:
        # Find the first row index where the condition is met and remove that row and all rows after it
        df = df.iloc[:success_row_index[0]]

    # Strip spaces from all string columns, except for 'ID' column
    df = df.apply(lambda col: col.str.strip() if col.dtype == 'object' and col.name != 'ID' else col)

    # Save the cleaned DataFrame with a new name in the Data_CleanUp_L folder
    output_filename = file.split('/')[-1].replace('.csv', '_cleaned.csv')
    output_path = os.path.join(output_folder, output_filename)

    # Save using the correct delimiter, don't drop the ID column
    df.to_csv(output_path, index=False, sep=';')  # index=False to avoid extra index column

    print(f"Processed and saved: {output_path}")
    print(df.head())  # Print the first few rows to check the result

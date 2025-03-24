import os
import csv


def remove_last_semicolon_from_files(folder_path, substring):
    """Reads CSV files from a folder, removes the last semicolon from each row, and overwrites the existing files."""
    # Get a list of all files in the folder
    for filename in os.listdir(folder_path):
        # Only process files that contain the specific substring in their name and are CSV files
        if substring in filename and filename.endswith('.csv'):
            input_file_path = os.path.join(folder_path, filename)

            print(f"Processing file: {input_file_path}")

            # Open the input file (and overwrite it)
            with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
                # Read the CSV content
                reader = csv.reader(infile, delimiter=';')
                rows = list(reader)  # Read all rows into a list

            # Modify the rows (remove last semicolon)
            with open(input_file_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=';')

                # Write the header (first row) back to the file
                writer.writerow(rows[0])

                # Iterate over the remaining rows and remove the last semicolon
                for row in rows[1:]:
                    if row[-1] == '':  # Check if the last element is empty (meaning there's a trailing semicolon)
                        row = row[:-1]  # Remove the last element (empty string)
                    writer.writerow(row)

            print(f"File overwritten: {input_file_path}")

    print("Processing complete!")


# Example usage
folder_path = "Pre-Pilot test L"  # Specify the folder containing the files
substring = "Uniy"  # Specify the string to match in the filenames
remove_last_semicolon_from_files(folder_path, substring)

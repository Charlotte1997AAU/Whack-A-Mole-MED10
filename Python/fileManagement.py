import os
import pandas as pd
import glob
import shutil
from pathlib import Path

letter = "C"


def get_id_from_csv(file_path, id_label):
    """Extracts the ID string from a CSV file using pandas."""
    df = pd.read_csv(file_path, sep=';', header=0)

    return df[id_label].iloc[0]


def processAllFiles(folder):
    testData = os.listdir(folder)
    mergedFiles = []

    unityFiles = [f for f in testData if 'Unity' in f]
    EMGFiles = [f for f in testData if 'EMG' in f]

    for uFile in unityFiles:
        for eFile in EMGFiles:
            unityPath = os.path.join(folder, uFile)
            EMGPath = os.path.join(folder, eFile)
            merged = compareIDs(unityPath, EMGPath)
            if merged is not None:
                mergedFiles.append(merged)

    return mergedFiles


def compareIDs(unityFile, EMGFile):
    unityID = get_id_from_csv(unityFile, 'ID')
    EMGID = get_id_from_csv(EMGFile, 'SessionID')

    if unityID == EMGID:
        print(f"Found ID match for {unityFile} and {EMGFile}, merging...")
        unityDf = pd.read_csv(unityFile, sep=';', header=0, skipinitialspace=True)
        emgDf = pd.read_csv(EMGFile, sep=';', header=0, skipinitialspace=True)

        unityDf['Timestamp'] = pd.to_datetime(unityDf['Timestamp'])
        emgDf['Timestamp'] = pd.to_datetime(emgDf['Timestamp'])

        gesture = unityDf['GoalGesture'].iloc[0]
        print(f"Successfully merged file for gesture: {gesture}")

        mergedDfs = pd.merge_asof(emgDf.sort_values('Timestamp'), unityDf.sort_values('Timestamp'), on='Timestamp',
                                  direction='nearest')
        mergedDfs = mergedDfs.drop(columns=['SessionID'])
        return mergedDfs


def createTrainingSet(folder):
    csv_files = glob.glob(f"{folder}/*.csv")

    # Read and concatenate all CSV files
    df_list = [pd.read_csv(file, sep=";") for file in csv_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    columns_to_keep = ["EMG1", "EMG2", "EMG3", "EMG4", "EMG5", "EMG6", "EMG7", "EMG8", "GoalGesture",
                       "ActiveCubeX", "ActiveCubeY", "ActiveCubeZ", "TrackerX", "TrackerY", "TrackerZ",
                       "State", "Event"]

    # Keep only the specified columns and drop others
    df_filtered = combined_df[columns_to_keep]

    # Save the merged data to a new CSV file
    df_filtered.to_csv(f"testDataWithPositions_{letter}.csv", index=False)
    print(f"Created test data set from folder {folder} ")


def cleanTrainingSet(fileToClean):
    data = pd.read_csv(fileToClean)
    data = data[data["State"].str.contains("In box", na=False)]
    data.drop(["State", "Event"], axis=1, inplace=True)
    data.to_csv(f"InBox_testDataWithPositions_{letter}.csv", index=False)

    print("Removed all data not in box")


file_path = f"Data_CleanUp_{letter}"

#createTrainingSet(file_path)
#cleanTrainingSet(f"testDataWithPositions_{letter}.csv")


def createParticipantFolder(base_path):
    # Ensure the base path exists
    os.makedirs(base_path, exist_ok=True)

    # List all folders in the base path that start with "Participant "
    existing_folders = [f for f in os.listdir(base_path)
                        if os.path.isdir(os.path.join(base_path, f)) and f.startswith("Participant ")]

    # Extract the participant numbers and find the next one
    numbers = []
    for folder in existing_folders:
        try:
            num = int(folder.replace("Participant ", ""))
            numbers.append(num)
        except ValueError:
            continue  # Skip folders with unexpected names

    next_number = max(numbers, default=0) + 1
    new_folder_name = f"Participant {next_number}"
    new_folder_path = os.path.join(base_path, new_folder_name)

    # Create the new folder
    os.makedirs(new_folder_path)
    print(f"Created folder for participant {next_number}")
    return new_folder_path, next_number


def moveUnityData(filename_contains=None, file_extension=None, expected_file_count=8):
    # Get the root directory (Whack-A-Mole-MED10)
    script_path = Path(__file__).resolve()
    project_root = script_path.parents[1]  # 'Python' is one level deep inside root

    # Define relative paths
    source_dir = project_root / "Assets" / "Med10" / "Training Logs"
    destination_dir = script_path.parent / "tempTestData"  # Or pass this as a param

    destination_dir.mkdir(exist_ok=True)

    # Move files
    moved_files = []
    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            if filename_contains and filename_contains not in file_path.name:
                continue
            if file_extension and not file_path.name.endswith(file_extension):
                continue

            target = destination_dir / file_path.name
            shutil.move(str(file_path), str(target))
            moved_files.append(target)

    if len(moved_files) != expected_file_count:
        print(f"ERROR: Expected {expected_file_count} files, but moved {len(moved_files)}.")
    else:
        print(f"Successfully moved {expected_file_count} files.")

# Example usage:
unityData = "Pre-Pilot test C/Unity_supination_C.csv"
EMGdata = "Pre-Pilot test C/EMG_supination_C.csv"

dataframesEMG = [
    "Final Pre Test/EMG_ExtensIon_L.csv",
    "Final Pre Test/EMG_Fist_L.csv",
    "Final Pre Test/EMG_Flexion_L.csv",
    "Final Pre Test/EMG_Pinch_L.csv"
]

dataframesUnity = [
    "Final Pre Test/Unity_Extension_L.csv",
    "Final Pre Test/Unity_Fist_L.csv",
    "Final Pre Test/Unity_Flexion_L.csv",
    "Final Pre Test/Unity_Pinch_L.csv"
]


#compareIDs("Data_CleanUp_C/tempTestData/Unity_log_2025_04_23_13_56_17_Med10.csv", "Data_CleanUp_C/tempTestData/EMG_log_2025_04_23_13_56_17_Med10.csv")



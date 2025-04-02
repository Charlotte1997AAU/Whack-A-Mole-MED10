import pandas as pd
import glob

letter = "C"

def get_id_from_csv(file_path, id_label):
    """Extracts the ID string from a CSV file using pandas."""
    df = pd.read_csv(file_path, sep=';', header=0)

    return df[id_label].iloc[0]


def compareIDs(unityFile, EMGFile):
    unityID = get_id_from_csv(unityFile, 'ID')
    EMGID = get_id_from_csv(EMGFile, 'SessionID')

    if unityID == EMGID:
        print(f"Found ID match for {unityFile} and {EMGFile}, merging...")
        mergeEMGandUnityData(unityFile, EMGFile)
        print("Merging complete!")
    else:
        print("No match in ID's!")


def mergeEMGandUnityData(unityFile, emgFile):
    unityDf = pd.read_csv(unityFile, sep=';', header=0, skipinitialspace=True)
    emgDf = pd.read_csv(emgFile, sep=';', header=0, skipinitialspace=True)

    unityDf['Timestamp'] = pd.to_datetime(unityDf['Timestamp'])
    emgDf['Timestamp'] = pd.to_datetime(emgDf['Timestamp'])


    gesture = unityDf['GoalGesture'].iloc[0]
    print(f"current gesture: {gesture}")

    mergedDfs = pd.merge_asof(emgDf.sort_values('Timestamp'), unityDf.sort_values('Timestamp'), on='Timestamp', direction='nearest')
    mergedDfs = mergedDfs.drop(columns=['SessionID'])
    mergedDfs.to_csv(f'Data_CleanUp_C/merged_file_{gesture}_L.csv', index=False, sep=";")


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

createTrainingSet(file_path)
cleanTrainingSet(f"testDataWithPositions_{letter}.csv")


# Example usage:
unityData = "Pre-Pilot test C/Unity_supination_C.csv"
EMGdata = "Pre-Pilot test C/EMG_supination_C.csv"

#compareIDs(unityData, EMGdata)



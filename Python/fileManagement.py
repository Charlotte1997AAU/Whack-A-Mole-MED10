import pandas as pd


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

    mergedDfs = pd.merge_asof(emgDf, unityDf, on='Timestamp', direction='nearest')
    mergedDfs = mergedDfs.drop(columns=['SessionID'])
    mergedDfs.to_csv('merged_file.csv', index=False)

# Example usage:
unityData = "Pre-Pilot test C/Unity_extension_C.csv"
EMGdata = "Pre-Pilot test C/EMG_extension_C.csv"

compareIDs(unityData, EMGdata)



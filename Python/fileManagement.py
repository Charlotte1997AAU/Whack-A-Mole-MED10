import pandas as pd


def get_id_from_csv(file_path, id_label):
    """Extracts the ID string from a specific row label in a CSV file using pandas."""
    df = pd.read_csv(file_path, sep=';', header=0)

    return df[id_label].iloc[0]


def compareIDs(unityFile, EMGFile):
    unityID = get_id_from_csv(unityFile, 'ID')
    EMGID = get_id_from_csv(EMGFile, 'SessionID')

    if unityID == EMGID:
        print("ID's matching!")
    else:
        print("No match in ID's!")

# Example usage:
unityFile = "Pre-Pilot test C/Unity_extension_C.csv"
EMGFile = "Pre-Pilot test C/EMG_extension_C.csv"

compareIDs(unityFile, EMGFile)



import pandas as pd

def emgInsight(filePath):
    data = pd.read_csv(filePath, delimiter=";", header=0, skipinitialspace=True)
    emgData = data.filter(items=['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])

    stats = emgData.agg(['mean', 'median', 'min', 'max']).round(2)
    #stats.to_csv(f'{filePath}_stats.csv', index=False)
    # Print results
    print(f"stats for file {filePath}:\n {stats}\n")

emgTest = [
    "Pre-Pilot test C/EMG_extension_C.csv",
    "Pre-Pilot test C/EMG_fist_C.csv",
    "Pre-Pilot test C/EMG_flexion_C.csv",
    "Pre-Pilot test C/EMG_pinch_C.csv",
    "Pre-Pilot test C/EMG_pronation_C.csv",
    "Pre-Pilot test C/EMG_supination_C.csv",
    "Pre-Pilot test L/EMG_extension_L.csv",
    "Pre-Pilot test L/EMG_fist_L.csv",
    "Pre-Pilot test L/EMG_flexion_L.csv",
    "Pre-Pilot test L/EMG_pinch_L.csv",
    "Pre-Pilot test L/EMG_pronation_L.csv",
    "Pre-Pilot test L/EMG_supination_L.csv"

]

tempfiles = [
    "tempFiles/extension.csv",
    "tempFiles/fist.csv",
    "tempFiles/flexion.csv",
    "tempFiles/pinch.csv",
    "tempFiles/rest.csv"
]

emgInsight("TestData/Participant 1/EMG_log_2025_05_06_10_15_56_Med10.csv")

def readPredictions():
    gesturePredict = []
    df = pd.read_csv("prediction_results.csv")
    print(df['prediction'].value_counts())
    for gesture in range(4):
        guessedGesture = df[df['prediction'] == gesture]
        gesturePredict.append(guessedGesture)

    for gestures in gesturePredict:
        conf = gestures.filter(items=['confidence'])
        stats = conf.agg(['mean', 'median', 'min', 'max']).round(2)
        gestureNum = gestures['prediction'].iloc[0]
        print(f"stats for gesture {gestureNum}: \n{stats}\n")

#readPredictions()

def check_emg_columns_for_nan_or_empty(df):
    """
    Print EMG columns that contain NaN or empty string values.
    """
    emg_columns = [col for col in df.columns if 'EMG' in col]
    # Create a mask for rows with NaN or empty string in any EMG column
    mask = df[emg_columns].isna().any(axis=1) | (df[emg_columns] == '').any(axis=1)
    cleaned_df = df[~mask].copy()
    return cleaned_df

#df = pd.read_csv("tempTestData/EMG_log_2025_05_06_14_21_03_Med10.csv", sep=";")
#df.to_csv("tempTestData/EMG_log_2025_05_06_14_21_03_Med10Clean.csv", index=False, sep=";")
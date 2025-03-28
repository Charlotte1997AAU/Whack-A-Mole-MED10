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
for files in emgTest:
    emgInsight(files)

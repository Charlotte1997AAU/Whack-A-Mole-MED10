import pandas as pd

def emgInsight(filePath):
    data = pd.read_csv(filePath, delimiter=";", header=0, skipinitialspace=True)
    emgData = data.filter(items=['EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])

    stats = emgData.agg(['mean', 'median', 'min', 'max']).round(2)
    stats.to_csv('stats.csv', index=False)
    # Print results
    print(stats)

emgInsight('Data_CleanUp_C/merged_file_pinch_C_cleaned.csv')

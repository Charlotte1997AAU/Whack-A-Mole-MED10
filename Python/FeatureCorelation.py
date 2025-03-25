import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import re


def featureCorrelation(filePath: str, saveImage: bool):
    """Run pandas Feature correlation on given dataframe.

    Args:
        filePath: reference to the file location
        saveImage: Set to True to save the image to a .png file

    """
    data = pd.read_csv(filePath, sep=';', header=0, skipinitialspace=True)
    data.drop(columns=['Index', 'Timestamp', 'ID', 'FrameNumber', 'ActivatedCube',
                       'ActiveCubeZ', 'GoalGesture', 'GesturesAtempted', 'AttemptsInCube',
                       'State', 'Event'], inplace=True)

    match = re.search(r"merged_file_(.*?)_cleaned\.csv", filePath)
    gestureName = match.group(1)  # Extract the dynamic part
    print(gestureName)
    print(data.head())
    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, mask=mask)
    plt.title(f"Feature Correlation for {gestureName}")
    if saveImage:
        plt.savefig(f"Images/Feature_Correlation_{gestureName}.png", dpi=300, bbox_inches="tight")
    plt.show()


gesture_files_L = [
    "Data_CleanUp_L/merged_file_extension_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_fist_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_flexion_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pinch_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pronation_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_supination_L_cleaned.csv"
]

gesture_files_C = [
    "Data_CleanUp_C/merged_file_extension_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_fist_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_flexion_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pinch_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pronation_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_supination_C_cleaned.csv"
]

for file in gesture_files_C:
    featureCorrelation(file, True)

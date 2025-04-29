import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import itertools

bogstav = "L"


def featureCorrelation(filePath: str, saveImage: bool):
    """Run pandas Feature correlation on given dataframe.

    Args:
        filePath: reference to the file location
        saveImage: Set to True to save the image to a .png file

    """
    data = pd.read_csv(filePath, sep=',', header=0, skipinitialspace=True)
    data = data.drop(columns=["EMG1Slope", "EMG2Slope", "EMG3Slope", "EMG4Slope", "EMG5Slope", "EMG6Slope",
                  "EMG7Slope", "EMG8Slope", "activeCube", "activeCubeX", "activeCubeY"])

    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=False, fmt=".2f", cmap='coolwarm', linewidths=0.5, mask=mask)
    plt.title(f"Feature Correlation for all gestures")
    if saveImage:
        plt.savefig(f"Images/Feature_Correlation_testData_{bogstav}.png", dpi=300, bbox_inches="tight")
    plt.show()


#featureCorrelation(f"test Data set/testData_{bogstav}.csv", False)


def GestureCorrelation(data, savefig: bool):
    df = pd.read_csv(data)
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "trackerX", "trackerY", "trackerZ", "GoalGesture"]

    # Split the DataFrame into groups by 'GoalGesture'
    grouped_dfs = {gesture: df[df['GoalGesture'] == gesture].drop(columns=excludeColumns)
                   for gesture in df['GoalGesture'].unique()}

    # Generate all unique pairs of gestures
    gesture_pairs = list(itertools.combinations(grouped_dfs.keys(), 2))

    # Loop through each pair and calculate cross-correlation
    for g1, g2 in gesture_pairs:
        df1 = grouped_dfs[g1].reset_index(drop=True)
        df2 = grouped_dfs[g2].reset_index(drop=True)

        # Ensure equal lengths
        min_len = min(len(df1), len(df2))
        df1 = df1.iloc[:min_len]
        df2 = df2.iloc[:min_len]

        # Full cross-correlation matrix
        corr_matrix = pd.DataFrame(
            {
                col1: [df1[col1].corr(df2[col2]) for col2 in df2.columns]
                for col1 in df1.columns
            },
            index=df2.columns
        )

        gestureNames = {
            1: 'Extension',
            2: 'Fist',
            3: 'Flexion',
            4: 'Pinch',
            0: 'Rest'
        }

        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix.astype(float), annot=False, fmt=".2f", cmap="coolwarm", vmin=-1,
                    vmax=1, xticklabels=corr_matrix.columns, yticklabels=corr_matrix.index)
        plt.title(f'Correlation Heatmap: {gestureNames[g1]} vs {gestureNames[g2]}')
        plt.tight_layout()
        if savefig:
            plt.savefig(f"Images/CorrelationHeatmap{gestureNames[g1]}{gestureNames[g2]}.png", dpi=300, bbox_inches="tight")
        plt.show()


GestureCorrelation("test Data set\TrainingSetWdeltas_L.csv", True)

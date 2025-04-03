import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import re

bogstav = "C"


def featureCorrelation(filePath: str, saveImage: bool):
    """Run pandas Feature correlation on given dataframe.

    Args:
        filePath: reference to the file location
        saveImage: Set to True to save the image to a .png file

    """
    data = pd.read_csv(filePath, sep=',', header=0, skipinitialspace=True)

    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=False, fmt=".2f", cmap='coolwarm', linewidths=0.5, mask=mask)
    plt.title(f"Feature Correlation for all gestures")
    if saveImage:
        plt.savefig(f"Images/Feature_Correlation_testData_{bogstav}.png", dpi=300, bbox_inches="tight")
    plt.show()


featureCorrelation(f"test Data set/testData_{bogstav}.csv", True)

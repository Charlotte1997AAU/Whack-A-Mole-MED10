import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import featureSelection
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split


def plot_emg_with_states(gesture_name, states_to_include, emg_signals_to_include=None, color_shading=True,
                         show_lines=True):
    """
    Plots selected EMG signals over time with optional color-coded state regions and vertical lines.
    The CSV file is dynamically loaded based on the gesture name.

    Parameters:
    gesture_name (str): The name of the gesture to focus on (e.g., "pinch").
    states_to_include (list): List of states to include in visualization.
    emg_signals_to_include (list): List of EMG signals to plot (e.g., [1, 3, 5] to plot EMG1, EMG3, and EMG5).
    color_shading (bool): If True, colors background regions for selected states.
    show_lines (bool): If True, shows vertical dashed lines at state change points.
    """

    # Load the appropriate CSV file based on the gesture_name
    file_path = f"fistData.csv" #Change to Data_CleanUp_L and to "L" after the gesture name
    df = pd.read_csv(file_path, delimiter=",")

    # Convert Timestamp column to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Identify state change points
    state_changes = df[(df["State"] != df["State"].shift()) & (df["State"].isin(states_to_include))]

    # Plot EMG signals
    plt.figure(figsize=(12, 6))

    # If emg_signals_to_include is None, include all EMG signals (EMG1 to EMG8)
    emg_signals_to_include = emg_signals_to_include or list(range(1, 9))  # Default to all 8 signals if not specified

    # Plot only the selected EMG signals
    for i in emg_signals_to_include:  # Loop through the selected EMG signals
        plt.plot(df["Timestamp"], df[f"EMG{i}"], label=f"EMG{i}")

    # Find min and max EMG values for better text positioning
    min_emg_value = df.iloc[:, 1:9].min().min()
    max_emg_value = df.iloc[:, 1:9].max().max()

    # Define colors for different states
    state_colors = {
        "MVC": "red",
        "In box": "blue",
        "Moving to Box": "green",
        "Resting": "lightyellow",
        "Moving to rest position": "gold",
    }

    # Add color-shaded regions
    if color_shading:
        prev_state = None
        start_time = None
        for _, row in df.iterrows():
            current_state = row["State"]
            if current_state in states_to_include:
                if prev_state != current_state:
                    if start_time is not None:
                        plt.axvspan(start_time, row["Timestamp"], color=state_colors.get(prev_state, "gray"), alpha=0.3)
                    start_time = row["Timestamp"]
                prev_state = current_state
        if start_time is not None:
            plt.axvspan(start_time, df["Timestamp"].iloc[-1], color=state_colors.get(prev_state, "gray"), alpha=0.3)

    # Add vertical dashed lines at state change points
    if show_lines:
        for _, row in state_changes.iterrows():
            plt.axvline(x=row["Timestamp"], color="black", linestyle="--", alpha=0.6)
            plt.text(row["Timestamp"], min_emg_value - 10, row["State"],
                     rotation=90, verticalalignment='bottom', fontsize=10, color="black", fontweight='bold')

    # Formatting the plot
    plt.xlabel("Time", fontsize=14, fontweight='bold')  # Bold label for x-axis
    plt.ylabel("EMG Signal", fontweight='bold')  # Bold label for y-axis
    plt.title(f"EMG Signals Over Time with State Annotations ({gesture_name.capitalize()} Gesture)", fontsize=16,
              fontweight='bold')  # Dynamic title based on gesture
    plt.legend()
    plt.grid(True)

    # Remove the timestamp from the x-axis by hiding the xticks
    plt.xticks([])  # This removes the x-axis tick labels

    # Make y-axis ticks bold and larger
    plt.tick_params(axis='y', labelsize=12, labelcolor='black', width=2)  # Change size and boldness
    plt.yticks(fontweight='bold', fontsize=14)  # Bold and larger font for y-ticks

    # Show the plot
    plt.show()


# Choose which states to include
states_to_include = ["MVC", "In box", "Moving to Box", "Resting", "Moving to rest position"]

# Choose which EMG signals to include, e.g., plot only EMG1, EMG3, and EMG5
emg_signals_to_include = [1, 2, 3, 4, 5, 6, 7, 8]

# Example usage:
gesture_name = "supination"  # choose which gesture to look at. "extension", "fist", "flexion", "pinch", "pronation" or "supination"
#plot_emg_with_states(gesture_name, states_to_include, emg_signals_to_include=emg_signals_to_include, color_shading=True)

plot_emg_with_states("fist", states_to_include, emg_signals_to_include)

#--------------------Best fitting line from here on---------------------------------
def plot_all_emg_trends(df):
    """
    Plots the best-fit lines for all EMG signals (EMG1 to EMG8) on the same graph.

    Parameters:
    df (DataFrame): The dataset containing EMG and state information.
    """

    # Convert Timestamp column to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Convert timestamps to numerical values (seconds since start)
    df["Time_Seconds"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()

    # Set up the figure
    plt.figure(figsize=(12, 6))

    # Define a color map for different EMG channels
    colors = ["blue", "green", "red", "purple", "orange", "brown", "pink", "cyan"]

    # Loop through all EMG signals (EMG1 to EMG8)
    for i in range(1, 9):
        x = df["Time_Seconds"].values
        y = df[f"EMG{i}"].values

        # Compute best-fit line using linear regression (y = mx + b)
        m, b = np.polyfit(x, y, 1)
        best_fit_line = m * x + b

        # Plot best-fit line for the EMG channel
        plt.plot(df["Timestamp"], best_fit_line, label=f"EMG{i} (Slope: {m:.6f})", color=colors[i-1], linestyle="--", linewidth=2)

    # Formatting the plot
    plt.xlabel("Time", fontsize=14, fontweight='bold')  # Bold label for x-axis
    plt.ylabel("EMG Signal", fontsize=14, fontweight='bold')  # Bold label for y-axis
    plt.title("Best-Fit Trends for All EMG Signals", fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True)

    # Remove the timestamp from the x-axis by hiding the xticks
    plt.xticks([])  # This removes the x-axis tick labels

    # Make y-axis ticks bold and larger
    plt.tick_params(axis='y', labelsize=12, labelcolor='black', width=2)
    plt.yticks(fontweight='bold', fontsize=14)

    # Show the plot
    plt.show()



def calculateRawEMGToVisualize():
    data = pd.read_csv("Archive/Final Pre Test/Merged/merged_fist_cleanedNew.csv", sep=";")
    cubeDataFrames = []
    windowSize = 40
    stepSize = 20
    emgColumns = [f'EMG{i}' for i in range(1, 9)]
    emgMeans = []

    for cube in range(9):
        cubeName = f"Cube {cube}"
        activeCube = data[data['ActivatedCube'] == cubeName]
        cubeDataFrames.append(activeCube)

    for dfs in cubeDataFrames:
        for start in range(0, len(dfs) - windowSize + 1, stepSize):
            currentWindow = dfs[start:start + windowSize]
            rawEMGMean = currentWindow[emgColumns].values.mean()  # This safely flattens the data
            emgMeans.append(float(rawEMGMean))
    return emgMeans


def visualizeAllFeatures():
    data = pd.read_csv("Archive/test Data set/TrainingSetWdeltas_L.csv")
    processedData = data[data['GoalGesture'] == 0]

    #processedData = featureSelection.createDataFrameWithCalculationsTraining(40, 20, data)
    emgData = calculateRawEMGToVisualize()
    mav = processedData[["EMG1DELTAMAV", "EMG2DELTAMAV", "EMG3DELTAMAV", "EMG4DELTAMAV", "EMG5DELTAMAV", "EMG6DELTAMAV", "EMG7DELTAMAV", "EMG8DELTAMAV"]]
    zc = processedData[["EMG1DELTAZC", "EMG2DELTAZC", "EMG3DELTAZC", "EMG4DELTAZC", "EMG5DELTAZC", "EMG6DELTAZC", "EMG7DELTAZC", "EMG8DELTAZC"]]
    slope = processedData[["EMG1DELTASlope", "EMG2DELTASlope", "EMG3DELTASlope", "EMG4DELTASlope", "EMG5DELTASlope", "EMG6DELTASlope",  "EMG7DELTASlope", "EMG8DELTASlope"]]
    ssc = processedData[["EMG1DELTASSC",  "EMG2DELTASSC", "EMG3DELTASSC", "EMG4DELTASSC", "EMG5DELTASSC", "EMG6DELTASSC", "EMG7DELTASSC", "EMG8DELTASSC"]]
    wfl = processedData[["EMG1DELTAWFL", "EMG2DELTAWFL", "EMG3DELTAWFL", "EMG4DELTAWFL", "EMG5DELTAWFL", "EMG6DELTAWFL", "EMG7DELTAWFL", "EMG8DELTAWFL"]]

    mavMean = mav.mean(axis=1)
    zcMean = zc.mean(axis=1)
    slopeMean = slope.mean(axis=1)
    sscMean = ssc.mean(axis=1)
    wflMean = wfl.mean(axis=1)

    minRows = mavMean.shape[0]
    emgData = emgData[:minRows]

    meanFeatures = [
        ("RAWEMG", emgData),
        ("DeltaMAV", mavMean),
        ("DeltaZC", zcMean),
        ("DeltaSlope", slopeMean),
        ("DeltaSSC", sscMean),
        ("DeltaWFL", wflMean)
    ]

    fig, axes = plt.subplots(len(meanFeatures), 1, figsize=(10, 12), sharex=True)
    x = np.arange(mavMean.shape[0])
    for i, (featureName, featureData) in enumerate(meanFeatures):
        axes[i].plot(x, featureData, label=f"{featureName}", color=f"C{i}")
        axes[i].set_ylabel(featureName)  # Label Y-axis for each channel
        axes[i].legend(loc="upper right")
        axes[i].grid(True)

    # Common X-axis label
    axes[-1].set_xlabel("Time (samples)")

    # Set a common title
    fig.suptitle("EMG Signals", fontsize=14)

    # Adjust layout for better spacing
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save plot
    plt.savefig(f"Images/ProcessedEMGSignalsForDeltaPinch.png", dpi=300, bbox_inches="tight")
    # Show plot
    plt.show()

#visualizeAllFeatures()

gesture_files_All = [
    "Data_CleanUp_L/merged_file_extension_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_fist_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_flexion_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pinch_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pronation_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_supination_L_cleaned.csv",
    "Data_CleanUp_C/merged_file_extension_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_fist_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_flexion_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pinch_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pronation_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_supination_C_cleaned.csv"
]

# Example usage:
#for file in gesture_files_All:
    #df = pd.read_csv(file, delimiter=";")  # Change file if needed
    #plot_all_emg_trends(df)  # Call function to visualize best-fit trends

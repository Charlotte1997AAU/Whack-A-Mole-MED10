import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from pathlib import Path

pd.set_option("display.max_columns", None)

participantNr = 5


def calculateTestStats(file, showPlot: bool):
    # Load and parse the CSV with semicolon delimiter
    df = pd.read_csv(file, delimiter=';')

    valid_df = df[(df['InCube'] == 'InCube')].copy()
    valid_df['GoalGesture'] = valid_df['GoalGesture'].astype(int)
    valid_df['Prediction'] = valid_df['Prediction'].astype(int)

    result_stats = []

    # Loop over each gesture class
    for gesture in sorted(valid_df['GoalGesture'].unique()):
        true_labels = (valid_df['GoalGesture'] == gesture).astype(int)
        pred_labels = (valid_df['Prediction'] == gesture).astype(int)

        gesture_names = {
            0: "Extension",
            1: "Fist",
            2: "Flexion",
            3: "Pinch"
        }

        precision = precision_score(true_labels, pred_labels, zero_division=0)
        recall = recall_score(true_labels, pred_labels, zero_division=0)
        f1 = f1_score(true_labels, pred_labels, zero_division=0)

        result_stats.append({
            'gesture': gesture_names[gesture],
            'precision': precision,
            'recall': recall,
            'f1-score': f1
        })

    results_df = pd.DataFrame(result_stats)

    if showPlot:
        # Get all valid GoalGesture classes (assuming these are always integers)
        gesture_labels = sorted(valid_df['GoalGesture'].unique())

        # Create the confusion matrix
        cm = confusion_matrix(valid_df['GoalGesture'], valid_df['Prediction'], labels=gesture_labels)

        # Display the confusion matrix
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=gesture_labels)
        disp.plot(cmap=plt.cm.Blues)
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.show()

    return results_df


testStats = calculateTestStats(f"TestData/Participant {participantNr}/Test_log_{participantNr}.csv", False)


def compareTrainAndTestSet(participantNr: int, testStats):
    root_dir = Path("TestData")
    target_folder_name = f"participant {participantNr}".lower()

    participant_folder = None

    # Locate the participant folder
    for subdir in root_dir.iterdir():
        if subdir.is_dir() and subdir.name.lower() == target_folder_name:
            participant_folder = subdir
            break

    if participant_folder is None:
        print(f"No folder found for participant {participantNr}")
        return

    report_file = participant_folder / "classification_report.csv"
    if not report_file.exists():
        print(f"'classification_report.csv' not found in {participant_folder}")
        return

    # Read test classification report
    try:
        train_df = pd.read_csv(report_file)
        train_df = train_df.iloc[:4]  # Only first 4 rows (the gestures)
        train_df = train_df.drop(columns=["support"], errors="ignore")  # Drop 'support' if present
        # print(f"\nTest Classification Report for Participant {participantNr}:\n")
        # print(train_df)
    except Exception as e:
        print(f"Failed to read {report_file}: {e}")
        return

    # Prepare trainStats (drop 'gesture' row if present)
    if "gesture" in testStats.index:
        test_df = testStats.drop(testStats["Gesture"], index=1)
    else:
        test_df = testStats.copy()

    # Align and compare
    try:
        comparison_df = pd.concat(
            [train_df.add_suffix(" (Train)"), test_df.add_suffix(" (Test)")],
            axis=1,
            join="inner"
        )

        comparison_df = (comparison_df * 100).round(2)
        comparison_df = comparison_df.drop(['gesture (Test)'], axis=1)

        # Add gesture names
        gesture_names = {
            0: "Extension",
            1: "Fist",
            2: "Flexion",
            3: "Pinch"
        }
        comparison_df["Gesture"] = comparison_df.index.map(gesture_names)
        comparison_df = comparison_df[["Gesture"] + [col for col in comparison_df.columns if col != "Gesture"]]

        print(f"\nComparison of Train vs. Test for Participant {participantNr}:\n")
        print(comparison_df.to_string())

        return comparison_df

    except Exception as e:
        print(f"Failed to compare classification reports: {e}")


#comparison_df = compareTrainAndTestSet(participantNr, testStats)


def plotGesturePerformanceComparison(comparison_df):
    """
    Creates a grouped bar chart comparing Train vs Test performance
    for precision, recall, and f1-score across all gestures.

    Parameters:
        comparison_df (pd.DataFrame): DataFrame with columns like:
            'precision (Test)', 'precision (Train)', etc.
    """

    # Reset index if gesture names are in index
    df = comparison_df.copy()
    if df.index.name or not df.index.equals(pd.RangeIndex(len(df))):
        df = df.reset_index()
        df = df.rename(columns={'index': 'Gesture'})

    # Melt the dataframe for plotting
    plot_df = df.melt(id_vars='Gesture', var_name='Metric-Set', value_name='Score')

    # Split Metric-Set into Metric and Set (Train/Test)
    plot_df[['Metric', 'Set']] = plot_df['Metric-Set'].str.extract(r'(\w+)\s+\((\w+)\)')

    # Filter for only the relevant metrics (precision, recall, f1-score)
    plot_df = plot_df[plot_df['Metric'].isin(['precision', 'recall', 'f1-score'])]

    # Create grouped bar chart
    plt.figure(figsize=(12, 6))  # Adjusted figure size for better spacing
    metrics = ['precision', 'recall', 'f1-score']
    sets = ['Train', 'Test']
    bar_width = 0.1  # Reduced bar width for better separation between bars
    gap_between_groups = 0.1  # Added gap between metric groups
    gestures = df['Gesture'].tolist()
    x = range(len(gestures))

    # Loop through each metric
    for i, metric in enumerate(metrics):
        for j, set_type in enumerate(sets):
            # Filter the data for the current metric and set
            subset = plot_df[(plot_df['Metric'] == metric) & (plot_df['Set'] == set_type)]

            # If the subset is empty, skip plotting for this combination
            if subset.empty:
                continue

            # Calculate the x positions for bars, ensuring they are spaced properly
            x_pos = [xi + (j - 0.5) * bar_width + i * (bar_width + gap_between_groups) for xi in x]

            # Plot the bars for the current metric and set
            plt.bar(x_pos, subset['Score'], width=bar_width, label=f"{metric.capitalize()} ({set_type})")

    # Formatting
    plt.xticks([xi + bar_width for xi in x], gestures)
    plt.ylabel("Score (%)")
    plt.title("Train vs Test Gesture Performance")
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


#plotGesturePerformanceComparison(comparison_df)


def calcOverallAverageScores():
    root_dir = Path("TestData")
    result_stats = []
    resultsList = []

    # Loop through all participant folders and CSV files
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "participant" in dirpath.lower():
            for file in filenames:
                if file.endswith(".csv") and "classification_report" in file:
                    full_path = Path(dirpath) / file
                    try:
                        df = pd.read_csv(full_path)
                        for gesture in range(4):
                            precision = df['precision'].iloc[gesture]
                            recall = df['recall'].iloc[gesture]
                            f1 = df['f1-score'].iloc[gesture]
                            result_stats.append({
                                'gesture': gesture,
                                'precision': precision,
                                'recall': recall,
                                'f1-score': f1
                            })

                        results_df = pd.DataFrame(result_stats)

                        gestureFrames = []
                        for gesture in range(results_df['gesture'].nunique()):
                            currentGesture = results_df[results_df['gesture'] == gesture]
                            gestureFrames.append(currentGesture)

                        averages = []
                        gesture_names = {
                            0: "Extension",
                            1: "Fist",
                            2: "Flexion",
                            3: "Pinch"
                        }

                        for frames in gestureFrames:
                            averages.append({
                                'gesture': gesture_names[frames['gesture'].iloc[0]],
                                'precision': np.mean(frames['precision']),
                                'recall': np.mean(frames['recall']),
                                'f1-score': np.mean(frames['f1-score'])
                            })

                        averagesTrainDf = pd.DataFrame(averages)

                    except Exception as e:
                        print(f"Failed to read {full_path}: {e}")

                if file.endswith(".csv") and "Test_log" in file and "moving" not in file:
                    full_path = Path(dirpath) / file
                    testResults = calculateTestStats(full_path, False)
                    resultsList.append(testResults)

                    combined_df = pd.concat(resultsList, ignore_index=True)

                    # Group by gesture and calculate the mean
                    averagesTestDf = combined_df.groupby("gesture").mean(numeric_only=True).reset_index()

    comparison_df = pd.concat(
        [averagesTrainDf.add_suffix(" (Train)"), averagesTestDf.add_suffix(" (Test)")],
        axis=1,
        join="inner"
    )

    comparison_df = (comparison_df * 100).round(2)
    comparison_df = comparison_df.drop(['gesture (Train)', 'gesture (Test)'], axis=1)

    # Add gesture names
    gesture_names = {
        0: "Extension",
        1: "Fist",
        2: "Flexion",
        3: "Pinch"
    }
    comparison_df["Gesture"] = comparison_df.index.map(gesture_names)
    comparison_df = comparison_df[["Gesture"] + [col for col in comparison_df.columns if col != "Gesture"]]

    macroStats = []
    macroStats.append({
        'Gesture': "Macro",
        'precision (Train)': np.mean(comparison_df['precision (Train)']),
        'recall (Train)': np.mean(comparison_df['recall (Train)']),
        'f1-score (Train)': np.mean(comparison_df['f1-score (Train)']),
        'precision (Test)': np.mean(comparison_df['precision (Test)']),
        'recall (Test)': np.mean(comparison_df['recall (Test)']),
        'f1-score (Test)': np.mean(comparison_df['f1-score (Test)']),
    })

    macroDf = pd.DataFrame(macroStats)

    combined_df = pd.concat([comparison_df, macroDf], ignore_index=True)

    print(combined_df)
    combined_df.to_csv("combinedScores.csv", index=False)

    return comparison_df

# Uncomment to plot average precision and recall scores for training and testing
#plotGesturePerformanceComparison(calcAverageScores())
calcOverallAverageScores()

def presenceMatrix():
    """
    Shows how many times each gesture was the goal for each box over all tests.
    :return: presence_matrix:
    Matrix containing count of each gesture for each cube
    """
    root_dir = Path("TestData")

    gesture_records = []

    # Loop through all participant folders and CSV files
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "participant" in dirpath.lower():
            for file in filenames:
                if file.endswith(".csv") and "Test_log" in file:
                    full_path = Path(dirpath) / file
                    try:
                        df = pd.read_csv(full_path, delimiter=';')
                        df = df[(df['InCube'] == 'InCube') & (df['Prediction'] != 'None')].copy()
                        df['GoalGesture'] = df['GoalGesture'].astype(int)
                        df['ActivatedCube'] = df['ActivatedCube'].str.extract(r'(\d+)').astype(int)

                        # Keep all records to count real frequencies
                        gesture_records.extend(df[['ActivatedCube', 'GoalGesture']].dropna().values.tolist())
                    except Exception as e:
                        print(f"Failed to read {full_path}: {e}")

    # Convert to DataFrame
    presence_df = pd.DataFrame(gesture_records, columns=['ActivatedCube', 'GoalGesture'])

    # Build presence matrix with counts
    presence_matrix = (
        presence_df
        .groupby(['ActivatedCube', 'GoalGesture'])  # No drop_duplicates here
        .size()
        .unstack(fill_value=0)
    )

    presence_matrix.loc['TotalPerGesture'] = presence_matrix.sum(axis=0)

    # Show result
    print("Overall Presence Matrix (with counts):")
    print(presence_matrix)

# presenceMatrix()

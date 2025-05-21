import os
import re
from datetime import timedelta
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from scipy.stats import shapiro, kruskal, f_oneway, levene
import glob
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
from pathlib import Path
from collections import defaultdict


pd.set_option("display.max_columns", None)

participantNr = 6


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
#print(testStats)


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
            [train_df.add_suffix(" (Offline)"), test_df.add_suffix(" (Online)")],
            axis=1,
            join="inner"
        )

        comparison_df = (comparison_df * 100).round(2)
        comparison_df = comparison_df.drop(['gesture (Online)'], axis=1)

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


comparison_df = compareTrainAndTestSet(participantNr, testStats)


def plot_connected_f1_scores(df):
    # Convert percentages to 0–1 scale
    df["f1-score (Offline)"] = df["f1-score (Offline)"] / 100
    df["f1-score (Online)"] = df["f1-score (Online)"] / 100

    plt.figure(figsize=(8, 5))

    for idx, row in df.iterrows():
        offline_score = row["f1-score (Offline)"]
        online_score = row["f1-score (Online)"]
        diff = online_score - offline_score

        # Plot line with markers
        plt.plot(["Offline", "Online"],
                 [offline_score, online_score],
                 marker="o",
                 label=f"{row['Gesture']} (Delta={diff:+.2f})")  # Δ in legend

    plt.title("F1-Score: Online vs Offline per Gesture", fontsize=16, fontweight="bold")
    plt.ylabel("F1-Score", fontsize=16, fontweight="bold")
    plt.xticks(fontsize=16, fontweight="bold")
    plt.yticks(fontsize=16, fontweight="bold")
    plt.ylim(0.7, 1.0)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Gesture (Delta F1)", fontsize=14, title_fontsize=16)
    plt.tight_layout()
    plt.savefig("connected_f1_scores.png")
    plt.show()


plot_connected_f1_scores(comparison_df)

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
    df = df[df['Gesture'] != 'Macro']
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
    sets = ['Offline', 'Online']
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
    plt.xticks([xi + bar_width for xi in x], gestures, fontsize=16, fontweight='bold')
    plt.yticks(fontsize=16, fontweight='bold')
    plt.ylabel("Score (%)", fontsize=16, fontweight='bold')
    plt.title("Offline vs Online Gesture Performance", fontsize=18, fontweight='bold')
    plt.legend(fontsize=14, loc='lower center')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("trainVsTestPerformance.png")
    plt.show()


#plotGesturePerformanceComparison(comparison_df)


def collect_online_f1_scores(base_path="TestData"):
    all_data = []

    for folder in os.listdir(base_path):
        if folder.startswith("Participant "):
            try:
                participantNr = int(folder.split(" ")[1])
                file_path = os.path.join(base_path, folder, f"Test_log_{participantNr}.csv")

                testStats = calculateTestStats(file_path, False)
                for _, row in testStats.iterrows():
                    all_data.append({
                        "Participant": participantNr,
                        "Gesture": row["gesture"],
                        "F1-score": row["f1-score"]
                    })
            except Exception as e:
                print(f"Skipping {folder}: {e}")

    return pd.DataFrame(all_data)


def collect_offline_f1_scores(base_path="TestData"):
    all_data = []

    gesture_names = {
        0: "Extension",
        1: "Fist",
        2: "Flexion",
        3: "Pinch"
    }

    for folder in os.listdir(base_path):
        if folder.startswith("Participant "):
            try:
                participantNr = int(folder.split(" ")[1])
                report_path = os.path.join(base_path, folder, "classification_report.csv")

                if not os.path.exists(report_path):
                    print(f"Missing classification report for Participant {participantNr}")
                    continue

                df = pd.read_csv(report_path)

                # Ensure we only use the first 4 rows (per gesture)
                df = df.iloc[:4]

                for i, row in df.iterrows():
                    gesture = gesture_names.get(i, f"Gesture {i}")
                    f1_score = row["f1-score"]
                    all_data.append({
                        "Participant": participantNr,
                        "Gesture": gesture,
                        "F1-score": f1_score
                    })

            except Exception as e:
                print(f"Skipping {folder}: {e}")

    return pd.DataFrame(all_data)


def plot_violin_by_gesture(f1_df):
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=f1_df, x="Gesture", y="F1-score", inner="box", palette="Set2")

    plt.title("Distribution of F1-Scores by Gesture Across Participants for Offline test", fontsize=16, fontweight='bold')
    plt.xlabel("Gesture", fontsize=16, fontweight='bold')
    plt.ylabel("F1-Score", fontsize=16, fontweight='bold')
    plt.xticks(fontsize=14, fontweight='bold')
    plt.yticks(fontsize=14, fontweight='bold')
    plt.ylim(0.5, 1)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig("Images/violin_f1_scores_by_gesture_Offline.png")
    plt.show()


#f1_df = collect_offline_f1_scores()
#plot_violin_by_gesture(f1_df)


def plotMacroF1ByParticipant(base_path="TestData"):
    macro_f1_scores = []

    # Loop through folders in base_path that start with 'Participant '
    for folder in os.listdir(base_path):
        if folder.startswith("Participant "):
            try:
                participantNr = int(folder.split(" ")[1])
                file_path = os.path.join(base_path, folder, f"Test_log_{participantNr}.csv")

                # Get gesture-level stats
                testStats = calculateTestStats(file_path, False)

                # Compute macro F1-score
                macro_f1 = testStats["f1-score"].mean()
                macro_f1_scores.append((participantNr, float(macro_f1)))

            except Exception as e:
                print(f"Skipping {folder}: {e}")


    # Convert to DataFrame for plotting
    df = pd.DataFrame(macro_f1_scores, columns=["Participant", "Macro F1"])
    df = df.sort_values("Macro F1")


    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(df)), df["Macro F1"], color="steelblue", width=0.6)
    plt.title("Macro F1-Score Across Participants", fontsize=16, fontweight='bold')
    plt.xlabel("Participant Number", fontsize=14, fontweight='bold')
    plt.ylabel("Macro F1-Score", fontsize=14, fontweight='bold')
    plt.xticks(range(len(df)), df["Participant"], fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("macro_f1_by_participant.png")
    plt.show()


#plotMacroF1ByParticipant()


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
        [averagesTrainDf.add_suffix(" (Offline)"), averagesTestDf.add_suffix(" (Online)")],
        axis=1,
        join="inner"
    )

    comparison_df = (comparison_df * 100).round(2)
    comparison_df = comparison_df.drop(['gesture (Offline)', 'gesture (Online)'], axis=1)

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
        'precision (Offline)': np.mean(comparison_df['precision (Offline)']),
        'recall (Offline)': np.mean(comparison_df['recall (Offline)']),
        'f1-score (Offline)': np.mean(comparison_df['f1-score (Offline)']),
        'precision (Online)': np.mean(comparison_df['precision (Online)']),
        'recall (Online)': np.mean(comparison_df['recall (Online)']),
        'f1-score (Online)': np.mean(comparison_df['f1-score (Online)']),
    })

    macroDf = pd.DataFrame(macroStats)

    combined_df = pd.concat([comparison_df, macroDf], ignore_index=True)

    print(combined_df)

    return combined_df


# Uncomment to plot average precision and recall scores for training and testing
#plotGesturePerformanceComparison(calcOverallAverageScores())


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


def avgScoresPerBox(boxNum: int = None, printScores: bool = False):
    root_dir = Path("TestData")
    resultsList = []

    # Collect all data
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "participant" in dirpath.lower():
            for file in filenames:
                if file.endswith(".csv") and "Test_log" in file and "moving" not in file:
                    full_path = Path(dirpath) / file
                    testResults = pd.read_csv(full_path, sep=";")
                    resultsList.append(testResults)

    # Combine all DataFrames
    combined_df = pd.concat(resultsList, ignore_index=True)
    combined_df = combined_df.dropna(subset=['ActivatedCube'])
    cube_names = sorted(
        combined_df['ActivatedCube'].unique(),
        key=lambda x: int(str(x).split()[-1])
    )

    # Helper to calculate scores for a single cube
    def compute_scores_for_cube(df, cube_name):
        y_true = df['GoalGesture']
        y_pred = df['Prediction']
        labels = sorted(df['GoalGesture'].unique())
        gesture_names = {
            0: "Extension",
            1: "Fist",
            2: "Flexion",
            3: "Pinch"
        }
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=labels, zero_division=0
        )

        gesture_labels = [gesture_names.get(label, str(label)) for label in labels]

        return pd.DataFrame({
            'gesture': gesture_labels,
            'precision': precision,
            'recall': recall,
            'f1-score': f1
        })

    # If a specific cube is provided
    if boxNum is not None:
        cubeName = f"Cube {boxNum}"
        filtered_df = combined_df[combined_df['ActivatedCube'] == cubeName]
        scores_df = compute_scores_for_cube(filtered_df, cubeName)
        if printScores:
            print(f"\nScores for {cubeName}:\n{scores_df}")
        return scores_df

    # If no cube specified, compute for all cubes
    else:
        cube_scores = {}
        f1_scores_per_cube = {}  # This will store macro F1 scores per cube

        for cubeName in cube_names:
            filtered_df = combined_df[combined_df['ActivatedCube'] == cubeName]
            scores_df = compute_scores_for_cube(filtered_df, cubeName)
            if printScores:
                print(f"\nScores for {cubeName}:\n{scores_df}")
            cube_scores[cubeName] = scores_df

            # Compute and store macro F1 score
            macro_f1 = scores_df['f1-score'].mean()
            f1_scores_per_cube[cubeName] = macro_f1

        return cube_scores, f1_scores_per_cube


def plot_cube_scores(cube_scores: dict):
    sns.set(style="whitegrid")

    num_cubes = len(cube_scores)
    rows, cols = 3, 3
    fig, axes = plt.subplots(rows, cols, figsize=(18, 12))
    fig.suptitle("Performance Metrics per Cube", fontsize=18, y=1.07)  # Move title up

    axes = axes.flatten()
    shared_handles, shared_labels = None, None

    desired_order = [2, 5, 8, 1, 4, 7, 0, 3, 6]
    ordered_keys = [f"Cube {i}" for i in desired_order]

    for idx, cube_name in enumerate(ordered_keys):
        df = cube_scores.get(cube_name)
        if df is None:
            continue  # skip if this cube isn't in the results

        ax = axes[idx]

        melted_df = df.melt(
            id_vars='gesture',
            value_vars=['precision', 'recall', 'f1-score'],
            var_name='metric',
            value_name='score'
        )

        show_legend = (shared_handles is None)
        sns.barplot(
            data=melted_df, x='gesture', y='score', hue='metric',
            ax=ax, legend=show_legend
        )
        ax.set_title(cube_name)
        ax.set_ylim(0, 1)
        ax.set_xlabel("")
        ax.set_ylabel("Score")

        if show_legend:
            shared_handles, shared_labels = ax.get_legend_handles_labels()
            ax.legend_.remove()

    # Remove unused subplots
    for i in range(idx + 1, len(axes)):
        fig.delaxes(axes[i])

    # Add shared legend — move it slightly lower
    fig.legend(
        shared_handles,
        shared_labels,
        title="Metric",
        loc='upper center',
        ncol=3,
        fontsize='medium',  # Slightly smaller font
        title_fontsize='medium',  # Smaller title
        bbox_to_anchor=(0.515, 0.915),
        frameon=True,  # Optional: remove box around legend
        handletextpad=0.5,  # Space between marker and text
        columnspacing=0.8,  # Space between columns
        labelspacing=0.3  # Vertical space between entries
    )


    # Leave more top margin for legend + title
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.subplots_adjust(top=0.9)  # Reserve space at the top
    plt.show()


def print_extreme_scores(cube_scores: dict):
    metrics = ['precision', 'recall', 'f1-score']
    gestures = cube_scores[next(iter(cube_scores))]['gesture'].tolist()

    for gesture in gestures:
        print(f"\n{gesture}:")
        for metric in metrics:
            highest_value = -1
            lowest_value = 2  # precision/recall/f1 are all <= 1

            highest_cube = None
            lowest_cube = None

            for cube_name, df in cube_scores.items():
                value = df.loc[df['gesture'] == gesture, metric].values[0]
                if value > highest_value:
                    highest_value = value
                    highest_cube = cube_name
                if value < lowest_value:
                    lowest_value = value
                    lowest_cube = cube_name

            difference = highest_value - lowest_value

            print(f"  Highest {metric} in {highest_cube} ({highest_value:.2%})")
            print(f"  Lowest  {metric} in {lowest_cube} ({lowest_value:.2%})")
            print(f"  → Difference: {difference:.2%}")

    avg_f1_scores = {}

    for cube_name, df in cube_scores.items():
        avg_f1 = df['f1-score'].mean()
        avg_f1_scores[cube_name] = avg_f1

    best_cube = max(avg_f1_scores, key=avg_f1_scores.get)
    worst_cube = min(avg_f1_scores, key=avg_f1_scores.get)

    print("\nOverall cube performance (by average f1-score):")
    print(f"  Best performing cube: {best_cube} ({avg_f1_scores[best_cube]:.2%})")
    print(f"  Worst performing cube: {worst_cube} ({avg_f1_scores[worst_cube]:.2%})")
    print(f"  → Difference: {(avg_f1_scores[best_cube] - avg_f1_scores[worst_cube]):.2%}")


#scores, f1_scores_per_cube = avgScoresPerBox(printScores=False)
#print_extreme_scores(scores)
#plot_cube_scores(scores)


def natural_key(string):
    """Sorts strings containing numbers in human order."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', string)]


def calcMovingBoxes():
    root_dir = Path("TestData")
    participant_data = defaultdict(list)  # key = participant name, value = list of DataFrames

    # Step 1: Collect and group data by participant
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "participant" in dirpath.lower():
            participant_name = Path(dirpath).name  # Use directory name as participant ID
            for file in filenames:
                if file.endswith(".csv") and "Test_log" in file:
                    full_path = Path(dirpath) / file
                    df = pd.read_csv(full_path, sep=";")
                    df = df[(df['movingCube'] == 'Moving box')].copy()
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                    df.dropna(subset=['Timestamp'], inplace=True)
                    if not df.empty:
                        participant_data[participant_name].append(df)

    # Step 2: Calculate stats per participant
    participant_results = {}  # key = participant, value = results DataFrame
    direction_results = []

    for participant, df_list in participant_data.items():
        result_stats = []

        # Combine all relevant DataFrames for this participant
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df['GoalGesture'] = combined_df['GoalGesture'].astype(int)
        combined_df['Prediction'] = combined_df['Prediction'].astype(int)

        gesture_names = {
            0: "Extension",
            1: "Fist",
            2: "Flexion",
            3: "Pinch"
        }

        # Step 3: Compute metrics per gesture
        for gesture in sorted(gesture_names.keys()):
            true_labels = (combined_df['GoalGesture'] == gesture).astype(int)
            pred_labels = (combined_df['Prediction'] == gesture).astype(int)

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
        participant_results[participant] = results_df

        # === Step 3b: Movement Direction Analysis ===
        directions = ["Right", "Up", "Left", "Down"]
        movement_duration = pd.Timedelta(seconds=2.5)

        # Sort and label movement chunks
        combined_df = combined_df.sort_values(by='Timestamp').reset_index(drop=True)
        start_time = combined_df['Timestamp'].iloc[0]
        end_time = combined_df['Timestamp'].iloc[-1]
        current_time = start_time
        direction_idx = 0

        combined_df['MovementDirection'] = pd.Series(dtype="object")

        while current_time < end_time:
            next_time = current_time + movement_duration
            mask = (combined_df['Timestamp'] >= current_time) & (combined_df['Timestamp'] < next_time)
            combined_df.loc[mask, 'MovementDirection'] = directions[direction_idx % 4]
            direction_idx += 1
            current_time = next_time

        combined_df.dropna(subset=['MovementDirection'], inplace=True)

        for direction in directions:
            df_direction = combined_df[combined_df['MovementDirection'] == direction]
            if not df_direction.empty:
                f1 = f1_score(df_direction['GoalGesture'], df_direction['Prediction'], average='macro', zero_division=0)
                direction_results.append({
                    'participant': participant,
                    'direction': direction,
                    'f1_score': f1
                })

    # Step 4: Print or return the results
    for participant in sorted(participant_results.keys(), key=natural_key):
        print(f"\n=== Results for {participant} ===")
        print(participant_results[participant])

    # Optional: return both gesture stats and direction stats
    direction_df = pd.DataFrame(direction_results)
    print(f"\nMacro f1 per direction: \n {direction_df.groupby('direction')['f1_score'].mean()}")

    grouped = [group['f1_score'].values for _, group in direction_df.groupby('direction')]
    stat, p = kruskal(*grouped)
    print(f"\nKruskal-Wallis for directions: \n H = {stat:.3f}, p = {p:.3f}")

    return participant_results, direction_df  # optional: return for further processing


#participantResults, directionResults = calcMovingBoxes()


def movingBoxKruskalWallis(movingBoxResults):
    long_data = []

    for participant, df in movingBoxResults.items():
        for _, row in df.iterrows():
            long_data.append({
                'participant': participant,
                'gesture': row['gesture'],
                'f1-score': row['f1-score']
            })

    anova_df = pd.DataFrame(long_data)

    for gesture in anova_df['gesture'].unique():
        scores = anova_df[anova_df['gesture'] == gesture]['f1-score']
        stat, p = shapiro(scores)
        print(f"{gesture} normality p-value: {p:.3f}")

    groups = [anova_df[anova_df['gesture'] == g]['f1-score'] for g in anova_df['gesture'].unique()]
    stat, p = levene(*groups)
    print(f"Levene’s test p-value: {p:.3f}")

    groups = [anova_df[anova_df['gesture'] == g]['f1-score'] for g in anova_df['gesture'].unique()]

    # Run Kruskal-Wallis H-test
    kruskal_result = kruskal(*groups)
    print(f"Kruskal-Wallis for moving overall: H = {kruskal_result.statistic:.3f}, p = {kruskal_result.pvalue:.3f}")


#movingBoxKruskalWallis(participantResults)


def computeANOVA():
    root_dir = Path("TestData")
    participant_f1s = defaultdict(lambda: defaultdict(list))  # participant_f1s[participant][cube] = list of f1s

    for dirpath, _, filenames in os.walk(root_dir):
        if "participant" in dirpath.lower():
            participant_name = Path(dirpath).name
            for file in filenames:
                if file.endswith(".csv") and "Test_log" in file and "moving" not in file:
                    full_path = Path(dirpath) / file
                    df = pd.read_csv(full_path, sep=";")
                    df = df.dropna(subset=['ActivatedCube', 'GoalGesture', 'Prediction'])

                    for cube_name, cube_df in df.groupby("ActivatedCube"):
                        y_true = cube_df['GoalGesture']
                        y_pred = cube_df['Prediction']

                        try:
                            macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
                            participant_f1s[participant_name][cube_name].append(macro_f1)
                        except Exception as e:
                            print(f"Error computing F1 for {participant_name} - {cube_name}: {e}")

    cube_f1_scores = defaultdict(list)

    for participant, cube_scores in participant_f1s.items():
        for cube, scores in cube_scores.items():
            if scores:
                cube_f1_scores[cube].extend(scores)

    # Only include cubes with at least 2 samples
    valid_groups = [scores for scores in cube_f1_scores.values() if len(scores) >= 2]
    if len(valid_groups) >= 2:
        levene_stat, levene_p = levene(*valid_groups)
        print(f"Levene's test: W = {levene_stat:.4f}, p = {levene_p:.4f}")

        if levene_p < 0.05:
            print("→ Variances are significantly different (heteroscedasticity)")
        else:
            print("→ Variances are not significantly different (homoscedasticity assumption holds)")
    else:
        print("Not enough data for Levene's test.")

    f_stat, p_val = f_oneway(*valid_groups)

    print(f"One-way ANOVA F = {f_stat:.4f}, p = {p_val:.4f}")


#computeANOVA()


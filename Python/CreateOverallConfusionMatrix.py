import os
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import dataPreProcessing
import featureSelection
import fileManagement
import dataCleanUp
import seaborn as sns
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

# Define gesture label mapping (known ahead of time)
gesture_names = {
    0: "extension",
    1: "fist",
    2: "flexion",
    3: "pinch"
}

# Create a LabelEncoder with fixed class order
le = LabelEncoder()
le.fit([gesture_names[i] for i in sorted(gesture_names.keys())])  # ['extension', 'fist', 'flexion', 'pinch']

# Define the Random Forest model only
models = {
    "random_forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        min_samples_split=10,
        min_samples_leaf=5
    )
}

# Paths to your datasets
dataset_paths = [f"TestData/Participant {i}" for i in range(1, 19)]

# Store confusion matrices for Random Forest only
model_name = "random_forest"
conf_matrices = {model_name: []}

def process_and_train(data_path, model_name):
    # Merge Unity + EMG data
    merged_files = fileManagement.processAllFiles(data_path)

    cleaned_files = [dataCleanUp.cleanMergedData(f) for f in merged_files]
    final_files = [featureSelection.createDataFrameWithCalculationsTraining(40, 20, f) for f in cleaned_files]

    feature_dataset = pd.concat(final_files, ignore_index=True)

    # Use consistent label encoding
    feature_dataset["GoalGesture"] = le.transform(feature_dataset["GoalGesture"])
    feature_dataset = feature_dataset.apply(pd.to_numeric)
    feature_dataset[["activeCubeX", "activeCubeY"]] = feature_dataset[["activeCubeX", "activeCubeY"]].round(3)

    final_dataset = featureSelection.calculateDeltaFeatures(feature_dataset)

    # No standardization needed for Random Forest

    X = final_dataset.drop(columns=["GoalGesture"])
    y = final_dataset["GoalGesture"]

    model = models[model_name]
    model.fit(X, y)
    y_pred = model.predict(X)

    # Compute confusion matrix with fixed label order
    cm = confusion_matrix(y, y_pred, labels=range(len(le.classes_)))
    return cm


# Train and collect confusion matrices for only the random forest model
for idx, data_path in enumerate(dataset_paths, start=1):
    print(f"Training {model_name} on dataset {idx}/{len(dataset_paths)}: {data_path}")
    cm = process_and_train(data_path, model_name)
    if cm is not None and cm.size > 0:
        conf_matrices[model_name].append(cm)
    else:
        print(f"Warning: No confusion matrix returned for {model_name} on {data_path}")

# Average confusion matrices
matrices = conf_matrices[model_name]
if len(matrices) == 0:
    print(f"No confusion matrices collected for {model_name}, cannot average or plot.")
else:
    shapes = [m.shape for m in matrices]
    if len(set(shapes)) > 1:
        print(f"Error: Confusion matrices shapes inconsistent for {model_name}, skipping averaging.")
    else:
        avg_cm = np.mean(matrices, axis=0).astype(int)
        print(f"\nAverage Confusion Matrix for {model_name}:")
        print(avg_cm)

        def plot_confusion_matrix(cm, model_name, labels):
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=labels, yticklabels=labels)
            plt.title(f"Average Confusion Matrix for Offline Test", fontsize=16, fontweight='bold')
            plt.xlabel("Predicted Label", fontsize=16, fontweight='bold')
            plt.ylabel("True Label", fontsize=16, fontweight='bold')
            plt.xticks(fontsize=16, fontweight='bold')
            plt.yticks(fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()

        plot_confusion_matrix(avg_cm, model_name, labels=le.classes_)

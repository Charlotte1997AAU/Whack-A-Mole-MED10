import os

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestClassifier
import dataPreProcessing
import joblib
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def trainModelAllDataframes(dataframes, model, filePath):
    # Combine all DataFrames into one
    dfNormalized = pd.concat(dataframes, ignore_index=True)
    model_name = type(model).__name__

    # Preprocess the data
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]

    X = dfNormalized.drop(columns=excludeColumns)  # Features
    y = dfNormalized['GoalGesture']  # Target

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)

    y_pred_best_model = model.predict(X_test)
    model_accuracy_best = accuracy_score(y_test, y_pred_best_model)
    model_cm = confusion_matrix(y_test, y_pred_best_model)

    print(f"Best accuracy for {model_name}: {model_accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(model_cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best_model))

    # Learning curve
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0], cv=5
    )

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, val_scores.mean(axis=1), label='Validation Accuracy', color='blue', marker='o')
    plt.plot(train_sizes, train_scores.mean(axis=1), label='Training Accuracy', color='green', marker='x')

    plt.title("Overall Learning Curve", fontsize=16, fontweight='bold')
    plt.xlabel("Training Set Size", fontsize=16, fontweight='bold')
    plt.xticks(fontsize=16, fontweight='bold')
    plt.yticks(fontsize=16, fontweight='bold')
    plt.ylabel("Accuracy", fontsize=16, fontweight='bold')
    plt.legend(loc='best', fontsize=16)
    plt.savefig("Images/overallLearningCurve.png")
    plt.show()



def load_all_training_data(root_dir, file_pattern="TrainingSet"):
    dataframes = []

    # Walk through all subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file_pattern in file and file.endswith(".csv"):
                full_path = os.path.join(dirpath, file)
                try:
                    df = pd.read_csv(full_path)
                    dataframes.append(df)
                    print(f"Loaded: {full_path}")
                except Exception as e:
                    print(f"Error loading {full_path}: {e}")

    return dataframes


all_dataframes = load_all_training_data("TestData")

model = RandomForestClassifier(n_estimators=100, max_depth=6, min_samples_split=10, min_samples_leaf=5)
trainModelAllDataframes(all_dataframes, model, "Results")
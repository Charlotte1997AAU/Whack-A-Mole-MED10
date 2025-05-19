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
import numpy as np


def generate_learning_curve(participant_datasets, train_sizes, model, n_repeats=3):
    all_train_acc = {size: [] for size in train_sizes}
    all_val_acc = {size: [] for size in train_sizes}

    for participant, (X, y) in participant_datasets.items():
        for size in train_sizes:
            train_accs = []
            val_accs = []
            for _ in range(n_repeats):
                # Split once to keep test set fixed
                X_train_full, X_test, y_train_full, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=None, stratify=y)

                # Sample subset of training data
                if size < len(X_train_full):
                    idx = np.random.choice(len(X_train_full), size=size, replace=False)
                    X_train = X_train_full[idx]
                    y_train = y_train_full[idx]
                else:
                    X_train = X_train_full
                    y_train = y_train_full

                # Train model
                model.fit(X_train, y_train)

                # Accuracy
                train_preds = model.predict(X_train)
                test_preds = model.predict(X_test)
                train_accs.append(accuracy_score(y_train, train_preds))
                val_accs.append(accuracy_score(y_test, test_preds))

            all_train_acc[size].append(np.mean(train_accs))
            all_val_acc[size].append(np.mean(val_accs))

    mean_train = [np.mean(all_train_acc[size]) for size in train_sizes]
    std_train = [np.std(all_train_acc[size]) for size in train_sizes]
    mean_val = [np.mean(all_val_acc[size]) for size in train_sizes]
    std_val = [np.std(all_val_acc[size]) for size in train_sizes]

    return mean_train, std_train, mean_val, std_val

def plot_learning_curve(train_sizes, mean_train, std_train, mean_val, std_val):
    plt.figure(figsize=(8, 5))
    plt.plot(train_sizes, mean_train, label='Training Accuracy', color='green')
    plt.plot(train_sizes, mean_val, label='Validation Accuracy', color='blue')
    plt.fill_between(train_sizes,
                     np.array(mean_train) - np.array(std_train),
                     np.array(mean_train) + np.array(std_train),
                     alpha=0.2, color='green')
    plt.fill_between(train_sizes,
                     np.array(mean_val) - np.array(std_val),
                     np.array(mean_val) + np.array(std_val),
                     alpha=0.2, color='blue')
    plt.xlabel("Training Set Size", fontsize=16, fontweight='bold')
    plt.ylabel("Accuracy", fontsize=16, fontweight='bold')
    plt.title("Learning Curve Averaged Across Participants", fontsize=18, fontweight='bold')
    plt.xticks(fontsize=16, fontweight='bold')
    plt.yticks(fontsize=16, fontweight='bold')
    plt.legend(fontsize=16)
    plt.grid(True)
    plt.tight_layout()
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

participant_datasets = {}
for i, df in enumerate(all_dataframes):
    X = df.drop(columns=["GoalGesture"]).values
    y = df["GoalGesture"].values
    participant_datasets[f"P{i+1}"] = (X, y)


trainsizes = [500, 1000, 2000, 3000, 4000]
model = RandomForestClassifier(n_estimators=100, max_depth=6, min_samples_split=10, min_samples_leaf=5)
mean_train, std_train, mean_val, std_val = generate_learning_curve(participant_datasets, trainsizes, model)
plot_learning_curve(trainsizes, mean_train, std_train, mean_val, std_val)

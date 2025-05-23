import pandas as pd
import numpy as np
from scipy.stats import shapiro, wilcoxon, stats

testResults = pd.read_csv("combinedTestScores1.csv")
trainResults = pd.read_csv("combinedTrainScores.csv")
testResults.columns = testResults.columns.str.strip()
trainResults.columns = trainResults.columns.str.strip()

def get_gesture_values(test_label, train_label, test_data, train_data):
    test_rows = test_data[test_data['gesture'] == test_label]
    train_rows = train_data[train_data['gesture'] == train_label]

    return {
        'test_precision': test_rows['precision'].tolist(),
        'test_recall': test_rows['recall'].tolist(),
        'test_f1': test_rows['f1-score'].tolist(),
        'train_precision': train_rows['precision'].tolist(),
        'train_recall': train_rows['recall'].tolist(),
        'train_f1': train_rows['f1-score'].tolist()
    }

'''
gestures = [
    ('Extension', 'extension'),
    ('Flexion', 'flexion'),
    ('Pinch', 'pinch'),
    ('Fist', 'fist')
]

gesture_data = {}

for test_label, train_label in gestures:
    gesture_data[test_label] = get_gesture_values(test_label, train_label, testResults, trainResults)

# Optional: print to verify
for gesture, values in gesture_data.items():
    print(f"=== {gesture} ===")

    for k, v in values.items():
        print(f"{k}: {v}")
        print(f"Count: {len(v)}")
    print()


metrics = ['precision', 'recall', 'f1']

for gesture in gesture_data:
    print(f"=== Wilcoxon test: {gesture} ===")
    for metric in metrics:
        test_scores = gesture_data[gesture][f'test_{metric}']
        train_scores = gesture_data[gesture][f'train_{metric}']

        if len(test_scores) != len(train_scores):
            print(f"{metric}: Skipped (length mismatch: test={len(test_scores)}, train={len(train_scores)})")
            continue

        try:
            stat, p = wilcoxon(test_scores, train_scores)
            print(f"{metric}: p = {p:.4f}")
        except ValueError as e:
            print(f"{metric}: Wilcoxon test failed: {e}")
    print()

'''

# Precision
# Extension, Fist, Flexion, Pinch
train_precision = [0.97, 0.84, 0.96, 0.80]
test_precision = [0.73, 0.87, 0.96, 0.69]

# Recall values
train_recall = [0.84, 0.90, 0.90, 0.91]
test_recall = [0.76, 0.62, 0.70, 0.82]

# F1 scores
train_f1 = [0.90, 0.87, 0.93, 0.86]
test_f1 = [0.75, 0.73, 0.81, 0.75]

precision_stat, precision_p = wilcoxon(train_precision, test_precision)
recall_stat, recall_p = wilcoxon(train_recall, test_recall)
f1_stat, f1_p = wilcoxon(train_f1, test_f1)

print("🔍 Wilcoxon Signed-Rank Test Results")
print(f"Precision: statistic={precision_stat}, p-value={precision_p:.4f}")
print(f"Recall:    statistic={recall_stat}, p-value={recall_p:.4f}")
print(f"F1 Score:  statistic={f1_stat}, p-value={f1_p:.4f}")
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score


def calculateTestStats(file):
    df = pd.read_csv(file, sep=";")

    #Todo: split data baseret på active cube, og beregn for hver. derefter kan der beregnes et average for alle gestures,
    # som kan compares med classification fra træning

    precision = precision_score(df['GoalGesture'], df['Prediction'], average='macro')
    recall = recall_score(df['GoalGesture'], df['Prediction'], average='macro')
    f1 = f1_score(df['GoalGesture'], df['Prediction'], average='macro')

    print(f"Precision (macro): {round(precision, 3)}")
    print(f"Recall (macro): {round(recall, 3)}")
    print(f"F1 Score (macro): {round(f1, 3)}")


calculateTestStats("Test_log_2025_05_05_14_07_37_Med10.csv")
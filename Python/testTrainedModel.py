import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

import dataPreProcessing
import joblib

loaded_model = joblib.load('SGD_model_L.pkl')

data = pd.read_csv("test Data set/testSet_L.csv")
excludeColumns = ["EMG1Slope", "EMG2Slope", "EMG3Slope", "EMG4Slope", "EMG5Slope", "EMG6Slope",
                  "EMG7Slope", "EMG8Slope", "activeCube", "activeCubeX", "activeCubeY"]
data.drop(columns=excludeColumns, inplace=True)

# Preprocess the data (standardization)
excludeColumns = ["activeCube","activeCubeX","activeCubeY","trackerX","trackerY","trackerZ","GoalGesture"]
dfNormalized = dataPreProcessing.standardizeDataframe(data, excludeColumns)
print(dfNormalized)

# Select features and target
X = dfNormalized.drop(columns=['GoalGesture'])  # Features
y = dfNormalized['GoalGesture']  # Target

predictions = loaded_model.predict(X)
print(classification_report(y, predictions))
print("Confusion Matrix:")
print(confusion_matrix(y, predictions))

print(f"predictions: {predictions}")

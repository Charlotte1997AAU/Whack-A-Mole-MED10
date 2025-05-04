import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

import dataPreProcessing
import joblib

loaded_model = joblib.load('NeuralNetworkModel.h5')
model_name = type(loaded_model).__name__

data = pd.read_csv("Archive/test Data set/TrainingSet_L.csv")
excludeColumns = ["activeCube", "activeCubeX", "activeCubeY"]
data.drop(columns=excludeColumns, inplace=True)

if model_name == "SGDClassifier":
    # Preprocess the data (standardization)
    excludeColumns = ["activeCube","activeCubeX","activeCubeY","trackerX","trackerY","trackerZ","GoalGesture"]
    data = dataPreProcessing.standardizeDataframe(data, excludeColumns)

# Select features and target
X = data.drop(columns=['GoalGesture'])  # Features
y = data['GoalGesture']  # Target

predictions = loaded_model.predict(X)
print(classification_report(y, predictions))
print("Confusion Matrix:")
print(confusion_matrix(y, predictions))


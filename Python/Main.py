from sklearn.preprocessing import LabelEncoder
import dataPreProcessing
import featureSelection
import fileManagement
import pandas as pd
import dataCleanUp
import MLTraining

# Path to the data the training set should be created from
trainingDataPath = "Final Pre Test"

# Merge Unity data with EMG data to create full raw dataset
mergedFiles = fileManagement.processAllFiles(trainingDataPath)

# Clean merged files
cleanedFiles = []
for file in mergedFiles:
    cleanedFiles.append(dataCleanUp.cleanMergedData(file))

# Calculate features for EMG channels
finalFiles = []
for file in cleanedFiles:
    cleanData = featureSelection.createDataFrameWithCalculationsTraining(40, 20, file)
    finalFiles.append(cleanData)

# Merge calculated feature dataframes for each gesture to final dataframe
finalDataset = pd.concat(finalFiles, ignore_index=True)
le = LabelEncoder()
finalDataset["GoalGesture"] = le.fit_transform(finalDataset["GoalGesture"])
finalDataset = finalDataset.apply(pd.to_numeric)
finalDataset.to_csv("TrainingSet_L.csv", index=False)
print("Training dataset created")

# Remove unnessecary columns
"""Fjern det her i fremtiden, bare lad vær med at lave de columns i stedet for at regne dem og fjerne lige efter"""
excludeColumns = ["EMG1Slope", "EMG2Slope", "EMG3Slope", "EMG4Slope", "EMG5Slope", "EMG6Slope",
                  "EMG7Slope", "EMG8Slope", "activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
dfNormalized = dataPreProcessing.standardizeDataframe(finalDataset, excludeColumns)

# Train model on dataframe
MLTraining.trainModel(dfNormalized)








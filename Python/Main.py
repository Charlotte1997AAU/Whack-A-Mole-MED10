from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
import dataPreProcessing
import featureSelection
import fileManagement
import pandas as pd
import dataCleanUp
import MLTraining
import NNTraining

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
finalDataset.to_csv("test Data set/TrainingSet_L.csv", index=False)
print("Training dataset created")

models = {
    "SGD": SGDClassifier(random_state=42, alpha=0.0001, eta0=0.001, learning_rate='optimal',
                          loss='hinge', max_iter=1000, penalty='l2', tol=0.0001, n_jobs=-1),

    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42,
                                            n_jobs=-1, max_depth=10, min_samples_split=2)
}

trainingModel = models["SGD"]

if trainingModel == models["SGD"]:
    # Remove unnecessary columns
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    finalDataset = dataPreProcessing.standardizeDataframe(finalDataset, excludeColumns)


# Train model on dataframe
#MLTraining.trainModel(finalDataset, trainingModel)
NNTraining.trainNN(finalDataset)





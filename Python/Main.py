from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
import dataPreProcessing
import featureSelection
import fileManagement
import pandas as pd
import dataCleanUp
import MLTraining


# Path to the data the training set should be created from
fileManagement.moveUnityData(file_extension=".csv")
trainingDataPath = "tempTestData"


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
featureDataset = pd.concat(finalFiles, ignore_index=True)
le = LabelEncoder()
featureDataset["GoalGesture"] = le.fit_transform(featureDataset["GoalGesture"])
print(le.classes_)
featureDataset = featureDataset.apply(pd.to_numeric)
featureDataset[["activeCubeX", "activeCubeY"]] = featureDataset[["activeCubeX", "activeCubeY"]].round(3)
finalDataset = featureSelection.calculateDeltaFeatures(featureDataset)
print("calculated delta values")

filePath, participantNr = fileManagement.createParticipantFolder("TestData")

featureDataset.to_csv(f"{filePath}/TrainingSet_{participantNr}.csv", index=False)
#finalDataset.to_csv("TestData/Participant c/TrainingSetWdeltas_C.csv", index=False)
print("Training dataset created")

models = {
    "SGD": SGDClassifier(random_state=42, alpha=0.0001, eta0=0.001, learning_rate='optimal',
                          loss='hinge', max_iter=1000, penalty='l2', tol=0.0001, n_jobs=-1),

    "random_forest": RandomForestClassifier(
                                            n_estimators=100,
                                            max_depth=6,
                                            min_samples_split=10,
                                            min_samples_leaf=5),

    "lda": LinearDiscriminantAnalysis(
        solver='lsqr',       # Use least squares solution, suitable for large datasets
        shrinkage='auto',    # Apply automatic shrinkage, which helps with regularization
        priors=None,         # Use uniform class priors (None means it will be inferred from data)
        n_components=None,   # Use all components (None means it will be set to min(n_classes-1, n_features))
        tol=0.0001           # Tolerance for singular matrix handling
    ),

    'SVM': SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)

}

trainingModel = models["random_forest"]

if trainingModel == models["SGD"] or trainingModel == models["SVM"]:
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    finalDataset = dataPreProcessing.standardizeDataframe(finalDataset, excludeColumns)

# Train model on dataframe
MLTraining.trainModel(finalDataset, trainingModel, filePath)
#NNTraining.trainNN(finalDataset)


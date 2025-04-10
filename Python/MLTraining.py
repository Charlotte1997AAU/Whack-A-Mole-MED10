from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import dataPreProcessing
import pandas as pd
import joblib
from sklearn.model_selection import learning_curve

def trainModel(data):
    # Load the dataset
    df = data

    # Preprocess the data (standardization)
    excludeColumns = ["EMG1Slope", "EMG2Slope", "EMG3Slope", "EMG4Slope", "EMG5Slope", "EMG6Slope",
                      "EMG7Slope", "EMG8Slope", "activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    dfNormalized = dataPreProcessing.standardizeDataframe(df, excludeColumns)

    dfTrain, dfTest = train_test_split(dfNormalized, test_size=0.2, random_state=42, stratify=dfNormalized["GoalGesture"])

    dfTest.to_csv("test Data set/testSet_L.csv", index=False)
    dfNormalized = dfTrain

    X = dfNormalized.drop(columns=excludeColumns)  # Features
    y = dfNormalized['GoalGesture']  # Target

    # Split the dataset into training and testing (with stratification for balanced classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Initialize the GridSearchCV object
    model = SGDClassifier(random_state=42, alpha=0.0001, eta0=0.001, learning_rate='optimal',
                          loss='hinge', max_iter=1000, penalty='l2', tol=0.0001, n_jobs=-1)

    # Fit the model with GridSearchCV
    model.fit(X_train, y_train)

    # Evaluate the best model on the test set
    y_pred_best = model.predict(X_test)

    # Calculate accuracy and print confusion matrix for the best model
    accuracy_best = accuracy_score(y_test, y_pred_best)
    cm = confusion_matrix(y_test, y_pred_best)
    print(f"Best Model Accuracy: {accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best))

    joblib.dump(model, "SGD_model_L.pkl")
    print("Trained and saved model")

"""
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0], cv=5
)

plt.plot(train_sizes, val_scores.mean(axis=1))
plt.title("Learning Curve")
plt.xlabel("Training set size")
plt.ylabel("Validation Accuracy")
#plt.savefig(f"Images/learning_curve_SGD.png", dpi=300, bbox_inches="tight")
plt.show()
"""


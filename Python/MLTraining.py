from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import dataPreProcessing
import pandas as pd
import joblib
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

def trainModel(data):
    # Load the dataset
    df = data

    # Preprocess the data (standardization)
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    dfNormalized = dataPreProcessing.standardizeDataframe(df, excludeColumns)

    dfTrain, dfTest = train_test_split(dfNormalized, test_size=0.2, random_state=42, stratify=dfNormalized["GoalGesture"])

    dfTest.to_csv("test Data set/testSet_L.csv", index=False)
    dfNormalized = dfTrain

    X = dfNormalized.drop(columns=excludeColumns)  # Features
    y = dfNormalized['GoalGesture']  # Target

    # Split the dataset into training and testing (with stratification for balanced classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Initialize the GridSearchCV object
    SGDC = SGDClassifier(random_state=42, alpha=0.0001, eta0=0.001, learning_rate='optimal',
                          loss='hinge', max_iter=1000, penalty='l2', tol=0.0001, n_jobs=-1)

    random_forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=10, min_samples_split=2)

    random_forest.fit(X_train, y_train)
    SGDC.fit(X_train, y_train)

    # Evaluate the best model on the test set
    y_pred_best_random = random_forest.predict(X_test)
    y_pred_best_SGDC = SGDC.predict(X_test)

    # Calculate accuracy and print confusion matrix for the best model
    random_forest_accuracy_best = accuracy_score(y_test, y_pred_best_random)
    random_forest_cm = confusion_matrix(y_test, y_pred_best_random)
    print(f"RandomForest: {random_forest_accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(random_forest_cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best_random))

    SGDC_accuracy_best = accuracy_score(y_test, y_pred_best_SGDC)
    SGDC_cm = confusion_matrix(y_test, y_pred_best_SGDC)
    print(f"SGDC: {SGDC_accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(SGDC_cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best_SGDC))

    joblib.dump(SGDC, "SGD_model_L.pkl")
    joblib.dump(random_forest, "random_forest_L.pkl")
    print("Trained and saved model")

    """
    train_sizes, train_scores, val_scores = learning_curve(
        random_forest, X, y, train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0], cv=5
    )

    # Plotting the learning curve
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, val_scores.mean(axis=1), label='Validation Accuracy', color='blue', marker='o')
    plt.plot(train_sizes, train_scores.mean(axis=1), label='Training Accuracy', color='green', marker='x')

    plt.title("Learning Curve for RandomForest Model")
    plt.xlabel("Training Set Size")
    plt.ylabel("Accuracy")
    plt.legend(loc='best')

    plt.show()
    """
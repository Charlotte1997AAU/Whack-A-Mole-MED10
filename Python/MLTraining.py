from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import dataPreProcessing
import joblib


def trainModel(data, model):
    # Load the dataset
    df = data
    model_name = type(model).__name__

    # Preprocess the data (standardization)
    excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
    dfNormalized = dataPreProcessing.standardizeDataframe(df, excludeColumns)

    X = dfNormalized.drop(columns=excludeColumns)  # Features
    y = dfNormalized['GoalGesture']  # Target

    # Split the dataset into training and testing (with stratification for balanced classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model.fit(X_train, y_train)

    # Evaluate the best model on the test set
    y_pred_best_model = model.predict(X_test)

    # Calculate accuracy and print confusion matrix for the best model
    model_accuracy_best = accuracy_score(y_test, y_pred_best_model)
    model_cm = confusion_matrix(y_test, y_pred_best_model)
    print(f"Best accuracy for {model_name}: {model_accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(model_cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best_model))

    joblib.dump(model, f"{model_name}_L.pkl")
    print(f"Trained and saved {model_name}")

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

def trainPCA(data, model):
    # Load the dataset
    df = data
    model_name = type(model).__name__


    X = df.drop(columns=['GoalGesture'])  # Features
    y = df['GoalGesture']  # Target

    # Split the dataset into training and testing (with stratification for balanced classes)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model.fit(X_train, y_train)

    # Evaluate the best model on the test set
    y_pred_best_model = model.predict(X_test)

    # Calculate accuracy and print confusion matrix for the best model
    model_accuracy_best = accuracy_score(y_test, y_pred_best_model)
    model_cm = confusion_matrix(y_test, y_pred_best_model)
    print(f"Best accuracy for {model_name}: {model_accuracy_best:.2f}")
    print("Confusion Matrix for Best Model:")
    print(model_cm)
    print("Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best_model))

    joblib.dump(model, f"{model_name}PCA_L.pkl")
    print(f"Trained and saved {model_name}")
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV #stratified split, so that we split all gestures equally
import pandas as pd
import dataPreProcessing
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
from sklearn.preprocessing import StandardScaler
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import to_onnx
import onnxruntime as rt
import numpy as np

# Load the dataset
df = pd.read_csv("test Data set/testData_L.csv")

# Preprocess the data (standardization)
excludeColumns = ["activeCube","activeCubeX","activeCubeY","trackerX","trackerY","trackerZ","GoalGesture"]
dfNormalized = dataPreProcessing.standardizeDataframe(df, excludeColumns)

dfTrain, dfTest = train_test_split(dfNormalized, test_size=0.2, random_state=42, stratify=dfNormalized["GoalGesture"])
# Select features and target

dfTest.to_csv("test Data set/testSet_L.csv", index=False)
dfNormalized = dfTrain

X = dfNormalized.drop(columns=['GoalGesture'])  # Features
X = X.astype(np.float32)
y = dfNormalized['GoalGesture']  # Target

# Split the dataset into training and testing (with stratification for balanced classes)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ---- Hyperparameter Tuning with GridSearchCV ----


# Define the parameter grid for tuning
param_grid = {
    'loss': ['hinge', 'log'],  # Most common: hinge for SVM, log for logistic regression
    'penalty': ['l2', 'l1'],  # Regularization: l2 for Ridge, l1 for Lasso
    'alpha': [0.0001, 0.001, 0.01],  # Regularization strength
    'max_iter': [100, 200, 500],  # Number of iterations (epochs)
    'tol': [1e-4, 1e-3],  # Tolerance for stopping criterion
    'learning_rate': ['constant', 'optimal'],  # Learning rate schedule
    'eta0': [0.001, 0.01],  # Initial learning rate for constant/optimal
}

# Initialize the GridSearchCV object
grid_search = GridSearchCV(SGDClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)

# Fit the model with GridSearchCV
grid_search.fit(X_train, y_train)

# Best parameters found by GridSearchCV
print(f"Best parameters: {grid_search.best_params_}")

# Best model after tuning
best_model = grid_search.best_estimator_

initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]

# Convert to ONNX with the correct input type
onnxModel = to_onnx(best_model, X[:1], initial_types=initial_type)
with open("SGD_Model.onnx", "wb") as f:
    f.write(onnxModel.SerializeToString())

sess = rt.InferenceSession("SGD_Model.onnx", providers=["CPUExecutionProvider"])
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

# Ensure X_test is of the right type (float32 numpy array)
onnx_pred = sess.run([label_name], {input_name: X_test.to_numpy().astype(np.float32)})[0]


# Evaluate the best model on the test set
y_pred_best = best_model.predict(X_test)

# Calculate accuracy and print confusion matrix for the best model
accuracy_best = accuracy_score(y_test, y_pred_best)
print(f"Best Model Accuracy: {accuracy_best:.2f}")
print("Confusion Matrix for Best Model:")
print(confusion_matrix(y_test, y_pred_best))
print("Classification Report for Best Model:")
print(classification_report(y_test, y_pred_best))

joblib.dump(best_model, "SGD_model_L.pkl")
print("Saved model to tha pickle jar")

"""
# Load the dataset
df = pd.read_csv("test Data set/testData_L.csv")

# Exclude non-feature columns (keeping only gesture features)
excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "trackerX", "trackerY", "trackerZ", "GoalGesture"]
feature_columns = [col for col in df.columns if col not in excludeColumns]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[feature_columns])

# Reduce features to 3D using PCA
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

# Convert to DataFrame
df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2", "PC3"])
df_pca["GoalGesture"] = df["GoalGesture"]  # Add target labels back

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df_pca.drop(columns=["GoalGesture"]),
    df_pca["GoalGesture"],
    test_size=0.2,
    random_state=42,
    stratify=df_pca["GoalGesture"]
)

# ---- Hyperparameter Tuning with GridSearchCV ----
param_grid = {
    'loss': ['hinge', 'log'],
    'penalty': ['l2', 'l1'],
    'alpha': [0.0001, 0.001, 0.01],
    'max_iter': [100, 200, 500],
    'tol': [1e-4, 1e-3],
    'learning_rate': ['constant', 'optimal'],
    'eta0': [0.001, 0.01],
}

# Initialize GridSearchCV with SGDClassifier
grid_search = GridSearchCV(SGDClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)

# Train the best model
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Evaluate on test data
y_pred_best = best_model.predict(X_test)
accuracy_best = accuracy_score(y_test, y_pred_best)

print(f"Best Model Accuracy: {accuracy_best:.2f}")
print("Confusion Matrix for Best Model:")
print(confusion_matrix(y_test, y_pred_best))
print("Classification Report for Best Model:")
print(classification_report(y_test, y_pred_best))

# Save the model
joblib.dump(best_model, "SGD_model_L.pkl")
print("Saved model to tha pickle jar")

# ---- Convert to a Point Cloud and Visualize ----
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(X_pca)  # Use PCA-reduced data

# Save the point cloud (optional)
o3d.io.write_point_cloud("gesture_point_cloud.ply", point_cloud)

# Visualize the point cloud
o3d.visualization.draw_geometries([point_cloud])
"""
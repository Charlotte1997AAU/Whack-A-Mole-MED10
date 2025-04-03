from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split #stratified split, so that we split all gestures equally
import pandas as pd
import dataPreProcessing
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("test Data set/testData_L.csv")

dfNormalized = dataPreProcessing.normalizeDataframe(df, ["activeCube","activeCubeX","activeCubeY","trackerX","trackerY","trackerZ","GoalGesture"])



X = dfNormalized.drop(columns=['GoalGesture'])  # Drop the target column from the features
y = dfNormalized['GoalGesture']  # Select the target column

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize the model
model = LinearRegression()

# Fit the model with training data
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Calculate R-squared (R²)
r2 = r2_score(y_test, y_pred)
print(f"R-squared: {r2}")
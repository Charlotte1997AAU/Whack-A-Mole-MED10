# Requirements: pip install websockets numpy

import joblib
import asyncio
from sklearn.svm import SVC
import websockets
import numpy as np
import pandas as pd
import dataPreProcessing
import featureSelection
from sklearn.preprocessing import StandardScaler
from scipy.special import softmax

participantNr = 18

WINDOW_SIZE = 40
NUM_CHANNELS = 11
loaded_model = joblib.load(f'TestData/Participant {participantNr}/RandomForestClassifier.pkl')
model_name = type(loaded_model).__name__
scaler = StandardScaler()
testSet = pd.read_csv(f"TestData/participant {participantNr}/TrainingSet_{participantNr}.csv")
excludeColumns = ["activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]
results_list = []

X = testSet.drop(columns=excludeColumns)
scaler.fit(X)  # Fit the scaler directly on the DataFrame

def modelPredict(emg_window):
    # Transpose the window data to fit the expected format
    emg_array_transposed = emg_window.T

    # Convert the array into a DataFrame with proper column names
    df = pd.DataFrame(emg_array_transposed, columns=['TrackerX', 'TrackerY', 'TrackerZ', 'EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])

    # Call the feature extraction function on the current window of data
    dfCalculated = featureSelection.createDataFrameWithCalculationsTest(df)

    # Normalize the features using the pre-trained scaler
    dfNormalized = scaler.transform(dfCalculated)
    dfNormalized = pd.DataFrame(dfNormalized, columns=dfCalculated.columns)
    dfWithDeltas = featureSelection.calculateDeltaFeatures(dfNormalized)

    # Make predictions using the pre-trained model
    predictions = loaded_model.predict(dfWithDeltas)
    
    if model_name == "SGDClassifier":
        # Get confidence scores and compute probability using softmax
        confidence_scores = loaded_model.decision_function(dfWithDeltas)
        probability = softmax(confidence_scores[0])
        predicted_class = predictions[0]
        class_index = list(loaded_model.classes_).index(predicted_class)
        confidence = round(probability[class_index], 3)

    if model_name == "RandomForestClassifier" or model_name == "SVC":
        # Get the probabilities for each class
        probabilities = loaded_model.predict_proba(dfWithDeltas)
        
        # Get the predicted class
        predicted_class = predictions[0]
        
        # Find the index of the predicted class in the model's class list
        class_index = list(loaded_model.classes_).index(predicted_class)
        
        # Get the confidence score (probability of the predicted class)
        confidence = round(probabilities[0][class_index], 3)

    return predictions, confidence


async def handler(websocket):
    print("Unity client connected.")
    async for message in websocket:
        try:
            # Convert flat string → float list
            values = list(map(float, message.strip().split(',')))
            expected_values = WINDOW_SIZE * NUM_CHANNELS
            if len(values) != expected_values:
                await websocket.send("error: invalid window size")
                print(f"Received {len(values)} values, expected {expected_values}")
                continue

            # Reshape to 2D list: (NUM_CHANNELS, WINDOW_SIZE)
            emg_window = np.array(values).reshape((NUM_CHANNELS, WINDOW_SIZE))

            prediction, confidence = modelPredict(emg_window)
            await websocket.send(f"{prediction[0]},{confidence}")
            print(f"{prediction[0]},{confidence}")
            results_list.append({
            'prediction': prediction[0],
            'confidence': confidence
            })

        except Exception as e:
            error_msg = f"error: {str(e)}"
            print(error_msg)
            await websocket.send(error_msg)

        #finally:
            # Client disconnected - save the results to a CSV
         #   if results_list:
         #       df_results = pd.DataFrame(results_list)
         #       df_results.to_csv("prediction_results.csv", index=False)
         #       print("Saved predictions to prediction_results.csv")
         #   else:
         #       print("No results to save.")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

# Requirements: pip install websockets numpy

import joblib
import asyncio
import websockets
import numpy as np
import pandas as pd
import dataPreProcessing
import featureSelection
from sklearn.preprocessing import StandardScaler

WINDOW_SIZE = 40
NUM_CHANNELS = 11
loaded_model = joblib.load('SGD_model_L.pkl')
scaler = StandardScaler()
testSet = pd.read_csv("test Data set/testData_L.csv")
excludeColumns = ["EMG1Slope", "EMG2Slope", "EMG3Slope", "EMG4Slope", "EMG5Slope", "EMG6Slope",
                  "EMG7Slope", "EMG8Slope", "activeCube", "activeCubeX", "activeCubeY", "GoalGesture"]

X = testSet.drop(columns=excludeColumns)
scaler.fit(X)  # Fit the scaler directly on the DataFrame

def modelPredict(emg_window):
    emg_array_transposed = emg_window.T
    df = pd.DataFrame(emg_array_transposed, columns=['TrackerX', 'TrackerY', 'TrackerZ', 'EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])
    dfCalculated = featureSelection.createDataFrameWithCalculationsTest(df)
    dfNormalized = scaler.transform(dfCalculated)
    dfNormalized = pd.DataFrame(dfNormalized, columns=dfCalculated.columns)
    predictions = loaded_model.predict(dfNormalized)
    return predictions

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

            prediction = modelPredict(emg_window)
            await websocket.send(str(prediction[0]))
        except Exception as e:
            error_msg = f"error: {str(e)}"
            print(error_msg)
            await websocket.send(error_msg)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

# Requirements: pip install websockets numpy

import joblib
import asyncio
import websockets
import numpy as np
import pandas as pd
import dataPreProcessing
import featureSelection

WINDOW_SIZE = 40
NUM_CHANNELS = 11
loaded_model = joblib.load('SGD_model_L.pkl')

# Dummy prediction logic
def modelPredict(emg_window):
    # emg_window shape: (NUM_CHANNELS, WINDOW_SIZE)
    emg_array_transposed = emg_window.T
    df = pd.DataFrame(emg_array_transposed, columns=[
    'TrackerX', 'TrackerY', 'TrackerZ', 'EMG1', 'EMG2', 'EMG3', 'EMG4', 'EMG5', 'EMG6', 'EMG7', 'EMG8'])
    df = featureSelection.createDataFrameWithCalculationsTest(df)
    dfNormalized = dataPreProcessing.standardizeDataframe(df)
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

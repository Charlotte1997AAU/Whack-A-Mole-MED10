# Requirements: pip install websockets numpy

import asyncio
import websockets
import numpy as np
import pandas as pd

WINDOW_SIZE = 40
NUM_CHANNELS = 8
columns = ["EMG1", "EMG2", "EMG3", "EMG4", "EMG5", "EMG6", "EMG7", "EMG8"]

# Dummy prediction logic
def modelPredict(emg_window):
    # emg_window shape: (NUM_CHANNELS, WINDOW_SIZE)
    emg_array = np.array(emg_window)
    emg_array = pd.DataFrame({'EMG1': emg_array[:, 0], 'EMG2': emg_array[:, 1], 'EMG3': emg_array[:, 2], 'EMG4': emg_array[:, 3],
                              'EMG5': emg_array[:, 4], 'EMG6': emg_array[:, 5], 'EMG7': emg_array[:, 6], 'EMG8': emg_array[:, 7]})
    print(emg_array.head())

    return emg_array

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
            await websocket.send(prediction)
        except Exception as e:
            error_msg = f"error: {str(e)}"
            print("oh noo", error_msg)
            await websocket.send(error_msg)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

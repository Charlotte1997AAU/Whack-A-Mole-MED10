# Requirements: pip install websockets

import asyncio
import websockets
import numpy as np

WINDOW_SIZE = 40
NUM_CHANNELS = 8

# Dummy model: if average EMG > 0.1 → "fist", else "relax"
def mock_predict(emg_window):
    emg_array = np.array(emg_window).reshape((1, WINDOW_SIZE * NUM_CHANNELS))
    return "fist" if np.mean(emg_array) > 0.1 else "relax"

async def handler(websocket):
    print("Client connected")
    async for message in websocket:
        try:
            values = list(map(float, message.strip().split(',')))
            if len(values) != WINDOW_SIZE * NUM_CHANNELS:
                await websocket.send("error: invalid window size")
                continue
            prediction = mock_predict(values)
            await websocket.send(prediction)
        except Exception as e:
            await websocket.send(f"error: {str(e)}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

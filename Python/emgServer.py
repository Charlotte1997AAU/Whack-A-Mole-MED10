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
"""
using NativeWebSocket;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

public class EMGStreamer : MonoBehaviour
{
    WebSocket websocket;

    // EMG buffer
    List<float[]> slidingWindow = new List<float[]>();
    const int windowSize = 40;
    const int overlap = 20;
    const int numChannels = 8;

    async void Start()
    {
        websocket = new WebSocket("ws://localhost:8765");

        websocket.OnOpen += () =>
        {
            Debug.Log("✅ Connected to Python WebSocket server");
        };

        websocket.OnError += (e) =>
        {
            Debug.LogError("❌ WebSocket Error: " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("🔌 WebSocket closed");
        };

        websocket.OnMessage += (bytes) =>
        {
            string prediction = Encoding.UTF8.GetString(bytes);
            Debug.Log("🧠 Prediction: " + prediction);

            // TODO: Handle gesture actions here (e.g. grab, punch)
        };

        await websocket.Connect();
    }

    void Update()
    {
        // Simulate one EMG sample per frame (at ~200Hz)
        float[] emgSample = GenerateFakeEMG();
        slidingWindow.Add(emgSample);

        if (slidingWindow.Count >= windowSize)
        {
            string message = FlattenWindow(slidingWindow);
            websocket.SendText(message);

            // Slide the window by `overlap`
            slidingWindow.RemoveRange(0, overlap);
        }

        // Required to handle WebSocket events on main thread
        websocket.DispatchMessageQueue();
    }

    float[] GenerateFakeEMG()
    {
        float[] sample = new float[numChannels];
        for (int i = 0; i < numChannels; i++)
        {
            sample[i] = Random.Range(0f, 0.2f); // Simulate muscle signal
        }
        return sample;
    }

    string FlattenWindow(List<float[]> window)
    {
        List<string> flat = new List<string>();
        foreach (var row in window)
        {
            foreach (var val in row)
            {
                flat.Add(val.ToString("F4"));
            }
        }
        return string.Join(",", flat);
    }

    private async void OnApplicationQuit()
    {
        await websocket.Close();
    }
}

"""
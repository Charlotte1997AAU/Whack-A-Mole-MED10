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
using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;
using System.Text;

public class EMGStreamer : MonoBehaviour
{
    private WebSocket ws;

    private List<float[]> slidingWindow = new List<float[]>();
    private const int windowSize = 40;
    private const int overlap = 20;
    private const int numChannels = 8;

    void Start()
    {
        ws = new WebSocket("ws://localhost:8765");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("Connected to Python WebSocket server");
        };

        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("🧠 Prediction: " + e.Data);

            // TODO: Handle prediction actions here
        };

        ws.OnError += (sender, e) =>
        {
            Debug.LogError("❌ WebSocket Error: " + e.Message);
        };

        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket closed");
        };

        ws.Connect();
    }

    void Update()
    {
        float[] emgSample = GenerateFakeEMG();
        slidingWindow.Add(emgSample);

        if (slidingWindow.Count >= windowSize)
        {
            string message = FlattenWindow(slidingWindow);
            ws.Send(message);

            // Slide window
            slidingWindow.RemoveRange(0, overlap);
        }
    }

    float[] GenerateFakeEMG()
    {
        float[] sample = new float[numChannels];
        for (int i = 0; i < numChannels; i++)
        {
            sample[i] = Random.Range(0f, 0.2f);
        }
        return sample;
    }

    string FlattenWindow(List<float[]> window)
    {
        StringBuilder builder = new StringBuilder();
        foreach (var row in window)
        {
            foreach (var val in row)
            {
                builder.AppendFormat("{0:F4},", val);
            }
        }
        if (builder.Length > 0)
        {
            builder.Length--; // remove last comma
        }
        return builder.ToString();
    }

    void OnApplicationQuit()
    {
        if (ws != null && ws.IsAlive)
        {
            ws.Close();
        }
    }
}


"""
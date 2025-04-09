using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;
using System.Text;
using System;

public class webSocket : MonoBehaviour
{
    private WebSocket ws;

    private Dictionary<string, List<float>> slidingWindow = new Dictionary<string, List<float>>();  // Store sliding window for each channel
    private const int windowSize = 40;  // Number of EMG samples for each window
    private const int overlap = 20;    // Overlap between windows (40 samples with 20 overlap)
    private const int numChannels = 11; // Number of EMG channels
    private GameObject tracker;
    private Vector3 trackerPos; // Position of tracker

    private Dictionary<string, object> emgDataForSocket = new Dictionary<string, object>();
    private Dictionary<int, string> gestureNames = new Dictionary<int, string>()
    {
        { 0, "Extension" },
        { 1, "Fist" },
        { 2, "Flexion" },
        { 3, "Pinch" },
        { 4, "Pronation" },
        { 5, "Supination" }
    };

    void Start()
    {
        tracker = GameObject.Find("Tracker");
        ws = new WebSocket("ws://localhost:8765");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("Connected to Python WebSocket server");
        };

        ws.OnMessage += (sender, e) =>
        {
            // Try to parse the e.Data as an integer (which is the key)
            if (int.TryParse(e.Data, out int gestureKey))
            {
                // Check if the key exists in the dictionary
                if (gestureNames.ContainsKey(gestureKey))
                {
                    // Log the corresponding gesture name
                    Debug.Log("Gesture: " + gestureNames[gestureKey]);
                }
                else
                {
                    // Handle case where the key doesn't exist in the dictionary
                    Debug.LogWarning("Invalid gesture key received: " + gestureKey);
                }
            }
            else
            {
                // Handle case where e.Data is not a valid integer
                Debug.LogWarning("Invalid prediction data: " + e.Data);
            }
        };

        ws.OnError += (sender, e) =>
        {
            Debug.LogError("WebSocket Error: " + e.Message);
        };

        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket closed");
        };

        ws.Connect();
    }

    void Update()
    {
        trackerPos = tracker.transform.position;
        emgDataForSocket["trackerX"] = trackerPos.x;
        emgDataForSocket["trackerY"] = trackerPos.y;
        emgDataForSocket["trackerZ"] = trackerPos.z;

        // Update sliding window with new data for each channel
        foreach (var entry in emgDataForSocket)
        {
            string channelKey = entry.Key;

            // Ensure there's a list for this channel in the sliding window
            if (!slidingWindow.ContainsKey(channelKey))
            {
                slidingWindow[channelKey] = new List<float>();
            }

            // Add new data to the channel's list
            slidingWindow[channelKey].Add(Convert.ToSingle(entry.Value));

        }

        bool sendMessage = true;

        List<string> keys = new List<string>(slidingWindow.Keys);

        foreach (var channelKey in keys)
        {
            if(slidingWindow[channelKey].Count > windowSize)
            {
                slidingWindow[channelKey].RemoveRange(windowSize, slidingWindow[channelKey].Count - windowSize);
            }

            if (slidingWindow[channelKey].Count < windowSize)
            {
                sendMessage = false;
                break;
            }
        }

        // If the sliding window has reached the window size, send data and slide
        if (sendMessage)
        {
            string message = FlattenWindow(slidingWindow);
            ws.Send(message);

            // Slide window: Remove overlap number of elements from each channel's list
            foreach (var channelKey in slidingWindow.Keys)
            {
                slidingWindow[channelKey].RemoveRange(0, overlap);
            }
        }
    }

    public void GetEmgData(Dictionary<string, object> emgData)
    {
        foreach (var entry in emgData)
        {
            if(entry.Value == null)
            {
                Debug.Log("Empty value");
                return;
            }
            else
            {
                emgDataForSocket[entry.Key] = entry.Value;
            }
        }
    }

    string FlattenWindow(Dictionary<string, List<float>> window)
    {
        StringBuilder builder = new StringBuilder();
        foreach (var channel in window)
        {
            foreach (var val in channel.Value)
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

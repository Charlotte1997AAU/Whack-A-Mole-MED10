using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;
using System.Text;
using System;
using System.Linq;

public class webSocket : MonoBehaviour
{
    private WebSocket ws;

    private Dictionary<string, List<float>> slidingWindow = new Dictionary<string, List<float>>();  // Store sliding window for each channel
    private const int windowSize = 40;  // Number of EMG samples for each window
    private const int overlap = 20;    // Overlap between windows (40 samples with 20 overlap)
    private const int numChannels = 11; // Number of EMG channels
    private GameObject tracker;
    private GameObject hannesHand;
    private Vector3 trackerPos; // Position of tracker
    public int currentGestureKey;
    public bool thresholdsCalculated = false;
    public bool isCalibrating = false;
    private bool handAnimEnabled = true;
    private CalibrationGhostHand calibrationGhostHand;

    private Dictionary<string, object> emgDataForSocket = new Dictionary<string, object>();
    public Dictionary<int, string> gestureNames = new Dictionary<int, string>()
    {
        { 0, "extension" },
        { 1, "fist" },
        { 2, "flexion" },
        { 3, "pinch" },
        { 4, "rest" }
    };

    List<(int predictedClass, float confidenceProb)> predictions = new List<(int, float)>();
    Dictionary<int, float> classAverageConfidence = new Dictionary<int, float>();

    void Start()
    {
        hannesHand = GameObject.Find("Hannes_Hand");
        tracker = GameObject.Find("Tracker");
        calibrationGhostHand = FindObjectOfType<CalibrationGhostHand>();

        ws = new WebSocket("ws://localhost:8765");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("Connected to Python WebSocket server");
        };

        ws.OnMessage += (sender, e) =>
        {
            try
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    string[] stringParts = e.Data.Split(",");

                    if (stringParts.Length < 2)
                    {
                        Debug.LogWarning("Invalid data format received: " + e.Data);
                        return;
                    }

                    if (!int.TryParse(stringParts[0], out int predictedClass))
                    {
                        Debug.LogWarning("Could not parse predicted class: " + stringParts[0]);
                        return;
                    }

                    if (!float.TryParse(stringParts[1], out float confidenceProb))
                    {
                        Debug.LogWarning("Could not parse confidence: " + stringParts[1]);
                        return;
                    }

                    if (!gestureNames.ContainsKey(predictedClass))
                    {
                        Debug.LogWarning("Invalid gesture class: " + predictedClass);
                        return;
                    }

                    if (float.IsNaN(confidenceProb) || float.IsInfinity(confidenceProb))
                    {
                        Debug.LogWarning("Invalid confidence value: " + confidenceProb);
                        return;
                    }

                    if (thresholdsCalculated)
                    {
                        if (classAverageConfidence.TryGetValue(predictedClass, out float minProb))
                        {
                            if (confidenceProb > minProb)
                            {
                                currentGestureKey = predictedClass;
                            }
                        }
                    }
                    else
                    {
                        predictions.Add((predictedClass, confidenceProb));
                    }
                }
                else
                {
                    Debug.LogWarning("Empty message received from WebSocket.");
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("Exception in ws.OnMessage: " + ex.Message + "\nStackTrace:\n" + ex.StackTrace);
            }
        };


        ws.OnError += (sender, e) =>
        {
            Debug.Log("WebSocket Error: " + e.Message);
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

        if (Input.GetKeyDown(KeyCode.C))
        {
            StartCoroutine(calibrationGhostHand.PlayAnimations());
            predictions.Clear();
            Debug.Log("Cleared predictions list, ready to collect ");
        }

        if (Input.GetKeyDown(KeyCode.B) && !thresholdsCalculated)
        {
            CalculateAverages();
            Debug.Log("Thresholds calculated and stored.");
            thresholdsCalculated = true;
            handAnimEnabled = false;
        }
        if (!handAnimEnabled)
        {
            hannesHand.GetComponent<TestModelAnimations>().enabled = true;
            Debug.Log("Hand animations enabled");
            handAnimEnabled = true;
        }

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

    public void CalculateAverages()
    {
        classAverageConfidence = predictions
            .GroupBy(p => p.predictedClass)
            .ToDictionary(
                g => g.Key,
                g => {
                    var values = g.Select(p => p.confidenceProb).ToList();
                    float mean = values.Average();
                    return mean;
                }
            );
    }

    public void CheckAndUpdateGestureKey(int predictedClass, float confidenceProb)
    {
        if (classAverageConfidence.TryGetValue(predictedClass, out float minProb))
        {
            if (confidenceProb > minProb)
            {
                currentGestureKey = predictedClass;
            }
        }
        else
        {
            Debug.LogWarning($"No threshold found for class {predictedClass}. Confidence: {confidenceProb:F3}");
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

using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;
using System.Text;

public class webSocketTest : MonoBehaviour
{
    private WebSocket ws;

    private List<float[]> slidingWindow = new List<float[]>();
    private const int windowSize = 40;
    private const int overlap = 20;
    private const int numChannels = 8;

    private Dictionary<string, object> emgDataForSocket = new Dictionary<string, object>();

    void Start()
    {
        ws = new WebSocket("ws://localhost:8765");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("Connected to Python WebSocket server");
        };

        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("Prediction: " + e.Data);

            // TODO: Handle prediction actions here
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
        if (emgDataForSocket.Count >= windowSize)
        {
            string message = FlattenWindow(slidingWindow);
            ws.Send(message);

            // Slide window
            slidingWindow.RemoveRange(0, overlap);
        }
    }


    public void GetEmgData(Dictionary<string, object> emgData)
    {
        foreach(var entry in emgData)
        {
            emgDataForSocket[entry.Key] = entry.Value;
        }
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

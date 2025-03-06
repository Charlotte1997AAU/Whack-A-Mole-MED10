using System.Collections.Concurrent;
using System.IO;
using UnityEngine;
using System;

public class HardwareDataLogger : MonoBehaviour
{
    private string filePath;
    private StreamWriter writer;
    private ConcurrentQueue<string> dataQueue = new ConcurrentQueue<string>();
    private bool isWriting = false;

    void Start()
    {
        // File path setup
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Logs");
        Directory.CreateDirectory(directoryPath);
        filePath = GetUniqueFilePath(directoryPath, "EMG_log", "csv");

        // Open the file for writing
        writer = new StreamWriter(filePath, append: true);

        // Write the header row once
        writer.WriteLine("EMG1,EMG2,EMG3,EMG4,EMG5,EMG6,EMG7,EMG8,Timestamp,FrameCount");
        writer.Flush();

        Debug.Log("CSV Created: " + filePath);
    }

    void Update()
    {
        // Write queued data in Update to avoid thread issues
        WriteQueuedData();
    }

    public void LogEMGData(float timestamp, int[] emgData)
    {
        if (emgData == null || emgData.Length != 8)
        {
            Debug.LogError("Invalid EMG data received.");
            return;
        }
        // Convert data to CSV format
        string row = $"{emgData[0]},{emgData[1]},{emgData[2]},{emgData[3]},{emgData[4]},{emgData[5]},{emgData[6]},{emgData[7]},{timestamp},{Time.frameCount}";
        //Debug.Log(row);

        // Enqueue data for writing
        dataQueue.Enqueue(row);
    }

    private void WriteQueuedData()
    {
        if (!isWriting && dataQueue.TryDequeue(out string row))
        {
            isWriting = true;
            writer.WriteLine(row);
            writer.Flush(); // Ensure immediate writing
            isWriting = false;
        }
    }

    // Utility function to create unique log files
    private string GetUniqueFilePath(string directory, string baseFileName, string extension)
    {
        int counter = 1;
        string filePath;

        do
        {
            string numberedFileName = $"{baseFileName}_{counter:D2}.{extension}";
            filePath = Path.Combine(directory, numberedFileName);
            counter++;
        }
        while (File.Exists(filePath));

        return filePath;
    }

    void OnApplicationQuit()
    {
        writer?.Close();
    }
}

using System.IO;
using System.Threading;
using UnityEngine;

public class ReadRawMyo : MonoBehaviour
{
    private Thread csvThread;
    private bool isWriting = false;
    private string filePath;

    // Reference to the EmgDataCollector script to access the shared queue
    public ThalmicMyo emgDataCollector;
    private int frameCounter = 0; // Counter for frames

    void Start()
    {
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Logs");

        // Ensure the directory exists
        Directory.CreateDirectory(directoryPath);

        // Generate a unique file name
        filePath = GetUniqueFilePath(directoryPath, "EMG_log", "csv");

        File.WriteAllText(filePath, "EMG1, EMG2, EMG3, EMG4, EMG5, EMG6, EMG7, EMG8, Counter\n");

        if (emgDataCollector != null)
        {
            StartCsvThread();
        }
    }

    private void Update()
    {
        Debug.Log("Running for " + Time.time + "Seconds");
    }

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

    void StartCsvThread()
    {
        isWriting = true;
        csvThread = new Thread(WriteDataToCsv);
        csvThread.IsBackground = true;
        csvThread.Start();
    }

    void WriteDataToCsv()
    {
        while (isWriting)
        {
            frameCounter++;
            int[] dataToWrite = null;

            // Retrieve the latest EMG data from the EmgDataCollector
            if (emgDataCollector.emgBuffer.Count > 0)
            {
                dataToWrite = emgDataCollector.emgBuffer.Peek(); // Peek at the latest EMG data in the buffer
            }
            else
            {
                Debug.Log("Waiting for bufer to fill...");
            }

            // Only write to CSV if data is available
            if (dataToWrite != null)
            {
                // Convert the EMG data array to a CSV-compatible string
                string csvLine = string.Join(",", dataToWrite);

                csvLine += $",{frameCounter}";

                if (dataToWrite.Length != 8)
                {
                    Debug.Log("Waiting for EMG Data...");
                    frameCounter = 0;
                }
                else
                {
                    File.AppendAllText(filePath, csvLine + "\n");
                }
                
            }

            // Sleep for 5ms to maintain the 200Hz writing rate
            Thread.Sleep(5);
        }
    }

    void WriteToCsv(int[] emgData)
    {
        // Convert the EMG data array to a CSV-compatible string
        string csvLine = string.Join(",", emgData);

        csvLine += $",{frameCounter}";

        // Write to CSV (ensure thread-safe file access)
        lock (this)
        {
            if (emgData.Length != 8)
            {
                Debug.Log("Waiting for EMG Data...");
                frameCounter = 0;
                return;
            }
            else
            {
                File.AppendAllText(filePath, csvLine + "\n");
            }
        }
    }

    public void StopWriting()
    {
        isWriting = false;
        if (csvThread != null && csvThread.IsAlive)
        {
            csvThread.Join(); // Ensure the thread finishes before exiting
        }
    }

    private void OnApplicationQuit()
    {
        StopWriting();
    }

}

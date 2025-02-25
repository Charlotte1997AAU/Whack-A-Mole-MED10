using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;

public class Logger : MonoBehaviour
{
    private string filePath;
    private float logInterval = 1f / 200f; // 200Hz = 5ms interval
    private string currentHoveredCube = ""; // To store current hovered cube
    private string currentActivatedCube = ""; // To store current activated cube
    private bool isCubeActivated = false; // To track whether a cube is activated
    private bool readyForGesture = false; // if true then the box is ready for a gesture

    private void Start()
    {
        // Get the directory path
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Logs");

        // Ensure the directory exists
        Directory.CreateDirectory(directoryPath);

        // Generate a unique file name
        filePath = GetUniqueFilePath(directoryPath, "log", "csv");

        // Create the file with headers
        File.WriteAllText(filePath, "Timestamp(ms),Activated, ReadyForGesture\n");
        Debug.Log("CSV File Path: " + filePath);

        // Start logging at 200Hz
        StartCoroutine(LogRoutine());
    }

    public void LogIfGestureReady(bool isReadyForGesture)
    {
        readyForGesture = isReadyForGesture;
    }

    public string LogActivatedCube(string cubeName)
    {
        currentActivatedCube = cubeName; // Store activated cube name
        isCubeActivated = true; // Mark as activated
        return currentActivatedCube;
    }

    public void LogDeactivatedCube()
    {
        currentActivatedCube = ""; // Clear activated cube name
        isCubeActivated = false; // Mark as deactivated
    }

    private IEnumerator LogRoutine()
    {
        while (true)
        {
            string timestamp = (Time.time * 1000f).ToString("F3"); // Time in milliseconds

            // If the cube is activated, continue logging it
            string logEntry = $"{timestamp},{(isCubeActivated ? currentActivatedCube : "")}, {readyForGesture}";

            // Write the log entry to the file
            File.AppendAllLines(filePath, new List<string> { logEntry });

            // Clear the hovered cube after logging it, but keep activated cube for continuous logging
            currentHoveredCube = "";

            yield return new WaitForSeconds(logInterval);
        }
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
}

using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Linq;

public class Logger : MonoBehaviour
{
    private string filePath;
    private float logInterval = 1f / 200f; // 200Hz = 5ms interval
    private string currentActivatedCube = ""; // To store current activated cube
    private string timestamp; // Timestamp with date
    private int IDnumber = 0; // Current number of participant
    private Vector3 cubeCoordinates; // Unity coordinates of current active cube
    private int frameNumber; // Frame number in unity to detect missing frames
    private bool isCubeActivated = false; // To track whether a cube is activated
    private triggerBox triggerBox; // Reference to triggerBox script to access tracker position, gestures completed and current state
    private Hover hover; // Reference to overall numbers and other values 
    private int gesturesCompleted = 0; // Counter for how many times a gesture has been performed sucessfully
    private LoggingManager loggingManager; // Reference to get sessionID


    private Dictionary<int, string> testStates = new Dictionary<int, string>()
    {
        {0, "Resting" },
        {1, "Moving to Box" },
        {2, "In box" },
        {3, "Moving to rest position" },
        {4, "Exited early" },
        {5, "MVC" }
    };

    private Dictionary<int, string> testEvents = new Dictionary<int, string>()
    {
        {0, "" },
        {1, "Successful Gesture" },
    };

    public enum currentGesture { fist, pinch, pronation, supination, flexion, extension, rest }
    [SerializeField] public currentGesture goalGesture; // Which gesture is supposed to be trained in this run


    private List<string> logEntries = new List<string>(); // List to accumulate log entries

    private void Start()
    {
        loggingManager = FindObjectOfType<LoggingManager>();
        triggerBox = FindObjectOfType<triggerBox>();
        hover = FindObjectOfType<Hover>();

        // Start logging at 200Hz
        StartCoroutine(LogRoutine());
    }

    public string LogActivatedCube(string cubeName, Vector3 cubePosition)
    {
        currentActivatedCube = cubeName; // Store activated cube name
        cubeCoordinates = cubePosition; // Store the position of activated cube
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
            timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.ffff"); // Timestamp in real time
            frameNumber = Time.frameCount;
            gesturesCompleted = hover.getGesturesCount();
            string currentState = testStates[hover.getCurrentState()];
            string currentEvent = testEvents[hover.getEvents()];
            int currentAttempts = hover.getAttempts();

            // If the cube is activated, continue logging it
            string logEntry = 
                $"{timestamp};" +
                $"{frameNumber};" +
                $"{(isCubeActivated ? currentActivatedCube : "None")};" +
                $"{(isCubeActivated ? (float?)cubeCoordinates.x : null)};" +
                $"{(isCubeActivated ? (float?)cubeCoordinates.y : null)};" +
                $"{(isCubeActivated ? (float?)cubeCoordinates.z : null)};" +
                $"{triggerBox.trackerPos().x};" +
                $"{triggerBox.trackerPos().y};" +
                $"{triggerBox.trackerPos().z};" +
                $"{goalGesture};" +
                $"{gesturesCompleted};" +
                $"{(isCubeActivated ? (int?)currentAttempts : null)};" +
                $"{currentState};" +
                $"{currentEvent}"
                ;

            // Write the log entry to the file
            logEntries.Add(logEntry);

            yield return new WaitForSeconds(logInterval);
        }
    }

    private void OnApplicationQuit()
    {
        // Get the directory path
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Logs");

        // Ensure the directory exists
        Directory.CreateDirectory(directoryPath);

        // Generate a unique file name
        filePath = GetUniqueFilePath(directoryPath, "Unity_log", "csv");

        string IDstring = loggingManager.sessionID;
        Debug.Log("ID string: " + IDstring);


        // Create the file with headers
        File.WriteAllText(filePath, "ID;Timestamp;FrameNumber;ActivatedCube;ActiveCubeX;ActiveCubeY;ActiveCubeZ;TrackerX;TrackerY;TrackerZ;GoalGesture;GesturesAttempted;AttemptsInCube;State;Event\n");

        var updatedLogEntries = logEntries.Select(entry => IDstring + ";" + entry).ToList();

        File.AppendAllLines(filePath, updatedLogEntries);

        StopCoroutine(LogRoutine());
    }


    private string GetUniqueFilePath(string directory, string baseFileName, string extension)
    {
        string filePath;

        do
        {
            string numberedFileName = $"{baseFileName}_{DateTime.Now:yyyy_MM_dd_HH_mm_ss}_Med10.{extension}";
            filePath = Path.Combine(directory, numberedFileName);
        } 
        while (File.Exists(filePath));

        return filePath;
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;

public class testLogger : MonoBehaviour
{
    private string timestamp;
    private int frameNumber;
    private bool isCubeActivated;
    private int goalGesture;
    private string currentActivatedCube;
    private int prediction;
    private float logInterval = 1f / 50f;
    private string filePath;
    private int participantNr;
    private int boxNumber;
    private bool cubeActivated = false;
    private bool isInside = false;
    private float timeInside = 0f;
    public float requriedTime = 5.0f;
    public bool testing = false;
    public bool testingBoxes = true;

    private MovingTarget movingCube;
    private resetPosition resetScript;
    private GameObject wall;
    private SliderFill sliderFill;
    public Material HighLightColor;
    public Material GestureColor;
    public Material gridColor;
    public Collider activeCubeCollider;
    public GameObject[] cubes;
    public GameObject activeCube;
    public CubeSpawner cubeSpawner;
    private webSocket ws;
    private List<string> logEntries = new List<string>();
    private static List<int> boxes = new List<int>();

    // Start is called before the first frame update
    void Start()
    {
        sliderFill = FindObjectOfType<SliderFill>();
        resetScript = FindObjectOfType<resetPosition>();
        movingCube = FindObjectOfType<MovingTarget>();
        ws = FindObjectOfType<webSocket>();
        wall = GameObject.Find("Wall");
        boxes = GenerateList(0);
        boxes = ShuffleList(boxes);
        cubeSpawner.SpawnCubes();
        cubeSpawner.cubePrefab.SetActive(false);
        cubes = GameObject.FindGameObjectsWithTag("cube");
    }

    private List<int> GenerateList(int size)
    {
        if (cubeSpawner.cubesAlongX == 0 || cubeSpawner.cubesAlongY == 0)
        {
            Debug.Log("Amount of cubes not set");
        }
        int amountOfBoxes = cubeSpawner.cubesAlongX * cubeSpawner.cubesAlongY;

        List<int> tempBoxes = new List<int>();
        // Step 1: Populate the initial list with values 0 to 8    
        for (int i = 0; i < amountOfBoxes; i++)
        {
            tempBoxes.Add(i);
        }
        // Step 2: Duplicate the list 'size' times    
        List<int> originalList = new List<int>(tempBoxes);
        for (int i = 0; i < size; i++)
        {
            tempBoxes.AddRange(originalList);
        }
        return tempBoxes;
    }

    public List<int> ShuffleList(List<int> list)
    {
        for (int i = list.Count - 1; i > 0; i--)
        {
            int j = UnityEngine.Random.Range(0, i + 1);

            // Perform the swap
            int temp = list[i];
            list[i] = list[j];
            list[j] = temp;

            // Check if adjacent elements are the same after swap
            if (i > 0 && list[i] == list[i - 1])
            {
                // If adjacent elements are the same, swap again
                j = UnityEngine.Random.Range(0, i + 1);
                temp = list[i];
                list[i] = list[j];
                list[j] = temp;
            }

            //Debug.Log("Testing the list: " + string.Join(", ", list));
        }

        return list;
    }


    public GameObject ActivateCube()
    {
        Debug.Log(boxes.Count);
        if (boxes.Count == 0)
        {
            Debug.Log("No boxes :(");
            testingBoxes = false;
            movingCube.activeCubeCollider.enabled = true;
            movingCube.movingBoxRender.enabled = true;
            movingCube.movingCubePhase = true;
            movingCube.ActivateCube();
            return activeCube;
        }

        if (boxes.Count > 0)
        {
            int randomIndex = UnityEngine.Random.Range(0, boxes.Count);
            boxNumber = boxes[randomIndex];
            boxes.RemoveAt(randomIndex);
            GameObject randomCube = cubes[boxNumber];

            Renderer cubeRenderer = randomCube.GetComponent<Renderer>();
            if (cubeRenderer != null && !cubeActivated)
            {
                cubeRenderer.material = HighLightColor;
                activeCube = randomCube;
                activeCubeCollider = activeCube.GetComponent<BoxCollider>();
                activeCubeCollider.enabled = true;
                Debug.Log("Activated Cube: " + randomCube.name + " | Boxes left: " + boxes.Count);
                currentActivatedCube = activeCube.name;
            }
        }
        return activeCube;
    }

    public void DeactivateCube()
    {
        if (activeCube == null) return;

        Renderer cubeRenderer = activeCube.GetComponent<Renderer>();
        if (cubeRenderer != null)
        {
            cubeRenderer.material = gridColor;
            cubeActivated = false;
            Debug.Log("Deactivated Cube: " + activeCube.name);
        }
        activeCube = null;
    }


    private IEnumerator LogRoutine()
    {
        while (true)
        {
            timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.ffff"); // Timestamp in real time
            frameNumber = Time.frameCount;
            prediction = ws.getGestureKey();

            // If the cube is activated, continue logging it
            string logEntry =
                $"{timestamp};" +
                $"{frameNumber};" +
                $"{(isCubeActivated ? currentActivatedCube : "None")};" +
                $"{goalGesture};" +
                $"{prediction}"
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

        // Create the file with headers
        File.WriteAllText(filePath, "ID;Timestamp;FrameNumber;ActivatedCube;ActiveCubeX;ActiveCubeY;ActiveCubeZ;TrackerX;TrackerY;TrackerZ;GoalGesture;GesturesAttempted;AttemptsInCube;State;Event\n");

        var updatedLogEntries = logEntries.Select(entry => participantNr + ";" + entry).ToList();

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

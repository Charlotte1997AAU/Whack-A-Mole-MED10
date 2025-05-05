using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using TMPro;
using UnityEngine;
using Random = UnityEngine.Random;

public class testLogger : MonoBehaviour
{
    private string timestamp;
    private int frameNumber;
    private bool isCubeActivated;
    public int goalGesture;
    private string currentActivatedCube;
    private int prediction;
    private float logInterval = 0.1f;
    private string filePath;
    private int boxNumber;
    private bool cubeActivated = false;
    public bool testing = false;
    public bool testingBoxes = true;
    public string gestureName;

    public enum goalGestureLatinSquare {goalGestures0, goalGesture1, goalGestures2, goalGestures3 };
    [SerializeField] public goalGestureLatinSquare goalSquare;
    private MovingTarget movingCube;
    private triggerBox trigger;
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
    private static List<int> goalGestures0 = new List<int> {0,1,2,3};
    private static List<int> goalGestures1 = new List<int> {1,2,3,0};
    private static List<int> goalGestures2 = new List<int> {2,3,0,1};
    private static List<int> goalGestures3 = new List<int> {3,0,1,2};
    public List<int> selectedGoalGestures;
    public TextMeshProUGUI textField;
    public Dictionary<int, string> gestureMap = new Dictionary<int, string>
{
    { 0, "Extension" },
    { 1, "Fist" },
    { 2, "Flexion" },
    { 3, "Pinch" }
};

    // Start is called before the first frame update
    void Start()
    {
        sliderFill = FindObjectOfType<SliderFill>();
        trigger = FindObjectOfType<triggerBox>();
        resetScript = FindObjectOfType<resetPosition>();
        movingCube = FindObjectOfType<MovingTarget>();
        ws = FindObjectOfType<webSocket>();
        wall = GameObject.Find("Wall");
        boxes = GenerateList(3);
        boxes = ShuffleList(boxes);
        cubeSpawner.SpawnCubes();
        cubeSpawner.cubePrefab.SetActive(false);
        cubes = GameObject.FindGameObjectsWithTag("cube");

        switch (goalSquare)
        {
            case goalGestureLatinSquare.goalGestures0:
                selectedGoalGestures = goalGestures0;
                break;
            case goalGestureLatinSquare.goalGesture1:
                selectedGoalGestures = goalGestures1;
                break;
            case goalGestureLatinSquare.goalGestures2:
                selectedGoalGestures = goalGestures2;
                break;
            case goalGestureLatinSquare.goalGestures3:
                selectedGoalGestures = goalGestures3;
                break;
            default:
                selectedGoalGestures = new List<int>(); // fallback in case of unexpected value
                break;
        }
        selectedGoalGestures = DuplicateList(selectedGoalGestures, 10);
        StartCoroutine(LogRoutine());

    }

    private void Update()
    {
        gestureName = gestureMap.ContainsKey(goalGesture) ? gestureMap[goalGesture] : "Unknown";
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
        if (boxes.Count == 0)
        {
            Debug.Log("No boxes :(");
            testingBoxes = false;
            movingCube.activeCubeCollider.enabled = true;
            movingCube.movingBoxRender.enabled = true;
            movingCube.movingCubePhase = true;
            movingCube.ActivateCube();
            wall.SetActive(false);
            return activeCube;
        }

        if (boxes.Count > 0)
        {
            isCubeActivated = true;
            goalGesture = selectedGoalGestures[0];
            Debug.Log("Goal Gesture: " + gestureName);
            textField.text = gestureName;
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
        selectedGoalGestures.RemoveAt(0);
        isCubeActivated = false;

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
                $"{(movingCube.isMoving ? "Moving box" : "None")};" +
                $"{goalGesture};" +
                $"{prediction};" +
                $"{(trigger.isInside ? "InCube" : "None")}"
                ;

            // Write the log entry to the file
            logEntries.Add(logEntry);

            yield return new WaitForSeconds(logInterval);
        }
    }

    private void OnApplicationQuit()
    {
        // Get the directory path
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Test Logs");

        // Ensure the directory exists
        Directory.CreateDirectory(directoryPath);

        // Generate a unique file name
        filePath = GetUniqueFilePath(directoryPath, "Test_log", "csv");

        // Create the file with headers
        File.WriteAllText(filePath, "Timestamp;FrameNumber;ActivatedCube;movingCube;GoalGesture;Prediction;InCube\n");

        var updatedLogEntries = logEntries.Select(entry => entry).ToList();

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

    public List<int> DuplicateList(List<int> originalList, int timesToRepeat)
    {
        List<int> result = new List<int>();

        for (int i = 0; i < timesToRepeat; i++)
        {
            result.AddRange(originalList);
        }

        return result;
    }
}

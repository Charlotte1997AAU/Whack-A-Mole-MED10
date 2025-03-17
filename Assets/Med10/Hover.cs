using UnityEngine;
using System.Collections.Generic;
using TMPro;

public class Hover : MonoBehaviour
{
    public LayerMask cubeLayer; 
    public Logger logger;
    public Material HighLightColor;
    public Material gridColor;
    public Material GestureColor;
    public GameObject[] cubes;
    public GameObject activeCube;
    public Collider activeCubeCollider;
    public GameObject gestureSignifier;
    private Animator gestureAnim;
    public int iterations = 1;

    private int gesturesCount = 0;
    private bool cubeActivated = false;
    public CubeSpawner cubeSpawner;
    private static List<int> boxes = new List<int>();
    public ThalmicMyo stopLogging;
    private int currentState = 3; // Moving to rest position
    private int eventKey = 0;     // Event is none
    private bool gestureComplete = false;
    private int attempts = 1;
    public TextMeshProUGUI textField;
    public string visibleText;


    //public static List<int> storeEMG08 = new List<int>();
    private int boxNumber;

    private void Start()
    {
        gestureAnim = gestureSignifier.GetComponent<Animator>();
        boxes = GenerateList(iterations);
        boxes = ShuffleList(boxes);
        cubeSpawner.SpawnCubes();
        cubeSpawner.cubePrefab.SetActive(false);
        cubes = GameObject.FindGameObjectsWithTag("cube"); // Ensure correct tag
        if (cubes.Length == 0) return;
        //ActivateCube();
        //logger.StartLogging();
    }

private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            ActivateCube();
            //dataLogger.CollectData();
        }
        if (Input.GetMouseButtonDown(1))
        {
            DeactivateCube();
            stopLogging.StopEmgCoroutine();
            foreach (int[] item in stopLogging.emgBuffer)
            {
                Debug.Log(string.Join(", ", item));
            }
        }

        if (getGestureComplete())
        {
            Debug.Log("Gesture completed ");
            setCurrentEvent(1);
            setGestureComplete(false);
        } else
        {
            setCurrentEvent(0);
        }

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



        public GameObject ActivateCube()
    {
        string currentAnim = logger.goalGesture.ToString();
        if(boxes.Count == 0)
        {
            Debug.Log("No boxes :(");
            return activeCube;
        }

        if (boxes.Count > 0)
        {
            Debug.Log("Curent animation: " + currentAnim);
            gestureAnim.SetTrigger(currentAnim);
            int randomIndex = UnityEngine.Random.Range(0, boxes.Count);
            boxNumber = boxes[randomIndex];
            boxes.RemoveAt(randomIndex);
            GameObject randomCube = cubes[boxNumber];

            Renderer cubeRenderer = randomCube.GetComponent<Renderer>();
            if (cubeRenderer != null && !cubeActivated)
            {
                cubeActivated = true;
                cubeRenderer.material = HighLightColor;
                activeCube = randomCube;
                activeCubeCollider = activeCube.GetComponent<BoxCollider>();
                activeCubeCollider.enabled = true;
                Debug.Log("Activated Cube: " + randomCube.name);
                textField.text = "";
                setCurrentState(1);
                logger.LogActivatedCube(activeCube.name, activeCube.transform.position);
            }
        }

        return activeCube; 
    }

    public void DeactivateCube()
    {
        gestureAnim.SetTrigger("rest");
        if (activeCube == null) return; 

        Renderer cubeRenderer = activeCube.GetComponent<Renderer>();
        if (cubeRenderer != null)
        {
            cubeRenderer.material = gridColor; 
            cubeActivated = false;
            logger.LogDeactivatedCube();
            Debug.Log("Deactivated Cube: " + activeCube.name);
            textField.text = "Rest";
            gesturesCount++;
            attempts = 1;
        }
        setCurrentState(3);
        activeCube = null;
    }


    public void setGestureComplete(bool completed)
    {
        gestureComplete = completed;
    }

    public bool getGestureComplete()
    {
        return gestureComplete;
    }

    public int getGesturesCount()
    {
        return gesturesCount;
    }
    public void setCurrentEvent(int eventInt)
    {
        eventKey = eventInt;
    }

    public int getEvents()
    {
        return eventKey;
    }

    public void setCurrentState(int stateKey)
    {
        currentState = stateKey;
    }

    public int getCurrentState()
    {
        return currentState;
    }

    public void setAttempts()
    {
        attempts++;
    }

    public int getAttempts()
    {
        return attempts;
    }
}

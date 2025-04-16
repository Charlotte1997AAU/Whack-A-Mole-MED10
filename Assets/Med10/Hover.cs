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
    private Animator activeHandAnimation;
    private Animator gestureAnim;
    public int iterations = 1;
    public GameObject hannesHand;
    private string currentAnim;
    [SerializeField] private StateManager stateManager;
    public webSocket ws;
    public Dictionary<int, string> predictedGesture;
    private int currentGestureKey;
    public string currentGestureString;
    public string lastTriggeredGesture = "";
    private Queue<string> gestureHistory = new Queue<string>();
    public int gestureSampleSize = 5;

    private int gesturesCount = 0;
    public bool cubeActivated = false;
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
        gestureAnim = gestureSignifier.GetComponentInChildren<Animator>();
        boxes = GenerateList(iterations);
        boxes = ShuffleList(boxes);
        cubeSpawner.SpawnCubes();
        cubeSpawner.cubePrefab.SetActive(false);
        cubes = GameObject.FindGameObjectsWithTag("cube"); // Ensure correct tag
        activeHandAnimation = hannesHand.GetComponentInChildren<Animator>();
        currentAnim = logger.goalGesture.ToString();
        if (cubes.Length == 0) return;
        predictedGesture = ws.gestureNames;
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


    public string runAnimations()
    {
        currentGestureKey = ws.currentGestureKey;
        string newGesture = predictedGesture[currentGestureKey];

        gestureHistory.Enqueue(newGesture);

        // Keep only the last X gestures
        if (gestureHistory.Count > gestureSampleSize)
        {
            gestureHistory.Dequeue();
        }

        // Check if all gestures in history are the same
        if (gestureHistory.Count == gestureSampleSize)
        {
            string firstGesture = gestureHistory.Peek();
            bool allSame = true;

            foreach (var gesture in gestureHistory)
            {
                if (gesture != firstGesture)
                {
                    allSame = false;
                    break;
                }
            }

            currentGestureString = allSame ? firstGesture : "rest";
        }
        else
        {
            currentGestureString = "rest"; // Still filling up history
        }
        return currentGestureString;
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
        if(boxes.Count == 0)
        {
            textField.text = "Done";
            Debug.Log("No boxes :(");
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
                cubeActivated = true;
                Renderer[] gestureSignifierRenderer = gestureSignifier.GetComponentsInChildren<Renderer>();
                for (int renders = 0; renders < gestureSignifierRenderer.Length; renders++)
                {
                    gestureSignifierRenderer[renders].enabled = true;
                }

                cubeRenderer.material = HighLightColor;
                activeCube = randomCube;
                activeCubeCollider = activeCube.GetComponent<BoxCollider>();
                activeCubeCollider.enabled = true;
                Debug.Log("Activated Cube: " + randomCube.name + " | Boxes left: " + boxes.Count);
                textField.text = "";
                setCurrentState(1);
                logger.LogActivatedCube(activeCube.name, activeCube.transform.position);
            }
        }

        return activeCube; 
    }

    public void DeactivateCube()
    {
        if (stateManager.state == StateManager.State.Testing)
        {
            activeHandAnimation.ResetTrigger(currentGestureString);

            // Return to the rest/neutral animation
            activeHandAnimation.SetTrigger("rest");

            // Optionally reset the gesture trigger tracking
            lastTriggeredGesture = "";
        }

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

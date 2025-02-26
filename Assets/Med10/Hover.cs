using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;

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
    public int iterations = 1;

    private bool cubeActivated = false;
    private Collider cubesCollider;
    public CubeSpawner cubeSpawner;
    private static List<int> boxes = new List<int>();

    //public static List<int> storeEMG08 = new List<int>();
    private int boxNumber;

    private void Start()
    {
        boxes = GenerateList(iterations);
        boxes = ShuffleList(boxes);
        cubeSpawner.SpawnCubes();
        cubeSpawner.cubePrefab.SetActive(false);
        cubes = GameObject.FindGameObjectsWithTag("cube"); // Ensure correct tag
        if (cubes.Length == 0) return;
    }

private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            ActivateCube();
        }
        if (Input.GetMouseButtonDown(1))
        {
            DeactivateCube();
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

            Debug.Log("Testing the list: " + string.Join(", ", list));
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
                cubeRenderer.material = HighLightColor;
                activeCube = randomCube;
                activeCubeCollider = activeCube.GetComponent<BoxCollider>();
                activeCubeCollider.enabled = true;
                Debug.Log("Activated Cube: " + randomCube.name);
                logger.LogActivatedCube(activeCube.name);
                logger.LogIfGestureReady(false);
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
            logger.LogDeactivatedCube();
            logger.LogIfGestureReady(false);
            Debug.Log("Deactivated Cube: " + activeCube.name);
        }

        activeCube = null;
    } 
    
}

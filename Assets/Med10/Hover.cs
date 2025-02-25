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

    private bool cubeActivated = false;
    private Collider cubesCollider;
    private static List<int> boxes = new List<int>() { 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8 };

    //public static List<int> storeEMG08 = new List<int>();
    private int boxNumber;

    private void Start()
    {
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

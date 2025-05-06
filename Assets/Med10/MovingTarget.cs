using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class MovingTarget : MonoBehaviour
{
    public LayerMask cubeLayer;
    public Material HighLightColor;
    public Material gridColor;
    public Material GestureColor;
    public Collider activeCubeCollider;
    public resetPosition resetScript;
    public Renderer movingBoxRender;
    public testLogger testLogger;


    public bool movingCubePhase = false;
    public int gestureCount = 0;
    public bool cubeActivated = false;
    public float moveDistance = 1.0f; // Distance for each side of the square
    public float moveSpeed = 1.0f; // Speed of movement
    public bool isMoving = false;
    public LineRenderer lineRenderer;
    public TextMeshProUGUI textField;

    private void Start()
    {
        movingBoxRender = GetComponent<Renderer>();
    }

    private void Update()
    {
        if (Input.GetMouseButtonDown(0) && movingCubePhase)
        {
            ActivateCube();
        }

        if (Input.GetMouseButtonDown(1) && movingCubePhase)
        {
            DeactivateCube();
        }

    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            if (movingBoxRender != null)
            {
                movingBoxRender.material = GestureColor;
            }
            testLogger.goalGesture = testLogger.selectedGoalGestures[0];
            textField.text = "";
            MoveCube();
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            if (movingBoxRender != null)
            {
                movingBoxRender.material = HighLightColor;
            }
        }
    }

        public void ActivateCube()
    {
        if (gestureCount == 4)
        {
            return;
        }

        if (gestureCount < 4)
        {
            gestureCount++;
            DrawGhostPath();
            string gestureName = testLogger.gestureMap.ContainsKey(testLogger.goalGesture) ? testLogger.gestureMap[testLogger.goalGesture] : "Unknown";
            textField.text = gestureName;
            Debug.Log("Goal Gesture: " + gestureName);
            Renderer cubeRenderer = GetComponent<Renderer>(); // Gets the Renderer on this GameObject
            if (cubeRenderer != null && !cubeActivated)
            {
                cubeActivated = true;
                cubeRenderer.material = HighLightColor;
                activeCubeCollider = GetComponent<BoxCollider>();
                activeCubeCollider.enabled = true;

            }
        }
    }


    public void MoveCube()
    {
        if (!isMoving)
        {
            StartCoroutine(MoveCubeEnum());
        }
    }

    private IEnumerator MoveCubeEnum()
    {
        isMoving = true;

        Vector3[] directions = new Vector3[]
        {
            Vector3.right,   
            Vector3.up,      
            Vector3.left,    
            Vector3.down 
        };

        foreach (Vector3 dir in directions)
        {
            Vector3 startPos = transform.position;
            Vector3 targetPos = startPos + dir * moveDistance;
            float elapsed = 0f;

            while (elapsed < moveDistance / moveSpeed)
            {
                transform.position = Vector3.Lerp(startPos, targetPos, (elapsed * moveSpeed) / moveDistance);
                elapsed += Time.deltaTime;
                yield return null;
            }

            transform.position = targetPos;
        }

        isMoving = false;
        DeactivateCube();
    }

    public void DrawGhostPath()
    {
        float d = moveDistance;
        Vector3 basePos = transform.position;

        // Keep Z consistent to avoid weird 3D distortions
        float z = basePos.z;

        Vector3[] points = new Vector3[5]
        {
            new Vector3(basePos.x, basePos.y, z),
            new Vector3(basePos.x + d, basePos.y, z),
            new Vector3(basePos.x + d, basePos.y + d, z),
            new Vector3(basePos.x, basePos.y + d, z),
            new Vector3(basePos.x, basePos.y, z) // back to start
        };

        lineRenderer.positionCount = points.Length;
        lineRenderer.useWorldSpace = true; // Important!
        lineRenderer.SetPositions(points);
    }


    public void DeactivateCube()
    {
        if (this.gameObject == null) return;

        Renderer cubeRenderer = GetComponent<Renderer>();
        if (cubeRenderer != null)
        {
            cubeRenderer.material = gridColor;
            cubeActivated = false;
            activeCubeCollider.enabled = false;
            resetScript.resetPosReady();
        }
        testLogger.selectedGoalGestures.RemoveAt(0);
    }
}

using UnityEngine;

public class Hover : MonoBehaviour
{
    public Camera mainCamera; // Reference to the main camera.
    public LayerMask cubeLayer; 
    public Logger logger;
    public Material HighLightColor;
    public Material gridColor;
    public Material GestureColor;
    public GameObject[] cubes;

    private bool cubeActivated = false;
    private GameObject activeCube;


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
        ChangeCubeColorOnCollision();

    }

    void ChangeCubeColorOnCollision()
{
    Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);
    RaycastHit hit;

    if (Physics.Raycast(ray, out hit, Mathf.Infinity, cubeLayer))
    {
        string cubeName = hit.collider.gameObject.name;
        if (cubeName == activeCube.name)
        {
            Renderer cubeRenderer = activeCube.GetComponent<Renderer>();
            if (cubeRenderer != null)
            {
                cubeRenderer.material = GestureColor;
                logger.LogIfGestureReady(true);
                Debug.Log("Changed to gesture ready: " + activeCube.name);
            }
        }
        else
        {
            Renderer cubeRenderer = activeCube.GetComponent<Renderer>();
            if (cubeRenderer != null)
            {
                cubeRenderer.material = HighLightColor;
                logger.LogIfGestureReady(false);
            }
        }
    }
    else
    {
        if (activeCube != null)
        {
            Renderer cubeRenderer = activeCube.GetComponent<Renderer>();
            if (cubeRenderer != null)
            {
                cubeRenderer.material = HighLightColor;
                logger.LogIfGestureReady(false);
            }
        }
    }
}
    GameObject ActivateCube()
    {
        cubes = GameObject.FindGameObjectsWithTag("cube"); // Ensure correct tag
        if (cubes.Length == 0) return null;

        int randomIndex = Random.Range(0, cubes.Length);
        GameObject randomCube = cubes[randomIndex];

        Renderer cubeRenderer = randomCube.GetComponent<Renderer>();
        if (cubeRenderer != null && !cubeActivated)
        {
            cubeActivated = true;
            cubeRenderer.material = HighLightColor;
            activeCube = randomCube;
            Debug.Log("Activated Cube: " + randomCube.name);
            logger.LogActivatedCube(activeCube.name);
            logger.LogIfGestureReady(false);
        }

        return activeCube; 
    }

    void DeactivateCube()
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

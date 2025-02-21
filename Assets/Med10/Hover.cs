using UnityEngine;

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
        int randomIndex = Random.Range(0, cubes.Length);
        GameObject randomCube = cubes[randomIndex];

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

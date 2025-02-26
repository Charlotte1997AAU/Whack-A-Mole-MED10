using UnityEngine;

public class CubeSpawner : MonoBehaviour
{
    public GameObject cubePrefab; // The cube prefab to spawn
    public int cubesAlongX = 4;   // Number of cubes along the X axis
    public int cubesAlongY = 3;   // Number of cubes along the Y axis
    public Vector2 spawnAreaSize = new Vector2(1.5f, 1.2f); // The size of the area to spawn cubes

    public void SpawnCubes()
    {
        // Calculate the size of each cube based on the number of cubes and the area size
        float cubeWidth = spawnAreaSize.x / cubesAlongX;
        float cubeHeight = spawnAreaSize.y / cubesAlongY;

        int cubeCount = 0;

        // Loop through the number of cubes to spawn along X and Y axes
        for (int x = 0; x < cubesAlongX; x++)
        {
            for (int y = 0; y < cubesAlongY; y++)
            {
                // Calculate position for each cube (spawn on X and Y, keep Z fixed)
                Vector3 spawnPosition = new Vector3(
                    transform.position.x + (x * cubeWidth) - (spawnAreaSize.x / 2) + (cubeWidth / 2), // Adjust for X spacing
                    transform.position.y + (y * cubeHeight) - (spawnAreaSize.y / 2) + (cubeHeight / 2), // Adjust for Y spacing
                    transform.position.z  // Keep Z axis constant
                );

                // Spawn the cube and set its scale
                GameObject cube = Instantiate(cubePrefab, spawnPosition, Quaternion.identity, transform);

                // Set the scale of the cube to fit the area (don't double the height)
                cube.transform.localScale = new Vector3(cubeWidth, cubeHeight, cubeHeight);
                //cube.transform.position = new Vector3(cube.transform.position.x, spawnPosition.y, cube.transform.position.z);

                cube.name = "Cube " + cubeCount;

                // Increment the cube count for the next name
                cubeCount++;
            }
        }
    }
}

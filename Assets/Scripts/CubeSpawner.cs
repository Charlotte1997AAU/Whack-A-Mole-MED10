using UnityEngine;

public class CubeSpawner : MonoBehaviour
{
    public GameObject cubePrefab; // The cube prefab to spawn
    public int cubesAlongX = 4;   // Number of cubes along the X axis
    public int cubesAlongY = 3;   // Number of cubes along the Y axis
    public Vector2 spawnAreaSize = new Vector2(1.5f, 1.2f); // The total area to spawn cubes in
    public float padding = 0.05f; // Space between cubes

    public void SpawnCubes()
    {
        // Calculate total padding
        float totalPaddingX = (cubesAlongX - 1) * padding;
        float totalPaddingY = (cubesAlongY - 1) * padding;

        // Calculate the size of each cube considering padding
        float cubeWidth = (spawnAreaSize.x - totalPaddingX) / cubesAlongX;
        float cubeHeight = (spawnAreaSize.y - totalPaddingY) / cubesAlongY;

        int cubeCount = 0;

        for (int x = 0; x < cubesAlongX; x++)
        {
            for (int y = 0; y < cubesAlongY; y++)
            {
                // Calculate position for each cube
                float posX = transform.position.x - (spawnAreaSize.x / 2) + (cubeWidth / 2) + x * (cubeWidth + padding);
                float posY = transform.position.y - (spawnAreaSize.y / 2) + (cubeHeight / 2) + y * (cubeHeight + padding);

                Vector3 spawnPosition = new Vector3(posX, posY, transform.position.z);

                // Spawn and scale cube
                GameObject cube = Instantiate(cubePrefab, spawnPosition, Quaternion.identity, transform);
                cube.transform.localScale = new Vector3(cubeWidth, cubeHeight, cubeHeight); // Customize Z if needed
                cube.name = "Cube " + cubeCount;

                cubeCount++;
            }
        }
    }
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;


public class triggerBox : MonoBehaviour
{
    public Hover hoverScript;
    public Logger logger;
    public EMGSaveData saver;

    private bool isInside = false;
    private float requriedTime = 5.0f;
    public float timeInside = 0f;

    public GameObject tracker;
    public static List<Vector3> trackerPositions = new List<Vector3>();

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            saver.resetEMGholders();
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            trackerPositions.Add(trackerPos());
            Renderer cubeRenderer = hoverScript.activeCube.GetComponent<Renderer>();
            if (cubeRenderer != null)
            {
                cubeRenderer.material = hoverScript.GestureColor;
                logger.LogIfGestureReady(true);
            }
            
            if (!isInside)
            {
                isInside = true;
                timeInside = 0f;
            }
            timeInside += Time.deltaTime;
            if (timeInside >= requriedTime)
            {
                saver.saveDataToCSV();
                hoverScript.DeactivateCube();
                hoverScript.activeCubeCollider.enabled = false;
                hoverScript.ActivateCube();
                Debug.Log("we have made it");
                timeInside = 0f;
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            if (hoverScript.activeCube != null)
            {
                Renderer cubeRenderer = hoverScript.activeCube.GetComponent<Renderer>();
                if (cubeRenderer != null)
                {
                    cubeRenderer.material = hoverScript.HighLightColor;
                    logger.LogIfGestureReady(false);
                }
            }

            isInside = false;
            timeInside = 0f;
        }
    }

    public Vector3 trackerPos()
    {
        float trackerX = tracker.transform.position.x;
        float trackerY = tracker.transform.position.y;
        float trackerZ = tracker.transform.position.z;

        Vector3 trackerPosition = new Vector3(trackerX, trackerY, trackerZ);

        return trackerPosition;
    }
}

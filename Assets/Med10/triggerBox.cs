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
}

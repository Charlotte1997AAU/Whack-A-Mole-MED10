using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class resetPosition : MonoBehaviour
{

    public Hover hoverScript;
    public Logger logger;
    public EMGSaveData saver;
    public Collider sphereCollider;
    public Material startColor;

    private bool isInside = false;
    private float requiredTime = 5.0f;
    private float timeInside = 0.0f;

    private void OnTriggerEnter(Collider other)
    {
        if(other.CompareTag("GameController"))
        {
            Debug.Log("Log at vi starter med at reste??");
        }
    }
    private void OnTriggerStay(Collider other)
    {
        Renderer sphereRenderer = this.GetComponent<Renderer>();
        if (other.CompareTag("GameController"))
        {
            if(sphereRenderer != null)
            {
            sphereRenderer.material = hoverScript.GestureColor;
            }
        }

        if (!isInside)
        {
            isInside = true;
            timeInside = 0f;
        }
        timeInside += Time.deltaTime;
        if (timeInside >= requiredTime)
        {
            sphereCollider = this.GetComponent<Collider>();
            sphereCollider.enabled = false;
            sphereRenderer.material = startColor;
            hoverScript.ActivateCube();
            Debug.Log("Done resting - maybe log this????");
            timeInside = 0f;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.CompareTag("GameController"))
        {
            Renderer sphereRenderer = this.GetComponent<Renderer>();
            if(sphereRenderer != null)
            {
            sphereRenderer.material = hoverScript.HighLightColor;
            }
            
            isInside = false;
            timeInside = 0f;
        }
    }


    public void resetPosReady()
    {
            sphereCollider = this.GetComponent<Collider>();
            sphereCollider.enabled = true;
            Renderer sphereRenderer = this.GetComponent<Renderer>();
            sphereRenderer.material = hoverScript.HighLightColor;
    }
}

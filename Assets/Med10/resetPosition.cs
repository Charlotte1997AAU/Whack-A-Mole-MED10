using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class resetPosition : MonoBehaviour
{

    public Hover hoverScript;
    public Logger logger;
    private Collider sphereCollider;
    public Material startColor;

    private bool isInside = false;
    private float requiredTime = 5.0f;
    private float timeInside = 0.0f;

    private void Start()
    {
        hoverScript = FindObjectOfType<Hover>();
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

        hoverScript.setCurrentState(0);

        if (!isInside)
        {
            isInside = true;
            timeInside = 0f;
            hoverScript.setCurrentState(4); 
        }

        timeInside += Time.deltaTime;
        if (timeInside >= requiredTime)
        {
            sphereCollider = this.GetComponent<Collider>();
            sphereCollider.enabled = false;
            sphereRenderer.material = startColor;
            hoverScript.ActivateCube();
            timeInside = 0f;
            hoverScript.setCurrentState(1);
            Debug.Log("Current State: " + hoverScript.getCurrentState());
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

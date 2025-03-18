using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class resetPosition : MonoBehaviour
{

    public Hover hoverScript;
    public Logger logger;
    private Collider sphereCollider;
    public Material startColor;
    public GameObject handAnchor;
    private Transform handTransform;
    private SliderFill sliderFill;


    private bool isInside = false;
    public float requiredTime = 3.0f;
    private float timeInside = 0.0f;
    public bool SetRestPosition = false;

    private void Start()
    {
        hoverScript = FindObjectOfType<Hover>();
        handTransform = handAnchor.GetComponent<Transform>();
        sliderFill = FindObjectOfType<SliderFill>();


    }

    private void Update()
    {
        if (SetRestPosition)
        {
            transform.position = handTransform.transform.position;
            SetRestPosition = false;
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

        hoverScript.setCurrentState(0);

        if (!isInside)
        {
            isInside = true;
            timeInside = 0f;
            hoverScript.setCurrentState(4); 
        }

        timeInside += Time.deltaTime;
        sliderFill.FillSliderOverTime(requiredTime);

        if (timeInside >= requiredTime)
        {
            sphereCollider = this.GetComponent<Collider>();
            sphereCollider.enabled = false;
            sphereRenderer.material = startColor;
            hoverScript.ActivateCube();
            timeInside = 0f;
            hoverScript.setCurrentState(1);
            sliderFill.resetTimer();
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
            sliderFill.resetTimer();
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

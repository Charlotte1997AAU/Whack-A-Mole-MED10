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
    public TextMeshProUGUI textField;
    private Renderer sphereRenderer;
    private MovingTarget movingTarget;
    private testLogger testLogger;
    [SerializeField] private StateManager stateManager;

    private bool isInside = false;
    public float requiredTime = 3.0f;
    public float MVCRequiredTime = 5.0f;
    private float timeInside = 0.0f;
    private float MVCtime = 0f;
    public bool getMVC = false;

    private void Start()
    {
        hoverScript = FindObjectOfType<Hover>();
        handTransform = handAnchor.GetComponent<Transform>();
        sliderFill = FindObjectOfType<SliderFill>();
        sphereCollider = GetComponent<Collider>();
        sphereRenderer = GetComponent<Renderer>();
        movingTarget = FindObjectOfType<MovingTarget>();
        testLogger = FindObjectOfType<testLogger>();
    }

    private void Update()
    {
        if (getMVC)
        {
            textField.text = "100% POWER!";
            hoverScript.setCurrentState(5);
            MVCtime += Time.deltaTime;
            sliderFill.FillSliderOverTime(MVCRequiredTime);
            if (MVCtime > MVCRequiredTime)
            {  
                hoverScript.setCurrentState(0);
                sliderFill.resetTimer();
                textField.text = "Rest";
                getMVC = false;
            }
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            sphereCollider.enabled = true;
            sphereRenderer.enabled = true;
            transform.position = handTransform.transform.position;
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

        if(!testLogger.testing)
        {
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

        if (testLogger.testing)
        {
            if(testLogger.testingBoxes)
            {
                if (timeInside >= requiredTime)
                {
                    sphereCollider = this.GetComponent<Collider>();
                    sphereCollider.enabled = false;
                    sphereRenderer.material = startColor;
                    testLogger.ActivateCube();
                    timeInside = 0f;
                    sliderFill.resetTimer();
                }
            }

            if(movingTarget.movingCubePhase)
            {
                if (timeInside >= requiredTime)
                {
                    sphereCollider = this.GetComponent<Collider>();
                    sphereCollider.enabled = false;
                    sphereRenderer.material = startColor;
                    movingTarget.ActivateCube();
                    timeInside = 0f;
                    sliderFill.resetTimer();
                }
            }
        }

        
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.CompareTag("GameController"))
        {
            if (stateManager.state == StateManager.State.Training)
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
            else
            {
                Renderer sphereRenderer = this.GetComponent<Renderer>();
                if (sphereRenderer != null)
                {
                    sphereRenderer.material = testLogger.HighLightColor;
                }
                sliderFill.resetTimer();
                isInside = false;
                timeInside = 0f;
            }

        }
    }


    public void resetPosReady()
    {
        sphereCollider = this.GetComponent<Collider>();
        sphereCollider.enabled = true;
        Renderer sphereRenderer = this.GetComponent<Renderer>();
        if (!testLogger.testing)
        { 
            sphereRenderer.material = hoverScript.HighLightColor;
        }
        else
        {
            sphereRenderer.material = testLogger.HighLightColor;
        }

    }
}

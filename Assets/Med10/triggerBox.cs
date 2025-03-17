using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using TMPro;


public class triggerBox : MonoBehaviour
{
    public Hover hoverScript;
    public Logger logger;
    public resetPosition resetScript;
    //private TextMeshPro timerText;
    private SliderFill sliderFill;


    private bool isInside = false;
    public float requriedTime = 5.0f;
    public float timeInside = 0f;
    public int attempts = 1;

    public GameObject tracker;
    public static List<Vector3> trackerPositions = new List<Vector3>();

    private void Start()
    {
       // timerText = GameObject.Find("TimerText").GetComponent<TextMeshPro>();
        sliderFill = FindObjectOfType<SliderFill>();

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
            }
            
            if (!isInside)
            {
                isInside = true;
                timeInside = 0f;
                hoverScript.setCurrentState(2);
            }
            timeInside += Time.deltaTime;
            sliderFill.FillSliderOverTime(requriedTime);
         
           // timerText.gameObject.SetActive(true);
           // timerText.text = $"{timeInside:F1} / {requriedTime}";
            
            if (timeInside >= requriedTime)
            {
                hoverScript.DeactivateCube();
                hoverScript.activeCubeCollider.enabled = false;
                resetScript.resetPosReady();
                timeInside = 0f;
                hoverScript.setGestureComplete(true);
                sliderFill.resetSlider();
           //     timerText.gameObject.SetActive(false);
                //attempts = 1;
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
                }
            }
            isInside = false;
            timeInside = 0f;

            if (!hoverScript.getGestureComplete())
            {
                hoverScript.setAttempts();
                hoverScript.setCurrentState(4);
                hoverScript.setCurrentEvent(1);
                hoverScript.setCurrentEvent(0);
            }
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

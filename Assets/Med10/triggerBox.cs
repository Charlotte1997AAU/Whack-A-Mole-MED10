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
    public GameObject hannesHand;
    private Animator activeHandAnimation;
    private Animator gestureAnim;
    public GameObject gestureSignifier;

    private bool isInside = false;
    public float requriedTime = 5.0f;
    public float timeInside = 0f;
    public int attempts = 1;
    private string currentAnim;
    public GameObject tracker;
    public static List<Vector3> trackerPositions = new List<Vector3>();

    private Transform startPosition;
    private Transform endPosition;
    private float offsetX = -0.13f;
    private float offsetY = 0.13f;
    private float offsetZ = -0.5f;
    private float timeElapsed = 0f;


    private void Start()
    {
       // timerText = GameObject.Find("TimerText").GetComponent<TextMeshPro>();
        sliderFill = FindObjectOfType<SliderFill>();
        activeHandAnimation = hannesHand.GetComponentInChildren<Animator>();
        gestureAnim = gestureSignifier.GetComponentInChildren<Animator>();
        currentAnim = logger.goalGesture.ToString();
    }

    private void OnTriggerEnter(Collider other)
    {
        Debug.Log("Entered Once");
        activeHandAnimation.SetTrigger(currentAnim);
        gestureAnim.ResetTrigger(currentAnim);
        gestureAnim.ResetTrigger("rest");  
        Renderer[] gestureSignifierRenderer = gestureSignifier.GetComponentsInChildren<Renderer>();
        for (int renders = 0; renders < gestureSignifierRenderer.Length; renders++)
        {
            gestureSignifierRenderer[renders].enabled = false;
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
            }
            
            if (!isInside)
            {
                isInside = true;
                sliderFill.isFilling = true;
                timeInside = 0f;
                hoverScript.setCurrentState(2);
            }

            timeInside += Time.deltaTime;
            sliderFill.FillSliderOverTime(requriedTime);
            Debug.Log("We have entered the box");
            
         
           // timerText.gameObject.SetActive(true);
           // timerText.text = $"{timeInside:F1} / {requriedTime}";
            
            if (timeInside >= requriedTime)
            {
                hoverScript.DeactivateCube();
                hoverScript.activeCubeCollider.enabled = false;
                resetScript.resetPosReady();
                timeInside = 0f;
                hoverScript.setGestureComplete(true);
                sliderFill.resetTimer();
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
            sliderFill.resetTimer();
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

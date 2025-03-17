using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Signifier : MonoBehaviour
{
    private Hover hover;
    private Vector3 startPosition;  // Starting position (you can leave this empty to use the object's current position)
    private Vector3 endPosition;    // Target position (where you want to move the object)
    private Animator gestureAnim;
    private Logger logger;
    public float duration = 5f;    // Time duration to reach the target position
    private float offsetX = -0.13f;
    private float offsetY = 0.13f;
    public float offsetZ = -0.5f;

    private float timeElapsed = 0f;
    private float timeInBox = 0f;
    private bool triggerActivated = false;

    // Start is called before the first frame update
    void Start()
    {
        gestureAnim = gameObject.GetComponentInChildren<Animator>();
        logger = FindObjectOfType<Logger>();
        hover = FindObjectOfType<Hover>();
    }

    // Update is called once per frame
    void Update()
    {
        if (hover.activeCube != null)
        {
            string currentAnim = logger.goalGesture.ToString();
            Debug.Log("Current animation: " + currentAnim);

            // Ensure we only reset and trigger once per loop
            if (!triggerActivated)
            {
                gestureAnim.SetTrigger(currentAnim);
                triggerActivated = true;
            }

            startPosition = new Vector3(hover.activeCube.transform.position.x - offsetX, hover.activeCube.transform.position.y - offsetY, hover.activeCube.transform.position.z - offsetZ);
            endPosition = new Vector3(hover.activeCube.transform.position.x - offsetX, hover.activeCube.transform.position.y - offsetY, hover.activeCube.transform.position.z);

            if (timeElapsed < duration)
            {
                // Increase the time elapsed
                timeElapsed += Time.deltaTime;

                // Calculate the fraction of time elapsed
                float t = timeElapsed / duration;

                // Move the object using Lerp
                transform.position = Vector3.Lerp(startPosition, endPosition, t);
            }
            else
            {
                // Ensure the object reaches the end position exactly at the end of the duration
                transform.position = endPosition;
                timeInBox += Time.deltaTime;
                if (timeInBox > 2)
                {
                    // Reset the time elapsed and other variables to start the loop again
                    timeElapsed = 0f;
                    timeInBox = 0f;
                    gestureAnim.SetTrigger("rest");
                    triggerActivated = false;
                }
            }
        }
    }
}

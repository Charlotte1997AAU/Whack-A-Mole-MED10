using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestModelAnimations : MonoBehaviour
{
    private Animator handAnimation;
    public webSocket ws;
    private Dictionary<int, string> predictedGesture;
    public calcEMGaverage averageEMG;

    private string lastGesture = "";
    private string currentGestureString;
    private bool isAnimating = false;

    void Start()
    {
        handAnimation = GetComponent<Animator>();
        predictedGesture = ws.gestureNames;
    }

    void Update()
    {
        if(ws.allSame)
        {

            currentGestureString = predictedGesture[ws.getGestureKey()];
            // Check if gesture has changed
            if (currentGestureString != lastGesture && !isAnimating)
            {
                Debug.Log("Playing new animation: " + currentGestureString);
                handAnimation.ResetTrigger(lastGesture); // Optional cleanup
                handAnimation.SetTrigger(currentGestureString);
                lastGesture = currentGestureString;
                isAnimating = true;
            }

            // Check if current animation is done
            AnimatorStateInfo stateInfo = handAnimation.GetCurrentAnimatorStateInfo(0);

            if (isAnimating && stateInfo.normalizedTime >= 1f && !stateInfo.IsTag("Idle"))
            {
                isAnimating = false;
            }
        }
    }
}



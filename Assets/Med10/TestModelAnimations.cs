using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestModelAnimations : MonoBehaviour
{
    private Animator handAnimation;
    public webSocket ws;
    private Dictionary<int, string> predictedGesture;

    private string lastGesture = "";
    private string currentGestureString;
    private bool isAnimating = false;
    private Queue<int> keyQueue = new Queue<int>();
    public int queueSize;

    void Start()
    {
        handAnimation = GetComponent<Animator>();
        predictedGesture = ws.gestureNames;
    }

    void Update()
    {
        int currentGestureKey = ws.currentGestureKey;
        keyQueue.Enqueue(currentGestureKey);

        if(keyQueue.Count > queueSize)
        {
            keyQueue.Dequeue();
        }

        if(keyQueue.Count == queueSize)
        {
            bool allSame = true;
            int firstKey = keyQueue.Peek();
            foreach(int key in keyQueue)
            {
                if(key != firstKey)
                {
                    allSame = false;
                    break;
                }
            }
            if(allSame)
            {
                currentGestureString = predictedGesture[firstKey];
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
}


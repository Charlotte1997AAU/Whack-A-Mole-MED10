using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CalibrationGhostHand : MonoBehaviour
{

    public Animator animator;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
    }

    public IEnumerator PlayAnimations()
    {
        yield return new WaitForSeconds(1f);
        yield return TriggerAndWait("fist", 3f);
        yield return TriggerAndWait("rest", 0.5f);
        yield return TriggerAndWait("pinch", 3f);
        yield return TriggerAndWait("rest", 0.5f);
        yield return TriggerAndWait("extension", 3f);
        yield return TriggerAndWait("rest", 0.5f);
        yield return TriggerAndWait("flexion", 3f);
        yield return TriggerAndWait("rest", 0.5f);

        Debug.Log("Done Calibrating");
        gameObject.SetActive(false);
    }

    private IEnumerator TriggerAndWait(string triggerName, float waitTime)
    {
        animator.SetTrigger(triggerName);
        yield return new WaitForSeconds(waitTime);
    }
}

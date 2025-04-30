using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CalibrationGhostHand : MonoBehaviour
{

    public Animator animator;
    public bool isCalibrating;

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
        yield return TriggerAndWait("rest", 1f); //wait for one second so the participant has time..
        yield return TriggerAndWait("fist", 3f);
        yield return TriggerAndWait("rest", 0.2f);
        yield return TriggerAndWait("pinch", 3f);
        yield return TriggerAndWait("rest", 0.2f);
        yield return TriggerAndWait("extension", 3f);
        yield return TriggerAndWait("rest", 0.2f);
        yield return TriggerAndWait("flexion", 3f);
        yield return TriggerAndWait("rest", 0.2f);

        Debug.Log("Done Calibrating");
    }

    private IEnumerator TriggerAndWait(string triggerName, float waitTime)
    {
        animator.SetTrigger(triggerName);
        yield return new WaitForSeconds(waitTime);
    }
}

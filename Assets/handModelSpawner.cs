using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class handModelSpawner : MonoBehaviour
{
    // a reference to the action
    public SteamVR_Action_Boolean HandOnOff;
    // a reference to the hand
    public SteamVR_Input_Sources handType;
    public GameObject controllerPos;
    //reference to the sphere
    public GameObject handModel;
    public Transform vrController;

    [Range(0.01f, 0.25f)]
    public float scale = 0.5f;

    public float offsetDistanceX;
    public float offsetDistanceY = 0.07f;
    public float offsetDistanceZ;

    void Start()
    {
        HandOnOff.AddOnStateDownListener(TriggerDown, handType);
    }

    void Update()
    {
        handModel.transform.localScale = new Vector3(scale, scale, scale);
        handModel.transform.position = new Vector3(controllerPos.transform.position.x - offsetDistanceX, controllerPos.transform.position.y - offsetDistanceY, controllerPos.transform.position.z - offsetDistanceZ);
    }

    public void TriggerDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        Debug.Log("Hand enabled");
        handModel.SetActive(true);
    }

}

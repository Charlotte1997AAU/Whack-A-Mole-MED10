using UnityEngine;
using Valve.VR;

public class handModelController : MonoBehaviour
{
    // a reference to the action
    public SteamVR_Action_Boolean HandOnOff;
    public SteamVR_Action_Boolean saveHandPosition;
    // a reference to the hand
    public SteamVR_Input_Sources handType;
    public GameObject controllerPos;
    // reference to the hand model (the object that you want to freeze in position)
    public float offset;
    public GameObject Tracker;

    [Range(0.01f, 0.05f)]
    public float scale = 0.04f;

    // Store the frozen position when the button is pressed
    private Vector3 frozenPosition;
    private Quaternion frozenRotation;
    private bool isFrozen = false;
    private Quaternion lastControllerRotation;  // To store the initial rotation when freezing

    void Start()
    {
        // Register the listener for the trigger press
        HandOnOff.AddOnStateDownListener(TriggerDown, handType);
        HandOnOff.AddOnStateUpListener(TriggerUp, handType); // Add this to listen for when the trigger is released
        saveHandPosition.AddOnStateDownListener(TrackpadDown, handType);
    }

    void Update()
    {
        if (controllerPos.activeSelf)
        {
            // Scale the hand model
            transform.localScale = new Vector3(scale, scale, scale);

            // When the trigger is pressed (frozen state)
            if (isFrozen)
            {
                // Keep the position frozen in world space, but allow rotation to continue around the model's own axes
                transform.position = frozenPosition;
                Quaternion deltaRotation = controllerPos.transform.rotation * Quaternion.Inverse(lastControllerRotation);
                transform.localRotation = frozenRotation * deltaRotation; // Apply relative rotation to the frozen model
            }
            else
            {
                // When the trigger is released, follow the controller's position and rotation
                transform.position = new Vector3(controllerPos.transform.position.x + offset, controllerPos.transform.position.y, controllerPos.transform.position.z);
                transform.rotation = controllerPos.transform.rotation;
            }
        }
    }

    // This method is called when the trigger is pressed down
    public void TriggerDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        Debug.Log("In rotation mode");

        // Freeze the position by saving the current world position
        frozenPosition = transform.position;
        frozenRotation = transform.rotation;  // Save the current rotation
        // Store the initial controller rotation when freezing
        lastControllerRotation = controllerPos.transform.rotation;

        // Set the flag to indicate position is frozen
        isFrozen = true;
    }

    // This method is called when the trigger is released
    public void TriggerUp(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        Debug.Log("Released trigger, following controller again");

        // Allow position and rotation to follow the controller again
        isFrozen = false;
    }

    public void TrackpadDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        isFrozen = false;
        transform.SetParent(Tracker.transform);

        controllerPos.SetActive(false);
    }
}

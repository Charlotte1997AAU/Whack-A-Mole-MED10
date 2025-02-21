using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColliderTrigger : MonoBehaviour
{

    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            Debug.Log("I'm colliding rn");
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("GameController"))
        {
            Debug.Log("No longer Colliding");
        }
    }
}

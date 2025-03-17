using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class animation_script : MonoBehaviour
{
    Animator anim;
    public Logger logger;

    void Start()
    {
        anim = gameObject.GetComponent<Animator>();

    }

    void Update()
    {


        // Other animations triggered by keys
        if (Input.GetKeyDown(KeyCode.Q))
        {
            Debug.Log("Fist");
            anim.SetTrigger("fist");
        }
        if (Input.GetKeyDown(KeyCode.A))
        {
            anim.SetTrigger("pinch");
        }
        else if (Input.GetKeyDown(KeyCode.W))
        {
            anim.SetTrigger("rest");
        }

        if (Input.GetKeyDown(KeyCode.T))
        {
            anim.SetTrigger("extension"); // up
        }

        if (Input.GetKeyDown(KeyCode.Y))
        {
            anim.SetTrigger("flexion"); // down
        }
    }

}


using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;

public class StoreEMG : MonoBehaviour
{
    public static List<DateTime> storeTimestamp = new List<DateTime>();
    public static List<int> storeEMG01 = new List<int>();
    public static List<int> storeEMG02 = new List<int>();
    public static List<int> storeEMG03 = new List<int>();
    public static List<int> storeEMG04 = new List<int>();
    public static List<int> storeEMG05 = new List<int>();
    public static List<int> storeEMG06 = new List<int>();
    public static List<int> storeEMG07 = new List<int>();
    public static List<int> storeEMG08 = new List<int>();
    public static List<float> timestamp = new List<float>();

    private HardwareDataLogger dataLogger;
    public int counter = 0;
    private ThalmicMyo myoScript;

    void Start()
    {
        dataLogger = FindObjectOfType<HardwareDataLogger>(); // Find logger in scene
        myoScript = FindObjectOfType<ThalmicMyo>(); // Find the ThalmicMyo script in the scene
        if (myoScript == null)
        {
            Debug.LogError("ThalmicMyo script not found in the scene!");
        }
    }

    void Update()
    {
        if (counter > 2)
        {
            int[] emg = myoScript.GetLatestEmgData();  // Get latest EMG safely
            //storeData(emg);
            logToCSV(emg);
        }
        counter++;
    }

    void storeData(int[] emg)
    {
        //Debug.Log("EMG Data: " + string.Join(", ", emg));
        if (emg == null)
        {
            Debug.LogError("Invalid EMG data received.");
            return;
        }

        storeEMG01.Add(emg[0]);
        storeEMG02.Add(emg[1]);
        storeEMG03.Add(emg[2]);
        storeEMG04.Add(emg[3]);
        storeEMG05.Add(emg[4]);
        storeEMG06.Add(emg[5]);
        storeEMG07.Add(emg[6]);
        storeEMG08.Add(emg[7]);
        timestamp.Add(Time.time);
    }

    public void logToCSV(int[] emg)
    {
        if (counter > 2)
        {
            if (emg == null)
            {
                Debug.LogError("Invalid EMG data received.");
                return;
            }

            if (emg == null || emg.Length != 8)
            {
                Debug.LogWarning("Waiting for valid EMG data...");
                return;
            }

            if (dataLogger != null)
            {
                dataLogger.LogEMGData(Time.time, emg);
            }

            counter++;
        }
        else
        {
            counter++;
        }
    }

}

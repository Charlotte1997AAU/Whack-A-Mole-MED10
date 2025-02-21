using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;

public class EMGSaveData : MonoBehaviour
{
    // EMG Data Holders
    private List<int> raw_emg_Pod01;
    private List<int> raw_emg_Pod02;
    private List<int> raw_emg_Pod03;
    private List<int> raw_emg_Pod04;
    private List<int> raw_emg_Pod05;
    private List<int> raw_emg_Pod06;
    private List<int> raw_emg_Pod07;
    private List<int> raw_emg_Pod08;
    private List<DateTime> raw_emg_time;

    public bool saveData = false;
    public static string filename;

    // Start is called before the first frame update
    void Start()
    {
        string shortFilename = "RawEMG-.csv";
        filename = AppendTimeStamp(shortFilename);
        Debug.Log("CSV created");
    }

    // Update is called once per frame
    void Update()
    {
        if (saveData)
        {
            rawEMGRoutine(filename);
            saveData = false;
            Debug.Log("Data saving has begun");
        }
    }

    public void rawEMGRoutine(string filename)
    {
        // Get raw EMG pod data values
        raw_emg_Pod01 = StoreEMG.storeEMG01;
        raw_emg_Pod02 = StoreEMG.storeEMG02;
        raw_emg_Pod03 = StoreEMG.storeEMG03;
        raw_emg_Pod04 = StoreEMG.storeEMG04;
        raw_emg_Pod05 = StoreEMG.storeEMG05;
        raw_emg_Pod06 = StoreEMG.storeEMG06;
        raw_emg_Pod07 = StoreEMG.storeEMG07;
        raw_emg_Pod08 = StoreEMG.storeEMG08;
        raw_emg_time = StoreEMG.timestamp;
        Debug.Log("Raw EMG done");

        // The sizes of EMG 01 and 06 are +1 element bigger than the others
        // This is fixed by trimming them in the savePrc function


        // ------------------------- Raw EMG -------------------------
        // Write raw EMG into a CSV file
        FunctionsCSV csv = new FunctionsCSV();
        csv.saveRawList(filename, raw_emg_Pod01, raw_emg_Pod02, raw_emg_Pod03, raw_emg_Pod04, raw_emg_Pod05, raw_emg_Pod06, raw_emg_Pod07, raw_emg_Pod08, raw_emg_time);
        Debug.Log("Raw EMG CSV file created!");
    }

    public void resetEMGholders()
    {
        // Empty raw EMG data holders
        StoreEMG.storeEMG01.Clear();
        StoreEMG.storeEMG02.Clear();
        StoreEMG.storeEMG03.Clear();
        StoreEMG.storeEMG04.Clear();
        StoreEMG.storeEMG05.Clear();
        StoreEMG.storeEMG06.Clear();
        StoreEMG.storeEMG07.Clear();
        StoreEMG.storeEMG08.Clear();
        StoreEMG.timestamp.Clear();
    }

        public string AppendTimeStamp(string fileName)
    {
        return string.Concat(
            Path.GetFileNameWithoutExtension(fileName),
            DateTime.Now.ToString("yyyy-MM-dd-HH.mm.ss"),
            Path.GetExtension(fileName)
            );
    }
}

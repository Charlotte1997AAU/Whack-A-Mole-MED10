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
    private List<float> raw_emg_time;
    private List<Vector3> trackerPos;

    public bool saveData = false;
    public static string filename;
    public string filePath;
    private string logEntry;
    private string activeCube = "";

    public Hover hover;
    public triggerBox triggerBox;

    // Start is called before the first frame update
    void Start()
    {
        CreateFilePath();
    }

    public void saveDataToCSV()
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
        trackerPos = triggerBox.trackerPositions;

        if (hover.activeCube == null)
        {
            activeCube = "null";
        } else
        {
            activeCube = hover.activeCube.name;
        }

        // The sizes of EMG 01 and 06 are +1 element bigger than the others
        // This is fixed by trimming them in the savePrc function

        // ------------------------- Raw EMG -------------------------
        // Write raw EMG into a CSV file       

        for (int i = 0; i < raw_emg_Pod01.Count; i++)
        {
            logEntry = $"{raw_emg_Pod01[i]}, {raw_emg_Pod02[i]}, {raw_emg_Pod03[i]}, " +
                              $"{raw_emg_Pod04[i]}, {raw_emg_Pod05[i]}, {raw_emg_Pod06[i]}, {raw_emg_Pod07[i]}, " +
                              $"{raw_emg_Pod08[i]}, {raw_emg_time[i]}, {activeCube}, {trackerPos[i].x}, {trackerPos[i].y}, {trackerPos[i].z}";
        
            File.AppendAllLines(filePath, new List<string> { logEntry });
        }
    }

    private string GetUniqueFilePath(string directory, string baseFileName, string extension)
    {
        int counter = 1;
        string filePath;

        do
        {
            string numberedFileName = $"{baseFileName}_{counter:D2}.{extension}";
            filePath = Path.Combine(directory, numberedFileName);
            counter++;
        }
        while (File.Exists(filePath));

        return filePath;
    }

    public string CreateFilePath()
    {
        string directoryPath = Path.Combine(Application.dataPath, "MED10", "Logs");

        // Ensure the directory exists
        Directory.CreateDirectory(directoryPath);

        // Generate a unique file name
        filePath = GetUniqueFilePath(directoryPath, "log", "csv");

        File.WriteAllText(filePath, "EMG1, EMG2, EMG3, EMG4, EMG5, EMG6, EMG7, EMG8, Timestamp, ActiveCube, trackerX, trackerY, trackerZ\n");

        return filePath;
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
        triggerBox.trackerPositions.Clear();
    }
}

using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using Thalmic.Myo; // Ensure Myo SDK is included

public class MyoLogger : MonoBehaviour
{
    public ThalmicMyo myo; // Assign in Unity Inspector
    private StreamWriter writer;
    private CancellationTokenSource cancelTokenSource;
    private bool isLogging = false;

    void Start()
    {


        string filePath = Path.Combine(Application.dataPath, "myo_data.csv");
        writer = new StreamWriter(filePath, false);
        writer.WriteLine("EMG1,EMG2,EMG3,EMG4,EMG5,EMG6,EMG7,EMG8");
        StartLogging();
    }

    void StartLogging()
    {
        if (myo == null)
        {
            Debug.LogError("Myo device not assigned!");
            return;
        }

        isLogging = true;
        cancelTokenSource = new CancellationTokenSource();
        Task.Run(() => LogMyoData(cancelTokenSource.Token));
    }

    async Task LogMyoData(CancellationToken token)
    {
        int intervalMs = 5; // 200 Hz = 5ms per sample
        while (!token.IsCancellationRequested)
        {
            if (myo.emg != null)
            {
                string dataLine = $"{Time.time},{string.Join(",", myo.emg)}";
                writer.WriteLine(dataLine);
            }
            await Task.Delay(intervalMs);
        }
    }
    void OnApplicationQuit()
    {
        StopLogging();
    }

    void StopLogging()
    {
        if (!isLogging) return;
        isLogging = false;
        cancelTokenSource.Cancel();
        writer?.Close();
        Debug.Log("Myo data logging stopped.");
    }
}
using System;
using System.Diagnostics;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using Debug = UnityEngine.Debug;
using Thalmic.Myo;

public class MyoLogger : MonoBehaviour
{
    bool log = true;
    int samplingFrequency = 4; // 5ms, = 125Hz, 4ms = 200Hz, 2ms = 500Hz
    List<int> numbers = new List<int>();
    List<int> emgData = new List<int>();
    CancellationTokenSource cancellationTokenSource = new CancellationTokenSource();
    Task sampleTask;
    Stopwatch writeStopwatch = new Stopwatch();
    private LoggingManager loggingManager;
    private bool manualFramecount = true;

    //  public GameObject thalmicMyo;
    //   private ThalmicMyo myo;

    public ThalmicMyo thalmicMyo;

    void Start ()
    {
        // Subscribe to the EmgData event from ThalmicMyo
        thalmicMyo._myo.EmgData += onReceiveData;
        StartLog();
    }

    // Start is called before the first frame update
    void OnApplicationQuit ()
    {
        StopLog();
    }

    public void StartLog() {
        loggingManager = GetComponent<LoggingManager>();
        loggingManager.CreateLog("Med10");
        writeStopwatch.Start();
    }

    private void onReceiveData(object sender, EmgDataEventArgs data)
    {
        Dictionary<string, object> emgData = new Dictionary<string, object>() {
                            {"EMG1", data.Emg[0]},
                            {"EMG2", data.Emg[1]},
                            {"EMG3", data.Emg[2]},
                            {"EMG4", data.Emg[3]},
                            {"EMG5", data.Emg[4]},
                            {"EMG6", data.Emg[5]},
                            {"EMG7", data.Emg[6]},
                            {"EMG8", data.Emg[7]},
                        };

        loggingManager.Log("Med10", emgData);

    }

    public void StopLog() {
        cancellationTokenSource.Cancel();
        //sampleTask.Wait();
        writeStopwatch.Stop();
        loggingManager.SaveLog("Med10", false);
        TimeSpan writeTs = writeStopwatch.Elapsed;
        string writeElapsedTime = String.Format("{0:00}:{1:0000}",
            writeTs.Seconds, writeTs.Milliseconds);
        Debug.Log(" numbers appended in " + writeElapsedTime);
    }
}

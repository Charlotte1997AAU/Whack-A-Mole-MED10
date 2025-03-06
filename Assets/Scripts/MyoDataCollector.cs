using System;
using System.Collections.Concurrent;
using System.Runtime.InteropServices;
using System.Threading;
using UnityEngine;

public class MyoDataCollector : MonoBehaviour
{
    public int sampleRate = 200;
    private Thread myoThread;
    private bool isRunning = false;
    private ConcurrentQueue<float[]> emgDataQueue = new ConcurrentQueue<float[]>();

    private IntPtr myoHub;
    private IntPtr myoDevice;

    void Start()
    {
        if (!InitializeMyo())
        {
            Debug.LogError("Failed to initialize Myo.");
            return;
        }
        StartMyoDataThread();
    }

    bool InitializeMyo()
    {
        // Initialize Myo SDK
        if (MyoLibrary.myo_init_hub(out myoHub, "com.example.unity") != 0)
            return false;

        // Find the first Myo device
        myoDevice = MyoLibrary.myo_wait_for_myo(myoHub, 5000);
        if (myoDevice == IntPtr.Zero)
            return false;

        // Enable EMG streaming
        MyoLibrary.myo_set_stream_emg(myoDevice, 2);
        return true;
    }

    void StartMyoDataThread()
    {
        isRunning = true;
        myoThread = new Thread(CollectMyoData);
        myoThread.IsBackground = true;
        myoThread.Start();
    }

    void CollectMyoData()
    {
        float sampleInterval = 1f / sampleRate;

        while (isRunning)
        {
            float[] emgSample = GetMyoEMGData();
            emgDataQueue.Enqueue(emgSample);
            Thread.Sleep((int)(sampleInterval * 1000));
        }
    }

    void Update()
    {
        while (emgDataQueue.TryDequeue(out float[] emgSample))
        {
            ProcessMyoData(emgSample);
        }
    }

    float[] GetMyoEMGData()
    {
        sbyte[] emgRaw = new sbyte[8];

        if (myoDevice != IntPtr.Zero)
        {
            MyoLibrary.myo_read_emg(myoDevice, emgRaw);
        }

        float[] emgProcessed = new float[8];
        for (int i = 0; i < 8; i++)
        {
            emgProcessed[i] = emgRaw[i] / 128.0f; // Normalize data
        }

        return emgProcessed;
    }

    void ProcessMyoData(float[] emgSample)
    {
        Debug.Log($"EMG: {string.Join(", ", emgSample)}");
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (myoThread != null && myoThread.IsAlive)
            myoThread.Join();

        if (myoHub != IntPtr.Zero)
            MyoLibrary.myo_shutdown_hub(myoHub);
    }
}

static class MyoLibrary
{
    private const string MyoDLL = "myo.dll"; // Use "libmyo.dylib" for Mac

    [DllImport(MyoDLL)]
    public static extern int myo_init_hub(out IntPtr hub, string appId);

    [DllImport(MyoDLL)]
    public static extern IntPtr myo_wait_for_myo(IntPtr hub, uint timeout);

    [DllImport(MyoDLL)]
    public static extern void myo_set_stream_emg(IntPtr myo, int mode);

    [DllImport(MyoDLL)]
    public static extern void myo_read_emg(IntPtr myo, sbyte[] emgData);

    [DllImport(MyoDLL)]
    public static extern void myo_shutdown_hub(IntPtr hub);
}

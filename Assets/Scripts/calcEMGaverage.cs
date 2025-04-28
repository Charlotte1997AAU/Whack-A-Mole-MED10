using System.Collections.Generic;
using UnityEngine;
using Thalmic.Myo;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class calcEMGaverage : MonoBehaviour
{
    [Header("UI Elements")]
    public TextMeshProUGUI percentageText;
    public Slider powerSlider;

    [Header("Settings")]
    public bool useEMA = true; // <-- Skift mellem EMA og Moving Average
    public float smoothingFactor = 0.1f; // For EMA
    public int smoothingWindow = 6;      // For Moving Average
    public float mvcRecordDuration = 5f;

    [Header("Debug/State")]
    public bool isCalibrated = false;
    private bool isRecordingMVC = false;

    private List<float> smoothingBuffer = new List<float>();
    private float runningSum = 0f; // Til Moving Average

    private List<float> mvcRecordingBuffer = new List<float>();
    private float maxBaselineValue = 1f;
    public ThalmicMyo thalmicMyo;
    private List<float> temporaryValues = new List<float>();
    private float rawEMG;

    private float smoothedValue = 0f; // EMA værdi

    void Start()
    {
        thalmicMyo._myo.EmgData += onReceiveData;
    }

    void Update()
    {
        float rectified = Mathf.Abs(rawEMG);
        rectified = Mathf.Clamp(rectified, 0f, 128f);

        if (useEMA)
        {
            // EMA smoothing
            smoothedValue = (smoothingFactor * rectified) + (1f - smoothingFactor) * smoothedValue;
        }
        else
        {
            // Moving Average smoothing
            smoothingBuffer.Add(rectified);
            runningSum += rectified;

            if (smoothingBuffer.Count > smoothingWindow)
            {
                runningSum -= smoothingBuffer[0];
                smoothingBuffer.RemoveAt(0);
            }

            if (smoothingBuffer.Count > 0)
                smoothedValue = runningSum / smoothingBuffer.Count;
            else
                smoothedValue = 0f;
        }

        if (Input.GetKeyDown(KeyCode.Space) && !isRecordingMVC && !isCalibrated)
        {
            StartCoroutine(RecordMVC());
        }

        if (isCalibrated)
        {
            float percentage = (smoothedValue / maxBaselineValue) * 100f;
            percentage = Mathf.Clamp(percentage, 0f, 100f);

            percentageText.text = percentage.ToString("F0") + "%";
            if (powerSlider != null)
                powerSlider.value = percentage / 100f;
        }
        else
        {
            percentageText.text = "Calibrating...";
        }

        // BONUS: Skift mellem EMA/Moving Average med en tast (ekstra feature)
        if (Input.GetKeyDown(KeyCode.T))
        {
            useEMA = !useEMA;
            Debug.Log("Smoothing mode toggled. Now using " + (useEMA ? "EMA" : "Moving Average"));
            ResetSmoothing(); // Ryd buffer når vi skifter metode
        }
    }

    IEnumerator RecordMVC()
    {
        Debug.Log("Starting MVC recording for " + mvcRecordDuration + " seconds...");
        isRecordingMVC = true;
        mvcRecordingBuffer.Clear();

        float startTime = Time.time;
        while (Time.time - startTime < mvcRecordDuration)
        {
            mvcRecordingBuffer.Add(smoothedValue);
            yield return null;
        }

        maxBaselineValue = 0f;
        foreach (float value in mvcRecordingBuffer)
        {
            if (value > maxBaselineValue)
                maxBaselineValue = value;
        }

        Debug.Log("MVC recording done. Max baseline: " + maxBaselineValue);
        isRecordingMVC = false;
        isCalibrated = true;
    }

    private void onReceiveData(object sender, EmgDataEventArgs data)
    {
        temporaryValues.Clear();
        for (int i = 0; i < 8; i++)
        {
            temporaryValues.Add(data.Emg[i]);
        }

        float averageEMG = 0f;
        foreach (float ch in temporaryValues)
            averageEMG += Mathf.Abs(ch);

        averageEMG /= temporaryValues.Count;
        rawEMG = averageEMG;
    }

    private void ResetSmoothing()
    {
        smoothingBuffer.Clear();
        runningSum = 0f;
        smoothedValue = 0f;
    }
}

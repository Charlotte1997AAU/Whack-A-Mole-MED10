using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Thalmic.Myo;
using System.Linq;
using TMPro;

public class emgContractionVisual : MonoBehaviour
{
    public ThalmicMyo thalmicMyo;
    private List<float> temporaryValues = new List<float>(); // Holds data temporarily for each frame
    private List<float> rectifiedValues = new List<float>(); // Holds the standardized values of the frame
    private List<float> MVCRectified = new List<float>();
    private List<float> MVCdata = new List<float>();
    public TextMeshProUGUI textField;
    private float rectifiedAverage;
    private float updateInterval = 1f / 10f;  // Interval of 30 Hz (30 updates per second, or 1/30 seconds)
    private float timeSinceLastUpdate = 0f;  // Tracks the time since the last update
    public resetPosition getMVC;
    private float min;
    private float max;

    // Start is called before the first frame update
    void Start()
    {
        thalmicMyo._myo.EmgData += onReceiveData;
    }

    private void onReceiveData(object sender, EmgDataEventArgs data)
    {
        // Add incoming EMG values to the temporary list each frame
        for (int i = 0; i < 8; i++)
        {
            if(getMVC.getMVC)
            {
                float rectifiedValue = Mathf.Abs(data.Emg[i]);
                MVCRectified.Add(rectifiedValue);
                MVCdata.Add(rectifiedValue); // Store the rectified sample directly
                min = MVCdata.Min();
                max = MVCdata.Max();
            }
            else
            {
                temporaryValues.Add(data.Emg[i]);

                RectifyData(temporaryValues);
                temporaryValues.Clear();
            }
        }

        // Process data and calculate the rectified average every frame
    }

    // Rectify all data in the temporary list (take absolute values) and calculate the average
    private float RectifyData(List<float> emgValues)
    {
        if (emgValues.Count == 0) return 0; // Don't process if the list is empty

        // Clear the rectified values list to store the newly rectified values
        rectifiedValues.Clear();

        // Take the absolute value of each item in the temporary list and store it in the rectified list
        foreach (float value in emgValues)
        {
            rectifiedValues.Add(Mathf.Abs(value)); // Take the absolute value (rectification)
        }

        // Calculate the rectified average for this frame
        rectifiedAverage = CalculateAverage(rectifiedValues);
        return rectifiedAverage;
    }

    private float calculateMapping(float emgAverage)
    {
        float mappedValue = (emgAverage - min) / (max - min) * (100f - 0f) + 0f;
        return mappedValue;
    }

    // Calculate the average of the list
    private float CalculateAverage(List<float> values)
    {
        if (values.Count == 0) return 0f;
        float sum = 0f;
        foreach (float value in values)
        {
            sum += value;
        }
        return sum / values.Count;
    }

    void Update()
    {
        // Accumulate time since last frame
        timeSinceLastUpdate += Time.deltaTime;

        // Check if enough time has passed (about 1/30th of a second)
        if (timeSinceLastUpdate >= updateInterval)
        {
            // Update the text field with the rectified average, rounded to 2 decimal places
            textField.text = calculateMapping(rectifiedAverage).ToString("F2");

            // Reset the timer
            timeSinceLastUpdate = 0f;
        }
    }
}


using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class SliderFill : MonoBehaviour
{
    public Slider slider;
    public float elapsedTime = 0f;
    public bool isFilling = false;

    private float startValue;
    private float targetValue = 1f;

    private void Start()
    {
        startValue = slider.value;
    }

    public void FillSliderOverTime(float duration)
    {
        if (elapsedTime < duration)
        {
            elapsedTime += Time.deltaTime; // Increment elapsed time
            slider.value = Mathf.Lerp(startValue, targetValue, elapsedTime / duration);
        }
        else
        {
            slider.value = 0; // Ensure slider is filled at the end
            isFilling = false; // Stop filling once completed
        }
    }


    public void resetTimer()
    {
        slider.value = 0;
        elapsedTime = 0f;
        isFilling = false; // Optionally stop the filling
    }

}

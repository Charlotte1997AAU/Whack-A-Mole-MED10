using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class SliderFill : MonoBehaviour
{
    public Slider slider;

    public IEnumerator FillSliderOverTime(float duration)
    {
        float startValue = slider.value;
        float targetValue = 1f; // Full slider value
        float elapsedTime = 0f;  // Reset elapsed time at the start of the coroutine

        while (elapsedTime < duration)
        {
            elapsedTime += Time.deltaTime; // Increment elapsed time
            slider.value = Mathf.Lerp(startValue, targetValue, elapsedTime / duration);
            yield return null; // Wait for the next frame
        }

        slider.value = targetValue;
    }

    public void resetSlider()
    {
        slider.value = 0f;
    }
}

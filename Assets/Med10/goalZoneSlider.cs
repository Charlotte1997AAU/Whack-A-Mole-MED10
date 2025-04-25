using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; // <- You need this!

public class goalZoneSlider : MonoBehaviour
{
    public Slider slider;
    public RectTransform goalArea; // <- Corrected (capital R)

    public Vector2 firstGoalRange = new Vector2(0.25f, 0.35f);
    public Vector2 secondGoalRange = new Vector2(0.55f, 0.65f);

    private int activationCount = 0;

    void Start()
    {
        hideSlider();
    }

    public void UpdateGoalArea(float start, float end)
    {
        RectTransform sliderRect = slider.GetComponent<RectTransform>(); // <- Corrected (capital R)

        float sliderWidth = sliderRect.rect.width;
        float goalWidth = (end - start) * sliderWidth;
        float goalPosX = start * sliderWidth;

        goalArea.SetSizeWithCurrentAnchors(RectTransform.Axis.Horizontal, goalWidth);
        goalArea.anchoredPosition = new Vector2(goalPosX, goalArea.anchoredPosition.y);
    }

    public void OnCubeActivated()
    {
        if (activationCount % 2 == 0)
        {
            UpdateGoalArea(firstGoalRange.x, firstGoalRange.y);
        }
        else
        {
            UpdateGoalArea(secondGoalRange.x, secondGoalRange.y);
        }

        showSlider();
        activationCount++;
    }

    public void OnCubeDeactivated()
    {
        hideSlider();
    }

    private void showSlider()
    {
        slider.gameObject.SetActive(true);
    }

    private void hideSlider()
    {
        slider.gameObject.SetActive(false);
    }
}

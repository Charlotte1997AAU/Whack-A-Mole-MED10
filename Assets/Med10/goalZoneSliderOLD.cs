using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class goalZoneSliderOLD : MonoBehaviour
{
    public Slider slider;
    public RectTransform goalArea;

    public Vector2 firstGoalRange = new Vector2(0.25f, 0.35f);
    public Vector2 secondGoalRange = new Vector2(0.55f, 0.65f);

    private int activationCount = 0;

    void Start()
    {
        hideSlider();
    }

    public void UpdateGoalArea(float start, float end)
    {
        RectTransform sliderRect = slider.GetComponent<RectTransform>();

        float sliderHeight = sliderRect.rect.height;  // Use height for vertical slider
        float goalHeight = (end - start) * sliderHeight;
        float goalPosY = start * sliderHeight;

        goalArea.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, goalHeight);

        goalArea.anchoredPosition = new Vector2(goalArea.anchoredPosition.x, goalPosY);
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
        SetSliderVisible(true);
    }

    private void hideSlider()
    {
        SetSliderVisible(false);
    }

    private void SetSliderVisible(bool visible)
    {
        CanvasRenderer[] renderers = slider.GetComponentsInChildren<CanvasRenderer>();
        foreach (var renderer in renderers)
        {
            renderer.SetAlpha(visible ? 1f : 0f);
        }
    }
}

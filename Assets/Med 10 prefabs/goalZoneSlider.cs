using UnityEngine;
using UnityEngine.UI;

public class goalZoneSlider : MonoBehaviour
{
    public Slider slider;
    public RectTransform highlightImage;

    private float idealMin = 30f;
    private float idealMax = 40f;

    private float firstGoalMin = 45;
    private float firstGoalMax = 55;
    private float secondGoalMin = 45;
    private float secondGoalMax = 55;
    public float offsetY;
    public float offsetX;

    private int activationCount = 0;

    private bool isVertical;

    void Start()
    {
        isVertical = (slider.direction == Slider.Direction.BottomToTop || slider.direction == Slider.Direction.TopToBottom);
        UpdateHighlight();
        hideSlider();
    }

    void Update()
    {
        UpdateHighlight();
    }

    void UpdateHighlight()
    {
        float minNormalized = Mathf.InverseLerp(slider.minValue, slider.maxValue, idealMin);
        float maxNormalized = Mathf.InverseLerp(slider.minValue, slider.maxValue, idealMax);

        if (isVertical)
        {
            // For vertical slider: set Y anchors
            highlightImage.anchorMin = new Vector2(highlightImage.anchorMin.x, minNormalized);
            highlightImage.anchorMax = new Vector2(highlightImage.anchorMax.x, maxNormalized);
        }
        else
        {
            // For horizontal slider: set X anchors
            highlightImage.anchorMin = new Vector2(minNormalized, highlightImage.anchorMin.y);
            highlightImage.anchorMax = new Vector2(maxNormalized, highlightImage.anchorMax.y);
        }

        highlightImage.offsetMin = Vector2.zero; // Reset offsets to avoid misalignment
        highlightImage.offsetMax = Vector2.zero;
    }

    public void OnCubeActivated()
    {
        if (activationCount % 2 == 0)
        {
            idealMin = firstGoalMin;
            idealMax = firstGoalMax;

        }
        else
        {
            idealMin = secondGoalMin;
            idealMax = secondGoalMax;
        }

        UpdateHighlight();
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

    public void changePosition(Vector3 activeCubePos)
    {
        Vector3 newSliderPos = activeCubePos + new Vector3(offsetX, offsetY, 0);
        slider.transform.position = newSliderPos;

    }
}


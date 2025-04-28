using UnityEngine;
using UnityEngine.UI;

public class sliderHighlightUniversal: MonoBehaviour
{
    public Slider slider;
    public RectTransform highlightImage;

    public float idealMin = 30f;
    public float idealMax = 40f;

    private bool isVertical;

    void Start()
    {
        isVertical = (slider.direction == Slider.Direction.BottomToTop || slider.direction == Slider.Direction.TopToBottom);
        UpdateHighlight();
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
}

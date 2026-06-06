---
title: Enhance Contrast
description: Histogram-based contrast stretching and equalisation.
---

The **Enhance Contrast** command improves image visibility by adjusting the intensity distribution.

## Parameters

| Parameter | Description |
|---|---|
| **Saturated pixels** | Fraction of pixels (%) to clip at each end of the histogram when stretching |
| **Normalize** | Rescale the histogram so the full intensity range is used |
| **Equalize histogram** | Redistribute intensities to flatten the histogram, maximising local contrast |

## Modes

### Normalize

Stretches the histogram so the darkest non-clipped pixel maps to 0 and the brightest maps to 65535 (for 16-bit). The **Saturated pixels** parameter allows a small fraction of extreme values to be clipped, which prevents a few bright outliers from compressing the rest of the range.

### Equalize histogram

Applies histogram equalization: each intensity value is remapped so that the cumulative distribution becomes uniform. This enhances local contrast in images where the signal occupies only a narrow portion of the available range.

## When to use

Enhance Contrast can improve visibility in the live preview or in exported control images. For analysis pipelines, normalisation before thresholding can reduce sensitivity to exposure variation between images.

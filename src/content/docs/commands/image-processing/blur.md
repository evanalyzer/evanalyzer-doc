---
title: Blur
description: Box (average) blur for noise reduction.
---

The **Blur** command applies a box (mean) filter to the image. Every pixel is replaced by the average intensity of its surrounding neighbourhood.

## When to use

Use Blur as a fast, lightweight noise-reduction step before segmentation. For better edge preservation, consider [Gaussian Blur](/commands/image-processing/gaussian-blur/) instead.

## Parameters

| Parameter | Description |
|---|---|
| **Kernel size** | Side length of the averaging kernel in pixels (must be odd; range 3–27) |

### Kernel size guidance

- **3–5** — subtle smoothing, preserves fine structure
- **7–11** — moderate noise reduction for typical fluorescence images
- **13+** — heavy smoothing; fine structures may be lost

## Notes

In image processing, a *kernel* (convolution matrix) is a small matrix applied to each pixel and its neighbours. A box blur kernel fills every element with 1/N, replacing each pixel with the neighbourhood mean.

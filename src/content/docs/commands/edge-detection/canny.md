---
title: Canny Edge Detection
description: Multi-stage edge detection with non-maxima suppression and hysteresis thresholding.
---

The **Canny Edge Detection** command detects edges by computing image gradients, suppressing non-maximal responses, and applying dual-threshold hysteresis to produce thin, clean edges.

## When to use

Use Canny when you need precise, thin edge maps. Compared to [Sobel](/commands/edge-detection/sobel/), Canny is more accurate but slower. It is well-suited as preprocessing for contour-based segmentation.

## Parameters

| Parameter         | Description                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| **Kernel size**   | Size of the Gaussian smoothing kernel applied before gradient computation (range 3–27) |
| **Threshold min** | Lower hysteresis threshold - edges weaker than this are discarded                      |
| **Threshold max** | Upper hysteresis threshold - edges stronger than this are always retained              |

### Hysteresis thresholding

Edges with gradient magnitude between the two thresholds are kept only if they are connected to a strong edge (above the upper threshold). This produces cleaner, more continuous edge maps than a single-threshold approach.

## Notes

A larger kernel size increases smoothing before gradient computation, making the detector less sensitive to fine noise at the cost of detecting coarser edges. As a starting point try `kernel_size=3`, `threshold_min=0.1`, `threshold_max=0.3`.

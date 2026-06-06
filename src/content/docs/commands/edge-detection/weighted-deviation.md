---
title: Weighted Deviation
description: Gaussian-weighted local standard deviation for texture and edge detection.
---

The **Weighted Deviation** command computes the Gaussian-weighted local standard deviation at each pixel. Pixels in smooth, uniform regions produce low values; pixels in textured or edge regions produce high values.

## When to use

Use Weighted Deviation to:
- Highlight regions with high local variation (edges, textures) while suppressing uniform areas.
- Create a feature image for thresholding heterogeneous structures.

## Parameters

| Parameter | Description |
|---|---|
| **Kernel size** | Size of the local window (range 3–27) |
| **Sigma** | Standard deviation of the Gaussian weighting within the window |

A larger kernel size and higher sigma increases the scale of the detected variation. Smaller values respond to fine-grained texture.

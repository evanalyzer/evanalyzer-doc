---
title: Sobel Edge Detection
description: Fast gradient-magnitude edge detection using Sobel operators.
---

The **Sobel Edge Detection** command computes the gradient magnitude of the image using horizontal and vertical Sobel kernels. Each pixel in the output represents the local rate of intensity change.

## When to use

Sobel is faster and simpler than [Canny](/commands/edge-detection/canny/), making it suitable for real-time preview or as a feature extraction step feeding into a threshold. Edges are broader and less precise than Canny but the computation is significantly faster.

## Parameters

| Parameter | Description |
|---|---|
| **Kernel size** | Size of the Sobel kernel (range 3–27) |

Larger kernel sizes smooth gradients over a wider neighbourhood before computing the magnitude, reducing noise sensitivity but producing thicker edges.

---
title: Median Subtract
description: Subtract a median-filtered version of the image to remove smooth background.
---

The **Median Subtract** command estimates the local background by computing a median-filtered version of the image and subtracting it from the original. The result retains only the features that differ from the local median — typically small bright objects on a smooth background.

## When to use

Use Median Subtract as an alternative to [Rolling Ball](/commands/image-processing/rolling-ball/) when the background variation is not gradual but is best captured by a local median.

## Parameters

| Parameter | Description |
|---|---|
| **Radius** | Radius of the median filter window in pixels |

A larger radius estimates the background over a wider area. The radius should be larger than the largest object of interest so those objects do not distort the background estimate.

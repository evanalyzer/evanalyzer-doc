---
title: Rank Filter
description: Non-linear min, median, or max neighbourhood filter.
---

The **Rank Filter** collects pixel intensities in a circular neighbourhood, sorts them by value, and replaces the centre pixel with the value at a chosen rank.

## Filter types

| Type | Rank | Common use |
|---|---|---|
| **Minimum** | Lowest value | Background estimation; erosion-like effect on bright objects |
| **Median** | Middle value | Impulse noise removal while preserving edges |
| **Maximum** | Highest value | Dilation-like effect; filling small gaps in bright regions |

## When to use

- **Median** — the most common choice for salt-and-pepper or impulse noise removal before thresholding.
- **Minimum / Maximum** — morphological-style operations when you need a non-linear, non-Gaussian effect.

## Parameters

| Parameter | Description |
|---|---|
| **Radius** | Radius of the circular neighbourhood in pixels |
| **Filter type** | *Minimum*, *Median*, or *Maximum* |

Larger radius values affect a wider neighbourhood and produce a stronger effect. Unlike convolution-based filters, rank filters are non-linear and cannot be described by a kernel matrix.

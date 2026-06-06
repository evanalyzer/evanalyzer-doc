---
title: Watershed
description: Split touching objects by flooding from intensity peaks.
---

The **Watershed** command separates objects that are close together or touching by treating pixel intensities as altitude and finding the valleys between peaks. It is placed after [Connected Components](/commands/segmentation/connected-components/).

## When to use

Use Watershed when high object density causes nearby objects to be detected as a single merged region after thresholding. Typical scenarios:
- Dense vesicle populations
- Touching cell nuclei

:::caution[Performance]
Watershed is a computationally expensive algorithm. Enable it only when necessary, as it significantly increases analysis time.
:::

## Parameters

| Parameter | Description |
|---|---|
| **Maximum finder tolerance** | Controls sensitivity to local intensity peaks. Range: 0.0–1.0. Lower values detect more (smaller) peaks and split more aggressively; higher values require more prominent peaks. |

## How it works

1. The distance-transform of the binary mask is computed.
2. Local maxima in the distance map are found using the tolerance parameter.
3. Each maximum is treated as a "seed" and the mask is flooded outward from each seed simultaneously.
4. Where the flooding fronts from different seeds meet, a watershed line is drawn.

The implementation is ported from [ImageJ](https://imagej.net/imaging/watershed).

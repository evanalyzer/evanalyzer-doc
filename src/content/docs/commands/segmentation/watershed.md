---
title: Watershed
description: Split touching objects by flooding from intensity peaks.
---

The **Watershed** command separates objects that are close together or touching by treating pixel intensities as altitude and finding the valleys between peaks. It is placed after [Connected Components](/commands/segmentation/connected-components/).

![Two touching blobs are split by flooding out from each distance-map peak until the fronts meet](../../../../assets/figures/cmd-watershed.svg)

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

1. The Euclidean distance transform of the binary mask is computed - every foreground pixel's value becomes its distance to the nearest background pixel, so the "deepest" interior of each blob becomes a local peak.
2. Local maxima in the distance map are found; nearby maxima that don't stick up above their connecting ridge by more than the tolerance are merged into one, which is what keeps noisy, near-flat peaks from over-splitting a single round object.
3. Each surviving maximum is a seed; the mask floods outward from every seed simultaneously, growing downhill.
4. Where two floods meet, a one-pixel-wide watershed line is drawn, splitting the original merged region into separate objects.

This is a faithful port of ImageJ's `Process > Binary > Watershed` (its `MaximumFinder` class applied to the distance map), so results should match ImageJ pixel-for-pixel for the same input.

## Background

The distance-map/immersion approach to watershed segmentation was formalized by Luc Vincent and Pierre Soille, "Watersheds in Digital Spaces: An Efficient Algorithm Based on Immersion Simulations," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 13, no. 6, pp. 583-598, 1991. The specific tolerance-based maximum-merging strategy ported here originates in ImageJ/Fiji - see Schindelin et al., "Fiji: An Open-Source Platform for Biological-Image Analysis," *Nature Methods*, vol. 9, pp. 676-682, 2012.

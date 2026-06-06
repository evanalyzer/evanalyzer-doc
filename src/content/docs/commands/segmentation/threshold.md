---
title: Threshold
description: Convert a greyscale image to a binary mask using manual or automatic thresholds.
---

The **Threshold** command is the primary segmentation step. It converts a greyscale image to a binary mask: pixels with intensity below the minimum threshold become 0 (background); pixels above become 65535 (foreground).

The output of Threshold feeds directly into [Connected Components](/commands/segmentation/connected-components/).

## Single threshold

Define one threshold entry to produce a simple binary mask:

| Parameter | Description |
|---|---|
| **Method** | *Manual* or one of the auto-threshold algorithms |
| **Min threshold** | Minimum intensity to include as foreground |
| **Max threshold** | Maximum intensity to include as foreground (set to 65535 to disable) |
| **Unit** | Intensity unit (*Absolute* 0–65535, *Percent* 0–100, or *Relative* 0–1) |
| **Object class** | The segmentation class assigned to objects detected by this threshold entry |

:::tip
Examine the image histogram to choose a starting value for the minimum threshold. Set it just above the highest background pixel intensity.
:::

:::caution
Always set a **minimum threshold greater than zero** even when using an auto-threshold method. Control images containing only background noise will otherwise produce false-positive detections.
:::

## Multiple threshold classes

Click **+ Add** to define additional threshold entries for the same image. Each entry uses a different intensity range and assigns a different segmentation class, allowing two or more object populations to be detected from one image in a single step.

Under the hood, each threshold class maps to a distinct greyscale value in the binary output (65535 for the first class, decrementing for subsequent classes). [Connected Components](/commands/segmentation/connected-components/) and [Extract ROIs](/commands/object/extract-rois/) use these values to distinguish the populations.

## Auto-threshold algorithms

When **Method** is not *Manual*, EVAnalyzer analyses the image histogram and computes a threshold automatically. Available methods include Otsu, Triangle, Mean, and others.

Auto-thresholds can fail on empty images (no objects, only noise) because they always find a separation. Prevent this by setting a non-zero **Min threshold** as a lower bound: if the computed value falls below it, EVAnalyzer uses the minimum instead.

## Maximum threshold

Setting **Max threshold** to a value below 65535 restricts detection to pixels within the `[min, max]` range. This allows extraction of a specific intensity band — for example to separate bright artefacts from dim objects, or to extract the background itself by setting Min to 0 and Max to just below the signal level.

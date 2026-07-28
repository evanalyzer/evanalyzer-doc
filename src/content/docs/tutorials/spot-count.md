---
title: Spot Count
description: Count extracellular vesicles or fluorescent spots in a single image channel.
---

This tutorial guides you through the **Spot Count** workflow - detecting and counting fluorescent spots (e.g. extracellular vesicles) in one image channel, with optional removal of calibration bead artefacts.

The workflow uses two pipelines:

1. **EV Detection** - detects spots in the EV channel.
2. **Tetraspeck** (optional) - detects calibration beads and removes any EV detections that coincide with them.

## Prerequisites

- Fluorescence microscopy images containing EVs/spots in at least one channel.
- Tetraspeck bead images in a separate channel (optional).

## Step 1: Project Setup

1. Open EVAnalyzer and set the **Image directory** to your image folder.
2. Set a **Job name** (e.g. `spot-count-01`).
3. If your images are from a plate experiment, configure **Grouping** and the filename regex.

## Step 2: Define Classes

In the **Classification** tab, add:

- `ch1@spot` - the EV/spot class (adjust the prefix to match your fluorophore)
- `tetraspeck@spot` - the calibration bead class (only if using the Tetraspeck pipeline)

## Step 3: EV Detection Pipeline

Create a new pipeline named `EV Detection` and add the following steps in order:

| Step                                                                                                   | Settings                                                                  |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| [Rolling Ball](/commands/image-processing/rolling-ball/)                                               | Radius: 4, Type: Paraboloid - removes uneven background                   |
| [Gaussian Blur](/commands/image-processing/gaussian-blur/) or [Blur](/commands/image-processing/blur/) | Kernel: 3, repeat 2× - reduces noise artefacts                            |
| [Threshold](/commands/segmentation/threshold/)                                                         | Method: Manual - **adapt to your images**; start with Min: 200            |
| [Connected Components](/commands/segmentation/connected-components/)                                   | Min size: 3–10 px² recommended to suppress single-pixel noise            |
| [Watershed](/commands/segmentation/watershed/)                                                         | Tolerance: 0.5 - separates closely touching spots                         |
| [Extract Objects](/commands/object/extract-objects/)                                                   | No settings                                                               |
| [Classify Objects](/commands/object/classify-objects/)                                                 | Target: `ch1@spot`; Min area: 3 px²; Min circularity: 0.1                 |
| [Save Image](/commands/object/save-image/)                                                             | Path: `images/${imageName}` - save a control image (remove if not needed) |

:::tip[Threshold selection]
Open the **advanced preview** to display the image histogram alongside the segmentation result. Set the minimum threshold just above the highest background-noise peak.
:::

## Step 4: Tetraspeck Pipeline (optional)

If you have a dedicated calibration-bead channel, create a second pipeline named `Tetraspeck`:

| Step                                                      | Settings                                                                                                                                                                                      |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rolling Ball                                              | Radius: 4, Type: Paraboloid                                                                                                                                                                   |
| Gaussian Blur                                             | Kernel: 3, repeat 2×                                                                                                                                                                          |
| Threshold                                                 | Method: Manual - adapt to bead channel                                                                                                                                                        |
| Connected Components                                      | -                                                                                                                                                                                             |
| Watershed                                                 | Tolerance: 0.5                                                                                                                                                                                |
| Extract Objects                                              | -                                                                                                                                                                                             |
| Classify Objects                                             | Target: `tetraspeck@spot`; Min area: 5 px²                                                                                                                                                    |
| [Classify Objects](/commands/object/classify-objects/) (second) | Source: `ch1@spot`; Intersects with: `tetraspeck@spot`; Target: `tetraspeck@spot` - moves any EV spot that overlaps a bead to the tetraspeck class, effectively removing it from the EV count |

## Step 5: Run and Inspect

Click **Play** to run the analysis. When complete:

- Open the results viewer and check the `ch1@spot` count per image.
- Open control images in the `images/` subfolder to visually verify segmentation.
- Adjust the threshold and rerun if objects appear over- or under-segmented.

## Tips

- The **Tetraspeck** pipeline should be **disabled** if no calibration bead channel is available.
- Add a [Classify Objects](/commands/object/classify-objects/) step after the EV classifier with additional filters (e.g. `Min area: 10`) to gate the population further without rerunning the full analysis.

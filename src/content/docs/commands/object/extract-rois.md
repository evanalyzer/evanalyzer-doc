---
title: Extract ROIs
description: Convert labelled binary regions into segmentation-class objects.
---

The **Extract ROIs** command reads the labelled image produced by [Connected Components](/commands/segmentation/connected-components/) (or [Watershed](/commands/segmentation/watershed/)) and creates one segmentation-class object per labelled region. These objects are the raw candidates passed to [Classify ROIs](/commands/object/classify-rois/) for final filtering and class assignment.

## Parameters

| Parameter | Description |
|---|---|
| **Max objects before fail** | Hard upper limit on the number of regions extracted. If more regions are found the pipeline step fails, preventing runaway processing on misconfigured segmentation (default: –1 = unlimited) |

## Pipeline position

```
Threshold → Connected Components → [Watershed] → Extract ROIs → Classify ROIs
```

Extract ROIs is always followed by [Classify ROIs](/commands/object/classify-rois/). The segmentation class assigned here is the intermediate class used internally; the final named object class is assigned by Classify ROIs.

:::note[New in EVAnalyzer vs ImageC]
In the predecessor application (ImageC), region extraction and classification were combined into a single *Classifier* step. EVAnalyzer splits them into Extract ROIs (geometry extraction) and Classify ROIs (filtering + class assignment) for greater flexibility and clearer pipeline structure.
:::

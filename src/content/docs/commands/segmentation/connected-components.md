---
title: Connected Components
description: Label each connected foreground region with a unique ID.
---

The **Connected Components** command scans the binary mask produced by [Threshold](/commands/segmentation/threshold/) and assigns a unique integer label to each connected group of foreground pixels. Each labelled region is one candidate object.

## When to use

Connected Components is a required intermediate step between Threshold and Extract ROIs. It separates the monolithic foreground mask into individually labelled regions that can be further split by [Watershed](/commands/segmentation/watershed/) or immediately passed to [Extract ROIs](/commands/object/extract-rois/).

## Parameters

This command has no configurable parameters. It operates on the binary mask from the previous step and outputs a labelled image.

## Pipeline position

```
Threshold → Connected Components → [optional Watershed] → Extract ROIs
```

:::note[New in EVAnalyzer vs ImageC]
Connected Components is an explicit pipeline step in EVAnalyzer. In the predecessor ImageC, this step was automatically performed inside the classifier command. Making it explicit allows more control over the segmentation pipeline.
:::

---
title: Metrics
description: Complete reference of all object metrics and statistics available in EVAnalyzer.
---

EVAnalyzer measures a set of metrics for every detected object and stores them in the results database. Metrics are visible in the results table and can be exported to XLSX or R.

## Available Metrics

| Metric | Description |
|---|---|
| **Count** | Number of detected objects in the image |
| **Area size** | Object area in px² |
| **Perimeter** | Object boundary length |
| **Circularity** | Roundness (0–1; 1 = perfect circle) |
| **Solidity** | Ratio of object area to convex hull area |
| **Aspect ratio** | Ratio of bounding box width to height |
| **Eccentricity** | Elongation measure from the fitted ellipse (0 = circle, 1 = line) |
| **Feret diameter** | Maximum calliper diameter of the object |
| **Intensity min** | Minimum pixel intensity within the object |
| **Intensity max** | Maximum pixel intensity within the object |
| **Intensity avg** | Mean pixel intensity within the object |
| **Intensity sum** | Sum of all pixel intensities within the object |
| **Center of mass X** | X coordinate of the centre of mass |
| **Center of mass Y** | Y coordinate of the centre of mass |
| **Intersection** | Number of objects from another class that overlap this object |
| **Colocalization partner count / IDs** | Per colocalization partner class: how many of that class's objects this object colocalises with, and their object IDs (see [Colocalization](/commands/object/colocalization/)) |
| **Object ID** | Unique object identifier within a run |
| **Origin object ID** | Object ID of the source when this object was copied by reclassification |
| **Parent object ID** | Object ID of the parent when this object was reclassified by intersection |
| **Tracking ID** | Shared ID linking related objects (e.g. colocalising spots) |
| **Distance from object ID** | Object ID of the "from" object in a distance measurement |
| **Distance to object ID** | Object ID of the "to" object in a distance measurement |
| **Distance centre to centre** | Centroid-to-centroid distance |
| **Distance centre to surface min** | Shortest centroid-to-boundary distance |
| **Distance centre to surface max** | Longest centroid-to-boundary distance |
| **Distance surface to surface min** | Shortest boundary-to-boundary distance |
| **Distance surface to surface max** | Longest boundary-to-boundary distance |

Intensity metrics are calculated independently for each image channel/plane that is configured in the [Classify ROIs](/commands/object/classify-rois/) step.

## Statistics

Statistics are computed per-image (Image view) and aggregated per-well (Plate view):

| Statistic | Image view | Plate view |
|---|---|---|
| **CNT** | Count of objects | Count of objects across the well |
| **AVG** | Mean value across objects | Mean of per-image averages |
| **MEDIAN** | Median value across objects | Mean of per-image medians |
| **MIN** | Minimum value across objects | Mean of per-image minimums |
| **MAX** | Maximum value across objects | Mean of per-image maximums |
| **STDEV** | Standard deviation across objects | Mean of per-image standard deviations |
| **SUM** | Sum of values across objects | Mean of per-image sums |

## Configuring Default Metrics

The columns shown when you first open a results file are controlled by the **Default metrics** setting in each class's [Class Editor](/guide/classification/). This can be changed at any time without re-running the analysis.

To add extra columns in an open results file, click the **Add column** button and select from the full metrics list.

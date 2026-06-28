---
title: Objects
description: What objects are, how they are identified, and the relationships between them.
---

An **object** is the result of an image classification step. It represents a quantified region of interest (ROI) extracted from an image plane and stored in the results database.

Every object is assigned to exactly one [object class](/guide/classification/). Together with the class assignment, a set of geometric and intensity metrics is calculated and stored.

## Object Metrics Overview

See [Metrics](/fundamentals/metrics/) for the full table of available measurements.

### Area Size

The count of non-black pixels inside the object boundary. Unit: px².

### Perimeter

The boundary length of the object. The algorithm counts straight edges as 1 pixel and corner transitions as √2 pixels.

$$
P = \text{boundary length} - (2 - \sqrt{2}) \times \text{non-adjacent corners}
$$

### Circularity

How closely the object resembles a circle. Range: 0 (linear) to 1 (perfect circle).

$$
c = \frac{4\pi \cdot \text{AreaSize}}{P^2}
$$

### Centroid (Position)

The geometrical centre of the object, calculated from first-order spatial moments:

$$
c_x = \frac{m_{10}}{m_{00}}, \quad c_y = \frac{m_{01}}{m_{00}}
$$

### Bounding Box

The smallest axis-aligned rectangle that contains all pixels of the object.

### Confidence

- **Threshold segmentation** - the threshold value that was used to extract the object. Range: 0–65535.

### Solidity, Aspect Ratio, Eccentricity, Feret Diameter

Additional shape descriptors available as filter criteria in [Classify ROIs](/commands/object/classify-rois/).

## Object Identifiers

### Object ID

A unique integer ID assigned to each object during a run, starting at 1. The ID is consistent within a single results file and is displayed in the results table when enabled.

Use the **With object ID** option in [Save Image](/commands/object/save-image/) to annotate the ID alongside the object in control images.

### Parent Object ID {#parent-object-id}

EVAnalyzer supports a parent–child hierarchy between objects. When [Classify ROIs](/commands/object/classify-rois/) or [Colocalization](/commands/object/colocalization/) is configured to intersect objects, the **parent object ID** of the child is set to the object ID of the containing parent.

An object can have at most one parent.

Example hierarchy:

- A **cell** object contains a **nucleus**.
- The nucleus's parent object ID is the cell's object ID.
- A **spot** inside the nucleus has the nucleus's object ID as its parent.

### Origin Object ID

When an object is duplicated (via a copy operation in [Classify ROIs](/commands/object/classify-rois/) or [Colocalization](/commands/object/colocalization/)), the new object records the origin object's ID. The origin ID propagates through further duplications.

### Tracking ID

Links objects that represent the same physical instance across different image channels or time frames. All objects sharing a tracking ID can be compared side by side in the results table.

Tracking IDs are assigned by the [Colocalization](/commands/object/colocalization/) command.

## Distance

EVAnalyzer calculates Euclidean distances between pairs of objects:

| Measurement                  | Description                                                        |
| ---------------------------- | ------------------------------------------------------------------ |
| **Centre-to-centre**         | Distance between the two centroids                                 |
| **Centre-to-surface (min)**  | Shortest distance from one centroid to the other object's boundary |
| **Centre-to-surface (max)**  | Longest distance from one centroid to the other object's boundary  |
| **Surface-to-surface (min)** | Shortest distance between the two boundaries                       |
| **Surface-to-surface (max)** | Longest distance between the two boundaries                        |

$$
d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}
$$

See [Distance Transform](/commands/object/distance-transform/) for how to measure distances.

## Intersection Count

The number of objects from another class that overlap with this object. Used as a filter criterion in [Classify ROIs](/commands/object/classify-rois/) and as input to [Colocalization](/commands/object/colocalization/).

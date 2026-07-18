---
title: Objects & Metrics
description: What objects are and the complete reference of all object metrics and statistics available in EVAnalyzer, with the formula behind each one.
---

An **object** is the result of an image classification step. It represents a quantified region of interest (ROI) extracted from an image plane and stored in the results database.

Every object is assigned to exactly one [object class](/guide/classification/). Together with the class assignment, a set of geometric, intensity, and relational metrics is calculated and stored - visible in the results table and exportable to CSV or XLSX.

## Geometric Metrics

### Area Size

The count of pixels inside the object's mask. Unit: px².

### Perimeter

The boundary length of the object, following ImageJ's boundary-walk algorithm: for every mask pixel, an orthogonal (up/down/left/right) neighbor that's background contributes 1, and a diagonal neighbor that's background contributes $\sqrt{2}$. Since every boundary contact is counted from both sides, the total is halved:

$$
P = \frac{N_{\text{orth}} + \sqrt{2} \, N_{\text{diag}}}{2}
$$

### Circularity

How closely the object resembles a circle, from its area and perimeter. Range: 0 (very irregular) to 1 (perfect circle).

$$
c = \frac{4\pi A}{P^2}
$$

### Roundness

Computed identically to [Circularity](#circularity) in the current implementation:

$$
r = \frac{4\pi A}{P^2}
$$

### Compactness

The reciprocal relationship to Circularity - lower is more compact (closer to a circle), higher means more perimeter for the enclosed area:

$$
k = \frac{P^2}{A} = \frac{4\pi}{c}
$$

### Solidity

Area divided by the area of the mask's convex hull (taken over the corners of its pixel squares, so the mask is always fully contained in its hull). Range: 0-1; 1 = perfectly convex, lower means more concave boundaries, bays, or holes.

$$
s = \frac{A}{A_{\text{hull}}}
$$

### Aspect Ratio

The ratio of the fitted ellipse's major to minor axis (see [Eccentricity](#eccentricity) for how the ellipse is fitted) - **not** the bounding box's width/height ratio.

$$
\text{AR} = \frac{\text{major axis}}{\text{minor axis}}
$$

### Eccentricity

Elongation of the object's fitted ellipse (0 = circle, approaching 1 = increasingly elongated). The ellipse is fitted from the mask's second-order central moments:

$$
\mu_{20} = \frac{\sum x^2}{A} - \bar{x}^2, \quad
\mu_{02} = \frac{\sum y^2}{A} - \bar{y}^2, \quad
\mu_{11} = \frac{\sum xy}{A} - \bar{x}\,\bar{y}
$$

$$
\text{major} = \sqrt{8\left(\mu_{20}+\mu_{02}+\Delta\right)}, \quad
\text{minor} = \sqrt{8\left(\mu_{20}+\mu_{02}-\Delta\right)}, \quad
\Delta = \sqrt{(\mu_{20}-\mu_{02})^2 + 4\mu_{11}^2}
$$

$$
e = \sqrt{1 - \left(\frac{\text{minor}}{\text{major}}\right)^{2}}
$$

### Feret Diameter

The diagonal of the object's axis-aligned bounding box - an approximation of the true maximum caliper diameter, not a rotating-calipers measurement:

$$
F = \sqrt{(x_{\max}-x_{\min})^2 + (y_{\max}-y_{\min})^2}
$$

### Min Feret Diameter

The minor axis length of the fitted ellipse described under [Eccentricity](#eccentricity) - an approximation of the true minimum caliper width.

### Center of Mass (Centroid)

Despite the name, this is the **center of the bounding box**, not an area- or intensity-weighted centroid:

$$
\left(c_x, c_y\right) = \left(\frac{x_{\min}+x_{\max}}{2},\ \frac{y_{\min}+y_{\max}}{2}\right)
$$

### Bounding Box

The smallest axis-aligned rectangle that contains all pixels of the object.

## Intensity Metrics

Calculated independently for each image channel/plane configured in the [Classify ROIs](/commands/object/classify-rois/) step, over the $n$ pixels of the object's mask:

$$
\text{Sum} = \sum_{i=1}^{n} v_i, \qquad
\text{Min} = \min_i v_i, \qquad
\text{Max} = \max_i v_i, \qquad
\text{Avg} = \frac{\text{Sum}}{n}
$$

## Object Identifiers

### Object ID

A unique integer ID assigned to each object during a run, starting at 1. The ID is consistent within a single results file and is displayed in the results table when enabled.

Use the **With object ID** option in [Save Image](/commands/object/save-image/) to annotate the ID alongside the object in control images.

### Parent Object ID

EVAnalyzer supports a parent-child hierarchy between objects. When [Classify ROIs](/commands/object/classify-rois/) or [Colocalization](/commands/object/colocalization/) is configured to intersect objects, the **parent object ID** of the child is set to the object ID of the containing parent.

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

## Distance Metrics

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

## Colocalization Partner Count / IDs

Per colocalization partner class: how many of that class's objects this object colocalises with, and their object IDs. See [Colocalization](/commands/object/colocalization/).

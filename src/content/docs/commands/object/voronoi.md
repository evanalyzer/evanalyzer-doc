---
title: Voronoi
description: Partition the image into regions based on the nearest object centre.
---

The **Voronoi** command constructs a Voronoi diagram from the centroid positions of a set of input objects. Each Voronoi cell is the region of the image closest to one particular centre point. The resulting cells are stored as objects of the configured output class.

A common use case is approximating cell boundaries from known nucleus positions when no cell-surface stain is available.

## Parameters

| Parameter | Description |
|---|---|
| **Centers** | Object class whose centroids are used as Voronoi seeds |
| **Center filter classes** | Additional classes used to refine which centres are included |
| **Mask** | An optional object class used to clip (intersect) the Voronoi cells |
| **Mask filter classes** | Additional classes used to refine the clipping mask |
| **Output class** | Object class assigned to the constructed Voronoi cells |
| **Max radius** | Maximum radius of a Voronoi cell (disabled if –1) |
| **Unit** | Size unit for max radius (*px*, *µm*, …) |
| **Exclude areas at edges** | Discard Voronoi cells that touch the image border |
| **Exclude areas without centre** | Discard cells that do not contain a seed point after masking |

## Max Radius

In sparse samples, Voronoi cells can grow arbitrarily large. Setting a **Max radius** limits cell size to a biologically meaningful maximum. Cells that would exceed the radius are truncated.

## Masking

When a **Mask** class is provided (e.g. a cell-area segmentation), Voronoi cells are intersected with the mask. Any cell area outside the mask is discarded.

:::tip
Enable **Exclude areas without centre** when combining Voronoi with a masking class. After masking, some residual areas may no longer contain their original seed point; this option removes those artefacts.
:::

:::tip[Typical configuration]
- **Centers**: `dapi@nucleus`
- **Mask**: segmented cell-body class (if available)
- **Output class**: `cell@voronoi`
:::

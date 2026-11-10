---
title: Measure Object Skeleton
description: Measure each skeleton's total length, longest path, end points, branch points and segments, and the mean diameter of the object it was made of.
---

**Measure Object Skeleton** measures the skeletons made by [Skeletonize Objects](/commands/object/skeletonize-objects/): for each skeleton its total length, the longest path through it, its end points, branch points and segments (the lines between them), their mean length and straightness, and - from the object it was made of - its mean diameter.

![A skeleton read as a graph: end points (green), a branch point (orange) and the three segments between them; the longest path (purple) runs from one end point to the farthest; the straightness of a segment compares its straight distance (dashed) with its length; the diameter is twice the distance from the skeleton to the outline of the object it was made of](../../../../assets/figures/cmd-measure-object-skeleton.svg)

Use it to compare how long and how branched neurites, vessels or fibres are. A typical pipeline:

[Skeletonize Objects](/commands/object/skeletonize-objects/) → [Relate Objects](/commands/object/relate-objects/) → **Measure Object Skeleton**

[Relate Objects](/commands/object/relate-objects/) is only needed for the diameter: it links each skeleton (child) to the object it was made of (parent). In a project file it is `MEASURE_OBJECT_SKELETON`.

## Parameters

| Parameter         | Description                                                                                                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**            | The step's ID, unique in the project. Its values' names in the results start with it (e.g. `skeleton_01`).                                                                              |
| **Objects**       | The skeletons measured (the **Skeleton Class** of Skeletonize Objects).                                                                                                                   |
| **Diameter From** | The class of the objects the skeletons were made of (e.g. the neurites), linked to them as their parents by Relate Objects. Unset (default): no diameter is measured.                    |

Without **Objects** the step stops with an error.

## Measurements

Seven values per skeleton, eight with **Diameter From**:

| Measurement             | Unit  | Description                                                                                       |
| ----------------------- | ----- | ------------------------------------------------------------------------------------------------- |
| **Total length**        | px    | The length of all the skeleton's lines.                                                           |
| **Longest path**        | px    | The longest of the shortest paths along the skeleton between two of its pixels.                  |
| **End points**          | count | The number of end points (pixels with one neighbour).                                            |
| **Branch points**       | count | The number of branch points (groups of pixels with three or more neighbours).                    |
| **Segments**            | count | The number of lines between end and branch points; a closed loop without either counts as one.    |
| **Mean segment length** | px    | The mean length of the segments.                                                                  |
| **Mean straightness**   | 0-1   | The mean over the segments of the straight distance between a segment's ends / its length.       |
| **Mean diameter**       | px    | Only with **Diameter From**: the mean width of the parent object along the skeleton.             |

Some values can be missing (stored as no number, NaN): **Mean segment length** without segments, **Mean straightness** without a segment that has two ends, **Mean diameter** for a skeleton without a parent of the **Diameter From** class.

## How it works

The skeleton is first thinned once more, as in steps 1 and 2 of [Skeletonize Objects](/commands/object/skeletonize-objects/#how-it-works) (without pruning). So an object that isn't a skeleton yet is measured as its skeleton. Then it is read as a graph of end points, branch points and the lines between them. Neighbours are the 8 surrounding pixels.

### Lengths

A step to a 4-neighbour is 1 px long, a diagonal step $\sqrt{2}$:

$$
L = n_{\text{straight}} + \sqrt{2}\, n_{\text{diagonal}}
$$

A diagonal step between two pixels that a 4-neighbour of both also connects (at the corner of a branch point) is not counted, so no stretch is counted twice. **Total length** is $L$ over all neighbouring pixel pairs of the skeleton.

### End points, branch points and segments

- An **end point** is a pixel with exactly one neighbour.
- A **branch point** is an 8-connected group of pixels with three or more neighbours. A line pixel between two pixels of the same branch point belongs to it too, so it isn't counted as a tiny loop.
- A **segment** is a line from an end or branch point to the next one. It is measured up to the branch point's pixel nearest the group's centre, so the segments add up to the total length. A closed loop without any end or branch point is one segment.

The straightness of a segment is

$$
\text{straightness} = \frac{d_{\text{straight}}}{L_{\text{segment}}}
$$

with $d_{\text{straight}}$ the straight distance between its two ends, at most 1. A straight line gives 1, a curved one less. A loop without end or branch point has no straightness and is left out of the mean; a loop that leaves a branch point and returns to it has straightness 0.

### Longest path

For each connected part of the skeleton: the distances along the skeleton (steps of 1 and $\sqrt{2}$) from one of its end points (or its first pixel, if it has none) to all its pixels, then from the farthest pixel found to all pixels again. The largest distance of this second sweep is the part's longest path; **Longest path** is the largest over the parts. This is exact for a tree.

### Mean diameter

Each skeleton pixel takes the exact Euclidean distance $d$ from its centre to the centre of the nearest pixel that is not part of the parent object (holes and anything beyond the parent count as outside). Its diameter is

$$
D = \max(2d - 1,\ 0)
$$

so a line 3 px wide has the diameter 3 on its centre line. A skeleton pixel outside the parent counts as 0 wide. **Mean diameter** is the mean of $D$ over the skeleton's pixels. The parent is the skeleton's parent of the **Diameter From** class, as linked by [Relate Objects](/commands/object/relate-objects/).

The command runs on the whole image at once, so skeletons across tile borders are measured as a whole.

## Limitations

- Lengths and the diameter are in pixels.
- With loops in the skeleton, **Longest path** is an approximation, a lower bound of the true longest path.
- 2D only.

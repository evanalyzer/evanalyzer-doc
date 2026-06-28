---
title: Spot Count per Cell
description: Count spots inside cells by combining nucleus/cell segmentation with spot detection.
---

This tutorial extends the [Spot Count](/tutorials/spot-count/) workflow to count spots on a per-cell basis. Three pipelines work together:

1. **Nucleus** - segment nuclei from the DAPI channel.
2. **Cell area** (optional) - segment the cell body, or use Voronoi approximation.
3. **EV Detection** - detect spots, then link each spot to the cell it falls in.

## Prerequisites

- Multi-channel images with: (1) a nuclear stain (DAPI/Hoechst), and (2) a spot channel (Cy5 etc.).
- Optionally: a cell-body stain (cell-fill marker) for more accurate cell boundaries.

## Step 1: Define Classes

| Class                 | Purpose                          |
| --------------------- | -------------------------------- |
| `dapi@nucleus`        | Segmented nuclei                 |
| `cy5@spot`            | Detected spots                   |
| `cy5@spot-in-nucleus` | Spots that fall inside a nucleus |
| `cy5@spot-outside`    | Spots outside any nucleus        |

## Step 2: Nucleus Pipeline

Create a pipeline named `Nucleus` targeting the DAPI channel:

| Step                 | Settings                                                        |
| -------------------- | --------------------------------------------------------------- |
| Rolling Ball         | Radius: 20–50 (larger than nuclei)                              |
| Gaussian Blur        | Kernel: 5                                                       |
| Threshold            | Manual or Otsu auto-threshold                                   |
| Connected Components | -                                                               |
| Watershed            | Tolerance: 0.3 (optional)                                       |
| Extract ROIs         | -                                                               |
| Classify ROIs        | Target: `dapi@nucleus`; Min area: 500 px²; Min circularity: 0.3 |

## Step 3: EV Detection Pipeline

Follow the [Spot Count](/tutorials/spot-count/) pipeline for the EV channel to produce `cy5@spot` objects.

## Step 4: Link Spots to Nuclei

After the Classify ROIs step in the EV pipeline, add a second **Classify ROIs** step:

| Setting                | Value                                                  |
| ---------------------- | ------------------------------------------------------ |
| Origin class           | `cy5@spot`                                             |
| Target class           | `cy5@spot-in-nucleus`                                  |
| Intersection condition | Intersects with `dapi@nucleus` (min intersection: 10%) |

Objects that intersect a nucleus are moved to `cy5@spot-in-nucleus`. Spots that do not intersect remain as `cy5@spot` and can optionally be moved to `cy5@spot-outside` by an additional step.

## Step 5: Results

In the results view:

- The `cy5@spot-in-nucleus` **Count** per image gives total spots inside nuclei.
- With the parent object ID relationship, you can query spots per nucleus in the DuckDB results file:

```sql
SELECT parent_object_id, COUNT(*) AS spots_per_nucleus
FROM objects
WHERE class = 'cy5@spot-in-nucleus'
GROUP BY parent_object_id;
```

## Voronoi cell approximation (no cell stain)

If no cell-body stain is available, use [Voronoi](/commands/object/voronoi/) to approximate cell territories from nucleus centres:

| Setting                      | Value                                |
| ---------------------------- | ------------------------------------ |
| Centers                      | `dapi@nucleus`                       |
| Max radius                   | 30 µm (adjust to expected cell size) |
| Output class                 | `cell@voronoi`                       |
| Exclude areas at edges       | enabled                              |
| Exclude areas without centre | enabled                              |

Then use `cell@voronoi` instead of `dapi@nucleus` in the intersection step.

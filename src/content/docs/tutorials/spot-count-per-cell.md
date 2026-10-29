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
| Extract Objects      | -                                                               |
| Classify Objects     | Target: `dapi@nucleus`; Min Size: 500 px²; Min circularity: 0.3 |

## Step 3: EV Detection Pipeline

Follow the [Spot Count](/tutorials/spot-count/) pipeline for the EV channel to produce `cy5@spot` objects.

## Step 4: Link Spots to Nuclei

After the Classify Objects step in the EV pipeline, add a **[Relate Objects](/commands/object/relate-objects/)** step:

| Setting                          | Value                            |
| -------------------------------- | -------------------------------- |
| Children                         | `cy5@spot`                       |
| Parents                          | `dapi@nucleus`                   |
| A child belongs to the parent if | Its centre is in the parent      |
| Remove children without a parent | On, to keep only spots in nuclei |

Every spot whose centre lies in a nucleus is linked to that nucleus. With **Remove children without a parent** off, the other spots stay as unlinked `cy5@spot` objects.

## Step 5: Results

In the [List View](/guide/results/#list-view) of the results:

- The `cy5@spot` **Count** per image gives the total number of linked spots.
- Under **Children**, tick the entry for the spots in the nuclei (e.g. _cy5@spot in dapi@nucleus_). Every nucleus row then gets the number of its spots (**· Count**, 0 for a nucleus without spots) and, for every ticked value column, an aggregate of its spots' values.
- Click a nucleus's spot count to list just its spots. [Export](/guide/results/#exporting-results) the list to get the spots per nucleus as a table.

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

---
title: Spot Colocalization
description: Detect spots in two channels and identify those that spatially overlap.
---

This tutorial demonstrates how to detect spots in two fluorescence channels and identify colocalising spot pairs - objects from both channels that overlap in the same spatial location.

## Prerequisites

- Multi-channel images with spots in at least two distinct channels (e.g. Cy5 and Cy7).

## Step 1: Define Classes

| Class          | Purpose                     |
| -------------- | --------------------------- |
| `cy5@spot`     | Spots in channel 1          |
| `cy7@spot`     | Spots in channel 2          |
| `coloc@cy5cy7` | Colocalisation overlap area |

## Step 2: Per-Channel Detection Pipelines

Create **one pipeline per channel** following the [Spot Count](/tutorials/spot-count/) workflow. Each pipeline should end with a Classify Objects step that assigns the respective class:

- Pipeline 1 → `cy5@spot`
- Pipeline 2 → `cy7@spot`

## Step 3: Colocalization Pipeline

Create a third pipeline with **Empty input** (no image channel needed). Add a single step:

**[Colocalization](/commands/object/colocalization/)**

| Setting                           | Value                          |
| --------------------------------- | ------------------------------ |
| Classes to colocalize             | `cy5@spot`, `cy7@spot`         |
| Class for overlapping areas       | `coloc@cy5cy7`                 |
| Min colocalization area           | 1 px²                          |
| Allow multi-object colocalization | disabled (one-to-one matching) |

## Step 4: Run and Inspect

After running:

- `cy5@spot` objects that colocalize are assigned a **tracking ID** shared with their matching `cy7@spot` partner.
- In the results table, sort by **Tracking ID** to see matched pairs side by side.
- The `coloc@cy5cy7` class contains one object per colocalising pair, representing the overlap area.

## Interpreting Results

| Metric               | Meaning                                             |
| -------------------- | --------------------------------------------------- |
| `cy5@spot` Count     | Total Cy5 spots detected                            |
| `cy7@spot` Count     | Total Cy7 spots detected                            |
| `coloc@cy5cy7` Count | Number of colocalising spot pairs                   |
| Colocalisation %     | `coloc count / cy5 count × 100` (compute in export) |

## Filtering by colocalization area

Add a **Classify Objects** step after Colocalization targeting `coloc@cy5cy7` to filter out low-overlap events:

| Filter   | Value                                                         |
| -------- | ------------------------------------------------------------- |
| Min area | 5 px² (discard single-pixel overlaps due to border artefacts) |

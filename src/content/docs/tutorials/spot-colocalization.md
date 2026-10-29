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

**[Colocalize Objects](/commands/object/colocalization/)**

| Setting            | Value                                          |
| ------------------ | ---------------------------------------------- |
| Colocalize         | `cy5@spot`, `cy7@spot`                         |
| Overlap regions as | `coloc@cy5cy7`                                 |
| By at least        | 1                                              |
| Size Unit          | px                                             |
| Partners           | Only the best-overlapping partner (one-to-one) |

## Step 4: Run and Inspect

After running:

- Every `cy5@spot` object records its `cy7@spot` partner, and the other way round. In the [List View](/guide/results/#list-view), the **Coloc with cy7@spot** column shows how many partners a spot has (0 or 1 here); click the count to list the partner.
- **A row per: [Coloc pairs](/guide/results/#coloc-pairs)** shows each matched pair in one row, with the partner's measurements next to the spot's own.
- The `coloc@cy5cy7` class contains one object per colocalising pair, representing the overlap area.

## Interpreting Results

| Metric               | Meaning                                             |
| -------------------- | --------------------------------------------------- |
| `cy5@spot` Count     | Total Cy5 spots detected                            |
| `cy7@spot` Count     | Total Cy7 spots detected                            |
| `coloc@cy5cy7` Count | Number of colocalising spot pairs                   |
| Colocalisation %     | `coloc count / cy5 count × 100` (compute in export) |

## Filtering by colocalization area

Add a **Classify Objects** step after Colocalize Objects targeting `coloc@cy5cy7` to filter out low-overlap events:

| Filter   | Value                                                         |
| -------- | ------------------------------------------------------------- |
| Min Size | 5 px² (discard single-pixel overlaps due to border artefacts) |

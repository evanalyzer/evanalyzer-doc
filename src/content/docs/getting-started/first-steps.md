---
title: First Steps
description: Create your first EVAnalyzer project and run your first analysis.
---

This guide walks you through the essential workflow: open a set of images, configure object classes and pipelines, run the analysis, and inspect the results.

## 1. Open EVAnalyzer

Start EVAnalyzer as described in [Installation](/getting-started/installation/). The application opens showing the project configuration panel on the left and an empty image viewport on the right.

## 2. Set Up Your Project

The left-hand navigation panel contains four tabs that must be configured in order: **Project → Images → Classification → Pipelines**.

### Project tab

Enter basic experiment metadata and select the image directory:

- **Image directory** — the folder containing your microscopy images. EVAnalyzer scans this folder recursively and lists all supported files.
- **Job name** — a label for this analysis run (auto-generated if left blank).
- **Grouping** — leave as *Ungrouped* for a simple run, or choose *Filename* / *Foldername* to group images into wells for plate-based experiments.

### Images tab

Once the directory is set, EVAnalyzer lists all found image files. Click an image to preview it and inspect its metadata (channels, pixel sizes, Z/T dimensions).

### Classification tab

Before building pipelines, define the **object classes** you want to detect — for example, `dapi@nucleus`, `cy5@spot`, `cy7@spot`.

- Click the **+** button to add a class.
- Assign a name and a display colour.
- Optionally choose which metrics to show by default in the results view.

:::tip[Naming convention]
Use `<fluorophore>@<object-type>` (e.g. `cy5@spot`). The prefix before `@` is used for sorting in drop-down lists.
:::

### Pipelines tab

Pipelines extract objects from image channels. Click **New pipeline** (or select a preset from the **+** dropdown) and then open the pipeline editor by clicking the pipeline name.

A minimal spot-detection pipeline looks like:

1. **Rolling Ball** — remove uneven background
2. **Gaussian Blur** — reduce noise
3. **Threshold** — convert greyscale to binary
4. **Connected Components** — label each foreground region
5. **Watershed** — split touching objects
6. **Extract ROIs** — assign the segmentation class
7. **Classify ROIs** — filter by size/circularity and assign an object class

The live preview on the right updates immediately as you change parameters.

## 3. Run the Analysis

Click the **Play** button in the toolbar. A progress dialog appears. When complete, click **Open results folder** to locate the output files, or click **Close** to view results within the application.

Results are saved to:

```
<image_directory>/evanalyzer/<job_name>/results.evadb
```

## 4. View Results

Click the results icon in the toolbar (or use **File → Open Results**) to open the results viewer.

- **Plate view** — aggregated statistics per well (only when grouping is configured).
- **Image view** — per-image statistics table.
- **Detail view** — density map and per-object interactive mode; click an object row to highlight it in the image.

See the [Results](/guide/results/) guide for full details.

## Next Steps

- Read [Project Setup](/guide/project-setup/) for all project options including Z-stack and T-stack handling.
- Read [Pipelines](/guide/pipelines/) for a detailed explanation of every pipeline option.
- Browse the [Commands](/commands/overview/) reference to learn what each pipeline step does.
- Follow a [Tutorial](/tutorials/spot-count/) for a complete worked example.

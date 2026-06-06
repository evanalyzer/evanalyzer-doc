---
title: Project Setup
description: Configure experiment metadata, image grouping, plate layout, and Z/T-stack handling.
---

The **Project** tab is the first configuration step. It holds metadata about your experiment and controls how images are loaded and grouped.

## Experiment Metadata

| Field | Description |
|---|---|
| First / Last name | Experimenter name stored with the project file |
| Organization | Institution or lab name |
| Experiment name | Human-readable label for this experiment |
| Notes | Free-text notes |

## Image Directory

Set **Image directory** to the root folder containing your microscopy images. EVAnalyzer performs a recursive search and lists every supported file under that folder in the [Images tab](/guide/images/).

## Job Name

The **Job name** identifies this particular analysis run. Results are stored under:

```
<image_directory>/evanalyzer/<job_name>/
```

If left blank, EVAnalyzer auto-generates a name from the current timestamp.

## Image Grouping {#image-grouping}

Grouping controls how images are aggregated in the results view.

| Mode | Behaviour |
|---|---|
| **Off** (Ungrouped) | Each image is independent; no plate/well view is shown |
| **Filename** | Group by regex match on the filename |
| **Foldername** | Group by the immediate parent folder name |

### Filename regex

When **Filename** grouping is selected, a regular expression is used to extract the well position (row, column) and image index from each filename.

The regex must capture three named groups in order: **row** (a letter `A–Z`), **column** (decimal number), and **index** (decimal number).

Example regex: `_((.)([0-9]+))_([0-9]+)`

For filenames like `sample_A1_1.tif`, `sample_A1_2.tif`, `sample_B3_1.tif` this extracts:
- Row: `A` / `B`
- Column: `1` / `3`
- Index: `1` / `2` / …

:::caution
Grouping settings cannot be changed after an analysis has been started. If you need different grouping, re-run the analysis with the corrected settings.
:::

### Well order matrix

The **Well order** matrix controls how individual images within a well are laid out in the results image view. The default `[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]` places image index 1 in the top-left, index 2 to its right, and so on.

## Plate Size

Select the microplate format (6-well, 12-well, 24-well, 96-well, …). Open the **Plate settings** dialog to define the well labelling order.

## Z-Stack Handling {#z-stack}

| Setting | Behaviour |
|---|---|
| **SingleStack** | Analyse only the selected Z index (default: 0) |
| **AllStacks** | Run the pipeline independently for every Z plane |
| **MaxIntensity** | Collapse all Z planes with a maximum-intensity projection |
| **MinIntensity** | Collapse with a minimum-intensity projection |
| **AvgIntensity** | Collapse with an average-intensity projection |
| **SumIntensity** | Collapse with a sum-intensity projection |
| **TakeTheMiddle** | Use the Z plane nearest to the centre of the stack |

When **MaxIntensity** (or any other projection) is selected, each pipeline must additionally specify which projection mode to use for its input channel.

## T-Stack Handling {#t-stack}

| Setting | Behaviour |
|---|---|
| **SingleStack** | Analyse only the selected time frame (default: 0) |
| **AllStacks** | Run the pipeline independently for every time frame |

When **AllStacks** is selected you can also set a **Playback speed** (frames per second) for the image viewer.

## Tile Size

For very large images (whole-slide imaging), EVAnalyzer automatically splits the image into tiles. The **tile width** and **tile height** settings (default: 4096 × 4096 px) control the maximum tile size loaded into RAM at once.

See [Image Formats — Big Images](/fundamentals/image-formats/#big-images) for details.

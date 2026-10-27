---
title: Measure Image & Object Colocalization
description: Measure how the intensities of two channels go together - Pearson, Manders M1/M2, overlap, K1/K2, RWC and Costes' thresholds - over the whole image (Measure Image Colocalization) or in each object of a class (Measure Object Colocalization).
---

**Measure Image Colocalization** and **Measure Object Colocalization** measure how the intensities of two channels go together, pixel by pixel: Pearson's correlation, Manders' M1 and M2, the overlap coefficient, K1 and K2, the rank-weighted colocalization (RWC) and, optionally, Manders with Costes' automatic thresholds. The two commands compute the same values; they differ in the region:

- **Measure Image Colocalization** treats the whole image as one region and gives one set of values per image plane.
- **Measure Object Colocalization** treats every object of a class as its own region and gives one set of values per object.

To get both, add both steps. The values are those of CellProfiler's MeasureColocalization, value for value.

![A scatter plot of the two channels' pixels: Pearson uses every pixel; the thresholds (a percentage of each channel's maximum) split the plot, and Manders, overlap, K1/K2 and RWC use the pixels above both thresholds (top right) against those above each channel's own threshold](../../../../assets/figures/cmd-measure-colocalization.svg)

These are **not** the [Colocalize Objects](/commands/object/colocalization/) object command. That one works on **objects**: it finds objects of different classes that overlap and links them. The two Measure commands work on **intensities**: they ask whether bright pixels in channel A are also bright in channel B.

Both are [measurement steps](/guide/pipelines/#measurement-steps): they run once per image plane, after all tiles of the image are read and all objects are found.

## Parameters

| Parameter                    | Description                                                                                         |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| **ID**                       | The step's ID, unique in the project. It is given automatically - `coloc_01`, … for Measure Image Colocalization, `object_coloc_01`, … for Measure Object Colocalization - and starts the names of its values in the results. |
| **Objects**                  | Measure Object Colocalization only: the objects measured. It must be set; the step stops with an error otherwise. |
| **Channel A**                | The first channel (default 0).                                                                      |
| **Channel B**                | The second channel (default 1).                                                                     |
| **Threshold (% of maximum)** | A pixel counts for Manders, the overlap, K1/K2 and RWC when it is brighter than this percentage of its channel's maximum - in the image (Measure Image Colocalization), or in the object (Measure Object Colocalization). Default 15 %. |
| **Costes thresholds**        | Manders with Costes' automatic thresholds, and how they are searched: **Off**, **Faster** (default), **Fast** or **Accurate** - see [Costes' thresholds](#costes-thresholds). |

## Measurements

Each name ends with the two channels, e.g. _"Pearson (channel 0 × channel 1)"_ - the same names for both commands. Measure Object Colocalization gives every value except the slope.

| Measurement             | Unit | Range   | Description                                                                          |
| ----------------------- | ---- | ------- | ------------------------------------------------------------------------------------ |
| **Pearson**             | -    | -1 to 1 | Correlation of A and B over all pixels. 1: they rise and fall together; 0: unrelated; -1: opposite. |
| **Slope**               | -    | -       | The slope of the least-squares line B = slope · A + c over all pixels. Measure Image Colocalization only. |
| **Manders M1**          | 0-1  | 0 to 1  | The part of A's intensity (above its threshold) in pixels where B is above its threshold too. |
| **Manders M2**          | 0-1  | 0 to 1  | The same for B: the part of B's intensity where A is above its threshold too.         |
| **Overlap**             | -    | 0 to 1  | Manders' overlap coefficient of the pixels above both thresholds.                    |
| **K1**                  | -    | ≥ 0     | Overlap split: how much A contributes.                                               |
| **K2**                  | -    | ≥ 0     | Overlap split: how much B contributes.                                               |
| **RWC 1**               | 0-1  | 0 to 1  | Like M1, but each pixel weighted by how similar its ranks in A and B are.            |
| **RWC 2**               | 0-1  | 0 to 1  | Like M2, weighted the same way.                                                      |
| **Manders M1 (Costes)** | 0-1  | 0 to 1  | M1 with Costes' automatic thresholds. Only when Costes thresholds is not Off.         |
| **Manders M2 (Costes)** | 0-1  | 0 to 1  | M2 with Costes' automatic thresholds. Only when Costes thresholds is not Off.         |

## How it works

The intensities $a_i, b_i$ of the two channels are taken as values from 0 to 1 (the gray value divided by the bit depth's maximum); an RGB image is turned into its luminance first. Measure Image Colocalization uses every pixel of the image, the background too; Measure Object Colocalization the pixels of each object's mask.

### Pearson and the slope

$$
r = \frac{\sum_i (a_i - \bar a)(b_i - \bar b)}{\sqrt{\sum_i (a_i - \bar a)^2 \, \sum_i (b_i - \bar b)^2}}, \qquad
\text{slope} = \frac{\sum_i (a_i - \bar a)(b_i - \bar b)}{\sum_i (a_i - \bar a)^2}
$$

Pearson uses every pixel, so a large dark background where both channels are low raises it. Use Measure Object Colocalization to look only at the cells.

### Thresholds

A pixel is "bright" in A when $a_i$ is above $t_A = p \cdot \max a / 100$, with $p$ the **Threshold (% of maximum)**, and the same for B. For Measure Image Colocalization the maximum is the image's; for Measure Object Colocalization it is the object's own. As in CellProfiler, over the image a pixel must be **above** the threshold, in an object **at or above** it.

### Manders, overlap and K1/K2

With $C$ the pixels bright in both channels:

$$
M_1 = \frac{\sum_{i \in C} a_i}{\sum_{a_i > t_A} a_i}, \qquad
M_2 = \frac{\sum_{i \in C} b_i}{\sum_{b_i > t_B} b_i}
$$

$$
\text{Overlap} = \frac{\sum_{C} a_i b_i}{\sqrt{\sum_{C} a_i^2 \, \sum_{C} b_i^2}}, \qquad
K_1 = \frac{\sum_{C} a_i b_i}{\sum_{C} a_i^2}, \qquad
K_2 = \frac{\sum_{C} a_i b_i}{\sum_{C} b_i^2}
$$

M1 answers "how much of A is where B is": 1 means all of A's bright signal lies in B's bright pixels. M1 and M2 can differ a lot - e.g. a small vesicle stain (A) inside a large cytoplasm stain (B) gives a high M1 and a low M2.

### Rank-weighted colocalization (RWC)

Each pixel gets its rank among the different values of its channel (0 for the darkest). With $R$ the larger number of different values in the two channels, a pixel in $C$ is weighted by how close its two ranks are:

$$
w_i = \frac{R - |\text{rank}(a_i) - \text{rank}(b_i)|}{R}, \qquad
\text{RWC}_1 = \frac{\sum_{C} a_i w_i}{\sum_{a_i > t_A} a_i}
$$

and RWC 2 the same for B. A pixel that is bright in both channels but much brighter in one counts less. For the image the ranks are those of the whole image; for the objects, those of the pixels of all the measured objects together.

### Costes' thresholds

Instead of a fixed percentage, Costes' method finds the thresholds from the data: candidate thresholds lie on the orthogonal regression line of B over A (through the pixels where either channel is not 0). Starting from the top, the threshold is lowered until the pixels **below** it (in A or in B) no longer correlate positively (Pearson ≤ 0). M1 and M2 are then computed with these thresholds (pixels strictly above them).

The three search methods are CellProfiler's:

| Method       | Search                                                                                           |
| ------------ | ------------------------------------------------------------------------------------------------ |
| **Faster**   | A window of candidates that shrinks around the answer - a few passes over the image, also for 16-bit images. |
| **Fast**     | Candidates from the top down, skipping several at a time while the correlation is far from 0. Slow on 16-bit images. |
| **Accurate** | Every candidate from the top down, one gray value at a time. Very slow on 16-bit images.           |

Measure Object Colocalization uses the whole image's Costes thresholds: it searches them over the whole image itself (no Measure Image Colocalization step is needed) and does not search them again for each object.

### Edge cases

As in CellProfiler: when no pixel of any object is bright in both channels, the per-object Manders, overlap, K1/K2 and RWC are 0. Values that can't be computed (e.g. Pearson of a constant channel, M1 with no bright A pixel) get no value.

## Results

The values of Measure Image Colocalization belong to the image plane; in the [List view](/guide/results/#list-view) they are under **Columns › Measurements**, named _"coloc_01 · Pearson (channel 0 × channel 1)"_. With **A row per: Images** each image shows its own value; with **A row per: Objects** each object row shows the value of its image plane.

The values of Measure Object Colocalization (_"object_coloc_01 · Pearson (channel 0 × channel 1)"_) belong to each object of the class and are shown on its row; with **A row per: Images** they are aggregated over the image's objects like any other column. The ranges (-1 to 1, 0 to 1) are fixed, so the colour scales of the [Plate view](/guide/results/#plate-view) stay comparable between plates.

The export option **Measurements - one row per value** writes every value with the image, plane, region (image or object), object ID, step, measurement, unit and key - see [Exporting Results](/guide/results/#exporting-results).

## Limitations

- Two channels per step. For more pairs, add a step for each.
- Values are per plane; there is no 3D colocalization over a z-stack.
- It measures the channels as they are loaded from the image: filters earlier in the pipeline (e.g. a background subtraction) do not change them. There is no background correction other than the thresholds.

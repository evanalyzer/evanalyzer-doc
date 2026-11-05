---
title: Intensity Transform
description: Apply a linear brightness/contrast adjustment or a log/square-root transform.
---

The **Intensity Transform** command adjusts pixel intensities using a configurable mathematical transformation.

The three modes trace out different curves through the same input→output space: Linear keeps proportions intact (twice as bright stays twice as bright), while Logarithmic and Square root bend the curve to compress the high end and expand the low end - useful when a few very bright pixels would otherwise dominate the visible range and hide dim but real signal.

![Linear keeps proportions; log/sqrt compress bright values and expand dark ones](../../../../assets/figures/cmd-intensity-transform.svg)

## Parameters

| Parameter      | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| **Mode**       | The transform to apply (see below)                             |
| **Contrast**   | Multiplicative scaling factor applied after the mode transform |
| **Brightness** | Additive offset applied after scaling                          |

## Transform Modes

| Mode            | Description                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------------- |
| **Linear**      | `output = contrast × input + brightness` - simple gain/offset adjustment                            |
| **Logarithmic** | `output = contrast × log(input + 1) + brightness` - compresses bright regions; expands dark regions |
| **Square root** | `output = contrast × sqrt(input) + brightness` - moderate compression of bright regions             |

## When to use

- **Linear** - correct for systematic over/under-exposure across a batch.
- **Logarithmic** - useful when signal spans several orders of magnitude (e.g. very dim and very bright objects in the same image).
- **Square root** - a milder alternative to log when the intensity range is not extreme.

## Citation

The step cites Hummel R., "Image Enhancement by Histogram Transformation," _Computer Graphics and Image Processing_, vol. 6, pp. 184-195, 1977. [doi:10.1016/S0146-664X(77)80011-7](https://doi.org/10.1016/S0146-664X(77)80011-7) See [Citation](/citation/#citing-the-algorithms-you-used) for exporting the citations of a project.

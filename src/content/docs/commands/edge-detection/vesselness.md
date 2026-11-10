---
title: Vesselness
description: Highlight lines (fibres, neurites, vessels) of a chosen width range, so a threshold can segment them (Frangi vesselness).
---

**Vesselness** turns the image into a map of how much each pixel looks like the middle of a line - a fibre, neurite or vessel - of the widths you give. The result is 0 to 1: high in the middle of a line, low for the background, blobs and flat areas. It follows Frangi et al.'s multiscale vesselness filter.

![The Hessian's two curvatures tell the shapes apart: a line curves strongly across (λ2) and hardly along (λ1), so R is near 0 and the vesselness is high; a blob curves equally in both directions (R near 1) and is suppressed; a flat area has no curvature (S near 0) and stays 0](../../../../assets/figures/cmd-vesselness.svg)

Use it before a [Threshold](/commands/segmentation/threshold/) to segment thin fibres that a threshold on the raw image can't separate from the background, for example:

**Vesselness** → [Threshold](/commands/segmentation/threshold/) → [Connected Components](/commands/segmentation/connected-components/) → [Extract Objects](/commands/object/extract-objects/) → [Skeletonize Objects](/commands/object/skeletonize-objects/)

It is a preprocessing step: its result replaces the image for the steps after it. In a project file it is `VESSELNESS`.

## Parameters

| Parameter            | Description                                                                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Min Width**        | The width of the thinnest lines to find (0.5 to 1000, default 2).                                                                                                                 |
| **Max Width**        | The width of the widest lines to find (0.5 to 1000, default 6).                                                                                                                   |
| **Width Steps**      | How many widths from the thinnest to the widest are tried, spaced evenly on a log scale (1 to 10, default 3). More: a steadier response over the widths, but slower.               |
| **Width Unit**       | Unit of the widths: **px** (default) or **nm**.                                                                                                                                   |
| **Polarity**         | **Bright** lines on a dark background (fluorescence, default) or **Dark** lines on a bright one (brightfield).                                                                    |
| **Blob Suppression** | Advanced. How strongly blobs are suppressed (Frangi's $\beta$, 0.05 to 5, default 0.5). Lower suppresses more, so only clearly elongated structures stay.                         |
| **Noise Level**      | Advanced. Structures much weaker than this count as noise (Frangi's $c$, on the 0-1 scale of the image's second derivatives, default 0). 0: automatic, half the strongest structure. |

## How it works

### Widths and scales

Each width $w$ is turned into a Gaussian scale

$$
\sigma = \frac{w}{\sqrt{6}}
$$

the scale at which the response to a bar of that width peaks (a bar of width $w$ has the spread $w / \sqrt{12}$, and the response to a line of spread $s$ peaks at $\sigma = \sqrt{2}\, s$). The **Width Steps** widths are spaced evenly on a log scale from **Min Width** to **Max Width**; with one step only **Min Width** is used. The defaults (2 to 6 px, 3 steps) give the widths 2, 3.46 and 6 px. Widths in nm are divided by the pixel size (the mean of its x and y size); without a pixel size they are taken as pixels.

### Vesselness at one scale

At each scale the [Hessian](/commands/edge-detection/hessian/) of every pixel is computed: the second derivatives of the image smoothed with a Gaussian of $\sigma$, multiplied by $\sigma^2$ so that the scales compare. The Gaussian and its derivatives are cut off at $3\sigma$; at the image border the edge pixels are repeated outward.

The Hessian's two eigenvalues are sorted so that $|\lambda_1| \le |\lambda_2|$. On a line, $\lambda_1$ (along it) is small and $\lambda_2$ (across it) is large - negative for a bright line, positive for a dark one. From them:

$$
R = \frac{\lambda_1}{\lambda_2}, \qquad S = \sqrt{\lambda_1^2 + \lambda_2^2}
$$

$R$ is near 0 for a line and near 1 for a blob; $S$ is the strength of the structure, small for flat areas and noise. The vesselness is

$$
V = \exp\!\left(-\frac{R^2}{2\beta^2}\right)\left(1 - \exp\!\left(-\frac{S^2}{2c^2}\right)\right)
$$

with $\beta$ = **Blob Suppression** and $c$ = **Noise Level**. $V$ is 0 where $\lambda_2$ has the wrong sign for the **Polarity** (for **Bright**: $\lambda_2 \ge 0$; for **Dark**: $\lambda_2 \le 0$), so lines of the other polarity are not found.

With **Noise Level** 0, $c$ is half the largest $S$ in the image at that scale (Frangi's suggestion). A flat image, where even the largest $S$ is below $10^{-5}$, stays 0.

### Result

The result is the largest $V$ of each pixel over all scales, from 0 to 1. To threshold it, the [Threshold](/commands/segmentation/threshold/) unit _Relative_ (0-1) takes the vesselness values directly.

The method is from A. F. Frangi, W. J. Niessen, K. L. Vincken and M. A. Viergever, "Multiscale Vessel Enhancement Filtering," _Medical Image Computing and Computer-Assisted Intervention (MICCAI'98)_, 1998, pp. 130-137, [doi:10.1007/BFb0056195](https://doi.org/10.1007/BFb0056195).

## Limitations

- 2D only: each plane is filtered on its own.
- At its centre a blob answers far less than a line, but its rim looks like a curved line at the smallest scale and does answer - Frangi's known behaviour.
- On a whole slide the filter runs per tile, without overlap: with **Noise Level** 0 each tile gets its own automatic level, so neighbouring tiles can be scaled slightly differently, and the image edge is repeated at every tile border. A fixed **Noise Level** gives the same scaling on every tile. Small images are one tile and not affected.

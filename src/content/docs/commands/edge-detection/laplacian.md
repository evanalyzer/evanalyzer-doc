---
title: Laplacian
description: Second-order derivative filter for edge detection via zero-crossings.
---

The **Laplacian** command applies the Laplacian operator - the sum of second-order partial derivatives - to detect edges via zero-crossings. The output highlights regions of rapid intensity change.

## When to use

The Laplacian is sensitive to fine detail and noise. Apply it after [Gaussian Blur](/commands/image-processing/gaussian-blur/) (the combined LoG - Laplacian of Gaussian - operator) for more robust edge and blob detection.

## Parameters

| Parameter       | Description                               |
| --------------- | ----------------------------------------- |
| **Kernel size** | Size of the Laplacian kernel (range 3–27) |

## Background

The Laplacian is defined as:

$$
\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}
$$

Zero-crossings in the output correspond to edges in the original image. Unlike gradient-based methods (Sobel, Canny), the Laplacian is isotropic - it responds equally to edges in all directions.

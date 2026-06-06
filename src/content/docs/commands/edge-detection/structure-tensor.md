---
title: Structure Tensor
description: Local orientation and coherence from the structure tensor.
---

The **Structure Tensor** command computes a scalar map from the structure (gradient) tensor of the image. It characterises local image orientation and the degree of directional coherence.

## Parameters

| Parameter | Description |
|---|---|
| **Mode** | Which scalar feature to extract (see below) |
| **Kernel size** | Size of the gradient kernel (range 3–27) |
| **Sigma** | Gaussian smoothing applied to the tensor components |

### Modes

| Mode | Highlights |
|---|---|
| **Coherence** | How strongly oriented the local structure is (0 = isotropic, 1 = perfect orientation) |
| **Orientation** | The dominant local gradient direction in radians |
| **Energy** | Total gradient magnitude; similar to Sobel but with tensor smoothing |

## When to use

Structure tensor analysis is useful for:
- Detecting and enhancing fibrous or elongated structures (collagen fibres, actin filaments).
- Filtering based on local anisotropy before segmentation.

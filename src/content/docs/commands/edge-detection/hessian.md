---
title: Hessian
description: Second-order image structure for blob and ridge detection.
---

The **Hessian** command computes a scalar map from the Hessian matrix of the image - the matrix of second-order partial derivatives. This captures local curvature and is useful for detecting blobs and ridges.

## When to use

- **Blob detection** - use the Determinant mode to find circular, blob-like structures (e.g. cell nuclei, vesicles).
- **Ridge detection** - use the Eigenvalue modes to detect filamentous or tubular structures.

## Parameters

| Parameter | Description                                                  |
| --------- | ------------------------------------------------------------ |
| **Mode**  | Which scalar feature to extract from the Hessian (see below) |

### Modes

| Mode              | Formula                             | Highlights                                                           |
| ----------------- | ----------------------------------- | -------------------------------------------------------------------- |
| **Determinant**   | $\det(H) = I_{xx}I_{yy} - I_{xy}^2$ | Blobs and corners                                                    |
| **Eigenvalues X** | Larger eigenvalue $\lambda_1$       | Maximum curvature; principal ridge axis                              |
| **Eigenvalues Y** | Smaller eigenvalue $\lambda_2$      | Secondary curvature; interest points when both eigenvalues are large |

## Background

The Hessian matrix at pixel $(x,y)$ is:

$$
H = \begin{pmatrix} I_{xx} & I_{xy} \\ I_{xy} & I_{yy} \end{pmatrix}
$$

where $I_{xx}$, $I_{yy}$, $I_{xy}$ are second-order spatial derivatives of the image intensity.

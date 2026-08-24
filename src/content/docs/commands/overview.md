---
title: Commands Overview
description: All 35 pipeline commands grouped by category.
---

Pipeline commands are the building blocks of an analysis. Each command takes either an image or a set of objects as input and produces either a processed image or an updated set of objects as output.

## Command Categories

| Category                     | Colour | Input                  | Output                         |
| ---------------------------- | ------ | ---------------------- | ------------------------------ |
| **Image processing**         | Grey   | Image                  | Image                          |
| **Edge & feature detection** | Grey   | Image                  | Image                          |
| **Segmentation**             | White  | Image                  | Binary mask                    |
| **Morphology**               | White  | Binary/greyscale image | Image                          |
| **AI segmentation**          | White  | Image                  | Binary mask / object instances |
| **Object processing**        | Green  | Objects                | Objects / measurements         |

:::note
Not every command sequence is valid. The command picker shows only those commands compatible with the current pipeline state.
:::

## Image Processing

Commands for reducing noise and enhancing signal before segmentation.

| Command                                                                | Purpose                                          |
| ---------------------------------------------------------------------- | ------------------------------------------------ |
| [Blur](/commands/image-processing/blur/)                               | Box/average blur to reduce noise                 |
| [Gaussian Blur](/commands/image-processing/gaussian-blur/)             | Edge-preserving Gaussian blur                    |
| [Rolling Ball](/commands/image-processing/rolling-ball/)               | Background subtraction                           |
| [Illumination Correction](/commands/image-processing/illumination-correction/) | Remove uneven illumination (vignetting) across the whole image |
| [Rank Filter](/commands/image-processing/rank-filter/)                 | Min / median / max neighbourhood filter          |
| [Enhance Contrast](/commands/image-processing/enhance-contrast/)       | Histogram-based contrast enhancement             |
| [Color Filter](/commands/image-processing/color-filter/)               | Retain pixels within an HSV colour range         |
| [Intensity Transform](/commands/image-processing/intensity-transform/) | Brightness and contrast adjustment               |
| [Median Subtract](/commands/image-processing/median-subtract/)         | Subtract the local median for background removal |
| [Image Math](/commands/image-processing/image-math/)                   | Combine two images mathematically                |
| [Image Cache](/commands/image-processing/image-cache/)                 | Store or retrieve an image from cache slots      |

## Edge & Feature Detection

Commands for detecting edges, ridges, and local structures.

| Command                                                            | Purpose                                         |
| ------------------------------------------------------------------ | ----------------------------------------------- |
| [Canny Edge Detection](/commands/edge-detection/canny/)            | Gradient-based edge detection with thresholding |
| [Sobel Edge Detection](/commands/edge-detection/sobel/)            | Fast gradient-magnitude edge detection          |
| [Hessian](/commands/edge-detection/hessian/)                       | Second-order structure (blobs and ridges)       |
| [Laplacian](/commands/edge-detection/laplacian/)                   | Zero-crossing edge detection                    |
| [Structure Tensor](/commands/edge-detection/structure-tensor/)     | Local orientation and coherence                 |
| [Weighted Deviation](/commands/edge-detection/weighted-deviation/) | Weighted local standard deviation               |

## Segmentation

Commands for separating foreground objects from background.

| Command                                                              | Purpose                                                        |
| -------------------------------------------------------------------- | -------------------------------------------------------------- |
| [Threshold](/commands/segmentation/threshold/)                       | Convert greyscale to binary with manual or automatic threshold |
| [Connected Components](/commands/segmentation/connected-components/) | Label each connected foreground region                         |
| [Watershed](/commands/segmentation/watershed/)                       | Split touching objects using intensity valleys                 |

## Morphology

Commands for modifying the shape of binary or greyscale regions.

| Command                                                                  | Purpose                             |
| ------------------------------------------------------------------------ | ----------------------------------- |
| [Morphological Transform](/commands/morphology/morphological-transform/) | Erosion, dilation, opening, closing |

## AI Segmentation

Commands that run a pretrained deep-learning model for segmentation. Only available in builds with the `ai` Cargo feature enabled.

| Command                                                            | Purpose                                                                                                   |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [Stardist](/commands/ai-segmentation/stardist/)                    | Instance segmentation via star-convex polygons - separates touching objects directly                      |
| [UNet](/commands/ai-segmentation/unet/)                            | Semantic foreground/background mask - pair with Connected Components (+ Watershed) to separate instances  |
| [Cellpose](/commands/ai-segmentation/cellpose/)                    | Instance segmentation via flow-field dynamics - handles irregular and overlapping shapes                  |
| [AI Pixel Classifier](/commands/ai-segmentation/pixel-classifier/) | Semantic mask from a Random Forest/k-NN/MLP model you [train yourself](/ai/training/) on painted examples |

## Object Processing

Commands that operate on extracted objects.

| Command                                                        | Purpose                                                                                                      |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [Fill Holes](/commands/object/fill-holes/)                     | Close enclosed background holes in the segmentation map                                                      |
| [Extract Objects](/commands/object/extract-objects/)           | Convert binary mask regions to segmentation-class objects                                                    |
| [Classify Objects](/commands/object/classify-objects/)         | Filter and assign final object classes                                                                       |
| [AI Object Classifier](/commands/object/ai-object-classifier/) | Classify objects with a Random Forest/k-NN/MLP model you [train yourself](/ai/training/) on painted examples |
| [Colocalization](/commands/object/colocalization/)             | Find overlapping objects across classes                                                                      |
| [Voronoi](/commands/object/voronoi/)                           | Partition space from object centroids                                                                        |
| [Object Transform](/commands/object/transform-objects/)        | Scale, snap, expand, shrink, or fit an ellipse to objects                                                    |
| [Object Math](/commands/object/object-math/)                   | Boolean set operations (AND, OR, XOR, Subtract) between two object classes                                   |
| [Distance Transform](/commands/object/distance-transform/)     | Measure distances between object pairs                                                                       |
| [Save Image](/commands/object/save-image/)                     | Write a control image to disk                                                                                |

## Typical Pipeline Order

```
Image
  └─ Preprocessing (Blur, Rolling Ball, Illumination Correction, …)
       └─ Segmentation (Threshold → Connected Components → Watershed)
            └─ Fill Holes (optional mask cleanup)
                 └─ Extract Objects
                      └─ Classify Objects
                           └─ Object Processing (Colocalization, Distance, …)
                                └─ Save Image
```

---
title: Commands Overview
description: All 55 pipeline commands grouped by category.
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
| **Measure**                  | Blue   | Image + final objects  | Measurements                   |
| **Dataset**                  | -      | Objects of all images  | Objects / measurements         |

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
| [Load Image Channel](/commands/image-processing/load-image-channel/)   | Load another channel as the current image        |
| [Color Deconvolution](/commands/image-processing/color-deconvolution/) | Separate the stains of a brightfield RGB image (e.g. H&E, H-DAB) |
| [Script](/commands/image-processing/script/)                           | Run your own Rhai script, using the other commands |

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
| [YOLOv5](/commands/ai-segmentation/yolov5/)                        | Instance segmentation or detection with boxes + masks - supports several object classes in one model     |
| [AI Pixel Classifier](/commands/ai-segmentation/pixel-classifier/) | Semantic mask from a Random Forest/k-NN/MLP model you [train yourself](/ai/training/) on painted examples |

## Object Processing

Commands that operate on extracted objects.

| Command                                                        | Purpose                                                                                                      |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [Fill Holes](/commands/object/fill-holes/)                     | Close enclosed background holes in the segmentation map                                                      |
| [Fill Object Holes](/commands/object/fill-object-holes/)       | Fill the holes inside every object, one object at a time                                                     |
| [Load Annotated Objects](/commands/object/load-annotated-objects/) | Bring hand-annotated objects into the pipeline as regular objects                                        |
| [Extract Objects](/commands/object/extract-objects/)           | Convert binary mask regions to segmentation-class objects                                                    |
| [Classify Objects](/commands/object/classify-objects/)         | Filter and assign final object classes                                                                       |
| [AI Object Classifier](/commands/object/ai-object-classifier/) | Classify objects with a Random Forest/k-NN/MLP model you [train yourself](/ai/training/) on painted examples |
| [Colocalize Objects](/commands/object/colocalization/)         | Find overlapping objects across classes                                                                      |
| [Voronoi](/commands/object/voronoi/)                           | Partition space from object centroids                                                                        |
| [Object Transform](/commands/object/transform-objects/)        | Scale, snap, expand, shrink, or fit an ellipse to objects                                                    |
| [Object Math](/commands/object/object-math/)                   | Boolean set operations (AND, OR, XOR, Subtract) between two object classes                                   |
| [Distance Transform](/commands/object/distance-transform/)     | Measure distances between object pairs                                                                       |
| [Propagation](/commands/object/propagation/)                   | Grow a region around each seed object through a channel (e.g. cells around nuclei)                           |
| [Relate Objects](/commands/object/relate-objects/)             | Link each child object to its parent (e.g. spots to their cell)                                              |
| [Save Image](/commands/object/save-image/)                     | Write a control image to disk, optionally with selected classes drawn on top                                 |

## Measure

Measure steps run once the objects are final. They measure the whole image or every object and add the values to the [results](/guide/results/).

| Command                                                                         | Purpose                                                                       |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [Measure Image Area Occupied](/commands/measure/area-occupied/)                 | How much of the image the objects of a class cover                            |
| [Measure Image Intensity](/commands/measure/image-intensity/)                   | Brightness statistics of a channel over the whole image                       |
| [Measure Image Quality](/commands/measure/image-quality/)                       | Focus, blur, saturation and noise of a channel                                |
| [Exclude Image](/commands/measure/exclude-image/)                               | Leave an image out of the results when its measurements say it's bad         |
| [Measure Image / Object Colocalization](/commands/measure/measure-colocalization/) | Pearson, Manders and related coefficients of two channels, over the image or per object |
| [Measure Image / Object Texture](/commands/measure/measure-texture/)            | Haralick texture features, over the image or per object                       |
| [Measure Object Shape](/commands/measure/measure-object-shape/)                 | Convex area, solidity, Euler number and radii of every object                 |
| [Measure Object Neighbors](/commands/measure/measure-object-neighbors/)         | Neighbours, percent touching and closest objects                              |
| [Measure Object Distance To Parent](/commands/measure/measure-distance-to-parent/) | Each child's distance to its parent (linked by Relate Objects)                |

## Dataset

[Dataset steps](/guide/pipelines/#dataset-steps) run once after every image has been analysed, on the stored objects of all images, frames and wells.

| Command                                              | Purpose                                                         |
| ---------------------------------------------------- | --------------------------------------------------------------- |
| [Simple Tracker](/commands/dataset/simple-tracker/)  | Link objects of a time-lapse into tracks (nearest neighbour)    |

## Modules

Several steps can be bundled into one reusable step with its own parameters - see [Modules](/guide/modules/).

## Typical Pipeline Order

```
Image
  └─ Preprocessing (Blur, Rolling Ball, Illumination Correction, …)
       └─ Segmentation (Threshold → Connected Components → Watershed)
            └─ Fill Holes / Fill Object Holes (optional cleanup)
                 └─ Extract Objects
                      └─ Classify Objects
                           └─ Object Processing (Colocalize Objects, Propagation, Relate Objects, …)
                                └─ Measure (Image Quality, Object Shape, Texture, …)
                                     └─ Save Image
```

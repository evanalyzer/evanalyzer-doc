---
title: Commands Overview
description: All 70 pipeline commands grouped by category.
---

Pipeline commands are the building blocks of an analysis. Each command takes either an image or a set of objects as input and produces either a processed image or an updated set of objects as output.

## Command Categories

Every command belongs to a category: what goes in and what comes out. The category gives the step its coloured stripe in the pipeline and its chip in the command picker (see [Step categories](/guide/pipelines/#step-categories)).

| | Category | In → out | Commands |
| --- | --- | --- | --- |
| <span class="evx-cat evx-cat-preprocess"></span> | **Preprocess** | image → image | [Image Processing](#image-processing), [Edge & Feature Detection](#edge--feature-detection), [Morphological Transform](/commands/morphology/morphological-transform/) |
| <span class="evx-cat evx-cat-segment"></span> | **Segment** | image → segmentation mask | Threshold, Find Maxima, [AI Segmentation](#ai-segmentation) |
| <span class="evx-cat evx-cat-object"></span> | **Instance Seg.** | mask → labelled mask | Connected Components, Watershed, Fill Holes, Morphological Transform |
| <span class="evx-cat evx-cat-extract"></span> | **Extract** | labelled mask → objects | Extract Objects, Fill Object Holes |
| <span class="evx-cat evx-cat-classify"></span> | **Object** | objects → objects | the other commands of [Object Processing](#object-processing) |
| <span class="evx-cat evx-cat-measure"></span> | **Measure** | objects / image → values | [Measure](#measure) |
| <span class="evx-cat evx-cat-dataset"></span> | **Dataset** | objects of all images → objects / values | [Dataset](#dataset) |
| <span class="evx-cat evx-cat-utility"></span> | **Utility** | - | [Script](/commands/image-processing/script/), [Save Image](/commands/object/save-image/), [Image Cache](/commands/image-processing/image-cache/) |

:::note
Not every command sequence is valid. The command picker starts on the categories that fit after the step before; the other chips can still be switched on.
:::

### Utility commands

**Utility** steps (grey) fit anywhere in a pipeline. The command picker always lists them, whatever chips are on. They have no category of their own at their place: the step after a utility step looks past it to the step before.

### Commands in several categories

A command can belong to more than one category. The first is its home. [Morphological Transform](/commands/morphology/morphological-transform/) is **Preprocess** (home) and **Instance Seg.**: before a segmentation it works on the image, after one (e.g. a Threshold) on the segmentation mask.

- The step's place decides which category it runs as - the first of its categories that may follow the step before it (utility steps skipped). The step's stripe shows that category's colour, and its settings show a read-only **Works on** line (_Image_ or _Segmentation mask_). Move the step to change it.
- The command picker lists such a command once: under its home when that chip is on, else under the first of its other categories whose chip is on, with a hint naming its home (_also Preprocess_).

## Image Processing

Commands for reducing noise and enhancing signal before segmentation.

| Command                                                                | Purpose                                          |
| ---------------------------------------------------------------------- | ------------------------------------------------ |
| [Blur](/commands/image-processing/blur/)                               | Box/average blur to reduce noise                 |
| [Gaussian Blur](/commands/image-processing/gaussian-blur/)             | Edge-preserving Gaussian blur                    |
| [Rolling Ball](/commands/image-processing/rolling-ball/)               | Background subtraction                           |
| [Bandpass](/commands/image-processing/bandpass/)                       | Remove fine noise and coarse background, keep objects of any size in between |
| [Illumination Correction](/commands/image-processing/illumination-correction/) | Remove uneven illumination (vignetting) across the whole image |
| [Rank Filter](/commands/image-processing/rank-filter/)                 | Min / median / max neighbourhood filter          |
| [Enhance Contrast](/commands/image-processing/enhance-contrast/)       | Histogram-based contrast enhancement             |
| [Color Filter](/commands/image-processing/color-filter/)               | Retain pixels within an HSV colour range         |
| [Color to Grayscale](/commands/image-processing/color-to-grayscale/)   | Turn an RGB image into one gray value per pixel  |
| [Intensity Transform](/commands/image-processing/intensity-transform/) | Brightness and contrast adjustment               |
| [Median Subtract](/commands/image-processing/median-subtract/)         | Subtract the local median for background removal |
| [Image Math](/commands/image-processing/image-math/)                   | Combine two images mathematically                |
| [Load Image Channel](/commands/image-processing/load-image-channel/)   | Load another channel as the current image        |
| [Color Deconvolution](/commands/image-processing/color-deconvolution/) | Separate the stains of a brightfield RGB image (e.g. H&E, H-DAB) |
| [Distance Transform](/commands/object/distance-transform/)             | Euclidean distance map of a binary image         |

## Edge & Feature Detection

Commands for detecting edges, ridges, spots and other local structures.

| Command                                                            | Purpose                                         |
| ------------------------------------------------------------------ | ----------------------------------------------- |
| [Canny Edge Detection](/commands/edge-detection/canny/)            | Gradient-based edge detection with thresholding |
| [Sobel Edge Detection](/commands/edge-detection/sobel/)            | Fast gradient-magnitude edge detection          |
| [Hessian](/commands/edge-detection/hessian/)                       | Second-order structure (blobs and ridges)       |
| [Laplacian](/commands/edge-detection/laplacian/)                   | Zero-crossing edge detection                    |
| [Laplacian of Gaussian](/commands/edge-detection/laplacian-of-gaussian/) | Enhance spots of one size before Find Maxima (scale-normalized LoG) |
| [Difference of Gaussians](/commands/edge-detection/difference-of-gaussians/) | Enhance spots of one size before Find Maxima (approximates the LoG) |
| [Wavelet Spots](/commands/edge-detection/wavelet-spots/)           | Enhance spots that stand out of the noise at several levels of detail |
| [Structure Tensor](/commands/edge-detection/structure-tensor/)     | Local orientation and coherence                 |
| [Weighted Deviation](/commands/edge-detection/weighted-deviation/) | Weighted local standard deviation               |
| [Vesselness](/commands/edge-detection/vesselness/)                 | Highlight lines (fibres, neurites, vessels) of a chosen width (Frangi) |

## Segmentation

Commands for separating foreground objects from background.

| Command                                                              | Purpose                                                        |
| -------------------------------------------------------------------- | -------------------------------------------------------------- |
| [Threshold](/commands/segmentation/threshold/)                       | Convert greyscale to binary with manual or automatic threshold |
| [Connected Components](/commands/segmentation/connected-components/) | Label each connected foreground region                         |
| [Find Maxima](/commands/segmentation/find-maxima/)                   | Find spots as local maxima - one-pixel objects                 |
| [Watershed](/commands/segmentation/watershed/)                       | Split touching objects using intensity valleys                 |

## Morphology

Commands for modifying the shape of regions. Morphological Transform is both **Preprocess** and **Instance Seg.** - see [Commands in several categories](#commands-in-several-categories).

| Command                                                                  | Purpose                             |
| ------------------------------------------------------------------------ | ----------------------------------- |
| [Morphological Transform](/commands/morphology/morphological-transform/) | Dilate, erode, open, close - the image or, after a segmentation, the mask |

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
| [Propagation](/commands/object/propagation/)                   | Grow a region around each seed object through a channel (e.g. cells around nuclei)                           |
| [Grow Regions](/commands/object/grow-regions/)                 | Grow each seed (e.g. a maximum) into its own region, with a stop level per seed - a magic wand per seed       |
| [Relate Objects](/commands/object/relate-objects/)             | Link each child object to its parent (e.g. spots to their cell)                                              |
| [Skeletonize Objects](/commands/object/skeletonize-objects/)   | Reduce each object to its 1-pixel skeleton, optionally with branch and end points as objects                 |
| [Trace Filaments](/commands/object/trace-filaments/)           | Trace each neuron's neurites from its soma into a tree of segments                                           |

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
| [Measure Object Skeleton](/commands/measure/measure-object-skeleton/)           | Length, longest path, branch and end points, segments and straightness of skeletons |
| [Measure Object Sholl](/commands/measure/measure-object-sholl/)                 | Sholl analysis of skeletons: crossings per circle around the soma (a profile) and its summary values |
| [Measure Filament Tree](/commands/measure/measure-filament-tree/)               | Branch level, Strahler order, path distance and length per traced segment; totals per neuron |

## Dataset

[Dataset steps](/guide/pipelines/#dataset-steps) run once after every image has been analysed, on the stored objects of all images, frames and wells.

| Command                                              | Purpose                                                         |
| ---------------------------------------------------- | --------------------------------------------------------------- |
| [Track LAP](/commands/dataset/track-lap/)  | Link objects into tracks by the globally best assignment - gaps, merges and splits (random motion) |
| [Track Kalman](/commands/dataset/track-kalman/)  | As Track LAP, predicting each track's next position from its velocity (directed motion) |
| [Track Overlap](/commands/dataset/track-overlap/)  | Link objects into tracks by mask overlap - for large objects such as cells |
| [Track Nearest Neighbor](/commands/dataset/track-nearest-neighbor/)  | Link objects into tracks by nearest neighbour between consecutive frames |
| [Measure Track Motion](/commands/dataset/measure-track-motion/)  | Measure how each track moved: speeds, straightness, turning and MSD (after a tracker) |

## Utility

Steps that fit anywhere in a pipeline - see [Utility commands](#utility-commands).

| Command                                                | Purpose                                                       |
| ------------------------------------------------------ | ------------------------------------------------------------- |
| [Script](/commands/image-processing/script/)           | Run your own Rhai script, using the other commands            |
| [Save Image](/commands/object/save-image/)             | Write a control image of this point of the pipeline to disk   |
| [Image Cache](/commands/image-processing/image-cache/) | Store or retrieve an image from cache slots                   |

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
```

Utility steps (Script, Save Image, Image Cache) can go anywhere in between.

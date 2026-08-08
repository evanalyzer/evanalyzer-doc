---
title: AI Models
description: Overview of the deep-learning segmentation models supported by EVAnalyzer.
---

EVAnalyzer can run pretrained deep-learning models as a segmentation step in a pipeline, in builds with the `ai` Cargo feature enabled (via [tch-rs](https://github.com/LaurentMazare/tch-rs)/libtorch). Models are supplied by you as a TorchScript export (`.pt`/`.pth`) - EVAnalyzer does not bundle or download any models itself.

:::tip[Importing a model from bioimage.io]
Rather than configuring a model's parameters by hand, you can import a [bioimage.io](https://bioimage.io) model's `rdf.yaml` directly from the command picker, which auto-detects the architecture and pre-fills the step for you. See [Importing bioimage.io Models](/ai/bioimageio-import/).
:::

Looking for the opposite direction - a model built from your own annotations rather than one you supply? See [Training a Classifier](/ai/training/), which trains a Random Forest, k-Nearest Neighbors, or neural-network pixel/object classifier from examples you paint directly on your images.

Three architectures are currently implemented as pipeline commands:

| Model                                           | Predicts                                  | Separates touching objects?       |
| ----------------------------------------------- | ----------------------------------------- | --------------------------------- |
| [Stardist](/commands/ai-segmentation/stardist/) | Star-convex polygon per object instance   | Yes, directly                     |
| [UNet](/commands/ai-segmentation/unet/)         | Per-pixel foreground/background mask      | No - requires a follow-up step    |
| [Cellpose](/commands/ai-segmentation/cellpose/) | Flow field (dY/dX) + cell-probability map | Yes, directly (via flow dynamics) |

---

## Stardist

[Stardist](https://github.com/stardist/stardist) represents each detected object as a **star-convex polygon**: a set of radial distances from the object centroid to its boundary, sampled at fixed angles. Because the model predicts complete object instances directly, EVAnalyzer's [Stardist](/commands/ai-segmentation/stardist/) command needs no follow-up splitting step - touching, non-overlapping objects (e.g. nuclei) come out already separated.

**When to use it:** objects that are roughly convex and don't overlap - stained nuclei are the classic case.

See the [Stardist command reference](/commands/ai-segmentation/stardist/) for parameters and model output requirements.

---

## UNet

[U-Net](https://en.wikipedia.org/wiki/U-Net) is a convolutional encoder–decoder network with skip connections between matching encoder/decoder levels, which preserve fine spatial detail lost during downsampling. EVAnalyzer's [UNet](/commands/ai-segmentation/unet/) command only extracts a **semantic foreground mask** - it has no concept of individual object instances, so touching objects come out as one merged blob unless you address it explicitly:

- **Boundary-aware models** (mask + boundary channels) - use the boundary channel to carve gaps between objects, then a plain Connected Components step.
- **Mask-only models** - chain Connected Components → Watershed to split blobs that still have a "waist".

**When to use it:** irregular or elongated shapes, or any model trained for pixel-level semantic segmentation rather than instance detection.

See the [UNet command reference](/commands/ai-segmentation/unet/) for the full parameter list and both splitting strategies.

---

## Cellpose

[Cellpose](https://github.com/MouseLand/cellpose) predicts a **flow field**: a vector at every pixel pointing toward the centre of the object it belongs to, plus a cell-probability map. EVAnalyzer's [Cellpose](/commands/ai-segmentation/cellpose/) command follows these flows pixel by pixel until they converge to a sink, then groups pixels that converge to the same sink into one instance - recovering individual objects directly, including ones with irregular or overlapping shapes that defeat star-convex polygons.

**When to use it:** whole cells (cytoplasm), irregular morphology, or any case where objects aren't well approximated by convex polygons.

See the [Cellpose command reference](/commands/ai-segmentation/cellpose/) for parameters and model output requirements.

---

## Choosing a Model

```
Does the model predict individual object instances directly?
  ├─ Star-convex polygon export (probability + ray distances) → Stardist
  ├─ Flow field + cell-probability export (dY, dX, cellprob)   → Cellpose
  └─ No, it's a semantic mask (foreground vs. background, optionally + boundary)
              └─ UNet, with Connected Components (+ Watershed or boundary carving)
```

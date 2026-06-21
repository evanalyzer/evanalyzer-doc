---
title: AI Stardist Segmentation
description: Instance segmentation using a pretrained StarDist model.
---

The **AI Stardist Segmentation** command runs instance segmentation using a pretrained [StarDist](https://github.com/stardist/stardist) model exported as TorchScript. Unlike threshold-based segmentation, StarDist predicts individual object instances directly — no [Connected Components](/commands/segmentation/connected-components/) or [Watershed](/commands/segmentation/watershed/) step is needed afterward.

:::note[Build requirement]
AI segmentation commands are only available in builds with the `ai` Cargo feature enabled (via [tch-rs](https://github.com/LaurentMazare/tch-rs)/libtorch).
:::

## Parameters

| Parameter | Description |
|---|---|
| **Model path** | Path to a TorchScript-exported StarDist model (`.pt` / `.pth`, via `torch.jit.script` or `torch.jit.trace`). |
| **Object class** | The segmentation class assigned to every detected object's pixels. |
| **Probability threshold** | Probability above which a grid cell is considered a candidate object centre. Range: 0.0–1.0 (default 0.5). |
| **NMS threshold** | Pixel-overlap ratio (intersection / union) above which a lower-scoring candidate polygon is suppressed in favour of an overlapping higher-scoring one. Range: 0.0–1.0 (default 0.3). |

## Model requirements

The model must accept a `[1, 1, H, W]` single-channel float tensor and return:
- An **object-probability map** `[1, 1, H', W']`
- A **ray-distance map** `[1, n_rays, H', W']` — the distance to the object boundary along `n_rays` equally-spaced angles (the StarDist star-convex-polygon representation)

`H'`/`W'` may be smaller than the input size if the model predicts on a coarser grid; EVAnalyzer detects this from the output shape and rescales the polygons back to image resolution automatically. Some TorchScript exports concatenate both outputs into a single `[1, 1 + n_rays, H', W']` tensor (channel 0 = probability, the rest = distances) — this layout is also supported.

## How it works

1. The model runs on the input image, producing per-grid-cell probability and ray-distance predictions.
2. Grid cells with probability ≥ **Probability threshold** are converted into star-convex polygon candidates.
3. Candidates are filtered with greedy non-maximum suppression: lower-scoring polygons overlapping a higher-scoring one by more than **NMS threshold** are discarded.
4. Surviving polygons are rasterised directly into the pipeline's segmentation and instance maps, each with a unique instance ID.

Runs on GPU automatically if CUDA is available in the linked libtorch build, otherwise falls back to CPU.

:::tip[Genuine StarDist exports only]
Only models that predict object probability + radial distances work with this command. A boundary-aware U-Net export (mask + boundary channels) is a different model type — use [AI UNet Segmentation](/commands/ai-segmentation/unet/) for those instead.
:::

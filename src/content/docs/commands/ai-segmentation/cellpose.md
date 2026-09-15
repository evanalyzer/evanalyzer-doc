---
title: AI Cellpose Segmentation
description: Instance segmentation using a pretrained Cellpose-SAM model.
---

The **AI Cellpose Segmentation** command runs instance segmentation using a pretrained [Cellpose-SAM](https://github.com/MouseLand/cellpose) model exported as TorchScript - Cellpose-SAM integrates the transformer image encoder from Meta's Segment Anything Model (SAM) with Cellpose's flow-field dynamics for improved generalization over earlier, convolutional Cellpose versions.
Like [Stardist](/commands/ai-segmentation/stardist/), it recovers individual object instances directly - no [Connected Components](/commands/segmentation/connected-components/) or [Watershed](/commands/segmentation/watershed/) step is needed afterward.

Rather than predicting a shape directly, the model predicts a vector field: at every pixel, "which direction is the centre of my cell?" Simulating each pixel's short walk along that field causes every pixel belonging to the same cell to converge on the same point - so instances fall out of _where pixels end up_, which handles irregular and overlapping shapes that a fixed polygon representation (like Stardist's) can't.

![Every foreground pixel is pushed along the predicted flow field toward its cell's centre; shared destinations become one instance](../../../../assets/figures/cmd-cellpose.svg)

:::note[Build requirement]
AI segmentation commands are only available in builds with the `ai` Cargo feature enabled (via [tch-rs](https://github.com/LaurentMazare/tch-rs)/libtorch).
:::

## Usage

1. **Download the model.** Ready-to-use Cellpose-SAM TorchScript exports are on the [Downloads page](/downloads/#ai-models) - download `cpsam_v2.zip` and unzip it; it contains a single `cpsam_v2.pt` file. See [Getting a model](#getting-a-model) below if you need a different checkpoint.
2. **Add AI Cellpose Segmentation to the pipeline.** Point **Model path** at the extracted `.pt` file and tune the parameters below. Normalize the image first (e.g. with [Enhance Contrast](/commands/image-processing/enhance-contrast/)) - see the tip in [How it works](#how-it-works).
3. **Follow with Extract Objects.** Append [Extract Objects](/commands/object/extract-objects/) directly after this command - AI Cellpose Segmentation already writes a per-instance label map, so Extract Objects can turn it straight into object records without a Connected Components/Watershed step in between. From there, [Classify Objects](/commands/object/classify-objects/) assigns the final object class.

## Parameters

| Parameter                 | Description                                                                                                                                                                                                      |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model path**             | Path to a TorchScript-exported Cellpose-SAM model (`.pt` / `.pth`, via `torch.jit.script` or `torch.jit.trace`).                                                                                                |
| **Object class**           | The segmentation class assigned to every detected object's pixels.                                                                                                                                              |
| **Input channels**         | Number of input channels the model expects. The grayscale image goes in channel 0; any further channels are zero-filled. `2` (cytoplasm + optional nucleus) is standard; `1` is for single-channel exports. Range: 1–3 (default 2), matching Cellpose-SAM's patch-embedding convolution, which only has weights for up to 3 input channels. |
| **Probability threshold**  | Cell probability above which a pixel takes part in the flow dynamics and can be assigned to an object. Range: 0.0–1.0 (default 0.5 - corresponds to Cellpose's default logit threshold of `0`).                |
| **Flow iterations**        | Number of Euler integration steps used to follow the flow field. Higher values let pixels in large cells reach their sink, at the cost of runtime. Range: 1–1000 (default 200, matching Cellpose's own default). |
| **Minimum object size**    | Minimum instance size in pixels; smaller instances are discarded after the dynamics. `0` disables the filter. Default 15.                                                                                       |

## Getting a model

Ready-made exports live on the [Downloads page](/downloads/#ai-models): download `cpsam_v2.zip`, unzip it, and point **Model path** at the `cpsam_v2.pt` file inside.

To export a different checkpoint yourself (e.g. a fine-tuned one), use [`convert_cellpose.py`](https://github.com/evanalyzer/evanalyzer/blob/main/docs/convert_cellpose.py) from the EVAnalyzer repository. It rebuilds the Cellpose-SAM network with the `cellpose` Python package, loads the requested weights, and re-saves them with `torch.jit` as a `.pt` file EVAnalyzer can load directly:

```bash
pip install "cellpose>=4" torch
python convert_cellpose.py --output cellpose_sam.pt
```

Only the Cellpose-SAM family (`cpsam`/`cpsam_v2`, backbone `sam_vitl`) is supported - classic Cellpose (v3.x and earlier, the convolutional CPnet architecture) has a different architecture and output layout and isn't handled by this command or the conversion script. A raw checkpoint downloaded by the `cellpose` package (or from [huggingface.co/mouseland/cellpose-sam](https://huggingface.co/mouseland/cellpose-sam)) holds only weights with no computation graph, so it can't be loaded directly either - it has to go through the conversion step above first.

## Model requirements

The model must accept a `[1, C, 256, 256]` float tensor, where `C` matches **Input channels**, and return a `[1, 3, 256, 256]` tensor with at least 3 channels, in Cellpose's spatial-gradient representation:

- Channel 0 - vertical flow (`dY`)
- Channel 1 - horizontal flow (`dX`)
- Channel 2 - cell-probability logits (a sigmoid is applied internally; the threshold above is in probability space, not logit space)

Cellpose-SAM's ViT (SAM) encoder bakes its positional embeddings for a fixed 256×256 token grid at export time, so the exported graph only ever runs at exactly that size. You never need to export at any other resolution - EVAnalyzer pads and splits larger (or smaller) images into overlapping 256×256 tiles internally and blends the results back together (see [How it works](#how-it-works)), so a model traced once at 256×256 handles any input size. Exports that wrap the output in a tuple (e.g. `(flows, style)`) are also supported - EVAnalyzer uses the first returned tensor with at least 3 channels.

## How it works

This is a Rust port of Cellpose's own _dynamics_ step, with tiling added for Cellpose-SAM's fixed input size:

1. The image (with any extra **Input channels** zero-filled) is padded and split into overlapping 256×256 tiles - Cellpose-SAM's ViT encoder only accepts that fixed size. Each tile is run through the model, and the per-tile flow/probability outputs are blended back into one image-sized tensor with a feathered (sigmoid taper) weight per tile, matching Cellpose's own `transforms.average_tiles`, so a segmentation spanning a tile boundary doesn't show a seam.
2. Pixels whose cell probability reaches **Probability threshold** are advected along the flow field for **Flow iterations** Euler steps (the predicted flow is divided by Cellpose's training scale factor of 5 to keep each step near one pixel), converging toward the centre ("sink") of their object.
3. Pixels that converge to the same sink are grouped into one instance, found via 8-connected connected components over the density of final pixel positions.
4. Instances smaller than **Minimum object size** are discarded; survivors are renumbered to contiguous instance IDs and written to the segmentation and instance maps.

Runs on GPU automatically if CUDA is available in the linked libtorch build, otherwise falls back to CPU.

:::tip[Normalize your image first]
Cellpose normally applies per-channel percentile normalization before the network runs, but that step lives in Cellpose's Python preprocessing, not in the exported TorchScript graph - feed this command a reasonably contrast-normalized image (e.g. via [Enhance Contrast](/commands/image-processing/enhance-contrast/) with **Normalize** enabled) for results comparable to the Cellpose GUI.
:::

:::tip[Choosing between Cellpose-SAM and Stardist]
Cellpose-SAM's flow-based approach handles irregular, elongated, and overlapping-but-distinct cell shapes that Stardist's star-convex polygons can't represent well. For round, convex objects like nuclei, Stardist is faster and equally accurate - see [Choosing a Model](/ai/overview/#choosing-a-model).
:::

## Background

Cellpose-SAM combines Cellpose's flow-field dynamics with a Segment-Anything-based image encoder:

Marius Pachitariu, Michael Rariden, and Carsen Stringer, "Cellpose-SAM: superhuman generalization for cellular segmentation," _bioRxiv_, 2025.

Carsen Stringer, Tim Wang, Michalis Michaelos, and Marius Pachitariu, "Cellpose: A Generalist Algorithm for Cellular Segmentation," _Nature Methods_, vol. 18, pp. 100-106, 2021.

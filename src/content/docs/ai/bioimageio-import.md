---
title: Importing bioimage.io Models
description: Import a pretrained model from bioimage.io and auto-configure an AI Segmentation step.
---

[bioimage.io](https://bioimage.io) is a community repository of pretrained deep-learning models for bioimage analysis, each published with a **Resource Description File** (`rdf.yaml`) describing its architecture, inputs/outputs, and (optionally) pre/post-processing requirements.

Instead of manually filling in a [Stardist](/commands/ai-segmentation/stardist/), [UNet](/commands/ai-segmentation/unet/), or [Cellpose](/commands/ai-segmentation/cellpose/) command by hand, you can point EVAnalyzer at a downloaded model's `rdf.yaml` and have it pre-fill an AI Segmentation step for you.

## Importing a Model

1. Download a model package from [bioimage.io](https://bioimage.io) and extract it to a local folder. The folder must contain an `rdf.yaml` (or `rdf.yml`) file.
2. In the **Pipelines** panel, click **+ Add step** at the position where the segmentation step should go.
3. In the command picker's **Segment** section, click **Import bioimage.io model…**.
4. Select the model's `rdf.yaml` file in the file picker.

EVAnalyzer parses the file, detects the model architecture, and inserts a pre-configured pipeline step at that position - no separate download step is needed for the RDF metadata itself.

## Supported Model Types

| Model                                           | Detected when…                                                                          |
| ----------------------------------------------- | --------------------------------------------------------------------------------------- |
| [Cellpose](/commands/ai-segmentation/cellpose/) | The RDF's name, description, or tags mention "cellpose"                                 |
| [Stardist](/commands/ai-segmentation/stardist/) | The RDF's name/description/tags mention "stardist", or it has a `config.stardist` block |
| [UNet](/commands/ai-segmentation/unet/)         | Fallback for any other segmentation model                                               |

Whatever is detected from the model card is filled in automatically:

- **Cellpose** - model path, and **Input channels** read from the RDF's input tensor shape (defaults to 2 if it can't be determined).
- **Stardist** - model path, plus **Probability threshold** / **NMS threshold** if present in the RDF's `config.stardist.thresholds` block.
- **UNet** - model path, and the output layout: a 2-channel mask+boundary output is mapped to **Independent Channels** (foreground = channel 0, boundary = channel 1); a multi-class softmax output assumes the foreground is the last channel.

After the step is inserted, a dialog lists any caveats about what was assumed - review these and adjust the step's parameters if they don't match your model:

- Channel count or output layout could not be determined from the RDF, so a default was used.
- The model declares input preprocessing (e.g. normalization) - EVAnalyzer does not apply this automatically; add equivalent steps (e.g. [Intensity Transform](/commands/image-processing/intensity-transform/)) before the AI Segmentation step.
- A boundary-aware UNet model was detected - add a [Connected Components](/commands/segmentation/connected-components/) step afterwards to separate touching objects.
- The model's weights are hosted remotely - download the weights file yourself and point **Model path** at the local file.

## Requirements

- The RDF must describe a `model` resource (not a dataset or notebook) and ship **TorchScript** weights (`weights.torchscript`, or the deprecated `weights.pytorch_script` key). A model that only provides raw `pytorch_state_dict` weights cannot be imported directly - convert it to TorchScript first.
- Both RDF spec versions 0.4 and 0.5 are supported.
- Only the three segmentation architectures above are recognised. Classification, detection, or other model types will not be configured correctly.
- Importing a model does not require AI/CUDA support to be installed - it only writes pipeline configuration. Running the resulting step still requires a build with the `ai` feature enabled (see [AI Models](/ai/overview/)).

:::tip
Always double-check the auto-filled parameters - especially channel counts and the foreground/boundary channel mapping - against the model's actual documentation before running a full analysis.
:::

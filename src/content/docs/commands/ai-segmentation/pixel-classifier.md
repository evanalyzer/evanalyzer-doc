---
title: AI Pixel Classifier
description: Classify every pixel of an image with a Random Forest, k-Nearest Neighbors, or neural-network model trained in the Train Classifier dialog.
---

The **AI Pixel Classifier** command applies a pixel classifier trained via the app's [Train Classifier dialog](/ai/training/) as a segmentation step. It recomputes the exact feature recipe baked into the model at training time, classifies every pixel of the image independently, and writes the result into the segmentation map - the same output shape [Threshold](/commands/segmentation/threshold/) produces, so downstream steps like [Connected Components](/commands/segmentation/connected-components/) and [Extract Objects](/commands/object/extract-objects/) don't need to care which one ran.

Available in builds with the `ai` Cargo feature enabled - see [AI Models](/ai/overview/).

## Parameters

| Parameter | Description |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Model Path** | Path to a trained pixel classifier `.evamodel` file, saved from the [Train Classifier](/ai/training/) dialog |
| **Segmentation Mapping** | Maps each of the model's predicted classes to one of this project's segmentation classes |

The model's own classes are a snapshot taken at training time and aren't guaranteed to line up with this project's segmentation class numbers - **Segmentation Mapping** is the bridge between the two. It's a repeatable list of `Segmentation Class → Object Class ID` pairs, one entry per model class you want to map through.

:::note[Unmapped classes become background]
A predicted class with no matching **Segmentation Mapping** entry is written as `Background` - the same convention [Threshold](/commands/segmentation/threshold/) uses for pixels outside every configured intensity range. Mapping only the classes you care about is a deliberate simplification, not an oversight; you don't need an entry for every class the model was trained on.
:::

The command errors if **Model Path** doesn't exist, or if it points at a model trained as an **Object Classifier** instead of a **Pixel Classifier**.

## Example

A pixel classifier `nuclei-px.evamodel` was trained on two classes: `Background` and `Nucleus`.

```
Model Path:            models/nuclei-px.evamodel
Segmentation Mapping:  Nucleus → 1
```

Pixels predicted as `Nucleus` are written to segmentation class `1`; pixels predicted as `Background` (left unmapped) fall back to segmentation class `0`. A typical follow-up pipeline: **AI Pixel Classifier** → [Connected Components](/commands/segmentation/connected-components/) → [Extract Objects](/commands/object/extract-objects/) → [Classify Objects](/commands/object/classify-objects/).

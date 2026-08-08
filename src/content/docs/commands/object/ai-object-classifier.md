---
title: AI Object Classifier
description: Classify already-extracted objects with a Random Forest, k-Nearest Neighbors, or neural-network model trained in the Train Classifier dialog.
---

The **AI Object Classifier** command applies an object classifier trained via the app's [Train Classifier dialog](/ai/training/) as a classification step: every object in the pipeline cache matching **Input Classes** is scored independently, using the same feature recipe used at training time, then remapped through **Segmentation Mapping** into this project's own classes and applied via **Match Handling**.

It uses the same input-selection logic as [Classify Objects](/commands/object/classify-objects/), but the output class comes from a trained model's prediction instead of a fixed shape/intersection rule - use it where the populations aren't cleanly separable by shape criteria, or to complement a Classify Objects step earlier in the pipeline.

Available in builds with the `ai` Cargo feature enabled - see [AI Models](/ai/overview/).

## Parameters

| Parameter | Description |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Model Path** | Path to a trained object classifier `.evamodel` file, saved from the [Train Classifier](/ai/training/) dialog |
| **Segmentation Mapping** | Maps each of the model's predicted classes to one of this project's object classes (despite the name, this maps *object* classes, not segmentation classes - a naming quirk carried over from the pixel classifier's equivalent field) |
| **Input Classes** | Restrict scoring to objects that already carry **every** one of these classes. Leave empty to evaluate every object regardless of its current class - same AND semantics as Classify Objects' Input Classes (see [Object Classes](/fundamentals/classes/)) |
| **Match Handling** | What to do with an object's classes once a mapped prediction is applied - see below |

### Match Handling

| Mode (GUI label) | Effect |
| --------------------------------------- | --------------------------------------------------------- |
| **Add class on match** | Add the mapped class alongside the object's existing classes |
| **Reclassify on match** *(default)* | Clear every class the object carries, then assign only the mapped class |

:::note[Unmapped predictions leave the object untouched]
A predicted class with no matching **Segmentation Mapping** entry - including a mapping row still left at its default, unset target - leaves the object's classes completely unchanged, in either **Match Handling** mode. This differs from [AI Pixel Classifier](/commands/ai-segmentation/pixel-classifier/), where an unmapped prediction resets the pixel to `Background`: here, "no rule matched" means "don't touch it," matching how a partially-configured mapping list is expected to behave mid-setup.
:::

The command errors if **Model Path** doesn't exist, or if it points at a model trained as a **Pixel Classifier** instead of an **Object Classifier**.

## Example

An object classifier `debris-vs-ev.evamodel` was trained on two classes: `Background` and `EV` (extracellular vesicle), using shape metrics to separate genuine vesicles from imaging debris that survived thresholding.

```
Model Path:            models/debris-vs-ev.evamodel
Input Classes:         cy5@spot
Segmentation Mapping:  EV → cy5@ev
Match Handling:        Reclassify on match
```

Every `cy5@spot` object is scored; objects predicted as `EV` are reclassified to `cy5@ev`, while objects predicted as `Background` (left unmapped) keep their original `cy5@spot` class untouched.

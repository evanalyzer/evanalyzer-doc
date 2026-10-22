---
title: Load Image Channel
description: Load an image channel as the image the following steps work on.
---

The **Load Image Channel** command replaces the current image with another channel of the same image. The following steps work on the loaded channel.

Use it

- as the **first step of a pipeline without an image source** (image source **None** in the pipeline dialog), or
- to **switch channels within a pipeline** - for example a [module](/guide/modules/) that detects nuclei in one channel and cells in another.

## Parameters

| Parameter   | Description              |
| ----------- | ------------------------ |
| **Channel** | The image channel to load. |

The objects, the segmentation and the memory slots of the pipeline are not touched - only the image is replaced.

## Notes

- In a module, the channel of a Load Image Channel step becomes a module parameter when the module is created, so every use of the module can pick its own channel.
- Before an analysis starts, EVAnalyzer checks that every image has the channels the pipelines load. An image without the channel fails with a message naming the channels it does have.
- [Focus mode](/guide/pipelines/#focus-mode) shows the channels a pipeline loads with this command, too.

---
title: Image Math
description: Combine two images using a mathematical operation.
---

The **Image Math** command applies a pixel-wise mathematical operation between the current pipeline image and a second image. The second image can come from a specific image channel or from a previously cached image.

## Parameters

| Parameter                | Description                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Operand**              | The mathematical operation to apply (_Add_, _Subtract_, _Multiply_, _Divide_, _Min_, _Max_, _And_, _Or_, …) |
| **Second image address** | Channel and plane of the second operand                                                                     |
| **Swap operands**        | If enabled, the second image is used as the first operand of the operation                                  |

## Second Image Source

The second image is specified by an `ImageAddress`:

- **Image channel** - loads the specified channel/Z/T plane from the current image file.
- **From cache** - loads an image previously stored by an [Image Cache](/commands/image-processing/image-cache/) step.

When loading from cache, the image channel settings are ignored.

## When to use

Common uses:

- **Subtract** a background channel from a signal channel.
- **Add** or **Multiply** to amplify co-stained regions.
- **Min/Max** to create composite masks from multiple channels.

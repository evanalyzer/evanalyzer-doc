---
title: Translate Image
description: Shift the image by a fraction of a pixel - e.g. a fixed shift between two channels of a microscope.
---

**Translate Image** shifts the image by a fraction of a pixel. The image keeps its size; the strip the shift empties at the edge is filled as set under **Padding**. Use it for a fixed shift between two channels of a microscope (chromatic shift, a second camera), or to align a channel before it is combined with another, e.g. in [Image Math](/commands/image-processing/image-math/).

To shift a reference channel onto the target and subtract it, with the shift estimated per image, use [Subtract Reference Channel](/commands/image-processing/subtract-reference-channel/).

![An image shifted by dy 0.5 and dx 1.5 px with Linear interpolation: the content moves down and right, between the pixels its values are interpolated, and the strip the shift empties at the top and left edge is filled by the padding. Below, the interpolation kernels: Nearest, Linear and Keys' Cubic](../../../../assets/figures/cmd-translate-image.svg)

In a project file it is `TRANSLATE_IMAGE`.

## Parameters

| Parameter | Description |
| --- | --- |
| **Dy** | Shift down (+) or up (−) in pixels, fractions allowed. Default 0, -1000 to 1000. |
| **Dx** | Shift right (+) or left (−) in pixels, fractions allowed. Default 0, -1000 to 1000. |
| **Interpolation** | How the values between pixels are computed. **Nearest**: the nearest pixel (the only choice for label images). **Linear** (default): bilinear, from the 4 nearest pixels. **Cubic**: bicubic, from the 16 nearest pixels - sharper than Linear, may over- and undershoot at edges. |
| **Padding** | What fills the strip the shift empties at the edge. **Replicate** (default): the edge pixel repeated. **Reflect**: mirrored at the edge without repeating the edge pixel (…, 2, 1, 0, 1, 2, …). **Constant**: the **Pad Value**. |
| **Pad Value** | _(advanced)_ The fill value for Padding Constant. Default 0. |

## How it works

$$
\text{output}(y, x) = \text{input}(y - d_y,\; x - d_x)
$$

Positive $d_y$ moves the content down, positive $d_x$ to the right - the convention of `scipy.ndimage.shift`, so shifts measured in Python can be used as they are.

The shift is the same for every pixel, so are the interpolation weights. Each axis has one kernel: one tap for Nearest or a whole-pixel shift, two for Linear ($1 - t$ and $t$, with $t$ the fraction of the shift), four for Cubic. Cubic is Keys' cubic convolution with $a = -\tfrac12$ (Catmull-Rom):

$$
W(s) = \begin{cases} \tfrac32|s|^3 - \tfrac52|s|^2 + 1 & |s| \le 1 \\ -\tfrac12|s|^3 + \tfrac52|s|^2 - 4|s| + 2 & 1 < |s| < 2 \\ 0 & \text{else} \end{cases}
$$

The rows are interpolated first, then the columns. A whole-pixel shift copies the pixels, whatever the interpolation, so it doesn't blur. A volume is shifted plane by plane, a colour image the same in every colour.

## Limitations

- Label images can only be shifted with **Nearest**; Linear or Cubic stop the step with an error.
- The shift must be smaller than the image.
- It runs per tile: on an image split into tiles (larger than 4096 px), the padding also fills a strip at the inner tile borders, as wide as the shift.

## In a project file

```json
{ "type": "TRANSLATE_IMAGE", "dy": 0.5, "dx": -1.25,
  "interpolation": "CUBIC", "padding": "REPLICATE", "padValue": 0.0 }
```

A [script](/commands/image-processing/script/) runs it as `run("translate_image", image, #{ dy: 0.5, dx: -1.2 })`.

## References

- Keys R., "Cubic convolution interpolation for digital image processing," _IEEE Transactions on Acoustics, Speech, and Signal Processing_, vol. 29, pp. 1153-1160, 1981. [doi:10.1109/TASSP.1981.1163711](https://doi.org/10.1109/TASSP.1981.1163711)

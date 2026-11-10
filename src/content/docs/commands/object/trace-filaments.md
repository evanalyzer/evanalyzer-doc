---
title: Trace Filaments
description: Trace each neuron as a tree from its soma to its neurite tips along the cheapest paths through the image, split into segments at its branch points.
---

**Trace Filaments** traces each neuron as a tree: from its soma along the neurites to their tips, as the cheapest paths through the image. The paths bridge the dim stretches where a threshold breaks a neurite, and each tip goes to the soma that reaches it most cheaply, so touching neurons are told apart. The tree is split at its branch points into **segments**: 1-pixel-wide objects, each linked to the next segment towards the soma and to its soma.

![A soma (blue) and the tips (orange dots): the cheapest paths from the tips back to the soma meet and go on as one; the tree is split at its branch points into segments, each linked to the next segment towards the soma; a short side branch is pruned; a tip beyond the reach is left out](../../../../assets/figures/cmd-trace-filaments.svg)

Use it for neuron morphology: a typical pipeline finds the somata, thresholds the neurites, [skeletonizes](/commands/object/skeletonize-objects/) them with an end point class, and traces from the somata to those end points. [Measure Filament Tree](/commands/measure/measure-filament-tree/) then measures the trees, and [Results › Trees](/guide/results/#trees) shows each neuron's tree as a dendrogram.

In a project file it is `TRACE_FILAMENTS`.

## Parameters

| Parameter             | Description                                                                                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Seeds**             | The somata: each the root of one tree.                                                                                                                                         |
| **Targets**           | The tips to reach (e.g. the end points of [Skeletonize Objects](/commands/object/skeletonize-objects/)).                                                                       |
| **Output Class**      | The class the segments get.                                                                                                                                                    |
| **Channel**           | The channel the neurites are in (their stain).                                                                                                                                 |
| **Follow Fibres**     | Follow tube-shaped structures (the [vesselness](/commands/edge-detection/vesselness/) of the channel at the fibre widths), else the brightness alone, which also follows blobs and debris. On by default. |
| **Min Width**         | With **Follow Fibres**: the thinnest fibres to follow (0.5 to 1000, default 2).                                                                                                |
| **Max Width**         | With **Follow Fibres**: the widest fibres to follow (0.5 to 1000, default 6).                                                                                                  |
| **Max Reach**         | How far from its soma a tip may be (1 to 100000, default 300). It sets the search window: the soma's bounding box grown by this on every side.                                 |
| **Min Branch Length** | Side branches shorter than this are removed (0 to 100000, default 5).                                                                                                          |
| **Unit**              | Unit of the widths, the reach and the branch length: **px** (default) or **nm**. Without a pixel size, nm are taken as pixels.                                                |

## Output

One object of the **Output Class** per segment: the pixels of the traced path between two branch points (or between the soma, a branch point and a tip), 1 pixel wide. Each segment is linked to two parents:

- its soma, as a parent of the **Seeds** class;
- the next segment towards the soma, as a parent of the **Output Class**. A segment that starts at the soma (a root segment) has none.

Each segment gets the segmentation class and plane of its soma, and its intensities are measured like any other object's. A soma without a tip it reaches gets no segments.

:::note
[Relate Objects](/commands/object/relate-objects/) is otherwise the only step that links objects. Trace Filaments links its segments itself, as the tree is known exactly while tracing; finding it again from overlap would fail for segments that touch or cross. A later Relate Objects can still add links to other parent classes.
:::

## How it works

Each soma is traced in its own window: its bounding box grown by **Max Reach** on every side, cut to the image. The windows are traced in parallel; the result is the same in every run.

**1. Cost.** Every pixel gets a price for crossing it, low along fibres. With **Follow Fibres**, $v$ is the vesselness of the channel (Frangi et al. 1998) at three widths, log-spaced from **Min Width** to **Max Width** (scale $\sigma = w / \sqrt{6}$, bright fibres, blob suppression 0.5, automatic noise level), the cost image that tracers such as NeuronJ (Meijering et al. 2004) and SNT (Longair et al. 2011) use. Without it, $v$ is the channel's brightness. With $v_{\max}$ the highest value in the window:

$$
c(p) = \frac{1}{v(p) / v_{\max} + 0.01}
$$

so about 1 on the strongest fibre and up to 100 on the background. Pixels outside the read image can't be crossed.

**2. Shortest paths.** A shortest-path search (Dijkstra 1959) runs from all somata whose box lies in the window at once, their pixels the start. Each pixel steps to its 8 neighbours; a step costs its length times the mean cost of its two pixels:

$$
\text{step}(p, q) = \ell \cdot \frac{c(p) + c(q)}{2}, \qquad \ell = 1 \text{ or } \sqrt{2}
$$

Every pixel learns its cheapest way back and the soma at its end. Where somata overlap, the first in image order keeps the shared pixels.

**3. The tree.** Each tip is the centre of a **Targets** object, rounded to the nearest pixel. From each tip whose cheapest way leads to this soma, the path is followed back to the soma; paths that meet go on as one. A tip outside the window, on a soma, or that no path reaches is left out. A tip that another soma reaches more cheaply goes to that soma's tree.

**4. Segments.** The tree is split where it branches: a segment runs from the soma or a branch point to the next branch point or tip. Root segments start on a pixel of the soma; paths that reach the soma at different pixels make separate root segments (primary neurites).

**5. Pruning.** A side branch (a segment ending in a tip that doesn't start at the soma) shorter than **Min Branch Length** is removed. A branch point left with one branch is no more one: its two segments become one. This repeats until nothing changes. Lengths count 1 per straight and $\sqrt{2}$ per diagonal step.

## Limitations

- **Crossing neurites.** Where two neurites cross in the image, the cheapest path can turn off at the crossing onto the other one, the known weakness of 2D tracers.
- **Competition within a window.** A tip goes to the cheapest soma among the somata in the tracing soma's window only. A soma outside it doesn't compete, so with a **Max Reach** smaller than the distance between neighbouring neurons, a tip near the window's edge can go to the wrong one. A larger reach helps, at more RAM.
- **RAM.** A window needs about 25 bytes per pixel, one window per thread: a reach of 300 px around a small soma is a window of about 600 × 600 px.
- The trace is 2D: it follows the neurites in the image plane only.

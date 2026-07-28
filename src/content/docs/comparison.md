---
title: EVAnalyzer vs. CellProfiler vs. QuPath
description: How EVAnalyzer compares to CellProfiler and QuPath, and when to choose one over the other.
---

While **CellProfiler** relies on a _rigid, linear pipeline_ and **EVAnalyzer** features a _high-performance, branching pipeline_, **QuPath** relies on an **object-centric, map-based workflow**.
It was originally created for massive whole-slide pathology images, but it handles high-throughput multiplex/multi-channel fluorescence data exceptionally well.

---

### Core Architectural Differences

| Feature | CellProfiler | EVAnalyzer / ImageC | QuPath |
| --- | --- | --- | --- |
| **Data Philosophy** | **Pixel-Based.** Computes mathematical pixel arrays in strict sequential blocks. | **Channel-Split Branches.** Distributes raw pixel streams down independent, custom-filtered steps. | **Object-Hierarchical.** Segments base "parent" structures (cells) and maps child objects inside them. |
| **Max Image Scale** | Limited by RAM. Large images over 2 gigapixels can cause performance bottlenecks or crashes. | **Pyramid/Tile-Based.** Automatically splits [big images](/fundamentals/image-formats/#big-images) into tiles for analysis and stitches the results, with a pyramid-based navigator minimap for viewing. | **Pyramid-Based/Infinite.** Handles massive Multi-Gigapixel whole-slide scans seamlessly via on-screen data tiling. |
| **Pipeline Creation** | Drag-and-drop a vertical stack of pre-built modules. | Compose 31+ functional commands into a custom routing flow. | **Macro-Recording Scripts.** Interactively execute commands; QuPath writes a Groovy script in the background. |
| **Multiplexing Strategy** | Linear calculation: every channel passes down the exact same sequential steps. | Branching paths: allows distinct, unique mathematical steps for each channel. | **Shared Cell Boundary:** Finds nuclei in one channel, builds cell boundaries, and measures all other channel intensities instantly. |

---

### What QuPath Can Do (That CellProfiler & EVAnalyzer Cannot)

- **Subcellular Object Hierarchy Mapping:** QuPath embeds an object hierarchy. Once it defines a cell boundary, it permanently understands that cell as a container. If you spot a protein spot inside it, QuPath tracks it natively as a "child object" belonging to that specific parent cell, maintaining spatial tissue coordinates.

---

### What QuPath & EVAnalyzer Can Do (That CellProfiler Cannot)

- **Handle Truly Massive, Multi-Gigapixel Whole Slides:** CellProfiler is built for field-of-view (FOV) microscope frames - feed it a single 20GB whole-tissue biopsy scan and it will lag or crash. QuPath and EVAnalyzer both handle multi-gigapixel whole-slide scans natively: QuPath loads only what's on screen via on-the-fly pyramid tiling, while EVAnalyzer automatically splits big images into tiles for pipeline analysis and stitches the results back together, using the same pyramid data for a navigator minimap.
- **Trainable Pixel Classifiers:** Instead of testing arbitrary mathematical threshold numbers, both tools let you train a classifier on labeled examples rather than hand-tuning thresholds. QuPath's is an interactive point-and-click workflow: draw shapes over cells, label them "Positive"/"Negative", and it trains a random forest classifier instantly. EVAnalyzer trains a pixel classifier (random forest or MLP) on labeled examples that can then be used as a segmentation step in a pipeline, like a pretrained model. CellProfiler has no equivalent - it relies on manually-set thresholds.

---

### What CellProfiler & EVAnalyzer Can Do (That QuPath Cannot)

- **Custom Geometric Math & Shape Morphing:** In QuPath, your cell body is usually derived by expanding a set distance outward from the nucleus. You cannot cleanly warp, shrink, subtract custom masks, or perform complex mathematical steps (like creating a 3-pixel wide rim around an organelle) mid-pipeline the way you can with CellProfiler, or with EVAnalyzer's [Object Math](/commands/object/object-math/) boolean object operations.
- **True Independent Per-Channel Preprocessing:** QuPath's fast cell detector requires choosing **one principal anchor channel** (usually DAPI/Nuclei) to locate cells. If you have a channel that requires a completely custom mathematical background extraction method or adaptive thresholding before detection, it is hard to isolate it. EVAnalyzer excels here by allowing you to split every channel into a completely custom [pipeline](/guide/pipelines/).

---

### Which tool matches your multiplex pipeline project?

- **Choose EVAnalyzer if:** You are working with high-throughput, multi-channel images (including massive whole-slide scans) where each fluorescence marker channel requires a completely different processing setup before you calculate colocalization, and you want the option to train a pixel classifier on your own data rather than hand-tuning thresholds.
- **Choose CellProfiler if:** You have regular-sized images and your science depends on extracting highly precise cell shape modifications, structural orientations, or deep texture details.
- **Choose QuPath if:** You want an interactive, point-and-click classifier-training workflow with a built-in parent/child object hierarchy, particularly for whole-slide pathology work.

---
title: EVAnalyzer vs. CellProfiler vs. QuPath
description: How EVAnalyzer compares to CellProfiler and QuPath, and when to choose one over the other.
---

**EVAnalyzer** relies on on a _branching pipeline_, **CellProfiler** on a _linear pipeline_, and **QuPath** on an **object-centric, map-based workflow**.
It was originally created for massive whole-slide pathology images, but it handles high-throughput multiplex/multi-channel fluorescence data exceptionally well.

---

### At a glance: which tool fits your project?

| Tool              | Choose it when...                                                                                                                                 | Core strength                                                                                                           | Its ceiling                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **EVAnalyzer**    | Multiplex/multi-channel fluorescence panels where every marker needs its own processing, especially at whole-slide scale.                         | Branching per-channel pipelines with built-in whole-slide tiling, live preview, and CLI batch/HPC execution.            | No time-lapse tracking, no true 3D volume rendering; a smaller measurement library than CellProfiler/ImageJ for classic single-channel quantification. |
| **CellProfiler**  | Deep, classic single- or few-channel quantification — precise shape, texture, colocalization, or particle-tracking metrics for a methods section. | The broadest, most mature measurement library here (Haralick texture, LAP tracking, Pearson's/Manders' colocalization). | One linear pipeline per run; per-channel branching and real multi-threaded throughput on large images both need manual workarounds.                    |
| **ImageJ / Fiji** | You need a specific plugin, a quick one-off manual measurement, or maximum flexibility via scripting (macros/Jython/Groovy).                      | The largest plugin ecosystem of any tool here — most niche bio-imaging algorithms exist as an ImageJ plugin.            | No structured no-code pipeline model; a reproducible pipeline means writing or recording macros yourself.                                              |
| **QuPath**        | Whole-slide digital pathology — parent/child object hierarchies (tissue → cell → sub-cell), TMA cores, point-and-click classifier training.       | Best-in-class whole-slide viewer/pyramid handling, plus a native object hierarchy no other tool here has.               | Not built for time-lapse/live-cell tracking, correlation-based colocalization, or independent per-channel preprocessing.                               |

---

### Detailed feature matrix

Support markings are a best-effort summary based on each project's public documentation: ✅ supported · ⚠️ partial/limited · — not supported or not documented. "ImageJ" covers the Fiji distribution (ImageJ2 plus its commonly bundled plugins, e.g. TrackMate, Coloc2, Trainable Weka Segmentation). Verify against each tool's current docs before relying on this for a purchasing or migration decision.

A checkmark alone can overstate real-world usability, for any tool here — see the "Its ceiling" column above for what each one still falls short on. One concrete example: CellProfiler's multi-threading (Section 7) technically exists, but scaling it to large images in practice typically means manually splitting images into tiles and launching multiple CellProfiler instances yourself. Its pipeline editor (Section 2, Live Preview) also has no continuous preview: you step through modules in Test Mode and wait for each run to complete, which gets slow on large images. Rows where a checkmark hides a gap like this carry a footnote.

### 1. File Import, I/O & Microscopic Data Handling

| Feature Name                      | Detailed Functionality                                                                                                                                                                                             | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ------------ | ------ | ------ |
| **Bio-Formats Integration**       | Native reader for vendor raw formats (`.czi`, `.nd2`, `.lif`, `.oib`, `.ome.tif`, `.svs`) using Bio-Formats or OME libraries. Avoids time-consuming pre-conversion to 8-bit TIFF and proprietary software lock-in. | ✅         | ✅           | ✅     | ✅     |
| **Metadata Parsing**              | Extracts spatial calibration ($\mu m/\text{pixel}$, Z-spacing), time intervals, channel names, emission wavelength, and objective info. Ensures accurate physical measurements without manual entry.               | ✅         | ✅           | ✅     | ✅     |
| **Automatic Channel Access**      | Individual channels of a multi-channel image are directly addressable right after import, without a separate per-channel mapping step.                                                                             | ✅         | ⚠️\*         | ✅     | ✅     |
| **Multidimensional (ND) Support** | Seamless display and navigation of 5D hyperstacks ($X, Y, Z, \text{Channel}, \text{Time/T}$).                                                                                                                      | ✅         | ⚠️           | ✅     | ✅     |
| **Microplate Grid Layouts**       | Automatic layout parsing for 96/384-well microplates with row/column coordinate mapping and tile stitching. Useful for high-throughput screening (HTS) workflows that group images by well/condition.              | ✅         | ✅           | ⚠️     | —      |
| **Lazy Loading & Virtual Stacks** | Streams image slices into RAM on demand instead of loading multi-gigabyte files entirely into memory.                                                                                                              | ✅         | ⚠️           | ✅     | ✅     |
| **Pyramidal / BigDataViewer**     | Supports multi-resolution image pyramids for rapid zooming and pan on terabyte-scale datasets.                                                                                                                     | ✅         | —            | ✅     | ✅     |
| **Whole-Slide Navigator Viewer**  | Dedicated interactive viewer with a pyramid-based navigator minimap for panning and zooming across gigapixel whole-slide scans.                                                                                    | ✅         | —            | ✅     | ✅     |

\*CellProfiler does not split channels automatically. You configure a **NamesAndTypes** module with filename regex/metadata rules (separate-file channels) or a channel-index mapping (single multi-channel file) to name and access each channel — get the mapping wrong and channels silently mismatch or drop.

---

### 2. GUI, Interactive UX & Daily Quality-of-Life

| Feature Name                      | Detailed Functionality                                                                                                                                                                    | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Flexible Contrast & LUTs**      | Per-channel histogram brightness/contrast tuning, non-destructive LUT application (HiLo, Fire, RGB, custom color maps). HiLo-style LUTs flag saturated and zero-value pixels at a glance. | ✅         | ⚠️           | ✅     | ✅     |
| **Keyboard Shortcuts & Commands** | Comprehensive keyboard hotkeys and searchable command palette (e.g., ImageJ Quick Search "Ctrl+L").                                                                                       | —          | ⚠️           | ✅     | ⚠️     |
| **Multi-Window Synchronization**  | Synchronized panning, zooming, and slice/time stepping across multiple image windows.                                                                                                     | —          | —            | ✅     | ⚠️     |
| **Undo / Redo Buffer**            | Multi-step history buffer for destructive pixel operations and ROI edits.                                                                                                                 | ✅         | ⚠️           | ⚠️     | ✅     |
| **Scale Bar & Dynamic Overlay**   | Burned-in or dynamic vector scale bars, timestamps, Z-depth indicators, and channel legends.                                                                                              | ✅         | ⚠️           | ✅     | ✅     |
| **Dark Mode / Theme UI**          | High-contrast dark theme option for interface components.                                                                                                                                 | ✅         | —            | ⚠️     | ✅     |
| **Image Viewer**                  | Built-in multi-channel viewer with per-channel visibility, colour, contrast, and Z/T navigation.                                                                                          | ✅         | ⚠️           | ✅     | ✅     |
| **Live Preview**                  | Immediate viewport update and live object count while editing a pipeline step, without re-running the full pipeline.                                                                      | ✅         | —\*          | ⚠️     | ✅     |

\*Test Mode lets you step through modules and inspect output windows, but there is no continuous, reactive preview while adjusting a setting — you re-run the step and wait, which is slow on large images.

---

### 3. Image Preprocessing, Filtering & Restoration

| Feature Name                   | Detailed Functionality                                                                                        | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Flat-Field Correction**      | Correction for uneven illumination profiles using flat-field / dark-field images or BaSiC / CIDRE algorithms. | ✅         | ✅           | ✅     | —      |
| **Background Subtraction**     | Rolling ball, top-hat, sliding paraboloid, or local background estimation algorithms.                         | ✅         | ✅           | ✅     | ⚠️     |
| **Noise Reduction Filters**    | Gaussian, Median, Anisotropic Diffusion, Bilateral, and Non-Local Means denoising filters.                    | ✅         | ✅           | ✅     | ⚠️     |
| **Image Registration & Drift** | Translation, rigid, affine, and elastic registration (e.g., Descriptor-based, TurboReg, StackReg).            | —          | ⚠️           | ✅     | ⚠️     |
| **Grid Stitching & Blending**  | Phase correlation stitching of overlapping tiles with non-linear seam blending.                               | —          | —            | ✅     | —      |
| **Deconvolution Tools**        | Theoretical/measured PSF generation and Richardson-Lucy / Tikhonov iterative deconvolution algorithms.        | —          | —            | ✅     | —      |

---

### 4. Segmentation, Object Detection & AI Tools

| Feature Name                           | Detailed Functionality                                                                                                                          | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Global & Local Thresholding**        | Classic automated thresholding (Otsu, Li, Yen, Maximum Entropy, Niblack, Bernsen, Sauvola).                                                     | ✅         | ✅           | ✅     | ✅     |
| **Morphological Operations**           | Erosion, Dilation, Opening, Closing, Hole Filling, Skeletonization, Distance Transform.                                                         | ✅         | ✅           | ✅     | ⚠️     |
| **Watershed Clustered Object Split**   | Marker-controlled watershed segmentation to separate touching or overlapping cells.                                                             | ✅         | ✅           | ✅     | ✅     |
| **Deep Learning AI Models**            | Native or plugin access to pretrained deep learning models (Cellpose, StarDist, Segment Anything / SAM).                                        | ⚠️         | ⚠️           | ✅     | ✅     |
| **bioimage.io Model Import**           | Import community-trained segmentation/classification models published in the bioimage.io model zoo format directly into a pipeline.             | ✅         | —            | ⚠️     | —      |
| **Machine Learning Pixel Classifiers** | Interactive scribble-based pixel classification (e.g., Trainable Weka Segmentation, Ilastik integration).                                       | ✅         | ⚠️           | ✅     | ✅     |
| **ROI Manager & Editing Tools**        | Store, group, rename, filter, dilate, measure, and export collections of vector ROIs.                                                           | ✅         | ⚠️           | ✅     | ✅     |
| **Object Math (Boolean Set Ops)**      | AND / OR / XOR / Subtract operations between object classes to combine, exclude, or reshape detected objects (e.g., a rim around an organelle). | ✅         | ⚠️           | ⚠️     | ⚠️     |

---

### 5. Quantification, Feature Extraction & Spatial Analysis

| Feature Name                      | Detailed Functionality                                                                                                  | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Morphometric Measurements**     | Area, perimeter, bounding box, major/minor axis, circularity, aspect ratio, roundness, solidity, 3D volume.             | ✅\*       | ✅           | ✅     | ✅     |
| **Densitometry & Intensity**      | Mean, min/max, median, integrated density, standard deviation of pixel values across channels.                          | ⚠️         | ✅           | ✅     | ✅     |
| **Colocalization Analysis**       | Pearson's correlation coefficient, Manders' overlap coefficients ($M_1/M_2$), Costes' thresholding, 2D cytofluorograms. | ⚠️         | ✅           | ✅     | —      |
| **Spatial Distance & Clustering** | Nearest neighbor distance, Delaunay triangulation, Voronoi tessellation, object-to-boundary distance.                   | ⚠️         | ⚠️           | ⚠️     | ✅     |
| **Texture Analysis (Haralick)**   | Grey-Level Co-occurrence Matrix (GLCM): contrast, correlation, energy, entropy, and local heterogeneity.                | —          | ✅           | ✅     | ✅     |
| **Filament & Skeleton Analysis**  | Branch point detection, filament length, segment classification, network connectivity metrics.                          | —          | ✅           | ✅     | —      |

\*No 3D volume support

---

### 6. Particle Tracking, Time-Lapse & Lineage Analysis

| Feature Name                      | Detailed Functionality                                                                                     | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Automated Particle Tracking**   | LAP (Linear Assignment Problem), Kalman filtering, or nearest-neighbor frame-to-frame linking algorithms.  | —          | ✅           | ✅     | —      |
| **Kinematic Trajectory Metrics**  | Velocity, instantaneous speed, directionality ratio, mean square displacement (MSD), confinement index.    | —          | ✅           | ✅     | —      |
| **Cell Division & Lineage Trees** | Handling cell division events (mitosis), branch creation, and full lineage tree visualization.             | —          | ✅           | ✅     | —      |
| **Manual Track Editing UX**       | Interactive track visualization with easy manual link breaking, joining, path deletion, and spot tweaking. | —          | —            | ✅     | —      |

---

### 7. Automation, Batch Processing & Reproducibility

| Feature Name                          | Detailed Functionality                                                                                                                                                                                                                                                    | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **No-Code Pipeline Builder**          | Compose a full analysis pipeline by adding and configuring pre-built commands, without writing scripts or macros.                                                                                                                                                         | ✅         | ✅           | ⚠️     | ⚠️     |
| **Multi-Channel Branching Pipelines** | Routes different channels or object classes down independent, custom-filtered processing branches within one project, instead of one linear sequence applied to everything. Lets each fluorescence marker get its own background correction, thresholding, or classifier. | ✅         | —            | ⚠️     | —      |
| **Macro / Action Recorder**           | GUI click recorder that generates executable script code based on user interactive steps.                                                                                                                                                                                 | —          | —            | ✅     | ✅     |
| **Batch Folder Processing**           | Applies saved macro/pipeline across entire directories without user intervention.                                                                                                                                                                                         | ✅         | ✅           | ✅     | ✅     |
| **Multi-Threading Support**           | Parallelizes image or tile processing across CPU cores during analysis runs.                                                                                                                                                                                              | ✅         | ⚠️\*         | ⚠️     | ✅     |
| **Headless / CLI Execution**          | Run pipeline from command line prompt without rendering GUI windows (Docker, HPC cluster support).                                                                                                                                                                        | ✅         | ✅           | ✅     | ✅     |
| **Audit Log & Pipeline Export**       | Saves pipeline parameters as JSON/XML and logs exact algorithm versions and numerical seeds.                                                                                                                                                                              | ✅         | ✅           | ⚠️     | ✅     |

\*CellProfiler parallelizes across images within a single run, but real throughput on large images in practice means manually tiling images and orchestrating multiple CellProfiler instances yourself.

---

### 8. Data Export, Visualization & Ecosystem

| Feature Name                       | Detailed Functionality                                                                                                                                                | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Open Format Data Export**        | Export measurements to standard tabular formats (`.csv`, `.tsv`, `.xlsx`, HDF5, Parquet).                                                                             | ✅         | ✅           | ✅     | ✅     |
| **SQL-Queryable Results Database** | Query results directly via SQL against a bundled analysis database, instead of only flat export files.                                                                | ✅         | ⚠️           | —      | —      |
| **Interactive Plotting & Gating**  | Scatter plots, histograms, and boxplots linked back to image views (click point -> highlight cell). Enables flow-cytometry-style gating directly from the data plots. | ✅         | ✅           | ⚠️     | —      |
| **3D Volume Rendering**            | Hardware-accelerated (OpenGL/Vulkan) 3D volume rendering, ISO-surface rendering, and orthoviewers.                                                                    | —          | —            | ✅     | —      |
| **Active Plugin Ecosystem**        | Centralized plugin repository/updater and active user community support.                                                                                              | —          | ✅           | ✅     | ✅     |

---

### Performance benchmark

A controlled benchmark ran the same reference pipeline (rolling-ball background subtraction → double blur → threshold → connected components → area filter → colocalization) against the same 81 Olympus `.vsi` microscopy images (2048×2048, 3 channels) across five tool configurations. QuPath is not included as a separate measurement — its viewer and processing core are built on ImageJ/Bio-Formats internals, so its performance is expected to track the plain Fiji macro figures below rather than differ meaningfully from them.

**Test system:** Intel Core Ultra 9 185H (16 cores / 22 threads), 62 GB RAM, Ubuntu 24.04.

Full per-image counts and per-step timing live in the project's own benchmark reports; this is a summary.

#### Wall-clock time

| Tool                              | Wall-clock | Avg cores used | Peak RAM | Total CPU-time | CPU-time / image | RAM / image | Speed vs. fastest | Compute cost vs. most efficient |
| --------------------------------- | ---------: | -------------: | -------: | -------------: | ---------------: | ----------: | ----------------: | ------------------------------: |
| evanalyzer core CLI               |     14.2 s |          15.65 |  3.75 GB |   222.2 core-s |     2.744 core-s |     47.4 MB |         **1.00x** |                           1.54x |
| EVAnalyzer Fiji plugin            |     35.2 s |          11.54 | 19.90 GB |   406.4 core-s |     5.017 core-s |    251.6 MB |             2.48x |                           2.81x |
| Plain Fiji macro                  |    126.5 s |           1.14 |  1.15 GB |   144.6 core-s |     1.786 core-s |     14.5 MB |             8.91x |                       **1.00x** |
| CellProfiler, single-process      |    528.2 s |           2.24 |  4.08 GB |  1184.2 core-s |    14.620 core-s |     51.6 MB |            37.20x |                           8.19x |
| CellProfiler, parallel (14 procs) |    192.9 s |          16.86 | 45.70 GB |  3251.3 core-s |    40.140 core-s |    577.6 MB |            13.58x |                          22.47x |

#### Where the underlying gap comes from

Comparing matched pipeline steps under identical single-threaded conditions (plain Fiji macro vs. CellProfiler single-process) isolates implementation from parallelism:

| Matched step                                     | EVAnalyzer / Fiji-based |        CellProfiler | Ratio    |
| ------------------------------------------------ | ----------------------: | ------------------: | -------- |
| Object extraction/measurement                    |             12.3 ms avg | ~1,073–1,445 ms avg | ~90–120x |
| Background/illumination correction (per channel) |                ~22.8 ms |       ~4,500 ms CPU | ~200x    |

Both tools do equivalent work at these steps — EVAnalyzer's Extract Objects step and CellProfiler's `MeasureObjectSizeShape` do the same job, as do both tools' background-correction steps. The gap tracks implementation, not algorithm: native (Rust or compiled Java) code operating on primitive arrays vs. a general-purpose Python module architecture that round-trips every step through a shared measurements object.

#### Accuracy note

Object counts weren't identical across tools, which matters for reading the speed numbers as "same job, different cost" rather than "different jobs." The EVAnalyzer Fiji plugin's counts were used as the reference; CellProfiler needed a calibration pass (swapping an auto-threshold for a fixed one, tuning per-channel background-fit tightness) to get within roughly 3–6% of that reference, since it has no direct equivalent to the rolling-ball algorithm the other tools share. EVAnalyzer's own project settings matched the reference without changes.

#### A note on setup

Getting a valid CellProfiler number took real debugging effort on this system — a sandboxed-CLI deadlock that required a conda reinstall, and a CLI flag that silently doubled the effective image count by recursing into sidecar files — on top of the threshold/background calibration above. The other configurations needed no comparable troubleshooting. That's a legitimate part of "which tool is practical to actually run day to day," alongside the timing numbers, not a separate criticism of CellProfiler's algorithms.

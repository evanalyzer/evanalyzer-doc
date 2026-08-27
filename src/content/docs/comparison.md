---
title: Features & Benchmarks
description: Feature-by-feature comparison and performance benchmarks — EVAnalyzer vs. CellProfiler, ImageJ, and QuPath.
---

## Feature matrix

Support markings are a best-effort summary based on each project's public documentation: ✅ supported · ⚠️ partial/limited · - not supported or not documented.
"ImageJ" covers the Fiji distribution (ImageJ2 plus its commonly bundled plugins, e.g. TrackMate, Coloc2, Trainable Weka Segmentation).
Verify against each tool's current docs before relying on this for a migration decision.

A checkmark alone can overstate real-world usability, for any tool here - see the "Its ceiling" column in the [at-a-glance table](#at-a-glance-which-tool-fits-your-project) below for what each one still falls short on.
Rows where a checkmark hides a gap like this carry a footnote.

### File Import, I/O & Microscopic Data Handling

| Feature Name                      | Detailed Functionality                                                                                                                                                                                             | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ------------ | ------ | ------ |
| **Bio-Formats Integration**       | Native reader for vendor raw formats (`.czi`, `.nd2`, `.lif`, `.oib`, `.ome.tif`, `.svs`) using Bio-Formats or OME libraries. Avoids time-consuming pre-conversion to 8-bit TIFF and proprietary software lock-in. | ✅†        | ✅           | ✅     | ✅     |
| **Metadata Parsing**              | Extracts spatial calibration ($\mu m/\text{pixel}$, Z-spacing), time intervals, channel names, emission wavelength, and objective info. Ensures accurate physical measurements without manual entry.               | ✅         | ✅           | ✅     | ✅     |
| **Automatic Channel Access**      | Individual channels of a multi-channel image are directly addressable right after import, without a separate per-channel mapping step.                                                                             | ✅         | ⚠️\*         | ✅     | ✅     |
| **Multidimensional (ND) Support** | Seamless display and navigation of 5D hyperstacks ($X, Y, Z, \text{Channel}, \text{Time/T}$).                                                                                                                      | ✅         | ⚠️           | ✅     | ✅     |
| **Microplate Grid Layouts**       | Automatic layout parsing for 96/384-well microplates with row/column coordinate mapping and tile stitching. Useful for high-throughput screening (HTS) workflows that group images by well/condition.              | ✅         | ✅           | ⚠️     | -      |
| **Lazy Loading & Virtual Stacks** | Streams image slices into RAM on demand instead of loading multi-gigabyte files entirely into memory.                                                                                                              | ✅         | -            | ⚠️     | ✅     |
| **Pyramidal / BigDataViewer**     | Supports multi-resolution image pyramids for rapid zooming and pan on terabyte-scale datasets.                                                                                                                     | ✅         | -            | -      | ✅     |
| **Whole-Slide Navigator Viewer**  | Dedicated interactive viewer with a pyramid-based navigator minimap for panning and zooming across gigapixel whole-slide scans.                                                                                    | ✅         | -            | -      | ✅     |

\*CellProfiler does not split channels automatically. You configure a **NamesAndTypes** module with filename regex/metadata rules (separate-file channels) or a channel-index mapping (single multi-channel file) to name and access each channel - get the mapping wrong and channels silently mismatch or drop.

†EVAnalyzer's is using a Rust port of the original Java written BioFormats library. This port may be unstable for some not widly used image formats right now.

---

### GUI, Interactive UX & Daily Quality-of-Life

| Feature Name                      | Detailed Functionality                                                                                                                                                                    | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Flexible Contrast & LUTs**      | Per-channel histogram brightness/contrast tuning, non-destructive LUT application (HiLo, Fire, RGB, custom color maps). HiLo-style LUTs flag saturated and zero-value pixels at a glance. | ✅         | ⚠️           | ✅     | ✅     |
| **Keyboard Shortcuts & Commands** | Comprehensive keyboard hotkeys and searchable command palette.                                                                                                                            | ✅         | ⚠️           | ✅     | ⚠️     |
| **Multi-Window Synchronization**  | Synchronized panning, zooming, and slice/time stepping across multiple image windows.                                                                                                     | -          | -            | ✅     | ⚠️     |
| **Undo / Redo Buffer**            | Multi-step history buffer for destructive pixel operations and ROI edits.                                                                                                                 | ✅         | ⚠️           | ⚠️     | ✅     |
| **Scale Bar & Dynamic Overlay**   | Burned-in or dynamic vector scale bars, timestamps, Z-depth indicators, and channel legends.                                                                                              | ✅         | ⚠️           | ✅     | ✅     |
| **Dark Mode / Theme UI**          | High-contrast dark theme option for interface components.                                                                                                                                 | ✅         | -            | ⚠️     | ✅     |
| **Image Viewer**                  | Built-in multi-channel viewer with per-channel visibility, colour, contrast, and Z/T navigation.                                                                                          | ✅         | -            | ✅     | ✅     |
| **Live Preview**                  | Immediate viewport update and live object count while editing a pipeline step, without re-running the full pipeline.                                                                      | ✅         | -\*          | ⚠️     | ✅     |

\*Test Mode lets you step through modules and inspect output windows, but there is no continuous, reactive preview while adjusting a setting - you re-run the step and wait, which is slow on large images.

---

### Image Preprocessing, Filtering & Restoration

| Feature Name                   | Detailed Functionality                                                                                        | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Flat-Field Correction**      | Correction for uneven illumination profiles using flat-field / dark-field images or BaSiC / CIDRE algorithms. | ✅         | ✅           | ✅     | -      |
| **Background Subtraction**     | Rolling ball, top-hat, sliding paraboloid, or local background estimation algorithms.                         | ✅         | ✅           | ✅     | ⚠️     |
| **Noise Reduction Filters**    | Gaussian, Median, Anisotropic Diffusion, Bilateral, and Non-Local Means denoising filters.                    | ✅         | ✅           | ✅     | ⚠️     |
| **Image Registration & Drift** | Translation, rigid, affine, and elastic registration (e.g., Descriptor-based, TurboReg, StackReg).            | -          | ⚠️           | ✅     | ⚠️     |
| **Grid Stitching & Blending**  | Phase correlation stitching of overlapping tiles with non-linear seam blending.                               | -          | -            | ✅     | -      |
| **Deconvolution Tools**        | Theoretical/measured PSF generation and Richardson-Lucy / Tikhonov iterative deconvolution algorithms.        | -          | -            | ✅     | -      |

---

### Segmentation, Object Detection & AI Tools

| Feature Name                           | Detailed Functionality                                                                                                                          | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Global & Local Thresholding**        | Classic automated thresholding (Otsu, Li, Yen, Maximum Entropy, Niblack, Bernsen, Sauvola).                                                     | ✅         | ✅           | ✅     | ✅     |
| **Morphological Operations**           | Erosion, Dilation, Opening, Closing, Hole Filling, Skeletonization, Distance Transform.                                                         | ✅         | ✅           | ✅     | ⚠️     |
| **Watershed Clustered Object Split**   | Marker-controlled watershed segmentation to separate touching or overlapping cells.                                                             | ✅         | ✅           | ✅     | ✅     |
| **Deep Learning AI Models**            | Native or plugin access to pretrained deep learning models (Cellpose, StarDist, Segment Anything / SAM).                                        | ✅†        | ⚠️           | ✅     | ✅\*   |
| **Machine Learning Pixel Classifiers** | Interactive scribble-based pixel classification (e.g., Trainable Weka Segmentation, Ilastik integration).                                       | ✅         | -            | -      | ✅     |
| **ROI Manager & Editing Tools**        | Store, group, rename, filter, dilate, measure, and export collections of vector ROIs.                                                           | ✅         | ⚠️           | ✅     | ✅     |
| **Object Math (Boolean Set Ops)**      | AND / OR / XOR / Subtract operations between object classes to combine, exclude, or reshape detected objects (e.g., a rim around an organelle). | ✅         | ⚠️           | ⚠️     | ⚠️     |

\*QuPath's Cellpose/StarDist support ships as separately installed extensions, not bundled by default.

† EVAnalyzer actually only supports models stored either in ONNX or torchscript. Tensorflow models are not supported.

---

### Quantification, Feature Extraction & Spatial Analysis

| Feature Name                      | Detailed Functionality                                                                                                  | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Morphometric Measurements**     | Area, perimeter, bounding box, major/minor axis, circularity, aspect ratio, roundness, solidity, 3D volume.             | ✅\*       | ✅           | ✅     | ✅     |
| **Densitometry & Intensity**      | Mean, min/max, median, integrated density, standard deviation of pixel values across channels.                          | ✅         | ✅           | ✅     | ✅     |
| **Colocalization Analysis**       | Pearson's correlation coefficient, Manders' overlap coefficients ($M_1/M_2$), Costes' thresholding, 2D cytofluorograms. | ✅†        | ✅           | ✅     | -      |
| **Spatial Distance & Clustering** | Nearest neighbor distance, Delaunay triangulation, Voronoi tessellation, object-to-boundary distance.                   | ⚠️\*\*     | ⚠️           | ⚠️     | ✅     |
| **Texture Analysis (Haralick)**   | Grey-Level Co-occurrence Matrix (GLCM): contrast, correlation, energy, entropy, and local heterogeneity.                | -          | ✅           | ✅     | ✅     |
| **Filament & Skeleton Analysis**  | Branch point detection, filament length, segment classification, network connectivity metrics.                          | -          | ✅           | ✅     | -      |

\*No 3D volume support

† Object based colocalization calculation, actually no Pearson's correlation supported

\*\* Support for voronoi grid

---

### Particle Tracking, Time-Lapse & Lineage Analysis

| Feature Name                      | Detailed Functionality                                                                                     | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Automated Particle Tracking**   | LAP (Linear Assignment Problem), Kalman filtering, or nearest-neighbor frame-to-frame linking algorithms.  | -          | ✅           | ✅     | -      |
| **Kinematic Trajectory Metrics**  | Velocity, instantaneous speed, directionality ratio, mean square displacement (MSD), confinement index.    | -          | ✅           | ✅     | -      |
| **Cell Division & Lineage Trees** | Handling cell division events (mitosis), branch creation, and full lineage tree visualization.             | -          | ✅           | ✅     | -      |
| **Manual Track Editing UX**       | Interactive track visualization with easy manual link breaking, joining, path deletion, and spot tweaking. | -          | -            | ✅     | -      |

---

### Automation, Batch Processing & Reproducibility

| Feature Name                          | Detailed Functionality                                                                                                                                                                                                                                                    | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **No-Code Pipeline Builder**          | Compose a full analysis pipeline by adding and configuring pre-built commands, without writing scripts or macros.                                                                                                                                                         | ✅         | ✅           | -      | ⚠️     |
| **Multi-Channel Branching Pipelines** | Routes different channels or object classes down independent, custom-filtered processing branches within one project, instead of one linear sequence applied to everything. Lets each fluorescence marker get its own background correction, thresholding, or classifier. | ✅         | -            | -      | -      |
| **Macro / Action Recorder**           | GUI click recorder that generates executable script code based on user interactive steps.                                                                                                                                                                                 | -          | -            | ✅     | ✅     |
| **Batch Folder Processing**           | Applies saved macro/pipeline across entire directories without user intervention.                                                                                                                                                                                         | ✅         | ✅           | ✅     | ✅     |
| **Multi-Threading Support**           | Parallelizes image or tile processing across CPU cores during analysis runs.                                                                                                                                                                                              | ✅         | ⚠️\*         | ⚠️     | ✅     |
| **Headless / CLI Execution**          | Run pipeline from command line prompt without rendering GUI windows (Docker, HPC cluster support).                                                                                                                                                                        | ✅         | ✅           | ✅     | ✅     |
| **Audit Log & Pipeline Export**       | Saves pipeline parameters as JSON/XML and logs exact algorithm versions and numerical seeds.                                                                                                                                                                              | ✅         | ✅           | ⚠️     | ✅     |
| **Pipeline Cite Export**              | One-click export (File → Export → Cite Project) of a step-by-step flow diagram for every enabled pipeline, each step tagged with its algorithm's citation, followed by a consolidated, publication-ready bibliography for every cited algorithm used.                     | ✅         | -            | -      | -      |

\*CellProfiler parallelizes across images within a single run, but real throughput on large images in practice means manually tiling images and orchestrating multiple CellProfiler instances yourself.

---

### Data Export, Visualization & Ecosystem

| Feature Name                       | Detailed Functionality                                                                                                                                                | EVAnalyzer | CellProfiler | ImageJ | QuPath |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ | ------ | ------ |
| **Open Format Data Export**        | Export measurements to standard tabular formats (`.csv`, `.tsv`, `.xlsx`, HDF5, Parquet).                                                                             | ✅\*       | ✅           | ✅     | ✅     |
| **SQL-Queryable Results Database** | Query results directly via SQL against a bundled analysis database, instead of only flat export files.                                                                | ✅         | ⚠️           | -      | -      |
| **Interactive Plotting & Gating**  | Scatter plots, histograms, and boxplots linked back to image views (click point -> highlight cell). Enables flow-cytometry-style gating directly from the data plots. | ✅         | ✅           | ⚠️     | -      |
| **3D Volume Rendering**            | Hardware-accelerated (OpenGL/Vulkan) 3D volume rendering, ISO-surface rendering, and orthoviewers.                                                                    | -          | -            | ✅     | -      |
| **Active Plugin Ecosystem**        | Centralized plugin repository/updater and active user community support.                                                                                              | -          | ✅           | ✅     | ✅     |

\*HDF5 and Parquet export aren't supported rihght now by EVAnalyzer.

---

## At a glance: which tool fits your project?

| Tool              | Choose it when...                                                                                                                                 | Core strength                                                                                                                                                               | Its ceiling                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **EVAnalyzer**    | Multiplex/multi-channel fluorescence panels where every marker needs its own processing, especially at whole-slide scale.                         | Very fast and also runs on lower performance computers smooth. Branching per-channel pipelines with built-in whole-slide tiling, live preview, and CLI batch/HPC execution. | No time-lapse tracking, no true 3D volume rendering; a smaller measurement library than CellProfiler/ImageJ for classic single-channel quantification. |
| **CellProfiler**  | Deep, classic single- or few-channel quantification - precise shape, texture, colocalization, or particle-tracking metrics for a methods section. | The broadest, most mature measurement library here (Haralick texture, LAP tracking, Pearson's/Manders' colocalization).                                                     | One linear pipeline per run; per-channel branching and real multi-threaded throughput on large images both need manual workarounds.                    |
| **ImageJ / Fiji** | You need a specific plugin, a quick one-off manual measurement, or maximum flexibility via scripting (macros/Jython/Groovy).                      | The largest plugin ecosystem of any tool here - most niche bio-imaging algorithms exist as an ImageJ plugin.                                                                | No structured no-code pipeline model; a reproducible pipeline means writing or recording macros yourself.                                              |
| **QuPath**        | Whole-slide digital pathology - parent/child object hierarchies (tissue → cell → sub-cell), TMA cores, point-and-click classifier training.       | Best-in-class whole-slide viewer/pyramid handling, plus a native object hierarchy no other tool here has.                                                                   | Not built for time-lapse/live-cell tracking, correlation-based colocalization, or independent per-channel preprocessing.                               |

**EVAnalyzer** relies on a _branching pipeline_ with a focus on speed and usability, **CellProfiler** on a _linear pipeline_ with a focus on comprehensive quantitative measurement, and **QuPath** on an **object-centric, map-based workflow** with a focus on pathology images. **ImageJ**, by contrast, is a feature-rich, plugin-based, all-around image editing tool rather than a fixed pipeline paradigm.

---

## Benchmark

A controlled benchmark ran the same reference pipeline (rolling-ball background subtraction → double blur → threshold → connected components → area filter → colocalization) against the same 81 Olympus `.vsi` microscopy images (2048×2048, 2 channels) across five tool configurations. QuPath is not included as a separate measurement - its viewer and processing core are built on ImageJ/Bio-Formats internals, so its performance is expected to track the plain Fiji macro figures below rather than differ meaningfully from them.

**Test system:** Intel Core Ultra 9 185H (16 cores / 22 threads), 62 GB RAM, Ubuntu 24.04.

Full per-image counts and per-step timing live in the project's own benchmark reports; this is a summary.

### Wall-clock time

| Tool                              | Wall-clock | Avg cores used | Peak RAM (aggregate) | RAM per core (avg) | Speed vs. fastest | RAM per core vs. lowest | Peak RAM vs. lowest |
| --------------------------------- | ---------: | -------------: | -------------------: | -----------------: | ----------------: | ----------------------: | ------------------: |
| EVAnalyzer core CLI               | **14.2 s** |          15.65 |              3.75 GB |        **0.24 GB** |         **1.00x** |               **1.00x** |               3.26x |
| EVAnalyzer Fiji plugin            |     35.2 s |          11.54 |             19.90 GB |            1.72 GB |             2.48x |                   7.17x |              17.30x |
| Plain Fiji macro                  |    126.5 s |            1.0 |              1.15 GB |            1.15 GB |             8.91x |                   4.79x |           **1.00x** |
| CellProfiler, parallel (14 procs) |    192.9 s |          16.86 |             45.70 GB |            2.72 GB |            13.58x |                  11.33x |              39.74x |
| CellProfiler, single-process      |    528.2 s |            1.0 |              4.08 GB |            4.08 GB |            37.20x |                  17.00x |               3.55x |

**EVAnalyzer**'s core CLI more than doubles the execution speed of its predecessor Fiji plugin (2.5x) and uses roughly a fifth of the peak RAM (5.3x less).
Compared to CellProfiler running in its parallel (multi-process) mode, it is 13.6x faster and uses 12.2x less peak RAM.

### Accuracy note

Object counts weren't identical across tools, which matters for reading the speed numbers as "same job, different cost" rather than "different jobs."
The EVAnalyzer Fiji plugin's counts were used as the reference; CellProfiler needed a calibration pass (swapping an auto-threshold for a fixed one, tuning per-channel background-fit tightness) to get within roughly 3–6% of that reference, since it has no direct equivalent to the rolling-ball algorithm the other tools share.
EVAnalyzer's own project settings matched the reference without changes.

### A note on setup

Getting a valid CellProfiler number took real debugging effort on this system - a sandboxed-CLI deadlock that required a conda reinstall, and a CLI flag that silently doubled the effective image count by recursing into sidecar files - on top of the threshold/background calibration above.
The other configurations needed no comparable troubleshooting.
That's a legitimate part of "which tool is practical to actually run day to day," alongside the timing numbers, not a separate criticism of CellProfiler's algorithms.

_Benchmark files_

- [evanalyzer_benchmark.evaproj](/downloads/benchmark/evanalyzer_benchmark.evaproj) - EVAnalyzer project file for the reference pipeline
- [cellprofiler_benchmark.cppipe](/downloads/benchmark/cellprofiler_benchmark.cppipe) - calibrated CellProfiler pipeline
- [imagej_benchmark.ijm](/downloads/benchmark/imagej_benchmark.ijm) - plain ImageJ/Fiji macro, no plugin

Download all three into the same directory (`$ROOT` below) alongside your own `images/` folder of test images before running the commands.

_Preparation_

```sh
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%dT%H%M%S)"
OUT="$ROOT/benchmark_runs/$STAMP"
mkdir -p "$OUT"
```

_EVAnalyzer benchmark_

```sh
/usr/bin/time -v "$ROOT/tools/evanalyzer" cli analyze \
  --project "$ROOT/evanalyzer_benchmark.evaproj" --images "$ROOT/images" --job-name "bench_$STAMP" \
  > "$OUT/evanalyzer_core.log" 2>&1
echo "exit=$? -- see $OUT/evanalyzer_core.log"
grep -E "Elapsed|Maximum resident|Percent of CPU|Done:" "$OUT/evanalyzer_core.log"
echo ""
```

_ImageJ benchmark_

```sh
/usr/bin/time -v "$ROOT/tools/Fiji/fiji-linux-x64" \
  --headless --run "$ROOT/imagej_benchmark.ijm" \
  > "$OUT/plain_fiji_macro.log" 2>&1
echo "exit=$? -- see $OUT/plain_fiji_macro.log"
grep -E "Elapsed|Maximum resident|Percent of CPU|DONE" "$OUT/plain_fiji_macro.log"
echo ""
```

_Cellprofiler benchmark_

```sh
export JAVA_HOME="$HOME/miniforge3/envs/cellprofiler/lib/jvm"
export LD_LIBRARY_PATH="$HOME/miniforge3/envs/cellprofiler/lib:$HOME/miniforge3/envs/cellprofiler/lib/mariadb:${LD_LIBRARY_PATH:-}"
CP_OUT="$OUT/cellprofiler_single"
mkdir -p "$CP_OUT"
/usr/bin/time -v "$ROOT/tools/cellprofiler/bin/cellprofiler" \
  -c -r -p "$ROOT/cellprofiler_benchmark.cppipe" -i "$ROOT/images" -o "$CP_OUT" \
  > "$OUT/cellprofiler_single.log" 2>&1
echo "exit=$? -- see $OUT/cellprofiler_single.log"
grep -E "Elapsed|Maximum resident|Percent of CPU" "$OUT/cellprofiler_single.log"
echo ""
```

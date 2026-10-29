---
title: Frequently Asked Questions
description: Common questions about EVAnalyzer.
---

## General

<details>
<summary>Who develops EVAnalyzer?</summary>

EVAnalyzer is a source-available project, free to use for non-commercial purposes, initiated as a leisure project by Joachim Danmayr and Melanie Schürz, in cooperation with the [Paris Lodron University of Salzburg](https://www.plus.ac.at/) and the [Ludwig Boltzmann Institute for Nanovesicular Precision Medicine](https://nvpm.lbg.ac.at/).

</details>

<details>
<summary>Is EVAnalyzer free to use? Is the source code available?</summary>

EVAnalyzer's source code is public, and its development takes place [on GitHub in the `evanalyzer/evanalyzer` repository](https://github.com/evanalyzer/evanalyzer). It is licensed under the [PolyForm Noncommercial License 1.0.0](https://github.com/evanalyzer/evanalyzer/blob/main/LICENSE): free for personal, academic, research and other non-commercial use. Commercial use - in a company, in a commercial product or service - needs a separate license; [open an issue](https://github.com/evanalyzer/evanalyzer/issues) or contact the maintainer.

Third-party components keep their own licenses. **EVA › About › Licenses** lists every one of them with its license text, and every download carries them in `THIRD-PARTY-NOTICES.txt` next to `LICENSE`.

</details>

<details>
<summary>I would like to request a new feature. How do I proceed?</summary>

Open a [feature request issue](https://github.com/evanalyzer/evanalyzer/issues) on GitHub describing your idea and use case.

</details>

<details>
<summary>I found a bug or have a question. What should I do?</summary>

Check the [GitHub issues page](https://github.com/evanalyzer/evanalyzer/issues) - your question may already be answered there. If not, open a new issue. See [Support](/support/) for details.

</details>

<details>
<summary>Can I use EVAnalyzer in a company or for commercial work?</summary>

Not without a separate license. EVAnalyzer is free for personal, academic, research and other non-commercial use under the [PolyForm Noncommercial License 1.0.0](https://github.com/evanalyzer/evanalyzer/blob/main/LICENSE). Using it in a company, or in a commercial product or service, needs a commercial license - [open an issue](https://github.com/evanalyzer/evanalyzer/issues) or contact the maintainer.

</details>

<details>
<summary>How do I cite EVAnalyzer?</summary>

See [Citation](/citation/) - it has the reference for this application, for the earlier ImageJ/Fiji plugin, and how to cite the algorithms behind the commands you used.

</details>

## Getting Started

<details>
<summary>Which download do I need?</summary>

Pick your operating system, then your processor - **x86-64** (Intel or AMD, most PCs) or **ARM64** (e.g. Snapdragon laptops, ARM servers; macOS is always Apple Silicon) - then **No CUDA** unless you have an NVIDIA GPU and use AI segmentation. The [download picker](/getting-started/installation/#downloading) finds the matching file for you.

</details>

<details>
<summary>Do I need an NVIDIA GPU?</summary>

No. Every feature, including the AI segmentation steps, runs on the CPU. A [CUDA build](/getting-started/system-requirements/#operating-systems) with a supported NVIDIA GPU only makes the AI steps faster.

</details>

<details>
<summary>Do I need to install anything, or admin rights?</summary>

No. Download one archive, extract it anywhere - also into your own user folder - and start EVAnalyzer. Everything it needs is inside: the image reader, the AI runtime and, in the CUDA builds, the CUDA libraries. Only GPU acceleration uses something from your computer: the NVIDIA graphics driver.

</details>

<details>
<summary>Windows or macOS says the app can't be opened. Is it safe?</summary>

Yes. Windows SmartScreen may warn about a new download, and macOS blocks apps that aren't notarized by Apple. The [installation guide](/getting-started/installation/#starting-evanalyzer) shows how to start EVAnalyzer anyway - you only need to do it once.

</details>

<details>
<summary>Linux: EVAnalyzer doesn't start - <code>GLIBC_2.39</code> not found</summary>

If starting EVAnalyzer prints an error like `version 'GLIBC_2.39' not found (required by ./evanalyzer)`, your Linux is older than EVAnalyzer supports. Check your version with `ldd --version` (the first line shows the glibc version; 2.39 or newer is needed). Update to a supported version, e.g. Ubuntu 24.04 LTS - see the [system requirements](/getting-started/system-requirements/#operating-systems). On Windows, WSL with the current Ubuntu works too.

</details>

## Images

<details>
<summary>My image file doesn't open.</summary>

Check that its format is in the [list of supported formats](/fundamentals/image-formats/#supported-formats) - only files with these extensions show in the Images panel, and a few formats that older versions opened can't be read any more. Convert other files to OME-TIFF (e.g. with Fiji). If a supported file still fails, please [open an issue](https://github.com/evanalyzer/evanalyzer/issues) and attach the file if you can.

</details>

<details>
<summary>The pixel size or the µm values are wrong.</summary>

Some files don't store the pixel size, or store it wrongly. Correct it in the image info of the Images panel - see [Pixel size](/guide/images/#pixel-size). It sets the scale bar and every measurement in physical units.

</details>

<details>
<summary>My file has several image series. Which one is analysed?</summary>

The series is chosen once per project and used for every image. EVAnalyzer asks the first time it opens such a file; you can change it later in the image chip of the top bar. See [Series selection](/guide/images/#series-selection).

</details>

<details>
<summary>How are z-stacks and time-lapses handled?</summary>

A z-stack is analysed as a projection (e.g. Max intensity), one plane, or plane by plane - a project setting. A time-lapse is analysed frame by frame, and the [Simple Tracker](/commands/dataset/simple-tracker/) can link objects across frames. See [Z-stack](/guide/images/#z-stack), [Time-lapse](/guide/images/#time-lapse) and [Orthogonal views and 3D view](/guide/images/#orthogonal-views-and-3d-view).

</details>

## Pipelines & Results

<details>
<summary>Why does the preview show fewer objects than the analysis?</summary>

The [live preview](/guide/pipelines/#live-preview) only runs on the part of the image in view, so that it updates at once while you tune. **Preview the whole image** (`Shift+F5`) runs it on the whole image; the analysis always does.

</details>

<details>
<summary>How do I count spots per cell?</summary>

Detect the cells and the spots in their own pipelines, then link each spot to its cell with [Relate Objects](/commands/object/relate-objects/). The results then show per cell the number of its spots and their mean, median, … - see [Parents and children](/guide/results/#parents-and-children) and the tutorial [Spot Count per Cell](/tutorials/spot-count-per-cell/).

</details>

<details>
<summary>What's the difference between Colocalize Objects and Measure Image / Object Colocalization?</summary>

[Colocalize Objects](/commands/object/colocalization/) works with **objects**: which objects of different classes overlap, and optionally new objects for the overlap regions. [Measure Image / Object Colocalization](/commands/measure/measure-colocalization/) works with **intensities**: how two channels' brightness goes together (Pearson, Manders, …), over the whole image or per object.

</details>

<details>
<summary>How do I leave out blurry or bad images?</summary>

Measure them with [Measure Image Quality](/commands/measure/image-quality/) (focus, saturation, noise), then add [Exclude Image](/commands/measure/exclude-image/) with rules such as _Focus score below 0.1_. Such images are still analysed, but left out of the results with the reason - you can take one back in by hand. Images can also be left out by hand in the [results](/guide/results/#leaving-images-out-from-the-list).

</details>

<details>
<summary>Where are my results, and how do I open them in Excel, R or Python?</summary>

Every analysis writes a results database to `<project folder>/results/<date>__<job name>/`. Open it in **Results** mode, then [export](/guide/results/#exporting-results) to XLSX or CSV for Excel, or Parquet for R and Python; the measurements export has one value per row, which reads straight into R or pandas. The [CLI](/cli/cli/#export) exports the same without the GUI.

</details>

<details>
<summary>How do I share a pipeline with a colleague?</summary>

Save the whole project as a [project template](/guide/pipelines/#saving-a-project-as-a-template) (`.evatemplate`) - classes, plate settings and all pipelines - or a part of a pipeline as a [module](/guide/modules/#module-library) (`.evamodule`). Your colleague opens the file with **EVA › Open…**. Ready-made ones are on the [Downloads](/downloads/) page.

</details>

## Data & Settings

<details>
<summary>Where are my settings, templates and modules stored?</summary>

In one folder in your home folder: `~/.evanalyzer/` on Linux, `~/evanalyzer/` on macOS, `C:\Users\<name>\evanalyzer\` on Windows. Copy it to take everything to another computer - see [Where EVAnalyzer stores its data](/guide/settings/#where-evanalyzer-stores-its-data). Project settings are saved in the project file itself.

</details>

<details>
<summary>Can I run analyses without the GUI, or on a server?</summary>

Yes. The [command line](/cli/cli/) (`evanalyzer cli analyze …`) runs a project's analysis and exports results, e.g. in scripts. With [remote control](/remote/remote-control/), the GUI or CLI on your laptop works with images and runs analyses on a workstation or server - analyses keep running when you disconnect.

</details>

## Performance

<details>
<summary>Do I need a powerful computer to run EVAnalyzer?</summary>

No! EVAnalyzer is designed to have a low performance footprint and can be run on a normal home PC or laptop. For minimum hardware requirements, see [System Requirements](/getting-started/system-requirements/).

</details>

<details>
<summary>My pipelines run very slowly. What should I do?</summary>

Several factors influence the processing speed of a pipeline:

- Bigger images take longer to analyze.
- The longer the pipeline, the longer the analysis time.
- The more objects detected in an image, the longer the analysis time.
- [Rolling Ball](/commands/image-processing/rolling-ball/), [Watershed](/commands/segmentation/watershed/), and [Rank Filter](/commands/image-processing/rank-filter/) are commands that cost a lot of time.
- Classical object segmentation is faster than AI-based object detection - and AI segmentation steps run substantially faster on a [CUDA build](/getting-started/installation/#downloading) with a compatible NVIDIA GPU.

EVAnalyzer tries to use all available CPU cores to run an analysis (see the [`--threads` CLI option](/cli/cli/#analyze)). Using a machine with more cores can significantly reduce processing time.

</details>

## Use Cases

<details>
<summary>What are typical use cases for EVAnalyzer?</summary>

EVAnalyzer was developed by a group of biologists specializing in extracellular vesicles (nano-sized vesicles). One of its main use cases is identifying spots in fluorescence microscopy images, counting them, and calculating colocalization between channels.

That said, EVAnalyzer is highly flexible and can be used in fields other than biology - for instance, in astronomy to count stars in the sky. In a nutshell: any application that needs to automatically quantify images and automate that process is a good fit.

</details>

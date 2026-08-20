---
title: Frequently Asked Questions
description: Common questions about EVAnalyzer.
---

## General

<details>
<summary>Who develops EVAnalyzer?</summary>

EVAnalyzer is an open source project initiated as a leisure project by Joachim Danmayr and Melanie Schürz, in cooperation with the [Paris Lodron University of Salzburg](https://www.plus.ac.at/) and the [Ludwig Boltzmann Institute for Nanovesicular Precision Medicine](https://nvpm.lbg.ac.at/).

</details>

<details>
<summary>Why was the project previously called ImageC?</summary>

Inspired by [ImageJ](https://imagej.net/ij/) - a **J**ava-written image processing tool for single-image processing - the project was originally named **ImageC**, signaling a high-throughput tool written in **C**++.

It has since been rewritten in Rust and rebranded **EVAnalyzer**, but the focus on high-throughput, easy-to-use image processing remains the same. See [About EVAnalyzer](/about/) for the full history.

</details>

<details>
<summary>Is EVAnalyzer open-source?</summary>

EVAnalyzer is fully open-source under the [AGPL-3.0](https://github.com/evanalyzer/evanalyzer/blob/main/LICENSE) license, and its development takes place [on GitHub in the `evanalyzer/evanalyzer` repository](https://github.com/evanalyzer/evanalyzer). EVAnalyzer is available as a free version under this license for non-commercial use.

</details>

<details>
<summary>I would like to request a new feature. How do I proceed?</summary>

Open a [feature request issue](https://github.com/evanalyzer/evanalyzer/issues) on GitHub describing your idea and use case.

</details>

<details>
<summary>I found a bug or have a question. What should I do?</summary>

Check the [GitHub issues page](https://github.com/evanalyzer/evanalyzer/issues) - your question may already be answered there. If not, open a new issue. See [Support](/support/) for details.

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

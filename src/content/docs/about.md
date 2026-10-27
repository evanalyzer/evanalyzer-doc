---
title: About EVAnalyzer
description: The story behind EVAnalyzer, what it stands for, and who builds it.
---

When we started our research, we were faced with the challenge of quantifying a large number of images taken using our microscopes. The number of images kept growing thanks to new microscopy technologies that allow automated image generation.

Starting with the search for a low-cost / free tool to help tame the amount of data, we looked at a number of tools including [ImageJ](https://imagej.net/ij/), [CellProfiler](https://cellprofiler.org/), and a couple of other smaller applications. All of them are feature-rich, but none fulfilled our requirements for an easy-to-use tool that can do reproducible data quantification.

This was the starting point of the [EVAnalyzer Fiji/ImageJ plugin](https://github.com/joda01/evanalyzer), which automates a lot of the processes involved in quantifying images in the research field of extracellular vesicles. It allows batch processing of hundreds of images using a set of predefined, often-used functions like counting and colocalization measurement of spots.

Over time the applications got more and more complex, beginning with the switch from _in vitro_ to _in vivo_. Histological images are large and require more effort to analyze. Further applications, such as serum assays, made the processing algorithms even more complex.

Even for these more complex applications we wanted to provide an easy-to-use tool, but it had to be more flexible than the EVAnalyzer Fiji/ImageJ plugin. So EVAnalyzer grew from a plugin into a standalone application written in Rust - the one described in these docs. It bridges the gap between tools like ImageJ, which excel at processing single images and provide a wide range of toolboxes, and tools like CellProfiler, which also provide a large number of plugins but can be more complex to use and require a deeper understanding of image processing - carrying the plugin's philosophy forward with better performance and memory safety.

## What makes EVAnalyzer

### Easy

EVAnalyzer's focus is on as-simple-as-possible usage with a modern graphical user interface. We decided against a plugin mechanism to keep the application simple and harmonized, providing a well-selected and documented set of processing algorithms instead. Where those aren't enough, [modules](/guide/modules/) bundle several steps into one reusable step with its own parameters, and the [Script](/commands/image-processing/script/) command adds loops and conditions around the built-in commands.

### Portable

EVAnalyzer users don't need to install any third-party software or plugins: one zip download contains everything - the application, its own image reader [scopeio](https://github.com/evanalyzer/scopeio) for the microscopy formats, and the AI runtime. Just download, extract, and start EVAnalyzer. The only exception is GPU acceleration: the CUDA builds bundle the CUDA libraries too, but use the NVIDIA graphics driver already installed on the computer. Even users with no programming experience should be able to apply complex image-processing algorithms using EVAnalyzer.

EVAnalyzer is provided for Windows and Linux (x86-64 and ARM64) and for macOS (Apple Silicon). It behaves the same regardless of which host system you start it on, and pipelines can be shared across operating systems without losing any functionality.

### Fast

EVAnalyzer has a focus on really high-throughput image processing. It's written in Rust, balancing C/C++-level performance with memory safety, and a [CUDA-accelerated build](/getting-started/installation/#downloading) is available for GPU-bound AI segmentation steps. In our [benchmark](/comparison/#benchmark), 81 two-channel 2048 × 2048 images took 14 s - 9× faster than a Fiji macro and 13.6× faster than CellProfiler in parallel mode, with 12× less RAM.

A side effect of this approach is that EVAnalyzer can be used on standard laptops, eliminating the need for expensive hardware even for complex pipelines.

### Free

The philosophy behind EVAnalyzer is to give everyone the opportunity to perform complex image processing and analysis. Even small laboratories without the funds to purchase expensive proprietary software should be able to conduct their research with EVAnalyzer.

Consequently, EVAnalyzer is free to use for non-commercial purposes, under the [PolyForm Noncommercial License 1.0.0](https://github.com/evanalyzer/evanalyzer/blob/relates/LICENSE).

## Who develops EVAnalyzer

EVAnalyzer is a source-available project, free to use for non-commercial purposes, initiated as a leisure project by Joachim Danmayr and Melanie Schürz.

## Acknowledgements

EVAnalyzer draws inspiration from scientific publications and uses components from various open-source projects. Thanks to all of them, but especially to:

- [ImageJ](https://imagej.net/ij/), which provides a large set of image-processing algorithms, some of which were ported for EVAnalyzer.
- [CellProfiler](https://cellprofiler.org/) for the idea of building processing pipelines.
- The [kornia-rs](https://github.com/kornia/kornia-rs) open-source project, a Rust computer-vision library that forms the basis of most of the implemented image-processing algorithms.
- The developers of [Slint](https://slint.dev/), whose libraries are used to build EVAnalyzer's graphical user interface.
- The developers of [DuckDB](https://duckdb.org/), the fast, feature-rich database used in the background for data storage, whose excellent documentation was also an inspiration.
- The [PyTorch](https://pytorch.org/) project, whose libtorch runtime (used through the [tch](https://github.com/LaurentMazare/tch-rs) bindings) runs every AI model in EVAnalyzer.
- The authors of [Cellpose](https://github.com/MouseLand/cellpose), [StarDist](https://github.com/stardist/stardist) and [YOLOv5](https://github.com/ultralytics/yolov5), whose models and methods the AI segmentation steps build on.

Last but not least, the biggest thanks go to the team of [AG Meisner-Kober](https://www.plus.ac.at/biosciences/the-department/research-groups/meisner-kober/?lang=en) at the [Paris Lodron University of Salzburg](https://www.plus.ac.at/) and the [Ludwig Boltzmann Institute for Nanovesicular Precision Medicine](https://nvpm.lbg.ac.at/), who made this project possible, driven by their own research needs, and actively supported its realization and testing.

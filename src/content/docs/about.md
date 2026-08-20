---
title: About EVAnalyzer
description: The story behind EVAnalyzer, what it stands for, and who builds it.
---

When we started our research, we were faced with the challenge of quantifying a large number of images taken using our microscopes. The number of images kept growing thanks to new microscopy technologies that allow automated image generation.

Starting with the search for a low-cost / free tool to help tame the amount of data, we looked at a number of tools including [ImageJ](https://imagej.net/ij/), [CellProfiler](https://cellprofiler.org/), and a couple of other smaller applications. All of them are feature-rich, but none fulfilled our requirements for an easy-to-use tool that can do reproducible data quantification.

This was the starting point of the [EVAnalyzer Fiji/ImageJ plugin](https://github.com/joda01/evanalyzer), which automates a lot of the processes involved in quantifying images in the research field of extracellular vesicles. It allows batch processing of hundreds of images using a set of predefined, often-used functions like counting and colocalization measurement of spots.

Over time the applications got more and more complex, beginning with the switch from _in vitro_ to _in vivo_. Histological images are large and require more effort to analyze. Further applications, such as serum assays, made the processing algorithms even more complex.

Even for these more complex applications we wanted to provide an easy-to-use tool, but it had to be more flexible than the EVAnalyzer Fiji/ImageJ plugin. So the development of a standalone C++ application, codenamed **ImageC**, began - bridging the gap between tools like ImageJ, which excel at processing single images and provide a wide range of toolboxes, and tools like CellProfiler, which also provide a large number of plugins but can be more complex to use and require a deeper understanding of image processing.

For stability reasons, ImageC was eventually rewritten in Rust, which led to the professional, final standalone application described in these docs, simply named **EVAnalyzer** - carrying the same philosophy forward with better performance and memory safety.

## What makes EVAnalyzer

### Easy

EVAnalyzer's focus is on as-simple-as-possible usage with a modern graphical user interface. We decided against a plugin mechanism to keep the application simple and harmonized, providing a well-selected and documented set of processing algorithms instead.

### Portable

EVAnalyzer users don't need to install any third-party software or plugins, and the application doesn't depend on any other software. Just download, extract, and start EVAnalyzer. Even users with no programming experience should be able to apply complex image-processing algorithms using EVAnalyzer.

EVAnalyzer is provided for Linux, Windows, and macOS. It behaves the same regardless of which host system you start it on, and pipelines can be shared across operating systems without losing any functionality.

### Fast

EVAnalyzer has a focus on really high-throughput image processing. It's written in Rust, balancing C/C++-level performance with memory safety, and a [CUDA-accelerated build](/getting-started/installation/#downloading) is available for GPU-bound AI segmentation steps.

A side effect of this approach is that EVAnalyzer can be used on standard laptops, eliminating the need for expensive hardware even for complex pipelines.

### Free

The philosophy behind EVAnalyzer is to give everyone the opportunity to perform complex image processing and analysis. Even small laboratories without the funds to purchase expensive proprietary software should be able to conduct their research with EVAnalyzer.

Consequently, EVAnalyzer will continue to be made available at no cost to non-commercial organizations.

EVAnalyzer is built as an unpaid leisure project. The developers don't earn any money with it, so we appeal to the idea of fair use and ask companies or for-profit organizations to get in touch if they intend to use it.

## Who develops EVAnalyzer

EVAnalyzer is an open source project initiated as a leisure project by Joachim Danmayr and Melanie Schürz.

## Acknowledgements

EVAnalyzer draws inspiration from scientific publications and uses components from various open-source projects. Thanks to all of them, but especially to:

- [ImageJ](https://imagej.net/ij/), which provides a large set of image-processing algorithms, some of which were ported for EVAnalyzer.
- [CellProfiler](https://cellprofiler.org/) for the idea of building processing pipelines.
- The [kornia-rs](https://github.com/kornia/kornia-rs) open-source project, a Rust computer-vision library that forms the basis of most of the implemented image-processing algorithms.
- The developers of [Slint](https://slint.dev/), whose libraries are used to build EVAnalyzer's graphical user interface.
- The [Bio-Formats](https://www.openmicroscopy.org/bio-formats/) project, used to decode and open the many supported image formats.
- The developers of [DuckDB](https://duckdb.org/), the fast, feature-rich database used in the background for data storage, whose excellent documentation was also an inspiration.

Last but not least, the biggest thanks go to the team of [AG Meisner-Kober](https://www.plus.ac.at/biosciences/the-department/research-groups/meisner-kober/?lang=en) at the [Paris Lodron University of Salzburg](https://www.plus.ac.at/) and the [Ludwig Boltzmann Institute for Nanovesicular Precision Medicine](https://nvpm.lbg.ac.at/), who made this project possible, driven by their own research needs, and actively supported its realization and testing.

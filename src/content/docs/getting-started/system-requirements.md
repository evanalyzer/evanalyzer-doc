---
title: System Requirements
description: Minimum and recommended hardware and software requirements for running EVAnalyzer.
---

For everyday images (e.g. 2048 x 2048 px microscope images) an ordinary laptop is enough. More power is only needed for whole slides, very large batches or AI models.

## Hardware by Use Case

- **Everyday images** - single images up to ~4096 x 4096 px, batches of hundreds to thousands, classic analyses (threshold, objects, measurements, colocalization).
- **Large batches** - 10,000+ images or millions of objects.
- **Whole slides** - slide scans of several gigapixels.
- **AI models** - [Cellpose](/commands/ai-segmentation/cellpose/), [StarDist](/commands/ai-segmentation/stardist/), [U-Net](/commands/ai-segmentation/unet/), YOLO.

|                   | Everyday images   | Large batches           | Whole slides                           | AI models                                                              |
| ----------------- | ----------------- | ----------------------- | -------------------------------------- | ---------------------------------------------------------------------- |
| **Minimum**       | 2 cores, 4 GB RAM | 4 cores, 8 GB RAM       | 4 cores, 8 GB RAM                      | 4 cores, 8 GB RAM (runs on the CPU, slowly)                            |
| **Recommended**   | 4 cores, 8 GB RAM | 8 cores, 16 GB RAM, SSD | 8+ cores, 16-32 GB RAM, SSD            | 8+ cores, 16-32 GB RAM, NVIDIA GPU                                     |
| **Disk**          | 2 GB + results    | 20 GB+ free, SSD        | 50-100 GB+ free, SSD (temporary files) | 5 GB+ (models, GPU package)                                            |
| **Graphics card** | Not needed        | Not needed              | Not needed                             | Not required; NVIDIA GPU recommended - see [below](#operating-systems) |

The analysis of everyday images needs only 0.2-0.5 GB of RAM (about 230 MB with one core, about 500 MB with four); the program with its image viewer adds about 0.5 GB. So EVAnalyzer runs on a 4 GB laptop next to the operating system and a browser. On a current CPU it analyses several to around ten 2048 x 2048 images per second.

EVAnalyzer adapts to weaker computers by itself: it picks threads and cache sizes from the free RAM, so large datasets still run, just more slowly. It can also draw without a graphics card (`Settings > Viewport > Draw in software`).

To keep the computer usable during a long analysis, limit the cores and RAM EVAnalyzer may use under `Settings > Performance`, or on the command line with `--max-threads N` / `--max-ram MB`.

## Operating Systems

| Operating system | Supported                                                                                                                           | AI models                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Windows**      | Windows 10 and 11, 64-bit (x86-64 and ARM64)                                                                                        | CPU; GPU with the CUDA package (x86-64 only)           |
| **Linux**        | x86-64 and ARM64 with glibc 2.39 or newer, e.g. Ubuntu 24.04+, Debian 13+, Fedora 40+; on X11 also the package `libxkbcommon-x11-0` | x86-64: CPU or GPU (CUDA package); ARM64: no AI models |
| **macOS**        | Apple Silicon (M1 or newer)                                                                                                         | CPU                                                    |

**GPU for AI models (CUDA package):** NVIDIA GeForce GTX 16xx / RTX 20xx or newer (compute capability 7.5+), driver 580 or newer. Older GPUs are detected and the models run on the CPU. See [Installation](/getting-started/installation/#downloading) for the CUDA downloads.

:::note[Good to know]

- **Temporary disk space for whole slides** - only used when RAM is short: up to width x height x channels x 4 bytes per image plane, e.g. about 29 GB for a 60,000 x 40,000 px RGB slide. The files are deleted automatically.
- **Results files** - about 0.5 GB per million objects.
  :::

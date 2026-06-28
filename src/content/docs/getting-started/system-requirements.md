---
title: System Requirements
description: Minimum and recommended hardware and software requirements for running EVAnalyzer.
---

## Minimum Requirements

| Component           | Minimum                                                      | Recommended                                               |
| ------------------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| **RAM**             | 8 GB                                                         | 16 GB or more for large whole-slide images                |
| **Free disk space** | ~5 GB                                                        | More if you plan to store multiple AI model files locally |
| **CPU**             | 64-bit x86-64 (Windows/Linux) or Apple Silicon arm64 (macOS) | Multi-core CPU for faster pipeline execution              |
| **Display**         | 1280×800                                                     | 1920×1080 or larger                                       |

## Supported Operating Systems

| Operating system | Notes                                                                                                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Windows**      | Windows 10 or later, x86-64                                                                                                                                                             |
| **Linux**        | A modern 64-bit distribution (glibc 2.31 or newer - e.g. Ubuntu 20.04+, Debian 11+, Fedora 34+); see the [Installation](/getting-started/installation/) page for required GUI libraries |
| **macOS**        | macOS 13 (Ventura) or later, Apple Silicon (arm64)                                                                                                                                      |

## GPU / CUDA Requirements

AI segmentation steps ([Stardist](/commands/ai-segmentation/stardist/), [UNet](/commands/ai-segmentation/unet/), [Cellpose](/commands/ai-segmentation/cellpose/)) run on CPU by default and work on every supported platform. For significantly faster inference, download a **CUDA build** (Windows or Linux only - see [Downloads](/getting-started/downloads/)) if your machine has:

| Component  | Requirement                                                             |
| ---------- | ----------------------------------------------------------------------- |
| **GPU**    | An NVIDIA GPU with compute capability 6.0 or higher                     |
| **Driver** | An NVIDIA driver new enough to support CUDA 12.x                        |
| **VRAM**   | 4 GB minimum; more for large images or batches of high-resolution tiles |

If you don't have a CUDA-capable GPU, install the regular CPU build - AI segmentation still works, just slower.

:::note
macOS builds are CPU-only. CUDA is an NVIDIA-only technology and is not available on Apple hardware.
:::

## Scaling with Image Size

EVAnalyzer streams large images in tiles rather than loading them fully into memory, but very large whole-slide or multi-well-plate datasets still benefit from more RAM and a faster disk (SSD recommended) - see [Image Formats](/fundamentals/image-formats/) for how tiled/pyramidal formats are handled.

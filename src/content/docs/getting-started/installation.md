---
title: Installation
description: How to download and install EVAnalyzer on Linux, Windows, or macOS.
---

EVAnalyzer is distributed as a pre-built binary for Linux, Windows, and macOS. No package manager or build toolchain is required to run the application.

Before downloading, check the [System Requirements](/getting-started/system-requirements/) page — in particular if you plan to use a CUDA build for GPU-accelerated AI segmentation.

## Downloading

Use the [Downloads](/getting-started/downloads/) page to pick the correct package for your operating system (and, for Windows/Linux, whether you want CUDA acceleration). It always links to the latest release.

Packages follow this naming scheme on the [GitHub Releases page](https://github.com/evanalyzer/evanalyzer/releases/latest):

| Platform | CPU-only | CUDA-accelerated |
|---|---|---|
| Windows x86-64 | `evanalyzer-windows-x86_64.zip` | `evanalyzer-windows-cuda-x86_64.zip` |
| Linux x86-64 | `evanalyzer-linux-x86_64.tar.gz` | `evanalyzer-linux-cuda-x86_64.7z.001` + `.7z.002` |
| macOS (Apple Silicon) | `evanalyzer-macos-arm64.tar.gz` | — (CUDA is not available on macOS) |

:::note[Linux CUDA package is split in two]
The CUDA-enabled Linux build bundles the CUDA runtime libraries and exceeds GitHub's 2 GB single-file limit, so it's published as a two-part 7-Zip archive. Download **both** `.7z.001` and `.7z.002` into the same folder, then extract with:

```sh
7z x evanalyzer-linux-cuda-x86_64.7z.001
```

7-Zip automatically pulls in the second part — you don't need to combine the files yourself first.
:::

Extract the downloaded archive to a directory of your choice.

### Linux additional libraries (GUI)

The GUI requires a few system libraries on Linux. Install them once with:

```sh
apt-get install libinput10 libxkbcommon0 libfontconfig1 libgbm1
```

## Starting EVAnalyzer

### Linux

```sh
./evanalyzer
```

### Windows

Double-click `evanalyzer.exe`, or from PowerShell:

```powershell
.\evanalyzer.exe
```

### macOS

Open `EVAnalyzer.app` from the extracted folder. On first launch, macOS Gatekeeper may require you to right-click the app and choose **Open** since the build is not notarized yet.

The application opens to the start screen showing the project configuration panel.

## Building from Source

See the [Building](/development/building/) guide if you want to compile EVAnalyzer yourself.

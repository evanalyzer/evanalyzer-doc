---
title: Installation
description: How to download and install EVAnalyzer on Linux or Windows.
---

EVAnalyzer is distributed as a pre-built binary. No package manager or build toolchain is required to run the application.

## System Requirements

| Component | Requirement |
|---|---|
| **Operating system** | Linux x86-64, Linux ARM64, or Windows x86-64 |
| **Java JDK** | Version 11 or later — required for Bio-Formats image reading |
| **RAM** | 8 GB recommended (more for large whole-slide images) |

:::caution[macOS not supported]
The current release targets Linux and Windows only. macOS support is not planned for the near future.
:::

### Linux additional libraries (GUI)

The GUI requires a few system libraries on Linux. Install them once with:

```sh
apt-get install libinput10 libxkbcommon0 libfontconfig1 libgbm1
```

### Java

EVAnalyzer bundles a Java Runtime Environment (JRE) that is unpacked on first launch. You do **not** need a separate JDK installation for running the application — only for building from source.

## Downloading a Release

1. Go to the [GitHub Releases page](https://github.com/evanalyzer/evanalyzer/releases/latest).
2. Download the archive for your platform:
   - `evanalyzer-linux-x86_64.tar.gz` — Linux 64-bit
   - `evanalyzer-linux-aarch64.tar.gz` — Linux ARM64
   - `evanalyzer-windows-x86_64.zip` — Windows 64-bit
3. Extract the archive to a directory of your choice.

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

The application opens to the start screen showing the project configuration panel.

## Building from Source

See the [Building](/development/building/) guide if you want to compile EVAnalyzer yourself.

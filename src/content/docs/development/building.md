---
title: Building
description: How to build EVAnalyzer from source on Linux or Windows.
---

EVAnalyzer is written in Rust (2024 edition) and uses Cargo as its build system.

## Requirements

| Tool | Version |
|---|---|
| [Rust toolchain](https://rustup.rs/) | 1.80 or later |
| Java JDK | 11 or later (required for Bio-Formats) |
| Linux system libraries (GUI) | `libinput10 libxkbcommon0 libfontconfig1 libgbm1` |

## Clone the repository

```sh
git clone https://github.com/evanalyzer/evanalyzer.git
cd evanalyzer
```

## Development toolchain

```sh
rustup component add rustfmt
cargo install slint-lsp      # language server for .slint UI files
cargo install slint-viewer   # live preview of .slint files
```

## Build targets

### Linux x86-64

```sh
cargo build-linux
```

### Windows x86-64 (cross-compile from Linux)

```sh
cargo install cargo-xwin
cargo build-win
```

### Linux ARM64

```sh
apt install gcc-aarch64-linux-gnu
rustup target add aarch64-unknown-linux-gnu
cargo build-linux-arm
```

Build artifacts are placed in `target/<target>/release/`.

## Workspace crates

The workspace is split into focused crates:

| Crate | Description |
|---|---|
| `evanalyzer_core` | Image I/O (Bio-Formats via JVM), processing algorithms, ROI model, pipeline execution |
| `evanalyzer_cfg` | Project settings, JSON serialisation, pipeline command configuration |
| `evanalyzer_app` | Application handle, shared project state |
| `evanalyzer_gui` | Slint-based desktop GUI — viewport, histogram, ROI tools, classification panel |
| `evanalyzer_cli` | Command-line interface for headless batch analysis |
| `evanalyzer_bin` | Binary entry point — launches GUI or CLI depending on arguments |

## Previewing the GUI inside a container

If developing inside a Docker devcontainer on Linux, allow X11 forwarding before starting the container:

```sh
xhost +local:docker
```

## Code coverage

```sh
cargo install cargo-llvm-cov
rustup component add llvm-tools-preview

cargo llvm-cov                                    # terminal report
cargo llvm-cov --html                             # HTML report → target/llvm-cov/
cargo llvm-cov --lcov --output-path lcov.info    # lcov format (e.g. VS Code Coverage Gutters)
```

## UI Performance Targets

| Action | Target | Rationale |
|---|---|---|
| Pan / drag | < 10 ms | Must feel attached to the cursor |
| Zoom | < 16 ms | Prevents motion sickness |
| Channel toggle | < 100 ms | Perceived as instant |
| Auto-adjust | < 200 ms | Acceptable for a complex calculation |

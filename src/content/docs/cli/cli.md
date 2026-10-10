---
title: Command Line Interface
description: Run EVAnalyzer headlessly for batch analysis, scripting, and exporting results.
---

EVAnalyzer can be driven entirely from the command line via the `evanalyzer cli` subcommand, enabling headless batch processing, integration into automated workflows, and remote execution on servers - no GUI/display required.

## Overview

The same `evanalyzer` binary handles both modes:

```sh
# Linux
./evanalyzer                              # launch the GUI
./evanalyzer cli <command> [options...]   # run a one-shot CLI command and exit

# Windows
evanalyzer.exe cli <command> [options...]
```

| Command                         | Purpose                                                                            |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| [`analyze`](#analyze)           | Run a project's enabled pipelines over its images and write a new results database |
| [`project-info`](#project-info) | Print a project's images, classes, and pipelines without running anything          |
| [`validate`](#validate)         | Check that every image referenced by a project can be found on disk                |
| [`view`](#view)                 | Print a quick summary and a page of rows from a results database                   |
| [`columns`](#columns)           | List the column ids available for grouping/chart axes in a results database        |
| [`export`](#export)             | Export a results database to CSV, XLSX, or Parquet                                 |
| [`train-classifier`](#train-classifier) | Train a pixel or object classifier from a project's labeled objects        |
| [`jobs`](#jobs-and-attach)      | List the analyses on the `--remote` server: the running one and recently finished ones |
| [`attach`](#jobs-and-attach)    | Follow an analysis on the `--remote` server again, e.g. after the connection dropped |

Every command supports `--help`:

```sh
./evanalyzer cli analyze --help
```

## Running on a Server

Every command can also run on another machine - for example a GPU workstation that holds the images. Add the [remote options](/remote/remote-control/#client-options):

```sh
./evanalyzer cli --remote wss://server-name:7400 --user alice --remote-fingerprint <SHA256> \
  analyze --project /data/experiment-12/experiment.evaproj
```

All paths (`--project`, `--images`, `--db`, `--out`, `--settings`) then refer to the server, and output files are written there. See [Remote Control](/remote/remote-control/) for setting up the server.

### jobs and attach

An analysis started on a server keeps running there if the connection drops - `analyze` then exits with a message naming the analysis id. Use the same `--remote` and `--user` options to find and follow it again:

```sh
# List the running analysis and recently finished ones
./evanalyzer cli --remote wss://server-name:7400 --user alice jobs

# Follow the running analysis (or a specific one with --job <id>)
./evanalyzer cli --remote wss://server-name:7400 --user alice attach
```

`attach` prints the progress like `analyze` does; `Ctrl+C` cancels the analysis. Both commands only work with `--remote`.

## analyze

Runs a project's enabled [pipelines](/guide/pipelines/) over its images and writes a new [results database](#results-database).

```sh
./evanalyzer cli analyze --project experiment.evaproj
```

| Argument           | Description                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `--project <path>` | Project file to analyze (required)                                                                                                          |
| `--images <dir>`   | Scan this directory and use it as the project's image root before running. If omitted, the project's already-saved image list is used as-is |
| `--threads <n>`    | Number of images to process in parallel. If omitted, EVAnalyzer picks the highest thread count that fits within available RAM and CPU cores |

The parallelism is automatically capped to whichever is lower — the number of CPU cores or the number of images that fit in available RAM — so a low-memory machine never launches more parallel workers than it can sustain.

The command prints a progress line per image as it completes, then a summary:

```
Project:   experiment.evaproj
Images:    48
Pipelines: 1 enabled
Output:    ./evanalyzer/EV Detection
Running with 7 parallel thread(s)...

[48/48] /data/plate1/A1_01.tif
Done: 48 image(s) analyzed in 32.4s (0 failed)
Results database written under: ./evanalyzer/EV Detection
```

A project with no images (and no `--images` override) fails fast with an error instead of running.

Press **Ctrl+C** to request a graceful stop; in-flight images will finish before the process exits.

## project-info

Prints a project's image count, classes, and pipelines without running anything - useful for sanity-checking a project file before kicking off a long batch run.

```sh
./evanalyzer cli project-info --project experiment.evaproj
```

| Argument           | Description                              |
| ------------------ | ---------------------------------------- |
| `--project <path>` | Project file to inspect (required)       |
| `--json`           | Emit machine-readable JSON instead of human-readable text |

```
Project:    experiment.evaproj
Name:       EV detection screen
Image root: /data/plate1
Images:     48
Reachable:  yes

Classes (3):
  - dapi@nucleus
  - cy5@spot
  - cy7@spot

Pipelines (1):
  - EV Detection [enabled] - 8 step(s)
```

If the configured image root can't be found on disk, **Reachable** reports why instead of just "no".

## validate

Checks that every image referenced by a project can be found on disk. Useful as a pre-flight step before starting a long headless run.

```sh
./evanalyzer cli validate --project experiment.evaproj
```

| Argument           | Description                        |
| ------------------ | ---------------------------------- |
| `--project <path>` | Project file to check (required)   |

The command exits with a non-zero status code if any images are missing, making it suitable for use in CI scripts:

```sh
./evanalyzer cli validate --project experiment.evaproj && \
  ./evanalyzer cli analyze --project experiment.evaproj
```

## Results Database

`analyze` writes results to a `results.evadb` file (DuckDB format) under the project's job folder - the same file the GUI's [Results](/guide/results/) view opens. `view`, `columns`, and `export` all read from this file via `--db`.

```sh
duckdb results.evadb "SELECT object_class_name, COUNT(*) FROM objects GROUP BY object_class_name"
```

## view

Prints a database summary (image/class counts, T/Z-stack ranges) followed by a paginated, human-readable table of per-object rows - a quick terminal preview without exporting anything.

```sh
./evanalyzer cli view --db results.evadb --limit 10
```

| Argument                      | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `--db <path>`                 | Results database produced by `analyze` (required)         |
| `--page <n>`                  | Zero-based page index (default `0`)                       |
| `--limit <n>`                 | Rows per page (default `25`)                              |
| `--channels`                  | Also show per-channel intensity columns                   |
| `--json`                      | Emit machine-readable JSON instead of human-readable text |
| `--image <name>`              | Restrict to this image name (repeatable)                  |
| `--class <name>`              | Restrict to this object class (repeatable)                |
| `--transpond <true\|false>`   | Show the classes side by side, see [Filter Arguments](#filter-arguments) |

:::note
`--colocalized <true|false>` is accepted by `view` and `export` but always errors today - row-level colocalization filtering has no equivalent in the current results backend yet.
:::

## columns

Lists every column id available in a results database - including per-channel intensity columns and per-partner-class colocalization counts - grouped the same way as the GUI's Columns picker (General, Geometry, Shape, Coloc, Intensity).

```sh
./evanalyzer cli columns --db results.evadb
```

| Argument      | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| `--db <path>` | Results database to inspect (required)                      |
| `--json`      | Emit machine-readable JSON instead of the formatted table   |

```
ID                             LABEL                          GROUP
object_id                      Object ID                      General
image_name                     Image                          General
object_class_name              Class                          General
count                          Count                           General
area_px                        Area [px]                      Geometry
area_nm2                       Area [nm²]                     Geometry
circularity                    Circularity                    Shape
solidity                       Solidity                       Shape
eccentricity                   Eccentricity                   Shape
n_colocalized_class_ch2@spot   Coloc with ch2@spot             Coloc
mean_scaled_ch0                Avg Intensity (Ch 0)           intensity
sum_scaled_ch0                 Sum Intensity (Ch 0)           intensity
```

Run this first when scripting `export` - column ids are the values to pass to `--group-by`-adjacent tooling and to `duckdb` queries against the same file.

## export

Exports a results database to CSV, XLSX, or Parquet, with the same filtering and (for `image` grouping) aggregation logic as the GUI's [Results List view](/guide/results/#list-view). Chart image export (histogram/scatter/boxplot PNGs) isn't wired up in the CLI yet - use the GUI's [Charts](/guide/results/#charts) tab for those.

### export csv / export xlsx

```sh
./evanalyzer cli export csv --db results.evadb --out results.csv
./evanalyzer cli export xlsx --db results.evadb --out results.xlsx \
  --group-by image --agg avg,median
```

| Argument       | Description                               |
| -------------- | ----------------------------------------- |
| `--db <path>`  | Results database to export (required)     |
| `--out <path>` | Output file path (required)               |
| _filter args_  | See [Filter Arguments](#filter-arguments) |
| _group args_   | See [Group Arguments](#group-arguments)   |

### export parquet

Writes the database's raw `objects` table straight to a Parquet file via DuckDB's own `COPY ... TO ... (FORMAT parquet)` - every column, completely unfiltered. There's no column selection, image/class filtering, or grouping to apply (that's the GUI's [Parquet export](/guide/results/#exporting-results) behavior too), so it takes a plainer set of arguments than `csv`/`xlsx`:

```sh
./evanalyzer cli export parquet --db results.evadb --out objects.parquet
```

| Argument       | Description                            |
| -------------- | --------------------------------------- |
| `--db <path>`  | Results database to export (required)  |
| `--out <path>` | Output file path (required)            |

### Filter Arguments

Shared by `view` and every `export` subcommand:

| Argument                      | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `--image <name>`              | Restrict to this image name (repeatable)                  |
| `--class <name>`              | Restrict to this object class (repeatable)                |
| `--transpond <true\|false>`   | Place the classes side by side instead of below each other - the CLI twin of the GUI's [Side by side layout](/guide/results/#side-by-side-layout-transposed-table). Default `false` |

:::note
`--transpond` is currently only applied by `view`; `export csv`/`export xlsx` accept it but still write the normal row layout. Use the GUI's **Transpond output table** export option for a transposed file.
:::

### Group Arguments

Shared by `export csv` and `export xlsx` - mirrors the GUI's [Grouping and Aggregating Rows](/guide/results/#grouping-and-aggregating-rows):

| Argument                            | Description                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `--group-by <image\|folder\|regex>` | Aggregate rows instead of exporting one row per object. Only `image` has a matching query today - `folder`/`regex` are recognized but currently rejected |
| `--agg <list>`                      | Comma-separated aggregate function(s) applied to every numeric column when grouping: `min`, `max`, `avg` (default), `median`, `stdev`, `sum` |
| `--split-colocalized`               | Accepted but currently rejected - no row-level "is this object colocalized at all" split exists in the current backend        |
| `--group-by-class`                  | No-op when grouping by image - `image` grouping always splits by class already                                                |

## train-classifier

Trains a pixel or object classifier from a project's labeled objects and saves it under `<project-dir>/models/` - the headless counterpart of the GUI's [training dialog](/ai/training/). Every object with an assigned class, across every image of the project, is used as training data.

```sh
./evanalyzer cli train-classifier --project experiment.evaproj --settings model.json
```

| Argument                     | Description                                                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--project <path>`           | Project file to train from (required)                                                                                                             |
| `--settings <path>`          | JSON file describing the model: metadata, backend hyperparameters (Random Forest / KNN / MLP), feature spec and class labels (required)          |
| `--model-name <name>`        | Name of the saved model file. Defaults to the name in the `--settings` metadata                                                                   |
| `--channel <n>`              | Image channel to read (pixel classifiers only, default `0`)                                                                                       |
| `--t-stack <n>`              | Time frame to read (pixel classifiers only, default `0`)                                                                                          |
| `--z-stack-handling <mode>`  | How to handle Z-stacks (pixel classifiers only): `single-stack` (default), `all-stacks`, `max-intensity`, `min-intensity`, `avg-intensity`, `sum-intensity`, `take-the-middle` |

## Project File

The CLI operates on an EVAnalyzer project file (`.evaproj`). Create and configure the project using the GUI, save it, and then use the saved file for headless runs.

The project file is a JSON document - it can be modified programmatically using any scripting language.

## Automated Parameter Variation

A common use case is running the same pipeline with multiple parameter sets. The project file can be modified by a script before each run.

### Example: vary blur kernel size with Python

```python
import json
import subprocess

def set_blur_kernel(filename, kernel_size):
    with open(filename) as f:
        data = json.load(f)

    for pipeline in data.get("pipelines", []):
        for step in pipeline.get("steps", []):
            if step.get("command", {}).get("type") == "blur":
                step["command"]["kernelSize"] = kernel_size

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def run_analysis(project_file):
    subprocess.run(
        ["./evanalyzer", "cli", "analyze", "--project", project_file],
        check=True,
    )

for size in [3, 5, 7, 9]:
    set_blur_kernel("experiment.evaproj", size)
    run_analysis("experiment.evaproj")
    print(f"Finished kernel_size={size}")
```

## Project File Format

The project file is a JSON document following the EVAnalyzer schema. Key top-level fields:

```json
{
  "metadata": { "name": "My experiment", ... },
  "classification": { "classes": [...] },
  "plate": { ... },
  "images": { "root": "/path/to/images", "list": { ... } },
  "pipelines": [
    {
      "id": "...",
      "name": "EV Detection",
      "enabled": true,
      "imageSource": { ... },
      "steps": [
        {
          "enabled": true,
          "command": { "type": "rollingBall", "radius": 4.0, "ballType": "paraboloid" }
        },
        ...
      ]
    }
  ]
}
```

### File extensions

| Extension | Description                      |
| --------- | -------------------------------- |
| `.evaproj` | EVAnalyzer project file         |
| `.evapt`   | Project template file           |
| `.evapipe` | Pipeline template file          |
| `.evadb`  | Results database (DuckDB format) |

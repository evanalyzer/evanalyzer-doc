---
title: Command Line Interface
description: Run EVAnalyzer headlessly for batch analysis, scripting, and exporting results.
---

EVAnalyzer can be driven entirely from the command line via the `evanalyzer cli` subcommand, enabling headless batch processing, integration into automated workflows, and remote execution on servers — no GUI/display required.

## Overview

The same `evanalyzer` binary handles both modes:

```sh
# Linux
./evanalyzer                              # launch the GUI
./evanalyzer cli <command> [options...]   # run a one-shot CLI command and exit

# Windows
evanalyzer.exe cli <command> [options...]
```

| Command | Purpose |
|---|---|
| [`analyze`](#analyze) | Run a project's enabled pipelines over its images and write a new results database |
| [`project-info`](#project-info) | Print a project's images, classes, and pipelines without running anything |
| [`view`](#view) | Print a quick summary and a page of rows from a results database |
| [`columns`](#columns) | List the column ids available for grouping/chart axes in a results database |
| [`export`](#export) | Export a results database to CSV, XLSX, or a chart image |

Every command supports `--help`:

```sh
./evanalyzer cli analyze --help
```

## analyze

Runs a project's enabled [pipelines](/guide/pipelines/) over its images and writes a new [results database](#results-database).

```sh
./evanalyzer cli analyze --project settings.improj
```

| Argument | Description |
|---|---|
| `--project <path>` | Project file to analyze (required) |
| `--images <dir>` | Scan this directory and use it as the project's image root before running. If omitted, the project's already-saved image list is used as-is |
| `--threads <n>` | Number of images to process in parallel (default: number of CPUs minus one) |

The command prints a progress line per image as it completes, then a summary:

```
Project:   settings.improj
Images:    48
Pipelines: 1 enabled
Output:    ./evanalyzer/EV Detection
Running with 7 parallel thread(s)...

[48/48] /data/plate1/A1_01.tif
Done: 48 image(s) analyzed in 32.4s (0 failed)
Results database written under: ./evanalyzer/EV Detection
```

A project with no images (and no `--images` override) fails fast with an error instead of running.

## project-info

Prints a project's image count, classes, and pipelines without running anything — useful for sanity-checking a project file before kicking off a long batch run.

```sh
./evanalyzer cli project-info --project settings.improj
```

```
Project:    settings.improj
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

## Results Database

`analyze` writes results to a `results.evadb` file (DuckDB format) under the project's job folder — the same file the GUI's [Results](/guide/results/) view opens. `view`, `columns`, and `export` all read from this file via `--db`.

```sh
duckdb results.evadb "SELECT object_class_name, COUNT(*) FROM rois GROUP BY object_class_name"
```

## view

Prints a database summary (image/class counts, T/Z-stack ranges) followed by a paginated, human-readable table of per-object rows — a quick terminal preview without exporting anything.

```sh
./evanalyzer cli view --db results.evadb --limit 10
```

| Argument | Description |
|---|---|
| `--db <path>` | Results database produced by `analyze` (required) |
| `--page <n>` | Zero-based page index (default `0`) |
| `--limit <n>` | Rows per page (default `25`) |
| `--channels` | Also show per-channel intensity columns |
| `--image <name>` | Restrict to this image name (repeatable) |
| `--class <name>` | Restrict to this object class (repeatable) |
| `--colocalized <true\|false>` | Restrict to colocalizing or non-colocalizing objects only |

## columns

Lists every column id available in a results database — including per-channel intensity columns and per-partner-class colocalization columns — along with whether each is numeric (and therefore usable for `--group-by`, chart axes, or `--metric`/`--agg`).

```sh
./evanalyzer cli columns --db results.evadb
```

```
ID                                   LABEL                            NUMERIC
roi_id                               ROI ID
image                                Image
class                                Class
area_px                              Area (px²)                      yes
area_nm2                             Area (nm²)                      yes
circularity                          Circularity                     yes
colocalized                          Colocalized
ch0_min_bit                          Ch0 Min (bit)                   yes
ch0_max_bit                          Ch0 Max (bit)                   yes
ch0_avg_bit                          Ch0 Avg (bit)                   yes
coloc_partner__cy7@spot__count       Coloc w/ cy7@spot (#)           yes
coloc_partner__cy7@spot__ids         Coloc w/ cy7@spot (IDs)
```

Run this first when scripting `export` — column ids are the values to pass to `--column`, `--x`/`--y`, and `--metric`.

## export

Exports a results database to a table file or a chart image, with the same filtering, grouping/aggregation, and charting logic as the GUI's [Results](/guide/results/) view.

### export csv / export xlsx

```sh
./evanalyzer cli export csv --db results.evadb --out results.csv
./evanalyzer cli export xlsx --db results.evadb --out results.xlsx \
  --group-by regex --group-regex '^([A-Z]\d+)_' --agg avg,median --group-by-class
```

| Argument | Description |
|---|---|
| `--db <path>` | Results database to export (required) |
| `--out <path>` | Output file path (required) |
| *filter args* | See [Filter Arguments](#filter-arguments) |
| *group args* | See [Group Arguments](#group-arguments) |

### export chart histogram / scatter / heatmap

Renders a chart straight to a PNG file — the CLI equivalent of the GUI's [Charts panel](/guide/results/#charts).

```sh
# Histogram of object area, log-scaled
./evanalyzer cli export chart histogram --db results.evadb --out area.png \
  --column area_px --buckets 30 --log-scale

# Circularity vs. area, colored by class
./evanalyzer cli export chart scatter --db results.evadb --out scatter.png \
  --x area_px --y circularity --color-by class

# Spatial density heatmap (objects per 256px cell)
./evanalyzer cli export chart heatmap --db results.evadb --out heatmap.png \
  --metric count --cell-size 256
```

| Argument | Histogram | Scatter | Heatmap |
|---|---|---|---|
| `--db <path>` | ✓ required | ✓ required | ✓ required |
| `--out <path>` | ✓ required | ✓ required | ✓ required |
| `--column <id>` | ✓ required | — | — |
| `--x <id>` / `--y <id>` | — | ✓ required | — |
| `--metric <count\|column-id>` | — | — | ✓ required |
| `--buckets <n>` (default `20`) | ✓ | — | — |
| `--log-scale` | ✓ | — | — |
| `--color-by <none\|class\|colocalized>` (default `none`) | — | ✓ | — |
| `--max-points <n>` (default `5000`, `0` = no cap) | — | ✓ | — |
| `--cell-size <px>` (default `256`) | — | — | ✓ |
| `--width <px>` / `--height <px>` (default `1000`×`700`) | ✓ | ✓ | ✓ |
| *filter args* | ✓ | ✓ | ✓ |

Column ids (`--column`, `--x`/`--y`, `--metric`) come from [`columns`](#columns).

### Filter Arguments

Shared by `view` and every `export` subcommand:

| Argument | Description |
|---|---|
| `--image <name>` | Restrict to this image name (repeatable) |
| `--class <name>` | Restrict to this object class (repeatable) |
| `--colocalized <true\|false>` | Restrict to colocalizing or non-colocalizing objects only |

### Group Arguments

Shared by `export csv` and `export xlsx` — mirrors the GUI's [Grouping and Aggregating Rows](/guide/results/#grouping-and-aggregating-rows):

| Argument | Description |
|---|---|
| `--group-by <image\|folder\|regex>` | Aggregate rows instead of exporting one row per object |
| `--group-regex <pattern>` | Regex used when `--group-by regex`; the first capture group (or the whole match if none) becomes the group key |
| `--agg <list>` | Comma-separated aggregate function(s) applied to every numeric column: `min`, `max`, `avg` (default), `median`, `stdev`, `sum` |
| `--split-colocalized` | Additionally split each group into a colocalizing / non-colocalizing row |
| `--group-by-class` | Additionally split each group by object class |

## Project File

The CLI operates on an EVAnalyzer project file (`.improj`). Create and configure the project using the GUI, save it, and then use the saved file for headless runs.

The project file is a JSON document — it can be modified programmatically using any scripting language.

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
    set_blur_kernel("settings.improj", size)
    run_analysis("settings.improj")
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

| Extension | Description |
|---|---|
| `.improj` | EVAnalyzer project file |
| `.impt` | Project template file |
| `.evadb` | Results database (DuckDB format) |

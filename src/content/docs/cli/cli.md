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
./evanalyzer --project experiment.evaproj # launch the GUI and open a project
./evanalyzer cli <command> [options...]   # run a one-shot CLI command and exit

# Windows
evanalyzer.exe cli <command> [options...]
```

The commands are grouped by what they work on:

| Command | Purpose |
| --- | --- |
| [`analyze`](#analyze) | Run a project's enabled pipelines over its images and write a new results database |
| [`project new`](#project-new) | Create a new empty project file |
| [`project info`](#project-info) | Print a project's images, classes, and pipelines without running anything |
| [`project validate`](#project-validate) | Check a project as a run would: its images on disk, its pipelines and modules, and the channels they read |
| [`project cite`](#project-cite) | Write a project's methods paragraph and the citations of its steps (Markdown) |
| [`results view`](#results-view) | Print a quick summary and a page of rows from a results database |
| [`results columns`](#results-columns) | List the column ids available for grouping/chart axes in a results database |
| [`results export`](#results-export) | Export a results database to CSV, XLSX, or Parquet |
| [`jobs list`](#jobs-list-and-jobs-attach) | List the analyses on the `--remote` server: the running one and recently finished ones |
| [`jobs attach`](#jobs-list-and-jobs-attach) | Follow an analysis on the `--remote` server again, e.g. after the connection dropped |
| [`train-classifier`](#train-classifier) | Train a pixel or object classifier from a project's labeled objects |

Every command and group has a help: `-h` prints one line per option, `--help` adds the details:

```sh
./evanalyzer cli --help            # every command
./evanalyzer cli results -h        # the commands of a group
./evanalyzer cli analyze --help    # a command's options in detail
```

## Global Options

These work in every mode - the GUI, every `cli` command and `server` - also after the command name:

| Option              | Description                                                                                                                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--max-threads <n>` | Most CPU cores EVAnalyzer uses - the analysis, AI models, the results database and everything else - e.g. to keep a computer usable during a long analysis. At least 1. Default: the **Most CPU cores** [setting](/guide/settings/#viewport), else all of them |
| `--max-ram <MB>`    | Most RAM in MB EVAnalyzer plans with - caches, threads and the results database are sized as if the computer had no more. Not a hard limit on every allocation (a container's limit is). A plain number of at least 1 (`8G` is not accepted). Default: the **Most RAM** [setting](/guide/settings/#viewport), else the computer's RAM |
| `--ai-devices <devices>` | Where AI models (Cellpose, StarDist, U-Net, YOLOv5) run: `auto` (every GPU, else the CPU), `cpu`, or GPU numbers like `0,2`. Applies where the analysis runs - this machine, or the workers of a `server` started with it; ignored with `--remote`. Default `auto` |
| `--gpu-slots <n>`   | Parallel AI inferences per GPU. Raise it for GPUs with memory to spare; a GPU that runs out of memory goes back down by itself. Default 1 |
| `--ai-plugin <file>` | The AI plugin library to try first (`libevanalyzer_ai.so`, `evanalyzer_ai.dll`, `libevanalyzer_ai.dylib`) - for development and tests; a package finds its own next to the program |

```sh
# Keep 4 cores and 8 GB for everything else on a 12-core, 16 GB computer
./evanalyzer --max-threads 8 --max-ram 8192 cli analyze --project experiment.evaproj
```

## Running on a Server

Every command can also run on another machine - for example a GPU workstation that holds the images. Add the [remote options](/remote/remote-control/#client-options):

```sh
./evanalyzer cli --remote wss://server-name:7400 --user alice --remote-fingerprint <SHA256> \
  analyze --project /data/experiment-12/experiment.evaproj
```

All paths (`--project`, `--images`, `--db`, `--out`, `--settings`) then refer to the server, and output files are written there. See [Remote Control](/remote/remote-control/) for setting up the server.

### jobs list and jobs attach

An analysis started on a server keeps running there if the connection drops - `analyze` then exits with a message naming the analysis id (_"Follow it again with `cli jobs attach --job <id>` (same --remote and --user)"_). Use the same `--remote` and `--user` options to find and follow it again:

```sh
# List the running analysis and recently finished ones
./evanalyzer cli --remote wss://server-name:7400 --user alice jobs list

# Follow the running analysis (or a specific one with --job <id>)
./evanalyzer cli --remote wss://server-name:7400 --user alice jobs attach
```

| Argument | Description |
| --- | --- |
| `--job <id>` | `jobs attach` only: id of the analysis, as `jobs list` shows it. Default: the running one |

`jobs attach` prints the progress like `analyze` does; `Ctrl+C` cancels the analysis. Both commands only work with `--remote`.

## Docker and Compute Clusters

For servers and compute clusters without a desktop, each release has command-line packages for Linux - the same program without the GUI, so no display or font libraries are needed. They hold everything but the GUI - `cli`, `server`, `worker` and `hash-password`; started without a command, the program says _"This build has no desktop app"_. See [Installation](/getting-started/installation/#command-line-packages-and-docker) for the files.

The same packages are also published as a Docker image, `joda001/evanalyzer`:

| Tag | Platforms | AI models (Cellpose, StarDist, U-Net, YOLOv5) |
| --- | --- | --- |
| `<version>`, `latest` | linux/amd64, linux/arm64 | On the CPU (amd64); none on arm64 |
| `<version>-cuda`, `cuda` | linux/amd64 | On an NVIDIA GPU, else the CPU |

`latest` and `cuda` are the newest stable release; pre-releases (e.g. `1.2.0-alpha.1`) only get their version tag.

Mount the folder with the project and its images at `/data`:

```sh
docker run --rm -v "$PWD":/data joda001/evanalyzer \
    cli analyze --project /data/my.evaproj --images /data/images --job-name run1
```

`--images` makes the mounted folder the project's image root, so image paths saved on another computer don't matter. The results land in `/data/results/` next to the project. The container runs as uid 65532: the mounted folder must be writable for it, or pass `--user "$(id -u):$(id -g)"`. Limit resources with Docker's `--cpus` / `--memory`, or with [`--max-threads` / `--max-ram`](#global-options).

For the GPU, use the `cuda` tag with `--gpus all`. The host needs only the NVIDIA driver (580 or newer) and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```sh
docker run --rm --gpus all -v "$PWD":/data joda001/evanalyzer:cuda \
    cli analyze --project /data/my.evaproj --images /data/images
```

The image also runs a [server](/remote/remote-control/): `docker run -d -p 7400:7400 -v "$PWD":/data -v evanalyzer-state:/var/lib/evanalyzer joda001/evanalyzer server --config /opt/evanalyzer/server.toml` - `docker logs` then shows the admin password and the TLS fingerprint.

### Apptainer / Singularity

Clusters usually run Apptainer instead of Docker. It runs the image as is, as your own user, and on any Linux - also on older cluster systems without glibc 2.39, which the plain Linux packages need:

```sh
apptainer pull evanalyzer.sif docker://joda001/evanalyzer:cuda
apptainer run --nv --bind /scratch/me/study:/data evanalyzer.sif \
    --max-threads "$SLURM_CPUS_PER_TASK" --max-ram 60000 \
    cli analyze --project /data/my.evaproj --images /data/images
```

In a Slurm job script, set `--max-threads` and `--max-ram` (MB) to the job's `--cpus-per-task` and `--mem`, so EVAnalyzer plans with what the job was given, not the whole node. `--nv` passes the node's GPUs and driver in.

## analyze

Runs a project's enabled [pipelines](/guide/pipelines/) over its images and writes a new [results database](#results-database).

```sh
./evanalyzer cli analyze --project experiment.evaproj
```

| Argument           | Description                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `--project <path>` | Project file to analyze (required)                                                                                                          |
| `--images <dir>`   | Scan this directory and use it as the project's image root before running. If omitted, the project's already-saved image list is used as-is |
| `--threads <n>`    | Number of images to process in parallel. If omitted, EVAnalyzer picks the highest thread count that fits within available RAM and CPU cores. Never more than [`--max-threads`](#global-options) |
| `--job-name <name>` | Name of the run: its results folder and `.evadb` file. Default: a random two-word name |
| `--set <SETTING=VALUE>` | Change a step's setting for this run only (repeatable) - see [Changing settings with --set](#changing-settings-with---set) |

The parallelism is automatically capped to whichever is lower — the number of CPU cores (or `--max-threads`) or the number of images that fit in available RAM (or `--max-ram`) — so a low-memory machine never launches more parallel workers than it can sustain.

The command prints a progress line per image as it completes, then a summary:

```
Project:   experiment.evaproj
Images:    48
Pipelines: 1 enabled
Output:    ./results/20261021T190435Z__EV Detection
Running with 7 parallel thread(s) (Ctrl+C to cancel)...

[48/48] /data/plate1/A1_01.tif
Done: 48 image(s) analyzed in 32.4s (0 failed)
Results database written under: ./results/20261021T190435Z__EV Detection
```

A project with no images (and no `--images` override) fails fast with an error instead of running.

Press **Ctrl+C** to request a graceful stop; in-flight images will finish before the process exits.

### Changing settings with --set

`--set` changes one setting of a step for this run, without editing the project file - e.g. to try several values of a parameter in a script:

```sh
./evanalyzer cli analyze --project experiment.evaproj \
  --set "Varroa detection.9.minObjectSize=100" \
  --set "Varroa detection.3.thresholds.0.method=Otsu"
```

Each value is written `Pipeline.step.setting=value`:

| Part | Description |
| --- | --- |
| `Pipeline` | The pipeline's name. A name may contain dots - the longest pipeline name the text starts with is used |
| `step` | The step's `id` in the project file (`"id": 9` in its entry under `steps`) - not its position in the editor's list |
| `setting` | The setting's name as in the project file (`minObjectSize`) or as in the editor (`min_object_size`) - case and `_` don't matter. An entry of a list is addressed by its number (`thresholds.0.method`), a [module](/guide/modules/) step's parameter by its key |
| `value` | The new value. A choice may be written as the editor shows it (`Distance Map`) or as the file spells it (`DISTANCE_MAP`); an on/off setting takes `true`/`false`, `yes`/`no`, `on`/`off` or `1`/`0` |

Each change is printed before the run starts:

```
Set:       pipeline “Varroa detection”, step 9 (WATERSHED): min_object_size 0 → 100
```

A value is set as the editor sets it and read back, so a value the setting doesn't take is an error instead of being ignored. Every `--set` that doesn't apply is reported at once and nothing runs, e.g.:

```
Error: --set "Bees.1.minSize=3": no pipeline it starts with - the project has “Varroa detection”, “Varroa detection.v2”
--set "Varroa detection.7.minSize=3": pipeline “Varroa detection” has no step 7 - its steps (id and command): 3 THRESHOLD, 9 WATERSHED
--set "Varroa detection.9.minObjectSiz=3": pipeline “Varroa detection”, step 9 (WATERSHED) has no setting `minObjectSiz` - did you mean `min_object_size`?
--set "Varroa detection.9.smoothingSigma=soft": pipeline “Varroa detection”, step 9 (WATERSHED): `soft` is no value for smoothing_sigma - it takes a number (it stays 0)
```

The project file stays as it is. The run's copy of the project, `<job>.evaproj` next to its results, records the values it ran with. [`project validate --set`](#project-validate) checks the project with the same changes, without running it.

## project new

Creates a new empty project file - to fill in with the GUI, or on a server with `--remote`, where it is created on the server's disk like every `project` command works there.

```sh
./evanalyzer cli project new --project experiment.evaproj
```

| Argument | Description |
| --- | --- |
| `--project <path>` | Project file to create (required). `.evaproj` is added if the name has another or no extension |

The project gets the creation time and, if one is set in this computer's [settings](/guide/settings/), the author. An existing file is never overwritten: _"… already exists - choose another name or delete it first"_.

## project info

Prints a project's image count, classes, and pipelines without running anything - useful for sanity-checking a project file before kicking off a long batch run.

```sh
./evanalyzer cli project info --project experiment.evaproj
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

## project validate

Checks a project as a run would - a pre-flight step before starting a long headless run:

- every image the project references, on disk
- its pipelines and [modules](/guide/modules/), as the editor checks them
- the channels the pipelines read, against the images' channels

```sh
./evanalyzer cli project validate --project experiment.evaproj
```

| Argument | Description |
| --- | --- |
| `--project <path>` | Project file to check (required) |
| `--set <SETTING=VALUE>` | Check the project with a step's setting changed (repeatable), as [`analyze --set`](#changing-settings-with---set) would run it. The project file stays as it is |

```
Project:    experiment.evaproj
Image root: /data/plate1
Checked 48 image(s)
All images found on disk.
Checked 1 pipeline(s) and 0 module(s)
No problems found in the pipelines.
```

Missing images are listed one per line, and each problem in the pipelines is printed with its place, e.g. `  warning: pipeline “EV Detection”, step 3: …` (here the step's position in the editor's list). Warnings are only printed; missing images and errors make the command fail with a non-zero exit code, e.g. _"Error: 2 of 48 image(s) could not be found on disk, 1 error(s) in the pipelines"_ - so it can guard a run in a script:

```sh
./evanalyzer cli project validate --project experiment.evaproj && \
  ./evanalyzer cli analyze --project experiment.evaproj
```

A project file that doesn't load fails here too, with every problem at its place - see [Project File](#project-file).

## project cite

Writes the same file as **EVA › Cite project** in the GUI: a ready-to-paste methods paragraph naming EVAnalyzer with its version, each pipeline's steps with their citations, and the full reference list - see [Citation](/citation/#citing-the-algorithms-you-used).

```sh
./evanalyzer cli project cite --project experiment.evaproj
```

| Argument           | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| `--project <path>` | Project file to cite (required)                                        |
| `--out <path>`     | Markdown file to write. Default: `citation.md` next to the project file |

It prints _"Citation written to <path>"_.

## Results Database

`analyze` writes results to a `<job name>.evadb` file (DuckDB format) in `results/<date>__<job name>/` next to the project - the same file the GUI's [Results](/guide/results/) view opens. The `results` commands - `view`, `columns` and `export` - all read from this file via `--db`.

```sh
duckdb results.evadb "SELECT object_class_name, COUNT(*) FROM objects GROUP BY object_class_name"
```

## results view

Prints a database summary (image/class counts, T/Z-stack ranges) followed by a paginated, human-readable table of per-object rows - a quick terminal preview without exporting anything.

```sh
./evanalyzer cli results view --db results.evadb --limit 10
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
| `--t <n\|a-b>`, `--z <n\|a-b>` | Only these time points / Z planes, see [Filter Arguments](#filter-arguments) |

## results columns

Lists every column id available in a results database - including per-channel intensity columns and per-partner-class colocalization counts - grouped the same way as the GUI's Columns picker (General, Geometry, Shape, Coloc, Intensity).

```sh
./evanalyzer cli results columns --db results.evadb
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

Measurement steps add a column per measurement, with the id `measurement:<step ID>/<measurement>` (group **Measurements**); a measurement that points to another object also has `measurement_object:<…>`.

Run this first when scripting `results export` - column ids are the values to pass to `--group-by`-adjacent tooling and to `duckdb` queries against the same file.

## results export

Exports a results database to CSV, XLSX, or Parquet, with the same filtering and (for `image` grouping) aggregation logic as the GUI's [Results List view](/guide/results/#list-view). Chart image export (histogram/scatter/boxplot PNGs) isn't wired up in the CLI yet - use the GUI's [Charts](/guide/results/#charts) tab for those.

### results export csv / xlsx

```sh
./evanalyzer cli results export csv --db results.evadb --out results.csv
./evanalyzer cli results export xlsx --db results.evadb --out results.xlsx \
  --group-by image --agg avg,median
```

| Argument       | Description                               |
| -------------- | ----------------------------------------- |
| `--db <path>`  | Results database to export (required)     |
| `--out <path>` | Output file path (required)               |
| _filter args_  | See [Filter Arguments](#filter-arguments) |
| _group args_   | See [Group Arguments](#group-arguments)   |
| `--tracks`     | A row per track instead of per object - see [Tracks](#tracks) |
| `--measurements` | A row per measurement value - see [Measurements](#measurements) |
| `--project <path>` `--view <name>` | Export as a List view of the project shows the results - see [Exporting as a view](#exporting-as-a-view) |

### Tracks

`--tracks` writes the [tracks table](/guide/results/#tracks): a row per track with when it was seen, how far, fast and straight it moved, and the `--agg` statistics (default `avg`) of every numeric column over its time points. It can't be combined with `--group-by`; `--group-regex` sets the pattern of its well column.

| Argument | Description |
| --- | --- |
| `--min-points <n>` | Only tracks with at least this many time points (default `1`) |
| `--from-start` | Only tracks there from the first time point |
| `--no-edge` | Leave out tracks with an object touching the image edge |
| `--speed-unit <px-frame\|um-min\|um-s>` | The speed's unit (default `um-min`; `px-frame` without a pixel size or frame interval) |

### Measurements

`--measurements` writes the values of the [measurement steps](/guide/pipelines/#measurement-steps), one row per value, with the columns `image_name`, `image_rel_path`, `z_stack`, `t_stack`, `region`, `object_id`, `related_object_id`, `object_class_name`, `step`, `measurement`, `unit`, `key` and `value` - the same table as the GUI's [Measurements export](/guide/results/#exporting-results). `--image`, `--t` and `--z` restrict it; every measurement is written. Results without a measurement step fail with _"These results have no measurements - a pipeline needs a measurement step"_. It can't be combined with `--tracks`.

```sh
./evanalyzer cli results export csv --db results.evadb --out measurements.csv --measurements
```

### Exporting as a view

`--view <name>` exports the results the way a [List view](/guide/results/#views) of the project shows them: its columns, classes, images (**Only disabled** exports just the images left out), its [children and linked-object columns](/guide/results/#parents-and-children), [Coloc pairs](/guide/results/#coloc-pairs), and a row per object or - with **A row per: Images** - per image with the view's aggregations. `--project` names the `.evaproj` file the view belongs to; both are needed together. The name is matched ignoring case.

```sh
./evanalyzer cli results export xlsx --db results.evadb --out qc.xlsx \
  --project experiment.evaproj --view QC
```

Explicit `--image`, `--class` and `--group-by` win over the view. Columns the view names but these results lack are left out, with a note on stderr (_"Not in these results, left out of the view: …"_). A name that isn't a view of the project fails with the list of its views; a Plate, Charts or Tracks view fails with _"--view exports List views"_. It can't be combined with `--tracks` or `--measurements`.

### results export parquet

Writes the database's raw `objects` table straight to a Parquet file via DuckDB's own `COPY ... TO ... (FORMAT parquet)` - every column, completely unfiltered. There's no column selection, image/class filtering, or grouping to apply (that's the GUI's [Parquet export](/guide/results/#exporting-results) behavior too), so it takes a plainer set of arguments than `csv`/`xlsx`:

```sh
./evanalyzer cli results export parquet --db results.evadb --out objects.parquet
```

| Argument       | Description                            |
| -------------- | --------------------------------------- |
| `--db <path>`  | Results database to export (required)  |
| `--out <path>` | Output file path (required)            |

### Filter Arguments

Shared by `results view` and every `results export` subcommand:

| Argument                      | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| `--image <name>`              | Restrict to this image name (repeatable)                  |
| `--class <name>`              | Restrict to this object class (repeatable)                |
| `--transpond <true\|false>`   | Place the classes side by side instead of below each other - the CLI twin of the GUI's [Transpose](/guide/results/#transpose). Default `false` |
| `--t <n\|a-b>`                | Only these time points: one (`3`) or a range (`2-5`, both ends included), 0-based. Default: all |
| `--z <n\|a-b>`                | Only these Z planes, written the same way. Default: all |

:::note
`--transpond` is currently only applied by `results view`; `results export csv`/`xlsx` accept it but still write the normal row layout. Use the GUI's **Transpond output table** export option for a transposed file.
:::

### Group Arguments

Shared by `results export csv` and `results export xlsx` - mirrors the GUI's [Grouping and Aggregating Rows](/guide/results/#grouping-and-aggregating-rows):

| Argument                            | Description                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `--group-by <kind>`                 | Aggregate rows instead of exporting one row per object. `image`: a row per image and class, per time point. `class`, `well`, `group`, `folder`, `regex`, `track`: a time course - a line per class (every image pooled), per well (from the image names), per `--group-regex` group (`regex` is the same), per folder or per track |
| `--group-regex <regex>`             | Regex on the image name for `--group-by group` / `regex`: its first capture group is the group |
| `--agg <list>`                      | Comma-separated statistic(s) of every numeric column when grouping: `min`, `max`, `avg`, `median`, `stdev`, `sum`, and for a time course also `q1`, `q3`. Default `avg`; for a time course `avg,stdev` |
| `--normalize <none\|t0>`            | Time course values relative to each line's first time point (`t0`: in % of it) |
| `--layout <long\|wide\|both>`       | Time course tables: `long` (default, a row per time point × line), `wide` (per value and statistic a row per time point and a column per line; for CSV one file each next to `--out`, named `<name>_<value>.csv`) or both |
| `--with-parents`                    | Time course per track: each track with its parents' history - a daughter's line starts with its mother's track, a fused track has a line per parent (results with divisions or fusions) |
| `--group-by-class`                  | Accepted, but has no effect: `image` grouping always splits by class already |

The `--colocalized` and `--split-colocalized` options are gone; use **A row per: Coloc pairs** in a [view](#exporting-as-a-view) for the partners of each object.

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
| `--z-stack-handling <mode>`  | How the analyses using the model handle Z-stacks, which decides the image each labeled object is trained on: `single-stack` (default) or `all-stacks` - its own plane of its time frame (objects drawn on a z-projection are left out); `max-intensity`, `min-intensity`, `avg-intensity`, `sum-intensity`, `take-the-middle` - that projection of its time frame. Applies to pixel and object classifiers |

Every time frame with labeled objects is used; the `--t-stack` option is gone.

## Project File

The CLI operates on an EVAnalyzer project file (`.evaproj`). Create and configure the project using the GUI (or start one with [`project new`](#project-new)), save it, and then use the saved file for headless runs.

The project file is a JSON document - it can be modified programmatically using any scripting language.

A project file that doesn't load - in the CLI as in the GUI - names every problem with its pipeline, step and field, e.g.:

```
the project file could not be loaded, 2 problems:
  - pipeline “Nuclei”, step 2 (WATERSHED): smoothingSigma: invalid type: string "soft", expected f32
  - pipeline “Nuclei”, step 4 (WATERSHD): unknown command `WATERSHD` - did you mean `WATERSHED`?
```

The step number here is its position in the pipeline. Up to 20 problems are listed.

## Automated Parameter Variation

A common use case is running the same pipeline with multiple parameter sets. [`--set`](#changing-settings-with---set) changes a setting for one run without touching the project file, so a shell loop is enough:

```sh
for size in 3 5 7 9; do
  ./evanalyzer cli analyze --project experiment.evaproj \
    --job-name "kernel-$size" \
    --set "EV Detection.2.kernelSize=$size"
done
```

Each run gets its own results folder, and its copy of the project (`<job>.evaproj`) records the value it ran with. Check the overrides first with `project validate --set ...`.

Editing the JSON with a script before each run still works too - e.g. for changes `--set` can't make, such as adding or removing steps:

```python
import json
import subprocess

with open("experiment.evaproj") as f:
    data = json.load(f)

for pipeline in data.get("pipelines", []):
    for step in pipeline.get("steps", []):
        if step.get("command", {}).get("type") == "gaussianBlur":
            step["command"]["kernelSize"] = 7

with open("experiment-k7.evaproj", "w") as f:
    json.dump(data, f, indent=2)

subprocess.run(["./evanalyzer", "cli", "analyze", "--project", "experiment-k7.evaproj"], check=True)
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
          "id": 1,
          "enabled": true,
          "command": { "type": "rollingBall", "radius": 4.0, "ballType": "paraboloid" }
        },
        ...
      ]
    }
  ]
}
```

The paths in `images.list` are relative to `images.root`. A project with an absolute image path, or one that contains `..` or a drive, is refused before any image is analysed: _"Cannot start: the image path "…" is outside the image folder"_.

### File extensions

| Extension     | Description                                      |
| ------------- | ------------------------------------------------ |
| `.evaproj`    | EVAnalyzer project file                          |
| `.evatemplate` | Project template file                           |
| `.evamodule`  | [Module](/guide/modules/) library file           |
| `.evamodel`   | Trained [AI classifier](/ai/training/)           |
| `.evadb`      | Results database (DuckDB format)                 |

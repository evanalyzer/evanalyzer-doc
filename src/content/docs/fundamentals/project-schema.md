---
title: Project File Schema
description: The JSON Schema describing EVAnalyzer's .evaproj project file format, including pipelines and commands.
---

EVAnalyzer project files (`.evaproj`) are JSON documents following a published [JSON Schema](https://json-schema.org/) (draft 2020-12). The schema is generated directly from the application's own Rust types, so it always matches what a given release actually reads and writes.

It's published at a stable URL on this site, refreshed from a pinned release of the [main EVAnalyzer repository](https://github.com/evanalyzer/evanalyzer) on every docs build:

```
https://evanalyzer.org/schema/project.schema.json
```

:::note[Machine-readable]
Because it's a real JSON Schema with a `oneOf` discriminated union for every pipeline command, this file is enough on its own to validate an existing `.evaproj` file or generate a new one programmatically - for example, from a script or an LLM - without needing to read prose documentation first.
:::

## Top-Level Structure

A project file's root object (`ProjectSettings`) has these top-level fields:

| Field | Description |
| --- | --- |
| `schemaVersion` | On-disk format version, used to migrate older project files forward. |
| `meta` | Descriptive info: name, description, author, creation time. |
| `images` | The collection of images in the project and their processing state. |
| `plate` | Multi-well plate layout, for high-content screening projects. |
| `classification` | The project's object class definitions - see [Classification](/guide/classification/). |
| `pipelines` | The array of analysis pipelines - see below. |
| `commandGroups` | The [command groups](/guide/modules/) of the project - see [Command Groups](#command-groups). |
| `tileMerge` | The [cross-tile merging](/fundamentals/cross-tile-merging/) settings. |

## Pipelines and Steps

Each entry in `pipelines` (`PipelineSettings`) has:

- `id` - a unique pipeline ID.
- `name` - a display name.
- `imageSource` - which image this pipeline reads: a channel index (`{"CHANNEL": 0}`), a named in-memory buffer (`{"MEMORY": "..."}`), or `"SCRATCHPAD"` for object-only pipelines that don't start from a raw image.
- `enabled` - disabled pipelines are skipped during analysis.
- `steps` - an ordered array of `PipelineStepSettings`. Each step has a stable `id`, `enabled`, and either a `command` (a single command) or a `group` (a use of a [command group](#command-groups)).

`command` is a `PipelineCommand` - a discriminated union keyed by a `type` string, with one variant per pipeline command (`"blur"`, `"threshold"`, `"connectedComponents"`, `"stardist"`, `"colocalizeObjects"`, and so on for [every command](/commands/overview/)). Each `type` value corresponds directly to a command documented in the [Commands reference](/commands/overview/), and the matching schema `$defs` entry (for example `BlurSettings`) lists that command's exact parameters, types, defaults, and limits.

A minimal single-step pipeline looks like:

```json
{
  "id": "pipeline-1",
  "name": "Nuclei",
  "imageSource": { "CHANNEL": 0 },
  "enabled": true,
  "steps": [
    {
      "id": 1,
      "enabled": true,
      "command": {
        "type": "blur",
        "kernelSize": 5
      }
    }
  ]
}
```

## Object Classes in Steps

A class setting is written as `"UNSET"`, `{"GLOBAL": 5}` (project class 5) or `{"LOCAL": 1}` (class 1 of the enclosing command group - only valid inside a group). Files written before command groups existed use `{"VALID": 5}`, which is still read as `GLOBAL`.

## Command Groups

`commandGroups` is an array of group definitions (`GroupDefinition`):

- `key` - unique key of the group in the project, e.g. `"CELL_RECONSTRUCTION"`.
- `meta` - name, short description, description, author, version.
- `steps` - the group's steps, in the same format as a pipeline's steps (groups can contain groups).
- `classes` - the group's own (internal) classes, referred to as `{"LOCAL": n}`.
- `parameters` - the parameters shown on the group card. Each has a `key`, a label, a description, a `default` value and `bindings`: the inner settings it sets, each as `{ "step": <step id>, "param": "<setting name>" }` (e.g. `"thresholds.0.min_threshold"`).
- `origin` - the library file (`.evagroup`) and version the group was inserted from, if any.

A step using a group refers to it by key and holds its own parameter values:

```json
{
  "id": 7,
  "enabled": true,
  "group": {
    "key": "CELL_RECONSTRUCTION",
    "values": { "cell_class": 3, "method": "PARABOLOID", "radius": 4.5 }
  }
}
```

Values are plain JSON (`4`, `4.5`, `true`, `"PARABOLOID"`, `[1, 2]`), keyed by the parameter's key; their meaning comes from the settings the parameter is bound to. A parameter missing from `values` has the definition's default.

Group library files (`.evagroup`) hold a group definition plus the groups it uses; their schema is `group_template.schema.json`.

## Plate Layout

The `plate` object (`PlateSettings`) holds the settings of the [Plate view](/guide/results/#plate-view) and the Plates/Wells export:

- `groupingMode` - how images are assigned to wells: `"AUTO"` (well detected from the image name), `"CUSTOM"` (`groupingRegex` on the image name) or `"FOLDER"` (one well per image folder).
- `groupingRegex` - the regex for `"CUSTOM"`; its groups are the well (`B03`), the plate row (`B`), the plate column (`03`) and the image number in the well (`01`).
- `plateSize` - `"AUTO"` or a fixed size such as `"PLATE8X12"` (96 wells).
- `wellLayout` - `"AUTO"` or a fixed grid `{"FIXED": {"rows": 2, "cols": 3}}`.
- `wellImageOrder` - for a fixed well grid: the image number shown at each grid position, row by row (`[1, 2, 3, 4]` = number order). Rearranging images by drag and drop in the well view writes this list.

Project files with the older plate format are migrated automatically when opened. The current project schema version is 4; older files are migrated forward when opened.

## Versioning

The schema is fetched from a specific release tag of the app repository (currently `0.1.0-alpha.16`), not the floating `main` branch, so it always describes a real released version rather than in-progress changes. If the fetch fails during a docs build (for example, a GitHub outage), the previously published copy is kept rather than the build failing.

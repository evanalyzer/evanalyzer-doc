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
| `metadata` | Descriptive info: name, description, author, creation time. |
| `images` | The collection of images in the project and their processing state. |
| `plate` | Multi-well plate layout, for high-content screening projects. |
| `classification` | The project's object class definitions - see [Classification](/guide/classification/). |
| `pipelines` | The array of analysis pipelines - see below. |

## Pipelines and Steps

Each entry in `pipelines` (`PipelineSettings`) has:

- `id` - a unique pipeline ID.
- `name` - a display name.
- `imageSource` - which image this pipeline reads: a channel index (`{"CHANNEL": 0}`), a named in-memory buffer (`{"MEMORY": "..."}`), or `"SCRATCHPAD"` for object-only pipelines that don't start from a raw image.
- `enabled` - disabled pipelines are skipped during analysis.
- `steps` - an ordered array of `PipelineStepSettings`, each an `{ enabled, command }` pair.

`command` is a `PipelineCommand` - a discriminated union keyed by a `type` string, with one variant per pipeline command (`"blur"`, `"threshold"`, `"connectedComponents"`, `"stardist"`, `"colocalization"`, and so on for all [31 commands](/commands/overview/)). Each `type` value corresponds directly to a command documented in the [Commands reference](/commands/overview/), and the matching schema `$defs` entry (for example `BlurSettings`) lists that command's exact parameters, types, defaults, and limits.

A minimal single-step pipeline looks like:

```json
{
  "id": "pipeline-1",
  "name": "Nuclei",
  "imageSource": { "CHANNEL": 0 },
  "enabled": true,
  "steps": [
    {
      "enabled": true,
      "command": {
        "type": "blur",
        "kernelSize": 5
      }
    }
  ]
}
```

## Versioning

The schema is fetched from a specific release tag of the app repository (currently `0.1.0-alpha.16`), not the floating `main` branch, so it always describes a real released version rather than in-progress changes. If the fetch fails during a docs build (for example, a GitHub outage), the previously published copy is kept rather than the build failing.

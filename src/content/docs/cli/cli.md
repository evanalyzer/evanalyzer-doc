---
title: Command Line Interface
description: Run EVAnalyzer headlessly for batch analysis and scripting.
---

EVAnalyzer can be driven entirely from the command line, enabling headless batch processing, integration into automated workflows, and remote execution on servers.

## Starting in CLI mode

```sh
# Linux
./evanalyzer --mode=cli --project settings.improj

# Windows
evanalyzer.exe --mode=cli --project settings.improj
```

| Argument | Description |
|---|---|
| `--mode=gui` | Launch the graphical interface (default when no `--mode` is given) |
| `--mode=cli` | Launch in headless CLI mode |
| `--project <path>` | Open this project file on startup |

Use `--help` to see all options:

```sh
./evanalyzer --help
```

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
        ["./evanalyzer", "--mode=cli", "--project", project_file],
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

## Results Database

Results are written to `results.evadb` in the job folder. The file is a standard DuckDB database and can be queried directly with any [DuckDB client](https://duckdb.org/docs/stable/clients/cli/overview.html):

```sh
duckdb results.evadb "SELECT class, COUNT(*) FROM objects GROUP BY class"
```

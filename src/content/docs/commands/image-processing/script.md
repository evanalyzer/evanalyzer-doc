---
title: Script
description: Run your own Rhai script as a pipeline step - with loops, conditions and the regular pipeline commands.
---

The **Script** command runs a short program written in [Rhai](https://rhai.rs), a small scripting language with a syntax close to JavaScript and Rust. A script can run the regular pipeline commands by name, keep intermediate images in variables, and decide what to do next based on the image - things a fixed sequence of steps can't express:

```rust
let raw = image();
let blurred = run("gaussian_blur", raw, #{ kernel_size: 3 });

// Too dim after blurring? Try again with a larger kernel.
if blurred.max() < 100.0 {
    blurred = run("gaussian_blur", raw, #{ kernel_size: 5 });
}

run("threshold", blurred, #{ "thresholds.0.method": "otsu" });
run("connected_components");
print(`objects: ${instance_count()}`);
```

## Parameters

| Parameter   | Description                                                                                                                                                             |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Source**  | The script. The step card shows a read-only preview; click **Edit script** to open the [script editor](#script-editor).                                                 |
| **Classes** | The object classes the script creates or uses. Commands run by the script may only use these classes - this way the pipeline knows them without having to run the script. |

## Script API

### Running commands

| Function                          | Description                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| `run("command")`                  | Runs a pipeline command with its default settings on the step's current image.                    |
| `run("command", #{ params })`     | The same, with the given parameters applied on top of the defaults.                               |
| `run("command", image [, #{ params }])` | Runs the command on `image` instead of the current image.                                   |

`run` returns the image the command produced, which also becomes the step's current image - the input of the next command, just like in a normal pipeline.

**Command names** are the command keys in lower case with underscores, e.g. `gaussian_blur`, `rolling_ball`, `threshold`, `connected_components`, `watershed`, `extract_objects`, `stardist`. The script editor lists all of them.

**Parameter names** are the names of the step settings, in lower case with underscores, e.g. `kernel_size`. Entries of a list parameter are addressed as `list.index.field`, e.g. `"thresholds.0.method"`; writing to the index one past the end of a list adds an entry. Dropdown values are matched loosely - case, spaces, `_` and `-` are ignored, so `"iso_data"` selects **Iso Data**.

Every command name, parameter name and value is checked: a typo, an unknown parameter or a value outside the allowed range fails the step with a message that lists what is available. Command names written as text in the script are checked before the script starts, so a misspelled command can't leave the image half-processed.

### Images

| Function              | Description                                                                                               |
| --------------------- | --------------------------------------------------------------------------------------------------------- |
| `image()`             | The step's current image.                                                                                 |
| `channel(index)`      | Channel `index` (0-based) of the raw image.                                                               |
| `set_image(image)`    | Makes `image` the step's current image, e.g. to continue from an image kept in a variable.               |
| `instance_count()`    | Number of distinct objects in the instance map, e.g. after `connected_components`.                        |
| `img.width`, `img.height` | Size of an image.                                                                                     |
| `img.mean()`, `img.min()`, `img.max()` | Mean, minimum and maximum pixel value of an image.                                       |

Images are values: keeping one in a variable is free, and a later command never changes an image a variable still holds. The segmentation and instance maps are not values - they belong to the step, as for any other pipeline step.

### Constants and output

The script sees the current tile as read-only constants: `image_width`, `image_height`, `tile_x`, `tile_y` (the tile's offset in the image) and `image_bits` (bit depth). `print(...)` writes to the log.

## Script editor

Click **Edit script** on the step card to open the editor:

- **Code area** with line numbers, syntax highlighting and a monospace font. **Tab** indents to the next multiple of four columns, **Enter** keeps the indentation (one level deeper after an opening bracket), and typing `}`, `)` or `]` on an empty line dedents.
- **Format** (or `Ctrl`+`Shift`+`F`) re-indents the whole script.
- **Command reference** - search the commands by name or key, see each command's parameters, and click **Insert at cursor** to insert a ready-to-edit `run("key", #{ … })` call with every parameter at its default value.
- **Syntax check** - below the editor, either **No syntax errors** or the first error with its line number.
- **Apply** writes the script to the step, **Cancel** discards the changes. Clicking outside the editor doesn't close it, so a stray click can't throw away an edited script.

## Limits

A script runs once per [tile](/fundamentals/cross-tile-merging/), so it can only run commands that work on a tile. The object commands (Classify Objects, AI Object Classifier, Colocalization, Object Math, Transform Objects, Voronoi, Load Annotated Objects) work on the whole image's objects and can't run inside a script - add them as regular steps after the script step. A script can't run another script.

Scripts run in a sandbox without file or network access. To keep a broken script from hanging an analysis (or a server), each run is limited to one million operations, 32 nested function calls, strings of 1 MB, arrays of 100,000 and maps of 10,000 entries. A script that exceeds a limit, doesn't parse or throws an error fails the step with the line and column of the problem.

## Citations

**Export → Cite project** ([Citation](/citation/#citing-the-algorithms-you-used)) cites a script step like the commands it runs: every command the script names in `run(...)` is cited, with its default settings - a command whose citation depends on a setting (such as the threshold method) is cited for its default.

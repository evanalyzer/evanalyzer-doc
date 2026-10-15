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

### Settings: `param`

A `param` line declares a value the script gets from the **step's settings** instead of from its code - so the same script can be used with other values without editing it:

```rust
param nuclei_channel: channel = 0;   // an image channel
param min_size = 20;                 // type from the value: a number
param use_watershed = true;          // a yes/no setting

let raw = channel(nuclei_channel);
// ...
```

Every `param` shows up as a setting on the step card, with its name and the default from the script. The step stores only values that differ from the default. In a [command group](/guide/command-groups/), a `param` can be exposed as a group parameter like any other setting.

| Type      | Value                         |
| --------- | ----------------------------- |
| `number`  | A whole number, e.g. `10`     |
| `decimal` | A decimal number, e.g. `2.5`  |
| `bool`    | `true` or `false`             |
| `text`    | A text, e.g. `"otsu"`         |
| `class`   | An object class (a number in the script) |
| `channel` | An image channel (a number in the script) |

Without `: type`, the type follows from the default. The default must be a plain value (a number, a decimal, `true`/`false` or a text), not an expression. Each name may be declared once and can't be one of the built-in constants below.

### Example: threshold series

This script thresholds the image at a series of values and turns each threshold into its own object class - class 1 for the objects above 100, class 2 for the objects above 200, and so on. The range of thresholds is set with `param`, so it can be changed on the step card without touching the code:

```rust
param start = 100;
param end = 1000;
param step = 100;

let raw = image();

let class = 1;

for th in range(start, end, step) {

    run("threshold", #{
            "thresholds.0.method": "Manual",
            "thresholds.0.min_threshold": th,
            "thresholds.0.max_threshold": 65535,
            "thresholds.0.unit": "bit",
            "thresholds.0.segmentation_class": class,
            "thresholds.0.value_source": "Actual Image",
    });
    run("connected_components", #{
            min_size: 0,
    });
    run("extract_objects", #{
            "class_mapping.0.segmentation_class": class,
            "class_mapping.0.object_class": class,
    });

    class = class + 1;
}
```

- `range(start, end, step)` stops **before** `end`, so with the defaults the loop runs for 100, 200, ..., 900 - nine thresholds, classes 1 to 9. Use `range(start, end + 1, step)` to include `end`.
- Each pass runs three commands with a parameter map `#{ ... }`. The list parameters `thresholds` and `class_mapping` are set through their first entry (`.0.`); keys that contain dots must be written in quotes, plain names like `min_size` don't need them.
- Every class the script uses (here 1 to 9) must be listed in the step's **Classes** parameter.

## Syntax reference

Scripts are written in [Rhai](https://rhai.rs). This section summarizes the parts of the language that are useful in a pipeline script; the complete description is the [Rhai language reference](https://rhai.rs/book/ref/index.html). Everything below is standard Rhai, except the functions listed under [Evanalyzer functions](#evanalyzer-functions).

### Comments and statements

```rust
// A comment to the end of the line
/* A block comment,
   over several lines */

let x = 1;          // statements end with a semicolon
{                   // a block groups statements and opens a new scope
    let y = x + 1;
}
```

The last statement of a block may omit the `;`, which makes it the block's value: `let a = { let t = 2; t * t };` sets `a` to `4`.

### Variables and constants

```rust
let size = 3;           // a variable, its type follows from the value
size = 5;               // can be changed later
let name;               // without a value it is () - "nothing"
const LIMIT = 100;      // a constant can't be changed
```

Names start with a letter or `_` and are case sensitive. Each `let` creates a new variable; a variable declared inside a block `{ }` only exists inside it. A variable can hold a value of any type, and the type may change on assignment.

### Value types

| Type          | Example                              | `type_of()`  | Notes                                                                     |
| ------------- | ------------------------------------ | ------------ | ------------------------------------------------------------------------- |
| Integer       | `42`, `-7`, `1_000_000`, `0xff`      | `"i64"`      | 64-bit whole number.                                                      |
| Decimal       | `3.14`, `1e-3`, `2.0`                | `"f64"`      | Floating-point number.                                                    |
| Boolean       | `true`, `false`                      | `"bool"`     |                                                                           |
| Text          | `"hello"`, `` `x = ${x}` ``          | `"string"`   | See [Texts](#texts).                                                      |
| Character     | `'a'`                                | `"char"`     | A single character.                                                       |
| Array         | `[1, 2, "three"]`                    | `"array"`    | See [Arrays](#arrays).                                                    |
| Object map    | `#{ a: 1, "b.c": 2 }`                | `"map"`      | See [Object maps](#object-maps).                                          |
| Range         | `0..10`, `0..=10`                    | `"range"`    | See [Loops](#loops).                                                      |
| Nothing       | `()`                                 | `"()"`       | The value of a variable without a value, or of a function without result. |
| Image         | `image()`                            |              | Evanalyzer image, see [Images](#images).                                  |

`type_of(x)` (or `x.type_of()`) returns the type name of a value.

:::caution[Integer and decimal numbers]
Integer and decimal numbers are different types. Dividing two integers gives an integer: `7 / 2` is `3`, while `7.0 / 2` is `3.5`. Use `to_float()` and `to_int()` to convert between them, e.g. `size.to_float() / 2`.
:::

### Operators

| Operator                         | Description                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------- |
| `+` `-` `*` `/`                  | Add, subtract, multiply, divide (integer division for two integers).         |
| `%`                              | Remainder, e.g. `7 % 3` is `1`.                                              |
| `**`                             | Power, e.g. `2 ** 10` is `1024`.                                             |
| `==` `!=` `<` `<=` `>` `>=`      | Comparison, gives `true` or `false`.                                         |
| `&&` `\|\|` `!`                  | Logical and, or, not. `&&` and `\|\|` stop as soon as the result is clear.   |
| `&` `\|` `^` `<<` `>>`           | Bitwise and, or, xor, shift (integers).                                      |
| `in`                             | Contained in, e.g. `x in 0..10`, `"a" in "abc"`, `3 in [1, 2, 3]`, `"key" in map`. |
| `=` `+=` `-=` `*=` `/=` `%=` `**=` | Assignment and compound assignment, e.g. `class += 1`.                     |
| `??`                             | `a ?? b` is `a`, or `b` if `a` is `()`.                                      |
| `?.` `?[ ]`                      | Property or index access that gives `()` instead of an error when the value is `()`. |

`++` and `--` don't exist in Rhai - write `x += 1`.

### Conditions

```rust
if count > 100 {
    print("many");
} else if count > 10 {
    print("some");
} else {
    print("few");
}

// if is also an expression: its value is the value of the branch taken
let radius = if count > 100 { 2 } else { 4 };
```

The condition must be a `true`/`false` value - a number is not accepted as a condition. The braces are always required.

`switch` compares a value against a list of cases; `_` is the default case and must come last:

```rust
let method = switch image_bits {
    8 => "otsu",
    12 | 16 => "triangle",          // several values
    0..8 => "manual",               // a range of numbers
    _ => "li"
};
```

A case can have an extra condition: `16 if dim => "li",`.

### Loops

```rust
for i in 0..5 { }                   // 0, 1, 2, 3, 4 (end excluded)
for i in 0..=5 { }                  // 0, 1, 2, 3, 4, 5 (end included)
for i in range(0, 50, 10) { }       // 0, 10, 20, 30, 40 (with a step)
for i in range(50, 0, -10) { }      // 50, 40, 30, 20, 10 (counting down)
for s in range(0.5, 2.0, 0.5) { }   // 0.5, 1.0, 1.5 (decimal steps)
for x in [3, 5, 7] { }              // the entries of an array
for (x, i) in [3, 5, 7] { }         // entry and its index 0, 1, 2

while value < 100 { value *= 2; }   // repeats while the condition is true
do { value *= 2; } while value < 100;   // runs at least once
loop { if done() { break; } }       // repeats until break
```

`break` leaves the loop, `continue` skips to the next pass. The loop variable of a `for` loop only exists inside the loop.

### Functions

```rust
fn area(w, h) {
    w * h               // the last expression is the result
}

fn clamp_size(s) {
    if s < 3 { return 3; }
    s
}

let a = area(image_width, image_height);
let k = 5.clamp_size();             // method syntax: same as clamp_size(5)
```

A function sees only its parameters - not the variables of the script around it, so pass everything it needs as a parameter. Parameters are passed as copies, so a function can't change a variable of its caller. Functions must be defined at the top level of the script, not inside a block or loop, and can be used before their definition. Functions with the same name but a different number of parameters are separate functions.

Anonymous functions (closures) are written `|x| x * 2` and called with `.call(...)`, e.g. `let double = |x| x * 2; double.call(4)`. They are mostly used with array methods such as `filter` and `map`.

### Texts

```rust
let name = "nuclei";
let msg = `found ${instance_count()} ${name}`;  // back-ticks: ${...} is replaced by the value
let path = "a" + "b" + 1;                       // "ab1" - + joins texts and other values
let lines = "multi\nline";                      // \n, \t, \", \\ escapes
```

| Function                         | Description                                                    |
| -------------------------------- | -------------------------------------------------------------- |
| `s.len`                          | Number of characters.                                          |
| `s.to_upper()`, `s.to_lower()`   | Upper / lower case copy.                                       |
| `s.trim()`                       | Removes leading and trailing whitespace (changes `s`).         |
| `s.contains(t)`, `t in s`        | Does `s` contain `t`?                                          |
| `s.starts_with(t)`, `s.ends_with(t)` | Does `s` start / end with `t`?                             |
| `s.index_of(t)`                  | Position of `t` in `s`, or `-1`.                               |
| `s.sub_string(start, len)`       | Part of the text.                                              |
| `s.split(t)`                     | Array of the parts between occurrences of `t`.                 |
| `s.replace(a, b)`                | Replaces every `a` with `b` (changes `s`).                     |
| `s.parse_int()`, `s.parse_float()` | Text to number, e.g. `"42".parse_int()`.                     |
| `x.to_string()`                  | Any value as text.                                             |

### Arrays

```rust
let sizes = [3, 5, 7];
sizes[0];               // 3 - the first entry
sizes[-1];              // 7 - negative indices count from the end
sizes[1] = 6;           // change an entry
sizes.push(9);          // add at the end
sizes += [11, 13];      // append another array
```

| Function                          | Description                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| `a.len`                           | Number of entries.                                              |
| `a.push(x)`, `a.pop()`            | Add an entry at the end / remove and return the last one.       |
| `a.insert(i, x)`, `a.remove(i)`   | Insert at / remove from position `i`.                           |
| `a.contains(x)`, `x in a`         | Is `x` in the array?                                            |
| `a.index_of(x)`                   | Position of `x`, or `-1`.                                       |
| `a.sort()`, `a.reverse()`         | Sorts / reverses the array in place.                            |
| `a.extract(start, len)`           | Copy of a part of the array.                                    |
| `a.filter(\|x\| x > 5)`           | Array of the entries for which the function returns `true`.     |
| `a.map(\|x\| x * 2)`              | Array of the function results.                                  |
| `a.reduce(\|sum, x\| sum + x, 0)` | Combines all entries into one value, e.g. a sum.                |
| `a.some(\|x\| ...)`, `a.all(\|x\| ...)` | Does any / every entry fulfill the condition?             |

Arrays can hold images, e.g. to keep the result of each pass of a loop: `let results = []; ... results.push(run("gaussian_blur", raw, #{ kernel_size: k }));`.

### Object maps

An object map is a list of named values. It is the format of the parameters passed to `run`:

```rust
let p = #{ kernel_size: 3, "thresholds.0.method": "otsu" };
p.kernel_size;                  // 3 - access by name
p["thresholds.0.method"];       // names with special characters need quotes and [ ]
p.kernel_size = 5;              // change a value
p.sigma = 1.5;                  // add a value
p.missing;                      // () - a missing name gives () instead of an error

run("gaussian_blur", p);
```

| Function                        | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| `m.len`                         | Number of entries.                                  |
| `m.keys()`, `m.values()`        | Array of the names / values.                        |
| `"name" in m`, `m.contains("name")` | Does the map have an entry `name`?              |
| `m.remove("name")`              | Removes an entry and returns its value.             |
| `m.mixin(other)`, `m += other`  | Adds (or overwrites) the entries of another map.    |

`m += other` is handy to build parameters from a common base: `let base = #{ ... }; run("threshold", base + #{ "thresholds.0.min_threshold": th });`.

### Numbers

| Function                                   | Description                                                   |
| ------------------------------------------ | ------------------------------------------------------------- |
| `x.abs()`, `x.sign()`                      | Absolute value, sign (`-1`, `0` or `1`).                      |
| `min(a, b)`, `max(a, b)`                   | Smaller / larger of two numbers.                              |
| `x.floor()`, `x.ceiling()`, `x.round()`    | Rounds a decimal down / up / to the nearest (stays a decimal). |
| `x.to_int()`, `x.to_float()`               | Converts between integer and decimal (`to_int` cuts off the decimals). |
| `x.sqrt()`, `x.exp()`, `x.ln()`, `x.log()` | Square root, e<sup>x</sup>, natural and base-10 logarithm.    |
| `x.sin()`, `x.cos()`, `x.tan()`, ...       | Trigonometric functions (radians).                            |
| `PI()`, `E()`                              | π and e.                                                      |
| `x.is_even`, `x.is_odd`, `x.is_zero`       | Properties of an integer.                                     |
| `x.is_nan`, `x.is_finite`                  | Properties of a decimal.                                      |

### Errors

`throw` stops the script with a message, which fails the step and shows the message:

```rust
if instance_count() == 0 {
    throw "no objects found - check the threshold";
}
```

`try { ... } catch (err) { ... }` catches an error - also an error from a command run by `run` - and continues with the `catch` block:

```rust
try {
    run("stardist");
} catch (err) {
    print(`stardist failed: ${err}, falling back to threshold`);
    run("threshold", #{ "thresholds.0.method": "otsu" });
}
```

### Evanalyzer functions

These functions and keywords are added by Evanalyzer and are not part of standard Rhai:

| Function / keyword                       | Description                                                      | Details                                   |
| ---------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| `param name [: type] = value;`           | A value that is set on the step card.                            | [Settings: `param`](#settings-param)      |
| `run("command" [, image] [, #{ params }])` | Runs a pipeline command, returns the resulting image.          | [Running commands](#running-commands)     |
| `image()`                                | The step's current image.                                        | [Images](#images)                         |
| `channel(index)`                         | A channel of the raw image.                                      | [Images](#images)                         |
| `set_image(image)`                       | Makes an image the step's current image.                         | [Images](#images)                         |
| `instance_count()`                       | Number of objects in the instance map.                           | [Images](#images)                         |
| `img.width`, `img.height`                | Size of an image.                                                | [Images](#images)                         |
| `img.mean()`, `img.min()`, `img.max()`   | Pixel statistics of an image.                                    | [Images](#images)                         |
| `image_width`, `image_height`, `tile_x`, `tile_y`, `image_bits` | Read-only constants describing the current tile. | [Constants and output](#constants-and-output) |
| `print(...)`                             | Writes to the log.                                               | [Constants and output](#constants-and-output) |

Modules (`import`) and `eval` are not useful in a pipeline script: scripts have no file access, and every script must be complete in the step's **Source**.

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

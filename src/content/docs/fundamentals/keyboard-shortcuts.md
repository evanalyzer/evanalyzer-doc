---
title: Keyboard Shortcuts
description: Every keyboard shortcut in EVAnalyzer, grouped by context.
---

Press **F1**, or choose **EVA › Help › Shortcuts**, to open this same reference inside the app at any time.

## File

| Shortcut       | Action                |
| -------------- | --------------------- |
| `Ctrl+S`       | Save                  |
| `Ctrl+Shift+S` | Save As               |
| `Ctrl+O`       | Open                  |
| `Ctrl+Shift+O` | Open an images folder |

## Edit

| Shortcut                  | Action                         |
| ------------------------- | ------------------------------ |
| `Ctrl+Z`                  | Undo                           |
| `Ctrl+Y` / `Ctrl+Shift+Z` | Redo                           |
| `Delete`                  | Delete the selected object/ROI |

`Delete` opens the same confirmation as **Delete object** in the [Objects](/guide/classification/#managing-objects) panel, rather than deleting immediately. With no object selected, it removes the selected step instead (see below).

Every brush stroke and every drawn shape is an undo step of its own.

## Pipeline

| Shortcut          | Action                                             |
| ----------------- | -------------------------------------------------- |
| `F5`              | Refresh the preview                                |
| `F`               | Focus on the selected pipeline (again: show all)   |
| `Alt`+click       | Focus on a pipeline (again: show all)              |
| Double-click      | Edit a pipeline's name and image source            |
| `Enter`           | The selected step's settings                       |
| `Ctrl+/`          | Disable / enable the selected step                 |
| `F9`              | Breakpoint on the selected step                    |
| `Ctrl+D`          | Duplicate the selected step                        |
| `Alt+↑` / `Alt+↓` | Move the selected step                             |
| `Delete`          | Remove the selected step (no object selected)      |

`F5` re-runs the pipeline preview once - the same as **Refresh preview** in the top bar - a single dry-run, distinct from switching **Auto preview** on or off.

`F` and `Alt`+click are the quick way into [Focus Mode](/guide/pipelines/#focus-mode): they show only the channel and classes of one pipeline. Plain `F` is used because `Ctrl+F` is the image search.

`F9` steps through the [breakpoint](/guide/pipelines/#breakpoints) states: stop, snapshot, off.

**Number fields** also take `↑` / `↓`, `Ctrl` + mouse wheel, and a sideways drag over the number.

## Canvas tools

| Shortcut       | Action            |
| -------------- | ----------------- |
| `M` / `Escape` | Move              |
| `S`            | Select            |
| `K`            | Paint marker      |
| `R`            | Paint rectangle   |
| `E`            | Paint ellipse     |
| `P`            | Paint polygon     |
| `O`            | Show / hide the objects |
| `A`            | Show / hide the annotate tool bar |

These are unmodified single-letter mnemonics, so they only fire when the image (not a text field) has keyboard focus - typing into a search box or name field types the letter normally instead of switching tools.

While [comparing](/guide/pipelines/#compare-with-the-original) a breakpoint image with the original, hold `Space` to see the whole original.

## Z stack and time series

| Shortcut                | Action                      |
| ----------------------- | --------------------------- |
| `Page Up` / `Page Down` | The previous / next Z slice |
| `,` / `.`               | The previous / next frame   |

## Navigation

| Shortcut | Action                                              |
| -------- | --------------------------------------------------- |
| `Ctrl+K` | Command palette: find an action, a step, a command  |
| `Ctrl+1` | Images                                              |
| `Ctrl+2` | Pipelines                                           |
| `Ctrl+3` | Results                                             |
| `Ctrl+F` | Jump to the image search field                      |
| `Tab`    | Hide / show all panels (nothing focused)            |
| `Alt+1`…`4` | Show / hide Steps, Classes, Image, Objects       |

`Ctrl+1`..`3` switch the [modes](/guide/workspace/#bottom-bar-and-modes) in the bottom bar, `Alt+1`..`4` the [panels](/guide/workspace/#view) (also in **EVA › View**). `Tab` hides all panels only while no field or button has the keyboard focus - there it still moves the focus. `Ctrl+F` switches to Images first if it isn't already active, then focuses its search field.

In the [command palette](/guide/workspace/#command-palette), `↑` / `↓` choose, `Enter` runs and `Escape` closes.

## Results, split with the image

| Shortcut  | Action                       |
| --------- | ---------------------------- |
| `↑` / `↓` | The previous / next object   |
| `Escape`  | Clear the selected object    |

See [Split with the image](/guide/results/#split-with-the-image).

## Dialogs

| Shortcut | Action                |
| -------- | --------------------- |
| `Escape` | Close the open dialog |
| `F1`     | Show this help        |

Dialogs don't block the window, so `Escape` closes the open dialog even after you clicked into the image. In a dialog that edits something - like the module settings - `Escape` works like **Cancel** and undoes the changes made while it was open.

Otherwise `Tab` moves between buttons, switches, list rows and steps; `Space` or `Enter` presses the focused one. The focus ring only shows when you use the keyboard.

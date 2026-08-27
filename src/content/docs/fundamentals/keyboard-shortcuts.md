---
title: Keyboard Shortcuts
description: Every keyboard shortcut in EVAnalyzer, grouped by context.
---

Press **F1**, or go to **Help → Shortcuts** in the menu bar, to open this same reference inside the app at any time.

## File

| Shortcut       | Action  |
| -------------- | ------- |
| `Ctrl+S`       | Save    |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+O`       | Open    |

## Edit

| Shortcut               | Action                         |
| ----------------------- | ------------------------------- |
| `Ctrl+Z`                | Undo                            |
| `Ctrl+Y` / `Ctrl+Shift+Z` | Redo                          |
| `Delete`                | Delete the selected object/ROI |

`Delete` opens the same confirmation dialog as the trash-can button in the [Object List](/guide/classification/#managing-objects) panel's footer, rather than deleting immediately, and only does anything while an object is actually selected.

## Pipeline

| Shortcut | Action              |
| -------- | -------------------- |
| `F5`     | Refresh the preview  |

Re-runs the pipeline preview once - the same as the toolbar's "eye" button or the Pipelines panel's **Preview** action - a single dry-run, distinct from toggling Auto Preview on or off.

## Canvas Tools

| Shortcut     | Action              |
| ------------- | -------------------- |
| `M` / `Escape` | Move                |
| `S`           | Select              |
| `K`           | Paint marker        |
| `R`           | Paint rectangle     |
| `O`           | Paint oval          |
| `P`           | Paint polygon       |
| `#`           | Show/Hide objects   |

These are unmodified single-letter mnemonics, so they only fire when the viewport (not a text field) has keyboard focus - typing into a search box or name field types the letter normally instead of switching tools.

## Navigation

| Shortcut | Action                          |
| -------- | -------------------------------- |
| `Ctrl+1` | Images tab                       |
| `Ctrl+2` | Meta tab                         |
| `Ctrl+3` | Pipelines tab                    |
| `Ctrl+4` | Results tab                      |
| `Ctrl+F` | Jump to the image search field   |

`Ctrl+1`..`4` follows the same convention as switching between browser tabs. `Ctrl+F` switches to the Images tab first if it isn't already active, then focuses its search field.

## Dialogs

| Shortcut | Action                |
| -------- | ---------------------- |
| `Escape` | Close the open dialog  |
| `F1`     | Show this help         |

`Escape` is deliberately disabled while a pipeline analysis or preview render is actively running: since cancelling a background job only *requests* cancellation rather than closing the dialog immediately, a reflexive Escape there would look like it silently did nothing while killing a possibly multi-minute run. Use the dialog's own **Cancel** button instead - the distinction is intentional.

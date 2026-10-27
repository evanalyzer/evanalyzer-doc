---
title: The Workspace
description: The EVAnalyzer window - the image first, panels floating over it, the EVA menu, the three modes and the command palette.
---

EVAnalyzer keeps the image in the middle of everything. The window has a **top bar**, a **bottom bar**, and between them the image. The panels float over the image instead of sitting beside it, so the image always gets the whole window.

![Top bar, steps panel on the left, Classes / Objects / Image panels on the right, the bottom bar with Images · Pipelines · Results. Light colors](../../../assets/screenshots/screenshot-workspace.png)

## Start page

As long as no project is open - when EVAnalyzer starts, and after **EVA › New** - the **Start** page fills the window:

| Action | What it does |
| --- | --- |
| **Select image folder…** (`Ctrl+Shift+O`) | The main way in: a new project for the images of a folder. Save it when you like. |
| **Open image…** (`Ctrl+I`) <span class="evx-new">NEW</span> | One image file, opened right away - the other images of its folder are listed too. |
| **Open project…** (`Ctrl+O`) | An `.evaproj` file - its images, pipelines and results. |
| **Empty project** | No images yet - to look at a pipeline or build a simple one. The **Images** tab of the bottom bar does the same. |

Below them, **New project from a template…** starts from the classes, plate settings and pipelines of a [project template](/guide/pipelines/#saving-a-project-as-a-template), and **Connect to a server…** works on a server with [remote control](/remote/remote-control/).

**Recent projects** lists up to 12 projects you opened or saved, with their path, the number of images and pipelines and when you last used them. A project that has moved shows **Locate…**; the **✕** takes it off the list, **Clear list** empties it. Tick **Open the last project when EVAnalyzer starts** to skip the Start page.

Whatever you open - images, a project, an empty project or a template - EVAnalyzer continues in **Images**.

![The four actions, Connect to a server…, and a few recent projects - cells drifting in the background](../../../assets/screenshots/screenshot-start-page.png)

## Top bar

From left to right:

- **EVA** - the [EVA menu](#the-eva-menu).
- **Undo**, **Redo**, **Save**, **Annotate** (switches the [annotate bar](/guide/images/#annotating-the-image) on and off, `A`) and **AI training…** (opens [AI training](/ai/training/), which learns from the annotations).
- The **image chip** - the image shown; click it to [go to another image](/guide/images/#go-to-image) by typing part of its name. For files with several series, **Series 2 of 5 ▾** beside it picks the [series](/guide/images/#series-selection).
- The project's name in the middle.
- **Compare** (only with a [breakpoint image](/guide/pipelines/#breakpoints)), then the preview in one group - **Refresh preview** (`F5`), **Preview the whole image** (`Shift+F5`, see [Live preview](/guide/pipelines/#live-preview)) and **Auto preview** - and **Run**. While an analysis runs, **Auto preview** and **Run** give way to its progress - see [Working while an analysis runs](#working-while-an-analysis-runs).
- **Hide all panels** / **Show the panels** at the right end.

In **Results** the top bar holds the results' controls instead - the analysis, the [views](/guide/results/#views) as tabs, **Full | Split with image** and **Export…** - see [Results](/guide/results/#the-results-bar).

## The EVA menu

Everything that used to be in the menu bar is in the **EVA** menu at the top left:

| Section | Items |
| --- | --- |
| **Project** | **New**, **Open…** (`Ctrl+O`), **Open recent ›**, **New from template…**, **Select image folder…** (`Ctrl+Shift+O`), **Save** (`Ctrl+S`), **Save as…**, **Save as template…**, **Project settings…**, **Cite project**, **View ›** |
| **Tools** | **AI training…**, **Debug mode**, **Connect to server…** (and **Disconnect** while connected) |
| | **Help ›** (**Shortcuts** `F1`, **evanalyzer.org**), **About** |

**Open…** opens a project (`.evaproj`), a project template (`.evatemplate`), an image, or a module file (`.evamodule`). A module file is copied into the project's modules, as from the [module library](/guide/modules/#module-library) - **Module added** then says how to use it: in a pipeline with **Add step › Modules**.

![The EVA menu: Project, Open recent, View, Tools, Help and About](../../../assets/screenshots/screenshot-eva-menu.png)

## The file dialog

EVAnalyzer opens and saves every file through its own file dialog - the same on every system, and on a server it lists the server's folders (see [Remote Control](/remote/remote-control/)).

On the left, **Places** lists, above **Home** and the drives:

- **Project** - the folder of the open project file (once it is saved),
- **Images** - the project's image folder, when it is somewhere else,
- **Templates** - the `templates` folder of [EVAnalyzer's folder](/guide/settings/#where-evanalyzer-stores-its-data), if it exists.

Below them come your own places <span class="evx-new">NEW</span>: **Add this folder** at the bottom of the list adds the folder shown; the **×** that appears when you point at one of them takes it off again. Your places are kept in the app settings (on a server, in the server's settings).

A dialog that doesn't open in a folder of its own starts in the last folder chosen for this project - else the project's folder, the image folder or Home. Drives and network folders can take a few seconds to list; a spinner shows while the places or a folder load.

<div class="evx-shot-todo">
<strong>File dialog with places</strong>
<span>The file dialog with Project, Images, Templates and a folder of your own under Places, the pointer on it showing its ×, "Add this folder" at the bottom.</span>
<code>src/assets/screenshots/screenshot-file-dialog.png</code>
</div>

### View

**EVA › View ›** decides what the workspace shows:

| Item | Key | What it does |
| --- | --- | --- |
| **Steps** (or **Images**), **Classes**, **Image**, **Objects**, **Measurements** | `Alt+1` … `Alt+5` | Show or hide that panel. |
| **Hide all panels** / **Show the panels** | `Tab` | Only the image - again: the panels come back. `Tab` does this while no field or button has the keyboard. |
| **Step values on a second line** | | A step's values below its name instead of beside it. |
| **Navigator** | | **Auto** (only zoomed in), **Always** or **Never**. |
| **Colors** | | **Light**, **Dark** or **Dim** - see [Colors](#colors). |

![EVA › View: the panels with Alt+1…4, Hide all panels (Tab), Step values on a second line, Navigator and Colors](../../../assets/screenshots/screenshot-eva-view.png)

## Bottom bar and modes

The bottom bar switches between the three modes of the window - **Images**, **Pipelines** and **Results** (`Ctrl+1`, `Ctrl+2`, `Ctrl+3`) - and shows the state of what you are doing: the cursor position and pixel value, the number of objects, the zoom, an analysis' progress, and where you work (**This computer** or the server's name, see [Remote Control](/remote/remote-control/)).

| Mode | Left | Right |
| --- | --- | --- |
| **Images** | The [images](/guide/images/) - as a list or as a plate | Classes, objects, image controls |
| **Pipelines** | The [steps](/guide/pipelines/) of the shown pipeline | Classes, objects, image controls |
| **Results** | The [results](/guide/results/) fill the window - or share it with the image | |

Switching modes keeps the image's zoom and position. The bottom bar also reminds you of the panel tricks: _Click a panel's title to fold it · Tab hides all panels · O objects on/off_.

## Floating panels

The panels float over the image and only take the room they need; the image shows through around them. Click a panel's title to fold it to its head, `Alt+1` … `Alt+5` show and hide them one by one, and `Tab` hides them all. Which panels are folded or hidden is remembered.

- **Classes** - the project's [classes](/guide/classification/).
- **Objects** - the objects of the image, as a list or as a [table](/guide/classification/#objects-as-a-table).
- **Image** - channels, overlay, [histogram](/guide/images/#histogram), Z and T, and the [navigator](/guide/images/#navigator).
- **Measurements** <span class="evx-new">NEW</span> - the values the preview's [measurement steps](/guide/pipelines/#measurement-steps) measured. Shown only when a pipeline or module has a measurement step.

Dialogs open where they belong - step settings next to the steps, class settings left of the right-hand panels, Settings as a sheet on the right. They don't block the window: the image, the panels and the shortcuts stay usable, and every dialog can be moved by its head. `Esc` closes the open one.

## Command palette

Press `Ctrl+K` (or the **Ctrl K** button in the steps panel's head) to find anything by typing: an action, a step of the pipeline, a setting, a command to add, an image or a class. A setting is found by its name - _"min"_ shows **Min Size · #8 ClassifyObjects · 5** - and opens its step. `↑` `↓` choose, `Enter` runs, `Esc` closes.

![The command palette with min typed: steps, settings such as Min Size of step 8 ClassifyObjects, and commands to add](../../../assets/screenshots/screenshot-command-palette.png)

## Colors

EVAnalyzer has three color schemes, picked under **EVA › View › Colors**:

- **Light** - white panels on a light grey ground.
- **Dark** - near-black panels; the image behind them is black.
- **Dim** - a softer dark grey, for long sessions in a dark room.

In every scheme the image's background stays black, so fluorescence reads the same. Buttons are black (white in the dark schemes); one indigo marks focus and the selected row. The colors of channels and classes come with your data and are never changed by the scheme.

![Light, Dark and Dim: colors light](../../../assets/screenshots/screenshot-colors-light.png)

![Light, Dark and Dim: colors dark](../../../assets/screenshots/screenshot-colors-dark.png)

![Light, Dark and Dim: colors dim](../../../assets/screenshots/screenshot-colors-dim.png)

## Working while an analysis runs

An analysis no longer locks the window. While it runs, **Run** in the top bar turns into its progress - **Analyzing ▬ 12 / 48 · ~2 s** and **Stop** - and the bottom bar names the image in work - the one started first, with the number of others running beside it (_"Analyzing · A03_01.tif (+3) · image 12 / 48"_). You can keep looking at images meanwhile.

Every run starts with the steps locked: the steps panel says **Steps are locked while the analysis runs.**, the settings can't be changed and no preview runs, so the analysis has the computer's memory to itself. **Unlock** in that strip lets you edit and preview anyway - _"The run uses a snapshot. Edits apply to the next run."_ - and **Lock** locks them again. When the analysis ends - finished, stopped or failed - the steps unlock by themselves and, with **Auto preview** on, the image shown is previewed again. Switching to another project asks first.

When it is done, **Analysis finished · 48 images** appears over the image, with **Open results**.

![Analysis finished · 48 images, with Open results, over the image](../../../assets/screenshots/screenshot-analysis-finished.png)

![The top bar while an analysis runs: Analyzing, the progress, 12 / 48 images, about 2 s left, and Stop](../../../assets/screenshots/screenshot-analysis-running.png)

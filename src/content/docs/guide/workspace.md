---
title: The Workspace
description: The EVAnalyzer window - the image first, panels floating over it, the EVA menu, the three modes and the command palette.
---

EVAnalyzer keeps the image in the middle of everything. The window has a **top bar**, a **bottom bar**, and between them the image. The panels float over the image instead of sitting beside it, so the image always gets the whole window.

<div class="evx-shot-todo" data-kind="new">
<strong>The whole workspace, Pipelines mode</strong>
<span>Top bar, steps panel on the left, Classes / Objects / Image panels on the right, the bottom bar with Images · Pipelines · Results. Light colors.</span>
<code>src/assets/screenshots/screenshot-workspace.png</code>
</div>

## Start page

As long as no project is open - when EVAnalyzer starts, and after **EVA › New** - the **Start** page fills the window:

| Action | What it does |
| --- | --- |
| **Open image folder…** (`Ctrl+Shift+O`) | The main way in: a new project for the images of a folder. Save it when you like. |
| **Open project…** (`Ctrl+O`) | An `.evaproj` file - its images, pipelines and results. |
| **Empty project** | No images yet - to look at a pipeline or build a simple one. |
| **New project from a template…** | Classes, plate settings and pipelines of a [project template](/guide/pipelines/#saving-a-project-as-a-template). |
| **Connect to a server…** | Work on a server with [remote control](/remote/remote-control/). |

**Recent projects** lists up to 12 projects you opened or saved, with their path, the number of images and pipelines and when you last used them. A project that has moved shows **Locate…**; the **✕** takes it off the list, **Clear list** empties it. Tick **Open the last project when EVAnalyzer starts** to skip the Start page.

After opening images or a project, EVAnalyzer continues in **Images**; after an empty project or a template, in **Pipelines**.

<div class="evx-shot-todo" data-kind="new">
<strong>Start page</strong>
<span>The four actions, Connect to a server…, and a few recent projects - cells drifting in the background.</span>
<code>src/assets/screenshots/screenshot-start-page.png</code>
</div>

## Top bar

From left to right:

- **EVA** - the [EVA menu](#the-eva-menu).
- **Undo**, **Redo**, **Save**, **Refresh preview** and **Annotate** (switches [annotate mode](/guide/images/#annotating-the-image) on and off).
- The **image chip** - the image shown, and for files with several series **Series 2 of 5 ▾** to pick the [series](/guide/images/#series-selection).
- The project's name in the middle.
- **Compare** (only with a [breakpoint image](/guide/pipelines/#breakpoints)), **Debug mode**, **Auto preview** and **Run**.

In **Results** the top bar holds the results' controls instead - see [Results](/guide/results/).

## The EVA menu

Everything that used to be in the menu bar is in the **EVA** menu at the top left:

| Section | Items |
| --- | --- |
| **Project** | **New**, **Open…** (`Ctrl+O`), **New from template…**, **Open images folder…** (`Ctrl+Shift+O`), the recent projects, **Save** (`Ctrl+S`), **Save as…**, **Save as template…**, **Project settings…**, **Cite project** |
| **Tools** | **AI training…**, **Debug mode**, **Connect to server…**, **Disconnect** |
| **Colors** | **Light**, **Dark** or **Dim** - see [Colors](#colors) |
| | **Shortcuts** (`F1`), **evanalyzer.org**, **About** |

## Bottom bar and modes

The bottom bar switches between the three modes of the window - **Images**, **Pipelines** and **Results** (`Ctrl+1`, `Ctrl+2`, `Ctrl+3`) - and shows the state of what you are doing: the cursor position and pixel value, the number of objects, the zoom, an analysis' progress, and where you work (**This computer** or the server's name, see [Remote Control](/remote/remote-control/)).

| Mode | Left | Right |
| --- | --- | --- |
| **Images** | The [images](/guide/images/) - as a list or as a plate | Classes, objects, image controls |
| **Pipelines** | The [steps](/guide/pipelines/) of the shown pipeline | Classes, objects, image controls |
| **Results** | The [results](/guide/results/) fill the window - or share it with the image | |

Switching modes keeps the image's zoom and position.

## Floating panels

The panels on the right - **Classes**, **Objects** and **Image** - are switched on and off by the three buttons above them. Each one only takes the room it needs; the image shows through around them.

- **Classes** - the project's [classes](/guide/classification/).
- **Objects** - the objects of the image, as a list or as a [table](/guide/classification/#objects-as-a-table).
- **Image** - channels, overlay, [histogram](/guide/images/#histogram), Z and T, and the [navigator](/guide/images/#navigator).

Dialogs open where they belong - step settings next to the steps, class settings left of the right-hand panels, Settings as a sheet on the right. They don't block the window: the image, the panels and the shortcuts stay usable, and every dialog can be moved by its head. `Esc` closes the open one.

## Command palette

Press `Ctrl+K` (or the **Ctrl K** button in the steps panel's head) to find anything by typing: an action, a step of the pipeline, a setting, a command to add, an image or a class. A setting is found by its name - _"min threshold"_ shows **Min threshold · #3 Threshold · 240** - and opens its step. `↑` `↓` choose, `Enter` runs, `Esc` closes.

<div class="evx-shot-todo" data-kind="new">
<strong>Command palette</strong>
<span>Ctrl+K open over the workspace, typed "thresh" - actions, a step, a setting and commands in the results.</span>
<code>src/assets/screenshots/screenshot-command-palette.png</code>
</div>

## Colors

EVAnalyzer has three color schemes, picked in the **EVA** menu under **Colors**:

- **Light** - white panels on a light grey ground.
- **Dark** - near-black panels; the image behind them is black.
- **Dim** - a softer dark grey, for long sessions in a dark room.

In every scheme the image's background stays black, so fluorescence reads the same. Buttons are black (white in the dark schemes); one indigo marks focus and the selected row. The colors of channels and classes come with your data and are never changed by the scheme.

<div class="evx-shot-todo" data-kind="new">
<strong>Light, Dark and Dim</strong>
<span>The same workspace in the three color schemes, side by side (or three screenshots for a compare slider).</span>
<code>src/assets/screenshots/screenshot-colors-light.png · -dark.png · -dim.png</code>
</div>

## Working while an analysis runs

An analysis no longer locks the window. While it runs, its progress is shown in a card at the bottom right, and you can keep editing pipelines and previewing images. Switching to another project asks first.

On a computer that needs all its memory for the analysis, switch this off in **EVA › Project settings… › Viewport › Edit while an analysis runs**: the window then waits until the analysis is done.

<div class="evx-shot-todo" data-kind="new">
<strong>Analysis running while editing</strong>
<span>The progress card at the bottom right, the steps panel still open and editable.</span>
<code>src/assets/screenshots/screenshot-analysis-running.png</code>
</div>

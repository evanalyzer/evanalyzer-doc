---
title: Settings
description: Project settings and the viewer's memory settings for this computer.
---

Open **File › Settings…** to change the settings of the open project and of EVAnalyzer on this computer. Use **Search settings** to find a setting by name, e.g. _"plate"_, _"merge"_ or _"memory"_.

**Project settings are saved with the project; viewport settings on this computer.** **Apply** saves the changes, **Cancel** discards them, and **Reset to defaults** sets the shown section back to its defaults.

## Project

### General

| Setting          | Description                     |
| ---------------- | ------------------------------- |
| **Project name** | Name of the project.            |
| **Author**       | Who created the project.        |
| **Organization** | University, institute, company. |

### Plate & grouping

How images are grouped into wells and how the plate and the wells are laid out - **Grouping**, **Regex**, **Plate size**, **Well size** (**Rows** / **Columns**) and **Images in well**. These are the same settings as in the results window's [Plate view](/guide/results/#grouping-images-into-wells); see there for what they mean.

### Object merging

The settings of [cross-tile object merging](/fundamentals/cross-tile-merging/#settings): **Merge objects across tiles**, **Exclude classes**, **Connectivity** and **Max fragments per group**.

## This computer

### Viewport

Memory settings of the image viewer. They matter most for large and whole slide images; the defaults suit most computers.

| Setting                                  | Description                                                                                                                                                                                               |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Keep earlier high-resolution renders** | Panning back or zooming shows the sharp earlier renders instead of the blurry overview - most useful for whole slide images. Off: only the current render and one overview are kept (least RAM).          |
| **Memory for earlier renders**           | In MB. The graphics card holds about as much again.                                                                                                                                                       |
| **Object overlay margin**                | In pixels: how far objects are drawn past the visible area, so panning doesn't uncover an empty border. 0 uses the least RAM; objects at a newly uncovered edge then appear once you stop moving.         |
| **Size caches automatically**            | Sizes the tile and overview caches from this computer's RAM. Off: use the sizes below.                                                                                                                    |
| **Tile cache**                           | In MB: image tiles kept after reading, so panning back or returning to an image doesn't read them from disk again.                                                                                        |
| **Overview cache**                       | In MB: whole-image overviews kept, so switching between images shows them at once.                                                                                                                        |
| **Free caches when an analysis starts**  | Gives a local analysis the RAM of both caches; they fill up again as you use the viewport.                                                                                                                |

---
title: Results
description: Viewing, exploring, and exporting analysis results - as a list, on a plate, in charts, or beside the image.
---

EVAnalyzer stores results in a DuckDB database file named `results.evadb`:

```
<image_directory>/evanalyzer/<job_name>/results.evadb
```

Results are a mode of the main window: switch to **Results** in the bottom bar (`Ctrl+3`).

## The results bar

In Results, the top bar holds the results' controls:

- **List | Plate | Charts** - the [three views](#list-view).
- **Analysis ▾** - the analysis shown, picked from every analysis of the project's images (**ANALYSES · N**). With none open, Results lists them to pick one; with none at all: _"None yet - Run writes one"_.
- Inside a well, a breadcrumb **Plate › Well C3 › image** to go back up.
- **Full | Split with image** - the results alone, or [beside the image](#split-with-the-image).
- **Export…**, **Refresh** and **Show the output folder**, and on the right a **Z/T** stepper when the data has Z-stacks or time-lapse frames - it applies to whichever view is open.

Each view has its settings in a panel on the left and its content beside it. The bottom bar shows the number of images (_"81 images · 1 disabled"_).

<div class="evx-shot-todo">
<strong>Results, List view</strong>
<span>Results mode with List: the results bar on top, the settings panel on the left (A row per, Images / Classes / Columns), the table beside it with one row selected.</span>
<code>src/assets/screenshots/screenshot-results-list.png</code>
</div>

## List View

The **List** view (the default) shows one row per detected object. The default columns are **Image**, **Object ID**, **Class** (with the class's color), **Area px**, **Area nm** and **Circularity**; more - geometry, and **Min/Max/Avg/Sum** per measured channel - are under **Columns**. For tracked objects (see [Simple Tracker](/commands/dataset/simple-tracker/)), the **Track ID** column (under **General**) shows the track each object belongs to.

The settings panel has three check lists - **Images**, **Classes** and **Columns** - each with **All** / **None** and a search. **Columns** groups per-channel intensity metrics so you can toggle a whole channel at once. Above the table, **N rows** and the page; use the arrows to page through the results rather than scrolling through everything at once.

Click a row to select it; it stays highlighted. **Show on image ↗** - or a double-click - opens the object on its image: the image opens in the editor with the object marked, and a bar over it, **RESULTS · Row 12 of 200 ‹ › Back to results**, steps to the previous or next row's object or takes you back.

<div class="evx-shot-todo" data-kind="new">
<strong>A result on its image</strong>
<span>After Show on image ↗: the image with the object marked and the bar "RESULTS · Row 12 of 200 ‹ › Back to results ✕" at the top.</span>
<code>src/assets/screenshots/screenshot-results-on-image.png</code>
</div>

### Grouping and Aggregating Rows

**A row per** switches the table from **Objects** (flat, one row per object) to **Images** (one row per image/class combination). With **Images**, **Aggregate** picks one or more of **Average**, **Minimum**, **Maximum**, **Std Dev**, **Sum**, **Median** and **Skewness**. Every numeric column is duplicated per selected aggregation (for example **Area (px²) \[avg\]** and **Area (px²) \[sum\]**), so you can compare, say, average object size against total covered area per image.

<div class="evx-shot-todo">
<strong>Rows per image, aggregated</strong>
<span>A row per: Images, Aggregate: Average and Sum - columns doubled per aggregation.</span>
<code>src/assets/screenshots/screenshot-results-table-view-group-by-image.png</code>
</div>

### Transpose

**Transpose** places the classes next to each other instead of below each other - handy when you want to compare classes per image, or paste the table into a spreadsheet that expects one column block per class.

- With **A row per: Images**, the table has **one row per image**, and for every class one block of columns (one column per measurement and aggregation).
- With **A row per: Objects**, the n-th object of each class in an image shares row n, with one block of columns per class. A class with fewer objects in that image leaves its block empty in the extra rows. The image name is the first column, the class is given by the block.

The **Classes** list decides which classes become column blocks.

<div class="evx-shot-todo">
<strong>Transposed table</strong>
<span>Transpose on, a row per image: one column block per class.</span>
<code>src/assets/screenshots/screenshot-results-side-by-side.png</code>
</div>

### Colocalization Details

With **A row per: Objects**, the **Coloc details** switch flattens each object's matched partners into their own columns - one set of measurement columns per partner class, with a dash where no partner was found.

<div class="evx-shot-todo">
<strong>Coloc details</strong>
<span>Coloc details on: partner columns per class, dashes where no partner was found.</span>
<code>src/assets/screenshots/screenshot-results-coloc-details-view.png</code>
</div>

## Charts

The **Charts** view plots the rows selected in the List's settings instead of listing them. Pick the chart as a tile: **Histogram**, **Scatter** or **Boxplot**.

- **Histogram** bins a chosen numeric property, optionally restricted to one class, and shows the object count and the distribution across bins. Under **Display**: the number of **Bins** and **Counts on a log scale**.
- **Scatter** plots two numeric columns (**X** and **Y**), optionally restricted to one class. Large datasets are downsampled for drawing - **Points drawn** sets how many. Click a point to see its object on its image.
- **Boxplot** draws one box (quartile box, median line, whiskers, and outlier dots) for a chosen property. **A box per** groups them by **class**, **image**, **well**, **plate row** or **plate column**. Click a box to see its objects in the List.

<div class="evx-shot-todo">
<strong>Charts</strong>
<span>Three shots: Histogram, Scatter, and Boxplot with "A box per: well".</span>
<code>src/assets/screenshots/screenshot-results-histogram.png · screenshot-results-scatter.png · screenshot-results-boxplot.png</code>
</div>

## Plate View

**Plate** lays results out as a physical plate/well grid instead of a table or chart - useful for spotting spatial patterns across a multi-well high-content screening plate. It drills down through three levels: **Plate → Well → Image**.

The settings panel holds the same settings on all three levels: **Class**, **Property** (the metric to color by), **Aggregate**, **Colors** (Excel, Viridis, Plasma, Inferno, Cividis, Coolwarm, Red-Blue, YlGnBu, Haline, Algae, or Thermal) and **Group by**. The legend shows the active color range - click it to switch between **Auto** and a **Manual** min/max.

Click a tile to select it: the card on the right shows its value - and for a well, its images. **Open well ›** / **Open image ›** drill in, or simply double-click the tile.

### Grouping images into wells

**Group by** decides how images are assigned to wells:

| Mode             | How the well is found                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Auto**         | The well is detected from the image name, e.g. `A01_01.tif` or `Exp_B3_s2.tif`.                                                                        |
| **Custom regex** | Your own regular expression on the image name. Group 1 is the well (`B03`), group 2 the plate row (`B`), group 3 the plate column (`03`), group 4 the image number inside the well (`01`) - e.g. `^(([A-H])([0-9]+))_([0-9]+)`. |
| **Folder**       | One well per image folder, placed on the plate when the folder is named like a well (`B03/image_01.tif`).                                               |

**Regex in use** shows the regex - for **Auto** and **Folder** read-only, so you can see what was detected.

Grouping, plate size and well layout are **project settings**: they are stored in the project file, are the same values as in **EVA › [Project settings…](/guide/settings/) › Plate & grouping** and the [Images panel's Plate](/guide/images/#plate), and are used by the [plate and well export](#exporting-results). Changing them in one place changes them everywhere.

### Plate

Each tile is one well, colored by the aggregated metric across everything grouped into it. Wells are placed by decoding their group label into a row/column coordinate (e.g. `A14`). Pick a **Plate size** - **Auto** (the smallest standard layout that fits your data) or a fixed layout from 1 to 3456 wells (e.g. **96 Well (8 x 12)**, **384 Well (16 x 24)**).

<div class="evx-shot-todo">
<strong>Plate view</strong>
<span>A 96-well plate heatmap, one well selected - its card on the right with the value and the well's images.</span>
<code>src/assets/screenshots/screenshot-results-matrix-plate-view.png</code>
</div>

### Well

Drill into a well to see its individual images (fields) laid out as their own grid. **Well layout** sets that grid:

- **Auto** - the smallest square-ish grid that holds the highest image number in the well, images placed in number order.
- **Rows** × **Columns** - a fixed grid, with a free choice of which image goes where.

**Rearranging images by drag and drop.** If the images were not acquired in the order the grid shows them (e.g. a meander scan), drag an image tile onto another position - the two images swap places. The new order is stored in the project's plate settings and applies to every well of the plate. If the layout was **Auto**, the grid shown becomes a fixed grid of the same size first. The same order can also be edited number by number under **Images in well** in [Settings](/guide/settings/).

<div class="evx-shot-todo">
<strong>Well view</strong>
<span>Inside a well: the images as a grid, the breadcrumb "Plate › Well C3" in the top bar, one image left out (crossed out).</span>
<code>src/assets/screenshots/screenshot-matrix-well-view.png</code>
</div>

### Leaving images out

An image can be excluded from the statistics, for example because it is out of focus or contains an artifact. Click its eye in the well's card (**Leave this image out of the results**); click it again to use it again.

An image left out:

- is left out of every aggregated value - the well's value in the plate view, and the plate/well exports;
- is shown crossed out in the well view, and the well containing it gets a small corner badge in the plate view;
- is shown struck through and dimmed in the [List view](#list-view);
- is skipped by exports that cover all images. If you select it explicitly in the export's images, it is exported anyway.

The setting is stored in the results database, so it is kept when the results are opened again.

### Failed images and incomplete runs

An image whose analysis stopped with an error only holds the objects found before the error. Such an image is marked with a warning badge in the plate and well views (and in its well), drawn in the warning color in the List view, and - like an image left out - left out of aggregated well values.

If the whole analysis did not finish (cancelled, failed or interrupted, e.g. by a crash), Results shows a warning banner at the top: the results are incomplete.

### Image Heatmap

The innermost level bins a single image's objects into square tiles - the **Square size** (36, 48, 64, 128, 256, or 1024 px) - colored by the same metric and aggregate as the levels above. Click a tile to select it; **Show on image ↗** shows that region of the image in the editor, marked with a rectangle.

<div class="evx-shot-todo">
<strong>Image heatmap</strong>
<span>One image binned into tiles, one tile selected with Show on image ↗ in its card.</span>
<code>src/assets/screenshots/screenshot-results-heatmap.png</code>
</div>

## Split with the image

**Split with image** in the results bar puts the results on the left and the image on the right, with a divider between them that you can drag. It works with **List** and **Plate**.

The analysis' objects are drawn on the image, in their class colors. Select a row in the List and the image **flies to its object** - a ring, faint lines and a card (class, ID, area, the mean of a channel you pick, position) mark it, and the other objects are dimmed. Click an object on the image to select its row.

- `↑` / `↓` (or **‹ ›**) step to the previous or next object; `Esc` lets go of it.
- **Follow selection** switches the flying off - the image then stays where it is.
- **Color by** **Class** or **Value** - with Value, the objects take the heatmap's colors for the chosen property.
- In **Plate**, a well shows its images in a filmstrip under the image.
- **Image controls** open the [image panel](/guide/images/#image-panel) as a drawer over the image.
- **Open in Images ↗** opens the image in the editor.

The width of the results, whether the split is on, and **Follow selection** are remembered. With **Reduce motion** on (**EVA › Project settings… › Viewport**), the image jumps to the object instead of flying there.

<div class="evx-shot-todo" data-kind="new">
<strong>Split with image, List</strong>
<span>The list on the left, one row selected; the image on the right with the object ringed and its card.</span>
<code>src/assets/screenshots/screenshot-results-split-list.png</code>
</div>

<div class="evx-shot-todo" data-kind="new">
<strong>Split with image, Plate</strong>
<span>The plate heatmap on the left, a well selected; its images as a filmstrip under the image, Color by: Value.</span>
<code>src/assets/screenshots/screenshot-results-split-plate.png</code>
</div>

## Exporting Results

**Export…** in the results bar opens the export card below it: what to export, the **Format**, the **Classes** and the folder (**To**). **More options ›** shows the rest. Every checked option is written out together in one run.

<div class="evx-shot-todo">
<strong>Export</strong>
<span>The export card below Export…: the four kinds, Format, Classes, To - and a second shot with More options › open.</span>
<code>src/assets/screenshots/screenshot-results-export-dialog.png</code>
</div>

**What:**

- **Objects - one row per object** - with **Images** to pick (all by default; [images left out](#leaving-images-out) are skipped unless you select them explicitly), and optionally **With coloc details** and **Each image in its own file**.
- **Per image** - the same aggregated-by-image data as [a row per image in the List](#grouping-and-aggregating-rows); optionally the **Image heatmap** (the per-image spatial heatmap grid, with its own square size).
- **Per well - plate layout (XLSX)** - the plate as a heatmap; optionally **Plate as list**, **Wells as heatmap** and **Wells as list**, with **Colors** for the heatmaps. Grouping, plate size and well layout are taken from the project's plate settings - the same ones the [Plate view](#grouping-images-into-wells) uses.
- **Images with objects drawn (PNG)** <span class="evx-new">NEW</span> - each image as a PNG, with its channels in their colors (auto-scaled) and every object's box in its class color. Large images are written at the pyramid level up to 4096 px.

**Format** - **XLSX** (default), **CSV**, or **Parquet**.

**More options ›:**

- **Name prefix** - put in front of every output file name as `{prefix}_{name}` (e.g. `exp1_list.xlsx`), so exports of several experiments can share one folder. Characters that aren't allowed in file names are replaced by `_`.
- **Transpose the tables** - writes the object and image tables [transposed](#transpose), with the classes next to each other.
- **Measurements** and **Aggregations** - which columns and aggregations to write.
- **Z planes** and **Time points** - restrict the export to a range.

The image heatmap and the plate and well exports are XLSX-only. **Parquet** goes further: picking it ignores every other setting (filters, columns, grouping, checkboxes) and writes a single `objects.parquet` file - a raw, unfiltered dump of every column in the results database, meant for downstream tools that read Parquet natively rather than for a human to open.

In XLSX exports, values that come from (or, for a well/plate, are affected by) an image left out are grayed out and struck through.

Click **Start export**; a progress bar tracks the run and a message confirms completion or reports an error. For XLSX/CSV, results are named for what they contain (`list.xlsx`/`.csv`, `grouped_by_image.xlsx`/`.csv`, `plate.xlsx`, `well.xlsx`, `plate_list.xlsx`, `well_list.xlsx`, `heatmap_{image}.xlsx`), each preceded by the name prefix if one is set.

:::tip
For colocalization exports, partner lookups are resolved in batches of 5,000 source objects at a time - large colocalization datasets export reliably without needing to load everything at once.
:::

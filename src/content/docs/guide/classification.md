---
title: Classes & Objects
description: Define the object classes your pipelines detect, and inspect, filter and edit the objects of an image.
---

The **Classes** panel on the right is where you define the object populations that your pipelines detect and measure.
Every detected object is assigned to one or more classes. The **Objects** panel below it lists the objects of the current image.

## What is a Class?

A class represents a distinct object population in your experiment. Examples:

- `dapi@nucleus` - nuclei stained with DAPI
- `cy5@spot` - extracellular vesicles in the Cy5 channel
- `cy7@spot` - vesicles in the Cy7 channel
- `coloc@cy5cy7` - vesicles colocalising across both channels

:::tip[Naming convention]
Use `<prefix>@<type>` where the prefix (typically the fluorophore) is used for sorting in selection drop-downs.
:::

## Classes panel

Each class is a row with its color, its name, its number of objects on the current image and an eye that shows or hides its objects. Click a class to select it.

- **+** (**New class**) adds a class and opens its settings.
- **⋯ › Edit name, color, id…** of a class opens its settings.
- The same menu has **Copy**, **Move up** / **Move down** and **Delete class…**.

<div class="evx-shot-todo">
<strong>Class settings</strong>
<span>The Class settings dialog left of the right-hand panels: Name, Notes, Class ID with Auto, the color grid (7 a row).</span>
<code>src/assets/screenshots/screenshot-class-settings.png</code>
</div>

**Class settings**:

| Field        | Description                                            |
| ------------ | ------------------------------------------------------ |
| **Name**     | Class label, e.g. `cy5@spot`                           |
| **Notes**    | Optional free-text description                         |
| **Class ID** | The class's number - see below                         |
| **Color**    | Display color used for the class's objects in the viewer |

Every class has a number, its **Class ID** - the number a [Threshold](/commands/segmentation/threshold/) entry's segmentation class must match (see [Object Classes](/fundamentals/classes/)). **Auto** gives a new class the number above the highest one, so the number of a deleted class isn't reused by accident (old pipelines and results may still refer to it). Pick a number from the list to choose a free one yourself.

Changing the ID of an existing class moves every reference with it: pipelines, [components](/guide/command-groups/) and annotated objects that use the class switch to the new ID. Results of earlier runs keep the old one. The background keeps its ID 0.

You can also create a class where you need it: the class pickers of the steps and the annotate bar's **Paint as** have **+ New class…** - the new class is picked at once.

### Add classes from the image

**⋯ › Add classes from the image** creates one class per channel of the current image, as a starting point, in the channels' colors. It can add the classes found in all images, merged, or replace the list with them.

### Hiding unclassified objects

**⋯ › Hide unclassified objects** hides objects that have no class yet - on by default, so a large unfiltered detection doesn't drown out the objects you've actually classified.

## Objects panel

The **Objects** panel lists every object on the current image: the live-preview objects of the pipelines and the objects you [drew by hand](/guide/images/#annotating-the-image).

Click a row to select it - the object is highlighted on the image, and selecting an object on the image selects its row. Click it again to unselect it.

### Filtering

Above the list are a **class filter** (**All classes** or one class) and a **search**. The search takes an object id, a class name, or a condition on a measurement - `area > 50`, `circ < 0.6` - and several terms separated by commas.

### Objects as a table

**⋯ › Show as a table** moves the objects to a table at the bottom of the window, between the left and right panels: one line per object with its **ID**, **classes**, **area**, **circularity** and the **mean** of each channel. **⋯ › Columns** picks the columns. The class filter and the search sit in the table's head. **Show as a list** brings back the list.

Whether an image opens with the list or the table is set in **EVA › Project settings… › Viewport › Objects as a table**.

<div class="evx-shot-todo" data-kind="new">
<strong>Objects as a table</strong>
<span>The objects table at the bottom of the window, a class chip and "area > 50" in its head, one row selected with its buttons.</span>
<code>src/assets/screenshots/screenshot-objects-table.png</code>
</div>

### The selected object

The selected object's details are shown in a card beside the panel:

- its classes,
- **Area** in pixels² and in the physical unit (nm²) from the image's pixel size,
- **Circularity**,
- the **mean** intensity of each channel,
- **Coloc with** - each class it colocalizes with, and how many of that class's objects.

An object found by a pipeline is read-only (**From the pipeline · read-only**). An object drawn by hand can be changed.

<div class="evx-shot-todo">
<strong>Objects panel with a selected object</strong>
<span>The Objects list on the right, one object selected; its card beside it with classes, area, circularity, means, Coloc with.</span>
<code>src/assets/screenshots/screenshot-roi-list.png</code>
</div>

### Managing objects

For the selected object:

- **Set class…** - pick a class, then **Add class** adds it to the object's classes, keeping the ones it has, or **Set class** replaces them.
- **Copy to manual** - copies a pipeline object into the hand-drawn annotations, where it can be edited.
- **Delete object** (or `Delete`) - removes a hand-drawn object, after a confirmation.

The panel's **⋯** menu, for all objects of the image:

| Item | What it does |
| --- | --- |
| **Copy pipeline objects to manual…** | Copies the pipeline's objects into the hand-drawn annotations. |
| **Export annotations (GeoJSON)…** <span class="evx-new">NEW</span> | Writes the hand-drawn annotations of every image to a folder, one `<image>.geojson` file per image - the layout QuPath uses. |
| **Import annotations (GeoJSON)…** <span class="evx-new">NEW</span> | Reads the `.geojson` files of a folder into the matching images - added to their hand-drawn annotations, or replacing them. |
| **Re-measure manual annotations** | Measures the hand-drawn objects again. |
| **Delete manual annotations…** | Removes every object drawn by hand on this image, after a confirmation. Objects found by pipelines are not affected. |

## How Classes Relate to Pipelines

Classes aren't just labels - they're what every object-processing pipeline step selects, filters, and reassigns by. See [Object Classes](/fundamentals/classes/) for the full lifecycle, from a `Threshold` entry's raw segmentation class through to a named class assigned by [Classify Objects](/commands/object/classify-objects/).

---
title: Colocalization
description: Find objects from multiple classes that spatially overlap and assign them a shared tracking ID.
---

The **Colocalization** command identifies objects from two or more input classes that overlap each other. Overlapping objects are defined as _colocalising_. EVAnalyzer assigns all colocalising objects a shared **tracking ID**, allowing them to be grouped in the results table.

Unlike [Object Math](/commands/object/object-math/), which *derives a new shape* from two object sets, Colocalization's job is to *link* objects that already exist - each overlapping pair (or group) keeps its own identity and metrics, but gains a shared tracking ID and, optionally, a new object recording the overlap area itself.

![Overlapping objects from two classes, plus the overlap region itself, all share one tracking ID](../../../../assets/figures/cmd-colocalization.svg)

## Parameters

| Parameter                             | Description                                                                                                     |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Classes to colocalize**             | Two or more object classes that must all have an overlapping member for an object to be considered colocalising |
| **Multiplicity**                      | How many partners an object may coloc with at once - see below                                                  |
| **Class for overlapping areas**       | A class assigned to a new object representing the actual overlap area                                           |
| **Exclude classes**                   | Objects that also overlap one of these classes are dropped entirely, even if they'd otherwise match - see below |
| **Min colocalization area**           | Minimum overlap area in the selected unit                                                                       |
| **Size unit**                         | Unit for the min area threshold                                                                                 |

:::note
**Filter classes**, an older secondary-overlap filter, still exists in the underlying project schema for compatibility with older projects, but is hidden from the command picker in favor of **Exclude classes** below.
:::

## Multiplicity

**Multiplicity** replaces the old "Allow multi-object colocalization" checkbox with three explicit modes:

| Mode (GUI label)                     | Effect                                                                                                                                     |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **No multi coloc (1:1)** *(default)* | Every object keeps only its single best-overlap match (largest overlap area) per other class                                             |
| **Allow multi coloc**                | Every object may coloc with every overlapping partner that meets **Min colocalization area**                                             |
| **Multi coloc only for selected**    | Only the listed classes may coloc with more than one partner - every other class in **Classes to colocalize** is still capped to its single best match |

**Multi coloc only for selected** is the tool for a "count spots per cell" shape: with **Classes to colocalize** set to `Cell, Spot` and multiplicity limited to `Cell`, a cell can coloc with any number of spots, but each spot still picks exactly one cell (the one it overlaps most) - so a spot sitting on the border between two cells is never double-counted under both.

Where an object is capped to a single best match, ties (equal overlap area) are broken toward the lower object ID, so the result is deterministic rather than depending on cache iteration order.

## Exclude Classes

**Exclude classes** is a blocklist evaluated *after* the classes-to-colocalize check: an object that satisfies **Classes to colocalize** is dropped entirely - no colocalization recorded, no overlap-area object created - if it also overlaps any object from one of these classes by at least **Min colocalization area**. Leave empty (the default) to disable this filter.

Example: to find objects colocalizing with a nucleus stain and a membrane stain, but excluding any that also overlap a dead-cell marker, set **Classes to colocalize** to the nucleus and membrane classes and **Exclude classes** to the dead-cell-marker class.

## Colocalizing handling

When an object is found to colocalize, one of two operations is applied:

- **Move** - the object's class is changed to a new class. The Object ID is unchanged.
- **Copy** - a new object is created with the new class; the origin object's ID is recorded in the copy's origin object ID field.

A new **colocalizing area** object is created for the overlapping region. This object is assigned to the class specified by **Class for overlapping areas** and can be used for further measurements.

All colocalising objects - input objects and the colocalization-area object - receive the same tracking ID. In the results table, rows with the same tracking ID appear adjacent to each other.

## Example: Two-channel spot colocalization

1. Classify spots in Cy5 channel → `cy5@spot`
2. Classify spots in Cy7 channel → `cy7@spot`
3. Add a Colocalization step:
   - Classes: `cy5@spot`, `cy7@spot`
   - Class for overlapping areas: `coloc@cy5cy7`
4. All Cy5 spots that overlap with a Cy7 spot (and vice versa) receive a common tracking ID.

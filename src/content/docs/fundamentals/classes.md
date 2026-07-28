---
title: Object Classes
description: How a class starts as a raw segmentation number from Threshold and ends as a named object class - and how Classify Objects moves an object between the two.
---

Every object carries zero or more **classes** - the labels every object-processing command, filter, and the results table use to select, count, and export object populations. Classes start life as a plain number assigned during segmentation and only become a name like `dapi@nucleus` once [Classify Objects](/commands/object/classify-objects/) says so. This two-tier system explains why several commands distinguish a "segmentation class" from an "object class," and why **Classify Objects** is the one command that can move an object between them.

## Two class types, one numbering space

| Type                 | Used by                                                      | Values                                       |
| --------------------- | -------------------------------------------------------------- | ---------------------------------------------- |
| **Segmentation class** | [Threshold](/commands/segmentation/threshold/), [Extract Objects](/commands/object/extract-objects/) | A plain number, one per `Threshold` entry |
| **Object class**      | Every object-processing command, the results table            | `Unset`, or a number - the same one a segmentation class carries, once extracted |

These aren't arbitrary - an object class and a segmentation class with the same number are the *same underlying ID*, just read by two different pipeline stages. [Extract Objects](/commands/object/extract-objects/) converts one into the other by wrapping the number, not through any lookup table.

## Naming a class

A class only has a human name and colour once it's defined in the [Classification](/guide/classification/) tab - that entry (name, colour, notes) is a label attached to one specific object-class number. If a `Threshold` entry's segmentation class number happens to match a class you've already named, objects created from it show that name immediately; if not, they show as a plain two-digit number (e.g. `01`) until [Classify Objects](/commands/object/classify-objects/) assigns them a real class.

This is why defining classes in the Classification tab *before* wiring up pipelines makes the rest of the workflow read naturally - the numbers are already meaningful the moment objects appear.

## Lifecycle: from pixels to a named object

1. **[Threshold](/commands/segmentation/threshold/)** - each threshold entry is given a segmentation class number, and pixels matching that entry's intensity range are tagged with it in the binary output.
2. **[Connected Components](/commands/segmentation/connected-components/) / [Watershed](/commands/segmentation/watershed/)** - label individual instances within the thresholded regions. They don't touch classes at all; they only add per-pixel instance IDs on top of the segmentation classes Threshold already assigned.
3. **[Extract Objects](/commands/object/extract-objects/)** - creates one object per instance, and gives it an object class equal to its segmentation class number. From this point on, every downstream command works with object classes only.
4. **[Classify Objects](/commands/object/classify-objects/)** - the only command that changes an object's classes after extraction. Its shape and intersection criteria decide whether an object *matches*, and its **Match Handling** mode decides what that does to the object's classes - add a class, strip one, or **reclassify** (clear everything and assign a new, named class). Reclassifying on match is how a segmentation class becomes a real named class such as `dapi@nucleus` for the first time.
5. **Everything after** - [Object Math](/commands/object/object-math/), [Colocalization](/commands/object/colocalization/), [Voronoi](/commands/object/voronoi/), [Object Transform](/commands/object/transform-objects/), [Distance Transform](/commands/object/distance-transform/), [Save Image](/commands/object/save-image/) - all select their input objects purely by object class name, with no awareness of segmentation classes at all.

## An object can carry more than one class

Object classes are stored as a **set**, not a single value - an object can carry several classes at once (for example, tagged by one Classify Objects step and again by another, without either removing the first). This is what makes **Add class on match** in Classify Objects useful: it layers a class on top of whatever the object already carries, rather than replacing it.

This also affects **Input Classes** in Classify Objects: an object is only selected if it carries **every** class listed there, not just one of them - so listing more than one class narrows the input population (a logical AND), it doesn't widen it. Leaving it empty is the only way to select every object regardless of class.

## Reserved values

A couple of segmentation class numbers and one object class value are reserved rather than user-assigned:

| Value                                | Meaning                                                                                     |
| -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Segmentation class `0`                | **Background** - pixels no threshold entry matched                                          |
| Segmentation class `0xFFFFFFFF`        | **Manual** - reserved for objects coming from manual [Region Annotation](/guide/images/#region-annotation) rather than a pipeline |
| Object class **Unset**                | No class at all - the state every object starts in before extraction assigns one, and the state **Reclassify**/**Remove all classes** modes put non-matching or matching objects back into. Unset objects don't appear in any class-filtered results, count, or export |

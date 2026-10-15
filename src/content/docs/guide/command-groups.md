---
title: Command Groups
description: Bundle several pipeline steps into one reusable step with its own parameters - in a project, or shared as a library file.
---

A **command group** is a step made of other steps. A group such as _"Cell reconstruction"_ (blur, threshold, connected components, watershed, Voronoi, …) sits in a pipeline like any other command, can be inserted, moved and duplicated, and shows only the few settings that matter - typically an image channel and the classes it writes. Everything else stays as the group's author set it, but can still be looked at and changed.

Groups are useful to

- **reuse** a proven sequence of steps in several pipelines or projects, with one place to change it;
- **hand over** an analysis to colleagues who don't want to build pipelines: they set two or three parameters and run;
- **keep intermediate results internal**: classes the group only needs on the way (seeds, candidates, rejected objects) don't clutter the class list or the results.

Groups and their steps are colored in the group accent color and marked with **◆**, both in the pipeline and in the command picker.

## Creating a group

1. On the step card of the first step you want to group, click **Group…**.
2. In the **Group steps** dialog, enter a **Group name** and choose the range of steps (from / to).
3. EVAnalyzer lists the project classes the steps use under **Classes** and suggests a role for each:

   | Role                      | Meaning                                                                                                                                       | Suggested when                                                                                    |
   | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
   | **Group parameter**       | The class becomes a setting on the group card - every use of the group picks its own class.                                                   | The class is also used outside the selected steps (other steps or pipelines, hand annotations, tile merging). |
   | **Internal (group only)** | The class becomes the group's own. Each use of the group has its own copy, and its objects **don't reach the results**.                       | The class is only used by the selected steps.                                                      |
   | **Fixed**                 | The class stays as it is.                                                                                                                     | Only a segmentation class without an Extract Objects among the steps.                              |

   Change a role with its dropdown. Image channels of [Load Image Channel](/commands/image-processing/load-image-channel/) steps become group parameters too, and memory slots only the selected steps use become [group memory](#memory-slots-in-groups).
4. Click **Create group**. The steps are replaced by one group step - what runs doesn't change.

## The group card

A group step shows the group's **parameters** - each with the same control (dropdown, number field, class picker, …) as the setting it controls, and a **?** with its help text. Every use of a group has its own parameter values.

The buttons of the card:

| Button              | Action                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **View**            | Opens the group read-only, to see what it does.                                                                                |
| **Edit**            | Opens the group for editing - see [Editing a group](#editing-a-group).                                                         |
| **Ungroup**         | Puts the steps back into the pipeline, with this step's parameter values. The group's own classes become new project classes, its memory slots pipeline slots. |
| **Update to v_N_**  | Shown when the [library](#group-library) has a newer version of the group.                                                     |
| **Duplicate**       | Adds a second use of the same group.                                                                                           |
| **Save as**         | Saves the group as a library file (`.evagroup`).                                                                               |
| **Remove**          | Removes the step from the pipeline. The group itself stays in the project.                                                     |

The **?** on any step card - group or command - shows what the step does: a command's summary and description, a group's short and long description.

## Editing a group

**Edit** opens the group's steps in the pipeline panel, with a bar on top: **‹ Back · Pipeline › ◆ Group**. Inside, you work as in a normal pipeline - add, remove, move steps and change settings.

Changes to a group **apply to every use of it**. If the group is used by more than one step, EVAnalyzer asks first:

- **Edit for all** - change the group; every step using it follows.
- **Only this step** - make a copy (_"Name (2)"_) just for this step, and edit the copy.

### Exposing settings as parameters

Next to every setting of an opened group is a **◇**. Click it to **expose** the setting as a group parameter - it then shows on the group card, with its current value as default. An exposed setting is marked **◆**; clicking it again hides it.

One parameter can set several settings at once - for example the same class in a Threshold, a Classify Objects and a Voronoi step. When you expose a setting that an existing parameter of the same kind could set, EVAnalyzer asks whether to create a **new parameter** or **add it to** the existing one.

A setting controlled by a parameter always runs with the parameter's value. Editing it inside the opened group changes the parameter's default, and every setting the parameter controls follows.

### Group settings

**Settings…** in the bar of an opened group (or **✎** next to a **◆**) opens the **Group settings** dialog:

- the group's **Name**, **Short description** (shown in the command picker), **Author**, **Organization** and **Description** (shown behind the group card's **?**);
- per parameter: its name on the group card, its help text (empty shows the controlled setting's own help; **Reset to the setting's own help** goes back to it), its default, which settings it **sets**, **↑ / ↓** for the order on the group card, and **✕** to stop exposing it.

### Checks

EVAnalyzer checks groups when a project is loaded and while editing - for example a parameter that controls settings of different kinds, a setting that no longer exists, or a [mixing of internal and project classes](#internal-classes). Problems are shown as **⚠** on the step card, the group card and in the bar of the opened group, so they are found before an analysis starts.

## Internal classes

An internal class belongs to the group: every use of the group has its own copy, so two uses of _"Cell reconstruction"_ never see each other's seeds. When a use of the group has run its last step, its internal objects are deleted - they **never reach the results database**, and the memory they took is freed right away.

The rules that follow from this:

- **Moving objects into a project class.** An object never carries an internal and a project class at the same time. [Classify Objects](/commands/object/classify-objects/) (and the AI Object Classifier) may _reclassify_ internal objects into a project class - a typical "filter" group: internal candidates in, project-class hits out. _Adding_ a project class to an internal object (or the other way round) is an error.
- **Commands that create new objects** are always fine: the new objects belong to the class they are written to. A Voronoi of internal seeds can write project-class cells.
- **Colocalization links to internal objects** are removed when the group ends. If you want the numbers that come from them (e.g. a spot count per cell), the spot class must be a project class - a group parameter.
- **Extract Objects** inside a group can map a segmentation class to one of the group's classes with its [class mapping](/commands/object/extract-objects/#class-mapping).
- **Dataset steps** such as the [Simple Tracker](/commands/dataset/simple-tracker/) only work on project classes.
- [Cross-tile merging](/fundamentals/cross-tile-merging/) merges internal objects of each use of a group separately.

## Memory slots in groups

The slot picker of [Image Cache](/commands/image-processing/image-cache/) (and other steps that read a stored image) offers inside a group an additional kind, **Group memory**: slots that belong to one use of the group, so a group's intermediate image never overwrites a slot of the surrounding pipeline - or of a second use of the same group. They are freed when the group ends.

## Groups in the command picker

The **◆ Groups** chip of the command picker lists the groups of the project (with **used N×**) and, under **LIBRARY**, the groups from library files that aren't in the project yet. A search also finds groups. The detail panel shows the group's parameters with their defaults and where it comes from (e.g. _"this project · Segment → Object"_ - the category of its first and last step).

Groups no pipeline uses any more can be removed with **Remove from project** in their detail panel, or all at once with **N groups no pipeline uses · Remove**.

## Group library

**Save as** on a group card saves the group as a library file (`.evagroup`) through the template dialog. Group files in the templates folder (`~/evanalyzer/templates/`) appear in the picker's **LIBRARY** section in every project.

- **Inserting** a library group copies it into the project, together with the groups it uses. From then on the project has its own copy: changes affect only the project, never the file, and the project stays complete without it.
- **Updates:** the project remembers which file and version a group came from. When the library has a newer version, the group card shows **Update to v_N_**. Updating keeps every step's parameter values; if the project changed the group since inserting it, EVAnalyzer warns that updating replaces those changes.
- **Pipeline templates** carry the groups their steps use, so a saved pipeline with group steps works in other projects too.

## Limitations

- Groups inside groups can only be created by inserting a group into an opened group, not with **Group…** inside an opened group.
- Breakpoints can't be set on steps inside a group.
- Steps are selected for grouping as a range (from / to), not by Shift-click.

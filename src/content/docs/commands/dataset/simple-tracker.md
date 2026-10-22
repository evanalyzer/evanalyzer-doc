---
title: Simple Tracker
description: Link the objects of a time-lapse into tracks by nearest-neighbour matching between consecutive frames.
---

The **Simple Tracker** links the objects of a time-lapse into **tracks**: each object in frame _t_ + 1 continues the track of the nearest object in frame _t_, if that one is close enough and not claimed by an even closer object. Every tracked object gets a **Track ID**, shown as a column in the [results](/guide/results/#list-view).

It is a [dataset step](/guide/pipelines/#dataset-steps): it runs once after every image has been analysed, on the stored objects of all frames.

The tracks it makes are shown in [Results › Tracks](/guide/results/#tracks): a row per track with its time points, speed and straightness, and its trail on the image.

## Parameters

| Parameter        | Description                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| **Object Class** | The object class to track.                                                                       |
| **Unit**         | Unit of **Max Distance**: **nm** or **px**.                                                      |
| **Max Distance** | How far an object may move from one frame to the next. Farther apart, it starts a new track.     |

## How it works

Per image and Z-plane, two consecutive frames are matched by **global greedy nearest neighbour**:

1. All pairs of objects in the two frames that are at most **Max Distance** apart (measured between the centres of their bounding boxes) are collected.
2. The pairs are linked closest first; each object is used only once.
3. An object without a partner starts a new track. A frame without objects ends every track.

Track IDs start at 1 and are unique across tracking steps: a second Simple Tracker for another class continues after the IDs the first one gave. Objects that are not tracked have no Track ID.

## Limitations

- No gap closing: an object missing in one frame ends its track, and its reappearance starts a new one.
- No divisions or merges: each object continues at most one track.
- Only project classes can be tracked, not the internal classes of a [module](/guide/modules/#internal-classes).

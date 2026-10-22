# Documentation screenshots

`take.py` drives the real EVAnalyzer GUI and writes the screenshots of the
docs into `src/assets/screenshots/`. Re-run it whenever the app's design
changes.

```sh
sh scripts/screenshots/setup.sh            # once
python3 scripts/screenshots/take.py        # all scenes, ~10 min
python3 scripts/screenshots/take.py --list # the scenes
python3 scripts/screenshots/take.py pipeline compare   # only these
```

## What it does

1. **A private display.** EVAnalyzer runs on a virtual X display (Xvfb,
   `:99`, 1440 × 900) with a throw-away home folder in
   `.cache/screenshots/home` - your desktop, settings and recent projects are
   never touched. Wayland is switched off for it, so the window can't open on
   your screen.
2. **Demo data.** `make_plate.py` writes a synthetic single-EV plate to
   `/data/ev_plate`: wells A–D × 1–6, two fields each, four channels (CY7,
   CY5, FITC, Tetraspeck beads) as OME-TIFF with pixel size and emission
   wavelengths. EV density rises across the columns (a dilution series),
   CY5 + FITC colocalization rises down the rows - so the plate heatmap,
   charts and colocalization classes have something to show.
   `make_project.py` writes `ev_plate.evaproj` (three spot pipelines and a
   colocalization pipeline, display ranges per image), and the CLI runs one
   analysis, `dilution_series`. `make_tracks.py` writes a small time-lapse to
   `/data/ev_tracks` (two fields, 15 frames 30 s apart, moving vesicles) with
   a Simple Tracker project; its analysis `tracking` feeds the Tracks and
   Over time screenshots.
3. **Scenes.** Each scene restarts the app, clicks to one screen and saves
   one or more PNGs. The scenes are plain Python functions in `take.py`.

## The binary

`take.py` uses `tools/evanalyzer-linux-x86_64/evanalyzer` (set `EVA_APP` for
another one). If it needs a newer glibc than the system has, `setup.sh`
unpacks Debian trixie's glibc and libstdc++ into `.cache/screenshots/glibc`
and `take.py` starts the app through that loader. The system's libraries
stay as they are.

## Options

| Variable | Default | |
| --- | --- | --- |
| `EVA_APP` | `tools/evanalyzer-linux-x86_64/evanalyzer` | The app to photograph |
| `EVA_DATA` | `/data/ev_plate` | Where the demo plate goes - its path shows in the screenshots |
| `EVA_TRACKS` | `/data/ev_tracks` | Where the time-lapse for the tracking screenshots goes |
| `EVA_SERIES_IMAGE` | - | A file with several image series (the app repo's `tests/Slide1_distal_zoom_40x.vsi`) for `screenshot-series.png`; without it that scene is skipped |
| `EVA_DISPLAY` | `:99` | The virtual display |

`--check` writes into `.cache/screenshots/check/` instead of the docs, to
look before replacing anything. `--steps` also saves an image after every
step of a scene into `.cache/screenshots/steps/`.

## When a scene breaks

The clicks are coordinates in the 1440 × 900 window. When the layout
changes, a scene clicks next to its target - a menu doesn't open, the shot
shows the wrong screen. Then:

1. `python3 scripts/screenshots/take.py <scene> --check --steps`
2. Look at `.cache/screenshots/steps/` to see where it went wrong.
3. Fix the coordinates. Things clicked in several scenes have one name at the
   top of `take.py` (`EVA`, `RUN`, `STEP_Y`, `RESULTS_VIEW` …) - fix them once
   there.

The app's log is in `.cache/screenshots/app.log`. A run first closes EVAnalyzer windows an aborted run left on the virtual display - a second window on top would take the clicks.

## Not scripted

- `screenshot-image-measure-points.png` (a measurement marker) and
  `screenshot-results-coloc-details-view.png` - still placeholders in the
  docs.
- The Windows SmartScreen screenshots of the installation page.

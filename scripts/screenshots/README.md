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
   a Track Nearest Neighbor and a Measure Track Motion step; its analysis
   `tracking` feeds the Tracks, Paths and Over time screenshots (an older
   project without Measure Track Motion is written again).
   `make_neurons.py` writes two fields of neurons to `/data/ev_neurons` (DAPI
   somata, MAP2 dendrites) with a project that skeletonizes the dendrites,
   traces each neuron (Trace Filaments) and measures the trees (Measure
   Filament Tree) and their Sholl profile; its analysis `neurons` feeds the
   Trees and Profile screenshots, and the ruler scene measures on it. `make_zstack.py` writes a z-stack to `/data/ev_zstack`
   (48 planes, nuclei, cytoplasm rims and a fibre crossing the stack) for the
   orthogonal views and the 3D view. `make_rgb.py` writes an H&E-like RGB section to
   `/data/ev_rgb` with a Color Filter pipeline, for the colour-image
   Image panel and the Color Filter range editor. The Measurements panel scene writes
   `ev_plate_measure.evaproj` beside the demo project: a copy with measure
   steps and an Exclude Image, so the demo project's own step counts stay.
3. **Scenes.** Each scene restarts the app, clicks to one screen and saves
   one or more PNGs. The scenes are plain Python functions in `take.py`.

## The binary

`take.py` uses `tools/evanalyzer-linux-x86_64/evanalyzer` (set `EVA_APP` for
another one) - a release download, or a build of the app's `main` when the
docs describe features not released yet. To build one (Linux, about 11 min
on 22 cores, ~4 GB in `target/`):

```sh
curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
sudo apt-get install libxkbcommon-dev libxcursor-dev libwayland-dev libudev-dev \
    libfontconfig-dev mold cmake clang
git clone https://github.com/evanalyzer/evanalyzer && cd evanalyzer
cargo build --target x86_64-unknown-linux-gnu --release --no-default-features --features gui
cp target/x86_64-unknown-linux-gnu/release/evanalyzer <docs>/tools/evanalyzer-linux-x86_64/
```

`--no-default-features --features gui` keeps the desktop app but leaves out
the libtorch AI plugin, which needs a
multi-GB download and isn't needed for the screenshots. If it needs a newer glibc than the system has, `setup.sh`
unpacks Debian trixie's glibc and libstdc++ into `.cache/screenshots/glibc`
and `take.py` starts the app through that loader. The system's libraries
stay as they are.

## Options

| Variable | Default | |
| --- | --- | --- |
| `EVA_APP` | `tools/evanalyzer-linux-x86_64/evanalyzer` | The app to photograph |
| `EVA_DATA` | `/data/ev_plate` | Where the demo plate goes - its path shows in the screenshots |
| `EVA_TRACKS` | `/data/ev_tracks` | Where the time-lapse for the tracking screenshots goes |
| `EVA_ZSTACK` | `/data/ev_zstack` | Where the z-stack for the orthogonal and 3D views goes |
| `EVA_NEURONS` | `/data/ev_neurons` | Where the neurons for the Trees, Profile and ruler screenshots go |
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

Known quirks:

- The 3D view ignores drags until its volume is loaded (the scene waits 25 s).
- The app now and then can't reach the X server right after a start -
  `start_app` tries three times.
- Some views (Results with a wide table) make the window grow beyond
  1440 px once, and it keeps that width. `click()` and `shot()` size it back
  (`fit_window`).
- Track numbers differ from run to run (the images are tracked in
  parallel): the Tracks scene sorts by VCL and takes the first row rather
  than a track by its number.

The app's log is in `.cache/screenshots/app.log`. A run first closes EVAnalyzer windows an aborted run left on the virtual display - a second window on top would take the clicks.

## Not scripted

- `screenshot-image-measure-points.png` (a measurement marker),
  `screenshot-results-coloc-details-view.png` and
  `screenshot-results-children.png` - still placeholders in the docs
  (see SCREENSHOTS.md).
- The Windows SmartScreen screenshots of the installation page.

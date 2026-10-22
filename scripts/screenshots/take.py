#!/usr/bin/env python3
"""Takes the documentation screenshots by driving the real EVAnalyzer GUI.

EVAnalyzer runs on its own virtual X display (Xvfb, 1440 x 900) with a
throw-away home folder, so nothing touches your desktop or your settings.
Every scene restarts the app, clicks its way to one screen and saves a PNG
into src/assets/screenshots/.

    python3 scripts/screenshots/take.py              # every scene
    python3 scripts/screenshots/take.py pipeline compare   # only these
    python3 scripts/screenshots/take.py --list
    python3 scripts/screenshots/take.py --check      # shots go to .cache only

Set up once with scripts/screenshots/setup.sh (see README.md there).

The clicks are screen coordinates of the 1440 x 900 window. When the UI's
layout changes, a scene clicks into the wrong place: run it alone with
--check, look at .cache/screenshots/check/<name>.png and the step images
(--steps), and fix the coordinates in SCENES below.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache" / "screenshots"
OUT = ROOT / "src" / "assets" / "screenshots"
DISPLAY = os.environ.get("EVA_DISPLAY", ":99")
APP = Path(os.environ.get("EVA_APP", ROOT / "tools" / "evanalyzer-linux-x86_64" / "evanalyzer"))
DATA = Path(os.environ.get("EVA_DATA", "/data/ev_plate"))
PROJECT = DATA / "ev_plate.evaproj"
# The time-lapse for the Tracks screenshots (make_tracks.py).
TRACKS = Path(os.environ.get("EVA_TRACKS", "/data/ev_tracks"))
TRACKS_PROJECT = TRACKS / "ev_tracks.evaproj"
# A file with several image series, for the "Which series" question
# (the app repo's tests/Slide1_distal_zoom_40x.vsi). Optional.
SERIES_IMAGE = os.environ.get("EVA_SERIES_IMAGE", "")
W, H = 1440, 900

env = dict(os.environ, DISPLAY=DISPLAY, HOME=str(CACHE / "home"), SLINT_BACKEND="winit-software")
env.pop("WAYLAND_DISPLAY", None)  # else the window opens on the desktop's Wayland session


# -- Low level --------------------------------------------------------------

def sh(*args, **kw):
    return subprocess.run(args, env=env, check=False, capture_output=True, text=True, **kw)


def sleep(s):
    time.sleep(s)


def app_command():
    """The app, through the newer glibc of setup.sh when the system's is too old."""
    loader = CACHE / "glibc" / "usr" / "lib" / "x86_64-linux-gnu" / "ld-linux-x86-64.so.2"
    if loader.exists():
        lib = loader.parent
        return [str(loader), "--library-path", f"{lib}:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu", str(APP)]
    return [str(APP)]


def ensure_display():
    if sh("xdotool", "getdisplaygeometry").returncode == 0:
        return
    subprocess.Popen(["Xvfb", DISPLAY, "-screen", "0", f"{W}x{H}x24", "-nolisten", "tcp"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if sh("xdotool", "getdisplaygeometry").returncode == 0:
            return
        sleep(0.1)
    sys.exit("Xvfb didn't start")


_proc = None


def stop_app():
    global _proc
    if _proc and _proc.poll() is None:
        _proc.terminate()
        try:
            _proc.wait(10)
        except subprocess.TimeoutExpired:
            _proc.kill()
    _proc = None


def start_app(*args):
    """Starts the app (args go to it, e.g. --project) and sizes its window."""
    global _proc
    stop_app()
    log = open(CACHE / "app.log", "w")
    _proc = subprocess.Popen(app_command() + list(args), env=env, stdout=log, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL)
    for _ in range(160):
        win = sh("xdotool", "search", "--onlyvisible", "--name", "EVAnalyzer").stdout.split()
        if win:
            sh("xdotool", "windowsize", win[0], str(W), str(H))
            geo = sh("xdotool", "getwindowgeometry", win[0]).stdout
            if f"{W}x{H}" in geo:
                sh("xdotool", "windowfocus", win[0])
                sleep(3)
                return
        sleep(0.25)
    sys.exit("EVAnalyzer's window didn't appear - see .cache/screenshots/app.log")


def click(x, y, wait=0.8):
    sh("xdotool", "mousemove", str(x), str(y), "click", "1")
    sleep(wait)


def hover(x, y, wait=0.8):
    sh("xdotool", "mousemove", str(x), str(y))
    sleep(wait)


def away():
    """The pointer off every button, so no hover state or tooltip shows."""
    sh("xdotool", "mousemove", str(W - 1), str(H - 1))
    sleep(0.3)


def type_text(text, wait=0.8):
    sh("xdotool", "type", "--delay", "60", text)
    sleep(wait)


def key(*keys, wait=0.6):
    sh("xdotool", "key", *keys)
    sleep(wait)


def scroll(x, y, clicks):
    """Mouse wheel at x, y: positive clicks scroll up (zoom in on the image)."""
    button = "4" if clicks > 0 else "5"
    sh("xdotool", "mousemove", str(x), str(y))
    for _ in range(abs(clicks)):
        sh("xdotool", "click", button)
        sleep(0.25)
    sleep(0.8)


def drag(points, wait=1.5):
    x, y = points[0]
    sh("xdotool", "mousemove", str(x), str(y), "mousedown", "1")
    for x, y in points[1:]:
        sh("xdotool", "mousemove", str(x), str(y))
        sleep(0.06)
    sh("xdotool", "mouseup", "1")
    sleep(wait)


_target = OUT
_steps = False
_step_n = 0


def shot(name, wait=1.0):
    sleep(wait)
    _target.mkdir(parents=True, exist_ok=True)
    path = _target / f"{name}.png"
    sh("import", "-window", "root", str(path))
    print(f"  -> {path.relative_to(ROOT)}")


def step_shot(label):
    """With --steps, an image after each helper - to find where a scene goes wrong."""
    global _step_n
    if _steps:
        _step_n += 1
        d = CACHE / "steps"
        d.mkdir(parents=True, exist_ok=True)
        sh("import", "-window", "root", str(d / f"{_step_n:03d}-{label}.png"))


# -- Places in the window ------------------------------------------------------
# One name per thing clicked more than once, so a moved button is fixed once.

EVA = (36, 20)
REFRESH_PREVIEW = (195, 20)
ANNOTATE = (227, 20)
COMPARE = (1137, 20)
RUN = (1343, 20)
MODE_IMAGES, MODE_PIPELINES, MODE_RESULTS = (34, 885), (104, 885), (175, 885)
IMAGE_ROW = (200, 360)           # 6th image of the list: A03_02
PICK_CY5 = (92, 185)             # "Pick a pipeline" list, 2nd pipeline
STEPS_HEAD = (90, 72)            # steps panel head: opens the pipeline switcher
STEP_Y = {1: 123, 2: 165, 3: 207, 4: 249, 5: 291, 6: 333, 7: 375, 8: 417}
STEP_GUTTER_X, STEP_MENU_X, STEP_EXPAND_X, STEP_PIN_X = 34, 327, 305, 349
ADD_STEP = (200, 455)
IMAGE_CENTER = (745, 450)
OVERLAY_KNOB = (503, 838)
EVA_VIEW = (70, 387)
VIEW_COLORS = {"light": (423, 597), "dark": (482, 597), "dim": (539, 597)}
RESULTS_VIEW = {"list": (229, 20), "plate": (287, 20), "charts": (354, 20)}
RESULTS_FULL, RESULTS_SPLIT = (433, 20), (533, 20)
EXPORT = (1383, 20)
CARD_BUTTON = (1277, 151)        # "Open well ›" / "Open image ›" on the right-hand card


# -- Steps used by several scenes --------------------------------------------

def open_project():
    start_app("--project", str(PROJECT))
    step_shot("project")


def open_image():
    click(*IMAGE_ROW, wait=3)
    step_shot("image")


def preview():
    click(*REFRESH_PREVIEW, wait=7)
    step_shot("preview")


def pipeline_cy5(with_preview=True):
    """Pipelines mode, CY5 spots shown, previewed, zoomed to ~200 %, overlay 34 %."""
    open_project()
    open_image()
    click(*MODE_PIPELINES, wait=1.5)
    click(*PICK_CY5, wait=1)
    if with_preview:
        preview()
        scroll(*IMAGE_CENTER, 11)
        drag([OVERLAY_KNOB, (490, 838), (478, 838)], wait=1)
    away()
    step_shot("pipeline")


def eva_view_menu():
    click(*EVA)
    hover(60, 380, wait=0.1)
    hover(*EVA_VIEW)


def set_colors(scheme):
    eva_view_menu()
    hover(400, 520, wait=0.1)
    click(*VIEW_COLORS[scheme])
    key("Escape")


def results(view="list"):
    open_project()
    click(*MODE_RESULTS, wait=2)
    click(595, 148, wait=5)        # the analysis in the "Analyses" list
    if view != "list":
        click(*RESULTS_VIEW[view], wait=4)
    away()
    step_shot(f"results-{view}")


# -- The scenes ---------------------------------------------------------------
# name -> function. A scene starts the app itself and saves one or more shots.

def sc_start_page():
    open_project()                 # so the recent projects list holds it
    start_app()
    shot("screenshot-start-page", 2)


def sc_series():
    if not SERIES_IMAGE:
        print("  (skipped - set EVA_SERIES_IMAGE to a file with several series)")
        return
    folder = DATA.parent / "slide"
    folder.mkdir(parents=True, exist_ok=True)
    dst = folder / Path(SERIES_IMAGE).name
    if not dst.exists():
        shutil.copy(SERIES_IMAGE, dst)
    # A project of just that folder (the folder dialog isn't scripted).
    project = json.loads(PROJECT.read_text())
    project["images"] = {"root": str(folder), "list": {}, "settings": project["images"]["settings"]}
    project["pipelines"], project["meta"]["name"] = [], "Slide"
    (folder / "slide.evaproj").write_text(json.dumps(project, indent=2))
    start_app("--project", str(folder / "slide.evaproj"))
    click(372, 72, wait=3)         # refresh the image list
    click(200, 140, wait=5)        # the slide: asks which series
    away()
    shot("screenshot-series")


def sc_images():
    open_project()
    open_image()
    away()
    shot("screenshot-images-list")
    click(238, 72, wait=1.5)       # Plate
    click(237, 243, wait=1.5)      # well C4
    away()
    shot("screenshot-images-plate")


def sc_image_panel():
    open_project()
    open_image()
    click(1220, 376)               # CY5 in the Image panel
    click(1265, 662)               # Values ›
    away()
    shot("screenshot-image-panel")
    click(340, 524, wait=1)        # All metadata ›
    away()
    shot("screenshot-image-meta")
    click(362, 429, wait=1)        # Less ‹
    click(31, 744, wait=1)         # CY7's color swatch
    away()
    shot("screenshot-image-channel-color")


def sc_workspace():
    pipeline_cy5()
    shot("screenshot-workspace")


def sc_pipeline():
    pipeline_cy5()
    click(89, STEP_Y[4])           # Threshold opens on the line
    away()
    shot("screenshot-pipeline")
    click(STEP_EXPAND_X, STEP_Y[4], wait=1.5)
    away()
    shot("screenshot-step-settings")


def sc_pick_pipeline():
    open_project()
    open_image()
    click(*MODE_PIPELINES, wait=1.5)
    away()
    shot("screenshot-pipeline-pick")


def sc_add_step():
    pipeline_cy5()
    click(*ADD_STEP, wait=1.5)
    click(520, 354, wait=1)        # Colocalization
    away()
    shot("screenshot-add-pipeline-step")


def sc_step_menu():
    pipeline_cy5(with_preview=False)
    hover(200, STEP_Y[1])
    click(STEP_MENU_X, STEP_Y[1])
    shot("screenshot-step-menu")


def sc_eva_menu():
    pipeline_cy5()
    click(*EVA)
    shot("screenshot-eva-menu")
    hover(60, 380, wait=0.1)
    hover(*EVA_VIEW)
    shot("screenshot-eva-view")


def sc_colors():
    pipeline_cy5()
    shot("screenshot-colors-light")
    for scheme in ("dark", "dim"):
        set_colors(scheme)
        click(*IMAGE_CENTER)
        away()
        shot(f"screenshot-colors-{scheme}")
    set_colors("light")            # the scheme is a user setting: leave it light


def sc_palette():
    pipeline_cy5(with_preview=False)
    click(286, 72)                 # "Ctrl K" in the steps panel head
    type_text("min")
    away()
    shot("screenshot-command-palette")
    key("Escape")


def sc_tuning():
    pipeline_cy5()
    hover(200, STEP_Y[8])
    click(STEP_PIN_X, STEP_Y[8], wait=1.5)   # ⌖ pins all settings of ClassifyObjects
    away()
    shot("screenshot-tuning")


def sc_compare():
    pipeline_cy5()
    click(STEP_GUTTER_X, STEP_Y[4])          # breakpoint: stop
    preview()
    click(*COMPARE, wait=5)
    away()
    shot("screenshot-compare")


def sc_switcher():
    pipeline_cy5(with_preview=False)
    click(*STEPS_HEAD)
    away()
    shot("screenshot-pipeline-switcher")
    click(349, 181)                # CY5's ⋯
    click(194, 244, wait=1.5)      # Edit pipeline…
    away()
    shot("screenshot-add-pipeline-dialog")
    click(687, 440)                # Cancel
    click(327, 181, wait=2)        # focus on CY5
    away()
    shot("screenshot-pipeline-focus")


def sc_classes():
    pipeline_cy5(with_preview=False)
    click(1410, 72)                # Classes ⋯
    shot("screenshot-classification")
    key("Escape")
    hover(1250, 174)
    click(1410, 174)               # cy5@spot's ⋯
    click(1296, 228, wait=1.5)     # Edit name, color, …
    away()
    shot("screenshot-class-settings")


def sc_annotate():
    pipeline_cy5()
    click(*ANNOTATE)
    click(875, 74)                 # Paint as
    click(916, 247)                # 05 tetraspeck@bead
    click(685, 74)                 # Brush (the bar re-lays out once a class is picked)
    path = [(600, 420), (620, 430), (650, 445), (680, 455), (710, 470), (740, 480), (770, 500),
            (790, 520), (800, 545), (795, 570), (775, 590), (745, 600), (715, 598), (690, 585),
            (670, 565), (655, 540), (640, 515), (625, 490), (612, 465), (604, 440)]
    drag(path, wait=2)
    hover(1000, 760)
    shot("screenshot-annotate-brush")


def sc_objects():
    open_project()
    open_image()
    preview()
    click(1250, 812, wait=1.5)     # 2nd object of the list
    away()
    shot("screenshot-roi-list")
    click(1410, 677)               # Objects ⋯
    shot("screenshot-objects-menu")
    click(1240, 715, wait=1.5)     # Show as a table
    click(915, 557)
    type_text("area > 40", wait=1.5)
    away()
    shot("screenshot-objects-table")


def sc_settings():
    open_project()
    open_image()
    click(*EVA)
    click(93, 322, wait=1.5)       # Project settings…
    hover(700, 899)
    shot("screenshot-project-settings")
    click(1070, 147)               # fold General
    click(1070, 238, wait=1)       # open Object merging
    hover(700, 899)
    shot("screenshot-project-settings-cross-tile-merging")


def sc_dialogs():
    open_project()
    open_image()
    click(*EVA)
    click(80, 448, wait=1.5)       # AI training…
    hover(700, 899)
    shot("screenshot-ai-training")
    click(1310, 834)               # Close
    click(*EVA)
    click(98, 285, wait=1.5)       # Save as template…
    hover(700, 899)
    shot("screenshot-save-as-template")


def sc_modules():
    pipeline_cy5(with_preview=False)
    hover(200, STEP_Y[1])
    click(STEP_MENU_X, STEP_Y[1])
    click(234, 376, wait=1.5)      # Create module
    click(520, 159)
    type_text("Spot detection")
    click(680, 227)                # To
    click(577, 443, wait=1.5)      # #8 ClassifyObjects
    hover(700, 899)
    shot("screenshot-create-module")
    click(782, 377, wait=3)        # Create module
    hover(200, STEP_Y[1])
    click(STEP_MENU_X, STEP_Y[1])
    click(226, 432, wait=2)        # Edit module
    click(324, 162, wait=1.5)      # Settings
    click(985, 72, wait=1.5)       # Parameters
    hover(700, 899)
    shot("screenshot-module-settings")


def sc_results_list():
    results("list")
    click(600, 227, wait=1)
    away()
    shot("screenshot-results-list")
    click(150, 659)                # A row per
    click(58, 646, wait=3)         # Images
    click(38, 311, wait=1.5)       # untick Background (no objects: NaN rows)
    click(150, 711)                # Aggregate
    click(43, 762)                 # + Sum
    key("Escape")
    scroll(150, 360, -3)           # the class list down to tetraspeck@bead
    click(38, 391, wait=2)         # untick it
    away()
    shot("screenshot-results-table-view-group-by-image")
    click(266, 742, wait=3)        # Transpose
    away()
    shot("screenshot-results-side-by-side")


def sc_results_plate():
    results("plate")
    click(787, 545, wait=2)        # well C4
    away()
    shot("screenshot-results-matrix-plate-view")
    click(*CARD_BUTTON, wait=0)    # Open well ›
    sleep(3)
    # The vanished button's tooltip stays (app quirk): hover the button now
    # there and leave it, that clears it.
    hover(*CARD_BUTTON, wait=1.2)
    hover(900, 760, wait=1)
    click(516, 470, wait=1.5)      # its first image
    click(1277, 600, wait=1.5)     # the card's empty part - drops a stale tooltip
    away()
    shot("screenshot-matrix-well-view")
    click(*CARD_BUTTON, wait=0)    # Open image ›
    sleep(3)
    hover(*CARD_BUTTON, wait=1.2)
    hover(900, 760, wait=1)
    click(150, 552)                # Square size
    click(52, 671, wait=3)         # 128 px
    click(894, 410, wait=1.5)
    hover(900, 600, wait=0.2)
    away()
    shot("screenshot-results-heatmap")


def sc_results_charts():
    results("charts")
    shot("screenshot-results-histogram")
    click(222, 113, wait=4)        # Boxplot
    away()
    shot("screenshot-results-boxplot")
    click(83, 173, wait=4)         # Scatter
    click(150, 323)                # Y
    click(66, 470, wait=4)         # Circularity
    away()
    shot("screenshot-results-scatter")


def sc_results_split():
    results("list")
    click(*RESULTS_SPLIT, wait=5)
    click(300, 557, wait=4)        # a row whose object sits mid-image
    away()
    shot("screenshot-results-split-list")
    click(*RESULTS_VIEW["plate"], wait=5)
    click(475, 375, wait=4)        # well C5
    away()
    shot("screenshot-results-split-plate")
    click(*RESULTS_FULL, wait=2)   # "split" is a user setting: leave it off


def sc_results_export():
    results("list")
    click(600, 557, wait=1)
    click(*EXPORT, wait=1.5)
    hover(1000, 899)
    shot("screenshot-results-export-dialog")
    click(1047, 455, wait=1)       # More options ›
    hover(1000, 899)
    shot("screenshot-results-export-more")
    click(1266, 862)               # Close
    hover(1200, 557)
    click(1360, 557, wait=5)       # Show on image ↗
    away()
    shot("screenshot-results-on-image")


def sc_results_tracks():
    start_app("--project", str(TRACKS_PROJECT))
    click(372, 72, wait=3)         # read the folder: the viewer needs the image list
    click(200, 140, wait=4)
    click(*MODE_RESULTS, wait=2)
    click(595, 148, wait=5)        # the analysis "tracking"
    # With tracks the results bar has a fourth view: the views shift.
    click(415, 20, wait=4)         # Tracks
    click(200, 189, wait=3)        # track #2 - a straight mover
    away()
    shot("screenshot-results-tracks")
    click(1119, 828, wait=8)       # Show in image
    click(1307, 127, wait=1.5)     # Trail: Whole track
    click(1121, 828, wait=4)       # the last time point
    away()
    shot("screenshot-results-tracks-split")
    click(493, 20, wait=2)         # Full
    click(346, 20, wait=4)         # Charts
    click(213, 173, wait=5)        # Over time
    click(266, 446, wait=4)        # Individual tracks, faint
    away()
    shot("screenshot-results-over-time")


def sc_run():
    open_project()
    open_image()
    click(*RUN, wait=1.5)
    hover(1000, 760)
    shot("screenshot-start-analysis")
    click(1247, 134)
    type_text("replicate_2", wait=0.2)
    click(1381, 260, wait=0.7)     # Run - the demo plate takes ~2 s
    shot("screenshot-analysis-running", 0)
    wait_for_run_button()
    shot("screenshot-analysis-finished", 0.3)


def pixel_luma(x, y):
    out = subprocess.run(["sh", "-c", f"import -window root -crop 1x1+{x}+{y} -depth 8 txt:- | tail -1"],
                         env=env, capture_output=True, text=True).stdout
    try:
        r, g, b = (int(v) for v in out.split("(")[1].split(")")[0].split(",")[:3])
    except (IndexError, ValueError):
        return 255
    return (r * 299 + g * 587 + b * 114) // 1000


def wait_for_run_button(timeout=120):
    """Until the analysis is done: the black Run button is back in the top bar
    (while it runs, the bar shows the light progress pill there)."""
    end = time.time() + timeout
    while time.time() < end:
        if pixel_luma(RUN[0] - 25, RUN[1]) < 80:
            return
        sleep(0.3)
    print("  (the analysis didn't finish in time)")


SCENES = {
    "images": sc_images, "image-panel": sc_image_panel, "workspace": sc_workspace, "pipeline": sc_pipeline,
    "pick-pipeline": sc_pick_pipeline, "add-step": sc_add_step, "step-menu": sc_step_menu,
    "eva-menu": sc_eva_menu, "colors": sc_colors, "palette": sc_palette, "tuning": sc_tuning,
    "compare": sc_compare, "switcher": sc_switcher, "classes": sc_classes, "annotate": sc_annotate,
    "objects": sc_objects, "settings": sc_settings, "dialogs": sc_dialogs, "modules": sc_modules,
    "results-list": sc_results_list, "results-plate": sc_results_plate, "results-charts": sc_results_charts,
    "results-split": sc_results_split, "results-export": sc_results_export,
    "results-tracks": sc_results_tracks,
    "run": sc_run,                 # writes a second analysis: after the results scenes
    "series": sc_series,
    "start-page": sc_start_page,
}


def fresh_home():
    """No settings, no recent projects: the app remembers panels, the open
    pipeline list, colors and more per user - a scene mustn't inherit them."""
    shutil.rmtree(CACHE / "home", ignore_errors=True)
    (CACHE / "home").mkdir(parents=True)


def prepare_data():
    """The synthetic plate, its project and one analysis (job "dilution_series")."""
    here = Path(__file__).parent
    if not list(DATA.glob("*.ome.tif")):
        subprocess.run([sys.executable, str(here / "make_plate.py"), str(DATA)], check=True)
    subprocess.run([sys.executable, str(here / "make_project.py"), str(DATA)], check=True)
    shutil.rmtree(DATA / "results", ignore_errors=True)
    analyze(PROJECT, "dilution_series")
    if not list(TRACKS.glob("*.ome.tif")) or not TRACKS_PROJECT.exists():
        subprocess.run([sys.executable, str(here / "make_tracks.py"), str(TRACKS)], check=True)
    shutil.rmtree(TRACKS / "results", ignore_errors=True)
    analyze(TRACKS_PROJECT, "tracking", "--images", str(TRACKS))


def analyze(project, job, *extra):
    r = subprocess.run(app_command() + ["cli", "analyze", "--project", str(project), *extra,
                                        "--job-name", job, "--threads", "4"],
                       env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("cli analyze failed:\n" + r.stdout + r.stderr)


def stop_strays():
    """Closes EVAnalyzer windows left on the display by an aborted run - a
    second window on top of the first takes the clicks."""
    me = str(APP)
    for line in subprocess.run(["ps", "-eo", "pid=,args="], capture_output=True, text=True).stdout.splitlines():
        pid, _, args = line.strip().partition(" ")
        if me in args and "take.py" not in args and not args.startswith(("bash", "/bin/sh", "sh ")):
            try:
                os.kill(int(pid), 15)
            except (ProcessLookupError, PermissionError):
                pass
    time.sleep(1)


def main():
    global _target, _steps
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("scenes", nargs="*", help="scenes to run (default: all)")
    p.add_argument("--list", action="store_true", help="list the scenes")
    p.add_argument("--check", action="store_true", help="write to .cache/screenshots/check, not the docs")
    p.add_argument("--steps", action="store_true", help="also an image after each step, in .cache/screenshots/steps")
    a = p.parse_args()
    if a.list:
        print("\n".join(SCENES))
        return
    unknown = [s for s in a.scenes if s not in SCENES]
    if unknown:
        sys.exit(f"unknown scene(s): {', '.join(unknown)} - see --list")
    if not APP.exists():
        sys.exit(f"no EVAnalyzer at {APP} - set EVA_APP")
    _target = CACHE / "check" if a.check else OUT
    _steps = a.steps
    CACHE.mkdir(parents=True, exist_ok=True)
    fresh_home()
    ensure_display()
    stop_strays()
    prepare_data()
    try:
        for name in a.scenes or SCENES:
            print(name)
            stop_app()
            fresh_home()
            SCENES[name]()
    finally:
        stop_app()


if __name__ == "__main__":
    main()

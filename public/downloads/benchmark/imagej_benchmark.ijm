// Plain ImageJ/Fiji macro replicating the EXACT pipeline the EVAnalyzer Fiji plugin
// runs for evanalyzer-fiji/evanalyzer-plugin.json (function "evColoc"), traced from
// the plugin's own source (evanalyzer-imagej/src/org/danmayr/imagej):
//
//   Pipeline.preFilterSetColoc() / Filter.java:
//     - RollingBall:  BackgroundSubtracter.rollingBallBackground(radius=4, lightBackground=false,
//                     useParaboloid=true, doPresmooth=true, correctCorners=true)
//                     == run("Subtract Background...", "rolling=4 sliding");
//     - Smooth x2:    ImageProcessor.smooth() (plain 3x3 MEAN filter, not Gaussian)
//                     == run("Smooth"); run("Smooth");
//     - ApplyThershold: threshold method "Default" is literally manual mode in this
//                     codebase (see Filter.ApplyThershold) -> setThreshold(min,max)
//   EVColoc.EvCounting: Filter.AnalyzeParticles(..., minSize=0, maxSize=-1, minCircularity)
//                     (no size filter at detection time)
//   ParticleInfo.validatearticle(): a particle counts as "valid" only if
//                     min_particle_size <= area <= max_particle_size and
//                     circularity >= min_circularity
//                     -> equivalent to running Analyze Particles with that size/circularity
//                        range directly, since we only report the valid count.
//   EVColoc.calculateRoiColoc(): a channel-1 particle colocalizes with a channel-2
//                     particle if their overlap area, as a fraction of the larger of
//                     the two particle areas, is >= min_coloc_factor (1%) -> approximated
//                     here as an AND of the two valid-particle masks + Analyze Particles
//                     with no minimum size (matches evanalyzer core's minColocArea=0.0).
//
// Channel settings pulled from evanalyzer-fiji/evanalyzer-plugin.json:
//   channel 0 (index 0, "EV_DAPI"): threshold 50-65535, min particle size 5, max 999999, min circularity 0
//   channel 1 (index 1, "EV_GFP"):  threshold 200-65535, min particle size 5, max 999999, min circularity 0
//
// Usage (headless):
//   Fiji/fiji-linux-x64 --headless --run plain_macro.ijm
// (input/output paths are set directly below rather than passed as a --run
// argument string: this Fiji/ImageJ2 build's script-parameter harvester swallows
// the classic ImageJ1 'key="value"' --run argument convention before getArgument()
// ever sees it, so hardcoding here is the reliable option.)

// EDIT THESE TWO LINES before running, to point at your own image and output folders.
input = "/path/to/your/images/";
output = "/path/to/your/results/plain_macro/";

macro "PlainMacroPerformanceCheck" {
    if (!File.exists(output)) File.makeDirectory(output);

    resultsCsv = output + "results.csv";
    File.saveString("image,count_EV_DAPI,count_EV_GFP,count_coloc,area_EV_DAPI,area_EV_GFP,area_coloc\n", resultsCsv);

    run("Bio-Formats Macro Extensions");

    list = getFileList(input);
    n = 0;
    for (i = 0; i < list.length; i++) {
        name = list[i];
        if (!endsWith(toLowerCase(name), ".vsi")) continue;
        processImage(input + name, name, resultsCsv);
        n++;
    }
    print("DONE processed=" + n);
    eval("script", "System.exit(0);");
}

function processImage(path, name, resultsCsv) {
    Ext.setId(path);
    Ext.setSeries(0);

    Ext.openImage("rawEV_DAPI", 0);
    idDapi = getImageID();

    Ext.openImage("rawEV_GFP", 1);
    idGfp = getImageID();

    // -- EV_DAPI: rolling-ball bg subtract, smooth x2, manual threshold 50-65535 --
    selectImage(idDapi);
    run("Subtract Background...", "rolling=4 sliding");
    run("Smooth");
    run("Smooth");
    setThreshold(50, 65535);
    run("Convert to Mask");
    idDapiMask = getImageID();
    countDapi = countParticlesAndArea(5, 999999);

    // -- EV_GFP: rolling-ball bg subtract, smooth x2, manual threshold 200-65535 --
    selectImage(idGfp);
    run("Subtract Background...", "rolling=4 sliding");
    run("Smooth");
    run("Smooth");
    setThreshold(200, 65535);
    run("Convert to Mask");
    idGfpMask = getImageID();
    countGfp = countParticlesAndArea(5, 999999);

    // -- Colocalization: AND of the two valid-particle masks, no minimum area --
    imageCalculator("AND create", idDapiMask, idGfpMask);
    countColoc = countParticlesAndArea(0, 999999999);

    line = name + "," + countDapi[0] + "," + countGfp[0] + "," + countColoc[0] + "," +
           countDapi[1] + "," + countGfp[1] + "," + countColoc[1] + "\n";
    File.append(line, resultsCsv);

    // cleanup: close everything so the next image starts from a clean slate
    while (nImages > 0) {
        selectImage(nImages);
        close();
    }
}

// Runs Analyze Particles on the currently-selected binary mask, filtered to
// [minSize, maxSize] pixel units (matches ParticleInfo.validatearticle's area
// bounds). Returns {count, totalArea}.
function countParticlesAndArea(minSize, maxSize) {
    run("Set Measurements...", "area redirect=None decimal=3");
    run("Analyze Particles...", "size=" + minSize + "-" + maxSize + " pixel display clear summarize");
    n = nResults;
    totalArea = 0;
    for (r = 0; r < n; r++) {
        totalArea += getResult("Area", r);
    }
    result = newArray(2);
    result[0] = n;
    result[1] = totalArea;
    return result;
}

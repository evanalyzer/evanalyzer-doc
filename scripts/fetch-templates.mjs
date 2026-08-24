#!/usr/bin/env node
// Fetches project/pipeline templates from evanalyzer/evanalyzer-templates and
// turns them into this site's downloads: the raw template files under
// public/downloads/templates/, and the matching content-collection entries
// under src/content/downloads/ that DownloadGallery.astro renders.
//
// Repo layout (see evanalyzer-templates' README):
//   project_templates/evanalyzer/<name>.evapt    - built-in, flat, no metadata folder
//   project_templates/<folder>/<name>.evapt      - contributed, one folder per template,
//                                                   optional README.md and images/
//   pipeline_templates/ mirrors the same split, with .evapipe files
//
// Every template file's `meta` block (name, shortDescription, description,
// authors, tags, ...) is the source of truth for the generated frontmatter -
// nothing here is hand-authored per template.
//
// A contributed folder's `images/` directory (example micrographs etc.) is
// zipped together with the template file into a single bundle download.
//
// Everything is built in a staging area first and only swapped into place on
// success, so a network hiccup (or GitHub outage) leaves the committed
// fallback copies untouched and never breaks a docs build - it only hard-fails
// if there's no fallback at all (first-time setup).

import { execFileSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "evanalyzer/evanalyzer-templates";
const REF = "main"; // tracked live (not pinned) - a daily cron rebuild picks up new templates.

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");

const PUBLIC_OUT = path.join(ROOT, "public/downloads/templates");
const CONTENT_PROJECT_OUT = path.join(ROOT, "src/content/downloads/templates");
const CONTENT_PIPELINE_OUT = path.join(ROOT, "src/content/downloads/pipelines");

// Built inside the repo (not os.tmpdir()) so the final swap is a same-filesystem
// rename, and so a Ctrl-C or crash leaves an obviously-named leftover behind.
const STAGE_ROOT = path.join(ROOT, ".tmp-fetch-templates");

const SECTIONS = [
  {
    dir: "project_templates",
    ext: ".evapt",
    category: "template",
    contentOut: CONTENT_PROJECT_OUT,
  },
  {
    dir: "pipeline_templates",
    ext: ".evapipe",
    category: "pipeline",
    contentOut: CONTENT_PIPELINE_OUT,
  },
];

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(kb < 10 ? 1 : 0)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(mb < 10 ? 2 : 1)} MB`;
  return `${(mb / 1024).toFixed(2)} GB`;
}

function slugify(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function isDir(p) {
  return existsSync(p) && statSync(p).isDirectory();
}

function fileSizeOf(p) {
  return statSync(p).size;
}

function frontmatterEscape(str) {
  return str.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

// Zips the template file together with its images/ folder, with both at the
// zip's top level - readable to a human unzipping it, not fighting nested paths.
function createBundleZip(zipPath, templateFilePath, imagesDir) {
  const stagingDir = mkdtempSync(path.join(STAGE_ROOT, "bundle-"));
  try {
    cpSync(templateFilePath, path.join(stagingDir, path.basename(templateFilePath)));
    cpSync(imagesDir, path.join(stagingDir, "images"), { recursive: true });
    mkdirSync(path.dirname(zipPath), { recursive: true });
    execFileSync("zip", ["-r", "-X", "-q", zipPath, "."], { cwd: stagingDir });
  } finally {
    rmSync(stagingDir, { recursive: true, force: true });
  }
}

function buildContentBody(meta, readmeText) {
  const parts = [meta.description?.trim() || meta.shortDescription?.trim() || ""];

  if (meta.authors?.length) {
    const who = meta.authors.join(", ") + (meta.authorOrganization ? ` (${meta.authorOrganization})` : "");
    parts.push(`**Contributed by:** ${who}`);
  }

  if (readmeText?.trim()) {
    parts.push("## About the example data", readmeText.trim());
  }

  return parts.filter(Boolean).join("\n\n") + "\n";
}

function writeContentEntry({ contentOut, category, slug, meta, file, fileSize, bundleFile, bundleSize, readmeText }) {
  const title = meta.name?.trim() || slug;
  const description = (meta.shortDescription?.trim() || meta.description?.trim() || title).slice(0, 500);
  const tags = Array.isArray(meta.tags) ? meta.tags : [];

  const frontmatterLines = [
    "---",
    `title: "${frontmatterEscape(title)}"`,
    `description: "${frontmatterEscape(description)}"`,
    `category: ${category}`,
    `file: ${file}`,
    `fileSize: "${fileSize}"`,
  ];
  if (bundleFile) {
    frontmatterLines.push(`bundleFile: ${bundleFile}`, `bundleSize: "${bundleSize}"`);
  }
  if (tags.length) {
    frontmatterLines.push(`tags: [${tags.map((t) => `"${frontmatterEscape(t)}"`).join(", ")}]`);
  }
  frontmatterLines.push("---");

  const body = frontmatterLines.join("\n") + "\n\n" + buildContentBody(meta, readmeText);

  mkdirSync(contentOut, { recursive: true });
  writeFileSync(path.join(contentOut, `${slug}.md`), body);
}

function processTemplateFile({ section, publicSubdir, contentSlugPrefix, templateFilePath, readmePath }) {
  const meta = JSON.parse(readFileSync(templateFilePath, "utf-8")).meta ?? {};
  const stem = path.basename(templateFilePath, section.ext);
  const slug = slugify(`${contentSlugPrefix}-${stem}`);

  const publicDir = path.join(PUBLIC_OUT_STAGE, section.dir, publicSubdir);
  mkdirSync(publicDir, { recursive: true });

  const destFileName = path.basename(templateFilePath);
  const destFilePath = path.join(publicDir, destFileName);
  cpSync(templateFilePath, destFilePath);
  const fileSize = formatSize(fileSizeOf(destFilePath));
  const publicFileUrl = `/downloads/templates/${section.dir}/${publicSubdir}/${destFileName}`;

  const imagesDir = path.join(path.dirname(templateFilePath), "images");
  let bundleFile;
  let bundleSize;
  if (isDir(imagesDir)) {
    const zipName = `${stem}-with-images.zip`;
    const zipPath = path.join(publicDir, zipName);
    createBundleZip(zipPath, templateFilePath, imagesDir);
    bundleSize = formatSize(fileSizeOf(zipPath));
    bundleFile = `/downloads/templates/${section.dir}/${publicSubdir}/${zipName}`;
  }

  const readmeText = readmePath && existsSync(readmePath) ? readFileSync(readmePath, "utf-8") : undefined;

  writeContentEntry({
    contentOut: path.join(CONTENT_OUT_STAGE(section)),
    category: section.category,
    slug,
    meta,
    file: publicFileUrl,
    fileSize,
    bundleFile,
    bundleSize,
    readmeText,
  });
}

function CONTENT_OUT_STAGE(section) {
  return section.category === "template" ? CONTENT_PROJECT_OUT_STAGE : CONTENT_PIPELINE_OUT_STAGE;
}

let PUBLIC_OUT_STAGE, CONTENT_PROJECT_OUT_STAGE, CONTENT_PIPELINE_OUT_STAGE;

function main() {
  rmSync(STAGE_ROOT, { recursive: true, force: true });
  mkdirSync(STAGE_ROOT, { recursive: true });

  PUBLIC_OUT_STAGE = path.join(STAGE_ROOT, "public/downloads/templates");
  CONTENT_PROJECT_OUT_STAGE = path.join(STAGE_ROOT, "content/templates");
  CONTENT_PIPELINE_OUT_STAGE = path.join(STAGE_ROOT, "content/pipelines");
  mkdirSync(PUBLIC_OUT_STAGE, { recursive: true });
  mkdirSync(CONTENT_PROJECT_OUT_STAGE, { recursive: true });
  mkdirSync(CONTENT_PIPELINE_OUT_STAGE, { recursive: true });

  const checkoutDir = mkdtempSync(path.join(os.tmpdir(), "evanalyzer-templates-"));

  try {
    execFileSync(
      "git",
      ["clone", "--depth", "1", "--branch", REF, `https://github.com/${REPO}.git`, checkoutDir],
      { stdio: ["ignore", "ignore", "inherit"] },
    );

    let templateCount = 0;

    for (const section of SECTIONS) {
      const sectionDir = path.join(checkoutDir, section.dir);
      if (!isDir(sectionDir)) continue;

      for (const entry of readdirSync(sectionDir, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        const folderPath = path.join(sectionDir, entry.name);

        if (entry.name === "evanalyzer") {
          // Built-in templates: flat files directly in this folder, no per-template metadata folder.
          for (const file of readdirSync(folderPath)) {
            if (!file.endsWith(section.ext)) continue;
            processTemplateFile({
              section,
              publicSubdir: "evanalyzer",
              contentSlugPrefix: "evanalyzer",
              templateFilePath: path.join(folderPath, file),
            });
            templateCount++;
          }
          continue;
        }

        // Contributed template: one folder, one template file, optional README.md + images/.
        const templateFile = readdirSync(folderPath).find((f) => f.endsWith(section.ext));
        if (!templateFile) continue;
        processTemplateFile({
          section,
          publicSubdir: entry.name,
          contentSlugPrefix: entry.name,
          templateFilePath: path.join(folderPath, templateFile),
          readmePath: path.join(folderPath, "README.md"),
        });
        templateCount++;
      }
    }

    if (templateCount === 0) {
      throw new Error("No template files found in the fetched repo - refusing to replace the existing downloads.");
    }

    // Everything succeeded - swap the staged output into place.
    rmSync(PUBLIC_OUT, { recursive: true, force: true });
    mkdirSync(path.dirname(PUBLIC_OUT), { recursive: true });
    cpSync(PUBLIC_OUT_STAGE, PUBLIC_OUT, { recursive: true });

    rmSync(CONTENT_PROJECT_OUT, { recursive: true, force: true });
    cpSync(CONTENT_PROJECT_OUT_STAGE, CONTENT_PROJECT_OUT, { recursive: true });

    rmSync(CONTENT_PIPELINE_OUT, { recursive: true, force: true });
    cpSync(CONTENT_PIPELINE_OUT_STAGE, CONTENT_PIPELINE_OUT, { recursive: true });

    console.log(`[fetch-templates] Updated ${templateCount} templates from ${REPO}@${REF}.`);
  } catch (err) {
    const hasFallback = existsSync(PUBLIC_OUT) && readdirSync(PUBLIC_OUT).length > 0;
    if (hasFallback) {
      console.warn(
        `[fetch-templates] Could not refresh templates from ${REPO}@${REF} (${err.message}) - keeping the committed copies.`,
      );
    } else {
      console.error(
        `[fetch-templates] Could not fetch templates from ${REPO}@${REF} (${err.message}) and no committed fallback exists.`,
      );
      process.exitCode = 1;
    }
  } finally {
    rmSync(checkoutDir, { recursive: true, force: true });
    rmSync(STAGE_ROOT, { recursive: true, force: true });
  }
}

main();

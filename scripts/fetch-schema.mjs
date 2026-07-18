#!/usr/bin/env node
// Fetches the project/pipeline JSON schema from a pinned release tag of the
// main EVAnalyzer app repo, so it's served on this docs site at a stable URL
// and stays in sync with released versions - without floating on `main`.
//
// On any failure (network error, bad status, invalid JSON) this leaves the
// committed fallback copy in public/schema/ untouched and warns instead of
// failing the build, so a GitHub outage never breaks a docs deploy. It only
// hard-fails if there's no fallback copy at all (first-time setup).
//
// Bump REF deliberately (not "main") when the app repo ships a schema change
// that should show up in the docs.

import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "evanalyzer/evanalyzer";
const REF = "0.1.0-alpha.16";
const SCHEMA_PATH_IN_REPO = "docs/project.schema.json";
const SOURCE_URL = `https://raw.githubusercontent.com/${REPO}/${REF}/${SCHEMA_PATH_IN_REPO}`;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_PATH = path.join(__dirname, "../public/schema/project.schema.json");

try {
  const res = await fetch(SOURCE_URL, { signal: AbortSignal.timeout(15000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const text = await res.text();
  const parsed = JSON.parse(text);

  mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  writeFileSync(OUT_PATH, JSON.stringify(parsed, null, 2) + "\n");
  console.log(`[fetch-schema] Updated public/schema/project.schema.json from ${REPO}@${REF}`);
} catch (err) {
  if (existsSync(OUT_PATH)) {
    console.warn(
      `[fetch-schema] Could not refresh schema from ${REPO}@${REF} (${err.message}) - keeping the committed copy.`,
    );
  } else {
    console.error(
      `[fetch-schema] Could not fetch schema from ${REPO}@${REF} (${err.message}) and no committed fallback exists at ${OUT_PATH}.`,
    );
    process.exit(1);
  }
}

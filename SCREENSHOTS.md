# Screenshots

The screenshots of the app are taken automatically by
`scripts/screenshots/take.py` - see [scripts/screenshots/README.md](scripts/screenshots/README.md).
Re-run it after a design change:

```sh
python3 scripts/screenshots/take.py
```

Still placeholders in the docs (a dashed `evx-shot-todo` box), not scripted yet:

- [ ] **Marker and pixel values** - `guide/images.md` - `src/assets/screenshots/screenshot-image-measure-points.png`
- [ ] **Coloc pairs** - `guide/results.md` - `src/assets/screenshots/screenshot-results-coloc-details-view.png` (A row per: Coloc pairs - the demo plate's rows show no partner columns)
- [ ] **Parents and children** - `guide/results.md` - `src/assets/screenshots/screenshot-results-children.png` (needs a project with Relate Objects, e.g. spots in cells)
- [ ] **Measurements panel** - `guide/pipelines.md` - `src/assets/screenshots/screenshot-measurements-panel.png` (needs a pipeline with Measure steps and an Exclude Image)

Find them with `grep -rn evx-shot-todo src/content/docs`.

# Screenshots

The screenshots of the app are taken automatically by
`scripts/screenshots/take.py` - see [scripts/screenshots/README.md](scripts/screenshots/README.md).
Re-run it after a design change:

```sh
python3 scripts/screenshots/take.py
```

Still placeholders in the docs (a dashed `evx-shot-todo` box), not scripted yet:

- [ ] **Marker and pixel values** - `guide/images.md` - `src/assets/screenshots/screenshot-image-measure-points.png`
- [ ] **Coloc details** - `guide/results.md` - `src/assets/screenshots/screenshot-results-coloc-details-view.png` (needs data where Coloc details shows partner columns)

Find them with `grep -rn evx-shot-todo src/content/docs`.

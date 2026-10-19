# Screenshots for the redesign

Placeholders in the docs that wait for screenshots of the redesigned UI (the `ai-plugin` branch).
Each one is a `<div class="evx-shot-todo">` block in the page; replace it with the image once taken.
*update* replaces an old screenshot, *new* is a screenshot that didn't exist before.

Regenerate this list: `grep -rn evx-shot-todo src/content/docs`.


## ai/training.md

- [ ] **Train classifier** (update) - The Train classifier sheet on the right: Pixel / Object, the classes with their counts, the training in short, "Uses the annotations of N images" - training a neural-network pixel classifier.  
  `src/assets/screenshots/screenshot-ai-training.png`

## fundamentals/cross-tile-merging.md

- [ ] **Object merging settings** (update) - The settings sheet searched for "merge": Merge objects across tiles, Exclude classes, Connectivity, Max fragments per group.  
  `src/assets/screenshots/screenshot-project-settings-cross-tile-merging.png`

## getting-started/first-steps.md

- [ ] **Start page** (update) - Open image folder…, Open project…, Empty project, New project from a template…, Connect to a server…, and the recent projects.  
  `src/assets/getting-started/screenshot-start-page.png`
- [ ] **Classes panel** (update) - The Classes panel on the right with a few classes, its ⋯ menu open on "Add classes from the image".  
  `src/assets/screenshots/screenshot-classification.png`
- [ ] **Edit pipeline dialog** (update) - The dialog next to the steps panel: Pipeline name, Image source (Channel picked, the channel picker open).  
  `src/assets/getting-started/screenshot-pipeline-edit.png`
- [ ] **Run analysis dialog** (update) - The dialog below the Run button: "N pipelines · M images", the job name field, Run.  
  `src/assets/screenshots/screenshot-start-analysis.png`
- [ ] **Results, list view** (update) - Results mode with a fresh analysis open: the list's settings on the left, the table of objects beside them.  
  `src/assets/screenshots/screenshot-results-list.png`

## guide/classification.md

- [ ] **Class settings** (update) - The Class settings dialog left of the right-hand panels: Name, Notes, Class ID with Auto, the color grid (7 a row).  
  `src/assets/screenshots/screenshot-class-settings.png`
- [ ] **Objects as a table** (new) - The objects table at the bottom of the window, a class chip and "area > 50" in its head, one row selected with its buttons.  
  `src/assets/screenshots/screenshot-objects-table.png`
- [ ] **Objects panel with a selected object** (update) - The Objects list on the right, one object selected; its card beside it with classes, area, circularity, means, Coloc with.  
  `src/assets/screenshots/screenshot-roi-list.png`

## guide/command-groups.md

- [ ] **Create component** (update) - The Create component dialog next to the steps panel: Component name, From / To, the classes with their roles.  
  `src/assets/screenshots/screenshot-create-component.png`
- [ ] **Component settings, Parameters** (update) - The Parameters tab: the list by section on the left, one parameter's form with Sets chips on the right.  
  `src/assets/screenshots/screenshot-component-settings.png`

## guide/images.md

- [ ] **Images panel, Plate** (update) - Images mode, the panel on Plate: wells with their state bars, one well picked and its images listed below. A second shot on List.  
  `src/assets/screenshots/screenshot-images-plate.png · screenshot-images-list.png`
- [ ] **Image info** (update) - The Image info card with All metadata › open: channels with their colors, pixel size, frame interval; one value marked "edited".  
  `src/assets/screenshots/screenshot-image-meta.png`
- [ ] **Channel color chooser** (update) - The color chooser open from a channel swatch: wavelength tiles, Emission (nm), Reset and Done.  
  `src/assets/screenshots/screenshot-image-channel-color.png`
- [ ] **Image panel** (update) - The Image panel: channels with eyes, Grayscale / Show objects, Overlay, the histogram with its black and white lines, Values › open, Z and T rows.  
  `src/assets/screenshots/screenshot-image-panel.png`
- [ ] **Series question** (new) - "Which series" over the image - the series with their sizes, Decide later.  
  `src/assets/screenshots/screenshot-series.png`
- [ ] **Marker and pixel values** (update) - A marker on the image with the values of all channels, the bottom bar showing position and pixel value.  
  `src/assets/screenshots/screenshot-image-measure-points.png`
- [ ] **Annotate mode with the brush** (new) - The annotate bar with Brush active, Paint as "Class 1", Size 12 - a painted region on the image.  
  `src/assets/screenshots/screenshot-annotate-brush.png`

## guide/pipelines.md

- [ ] **Steps panel** (update) - Pipelines mode: the steps panel with 5–6 steps, colored stripes, one step open with its settings, a breakpoint on one step number.  
  `src/assets/screenshots/screenshot-pipeline.png`
- [ ] **Pipeline switcher** (new) - The switcher open from the steps panel's head: pipelines with ⋮⋮, one being dragged, New pipeline at the bottom.  
  `src/assets/screenshots/screenshot-pipeline-switcher.png`
- [ ] **Edit pipeline dialog** (update) - Pipeline name and Image source, next to the steps panel.  
  `src/assets/screenshots/screenshot-add-pipeline-dialog.png`
- [ ] **Add step** (update) - The command picker next to the steps panel: category chips, the list, the description pane, "✓ Added … as step 3" in the footer.  
  `src/assets/screenshots/screenshot-add-pipeline-step.png`
- [ ] **Step settings dialog** (new) - "Threshold · step 3 · settings" next to the steps panel: the tabs, the search, the setting rows.  
  `src/assets/screenshots/screenshot-step-settings.png`
- [ ] **Tuning panel** (new) - The Tuning panel next to the steps with "All pinned · 4" and a tab per step; settings of two steps pinned.  
  `src/assets/screenshots/screenshot-tuning.png`
- [ ] **Compare** (new) - A breakpoint on Threshold, Compare on: the original left, the mask right, the divider in the middle.  
  `src/assets/screenshots/screenshot-compare.png`
- [ ] **Focus mode** (update) - A pipeline focused: the "Focused on …" banner above the classes, only its channel visible.  
  `src/assets/screenshots/screenshot-pipeline-focus.png`
- [ ] **Save as template** (update) - The Save as template dialog: Name, Short description, Description, Author, Organization.  
  `src/assets/screenshots/screenshot-save-as-template.png`

## guide/results.md

- [ ] **Results, List view** (update) - Results mode with List: the results bar on top, the settings panel on the left (A row per, Images / Classes / Columns), the table beside it with one row selected.  
  `src/assets/screenshots/screenshot-results-list.png`
- [ ] **A result on its image** (new) - After Show on image ↗: the image with the object marked and the bar "RESULTS · Row 12 of 200 ‹ › Back to results ✕" at the top.  
  `src/assets/screenshots/screenshot-results-on-image.png`
- [ ] **Rows per image, aggregated** (update) - A row per: Images, Aggregate: Average and Sum - columns doubled per aggregation.  
  `src/assets/screenshots/screenshot-results-table-view-group-by-image.png`
- [ ] **Transposed table** (update) - Transpose on, a row per image: one column block per class.  
  `src/assets/screenshots/screenshot-results-side-by-side.png`
- [ ] **Coloc details** (update) - Coloc details on: partner columns per class, dashes where no partner was found.  
  `src/assets/screenshots/screenshot-results-coloc-details-view.png`
- [ ] **Charts** (update) - Three shots: Histogram, Scatter, and Boxplot with "A box per: well".  
  `src/assets/screenshots/screenshot-results-histogram.png · screenshot-results-scatter.png · screenshot-results-boxplot.png`
- [ ] **Plate view** (update) - A 96-well plate heatmap, one well selected - its card on the right with the value and the well's images.  
  `src/assets/screenshots/screenshot-results-matrix-plate-view.png`
- [ ] **Well view** (update) - Inside a well: the images as a grid, the breadcrumb "Plate › Well C3" in the top bar, one image left out (crossed out).  
  `src/assets/screenshots/screenshot-matrix-well-view.png`
- [ ] **Image heatmap** (update) - One image binned into tiles, one tile selected with Show on image ↗ in its card.  
  `src/assets/screenshots/screenshot-results-heatmap.png`
- [ ] **Split with image, List** (new) - The list on the left, one row selected; the image on the right with the object ringed and its card.  
  `src/assets/screenshots/screenshot-results-split-list.png`
- [ ] **Split with image, Plate** (new) - The plate heatmap on the left, a well selected; its images as a filmstrip under the image, Color by: Value.  
  `src/assets/screenshots/screenshot-results-split-plate.png`
- [ ] **Export** (update) - The export card below Export…: the four kinds, Format, Classes, To - and a second shot with More options › open.  
  `src/assets/screenshots/screenshot-results-export-dialog.png`

## guide/settings.md

- [ ] **Settings** (update) - The settings sheet on the right: the search on top, Project › General open, Plate & grouping and Object merging folded, This computer › Viewport below.  
  `src/assets/screenshots/screenshot-project-settings.png`

## guide/workspace.md

- [ ] **The whole workspace, Pipelines mode** (new) - Top bar, steps panel on the left, Classes / Objects / Image panels on the right, the bottom bar with Images · Pipelines · Results. Light colors.  
  `src/assets/screenshots/screenshot-workspace.png`
- [ ] **Start page** (new) - The four actions, Connect to a server…, and a few recent projects - cells drifting in the background.  
  `src/assets/screenshots/screenshot-start-page.png`
- [ ] **Command palette** (new) - Ctrl+K open over the workspace, typed "thresh" - actions, a step, a setting and commands in the results.  
  `src/assets/screenshots/screenshot-command-palette.png`
- [ ] **Light, Dark and Dim** (new) - The same workspace in the three color schemes, side by side (or three screenshots for a compare slider).  
  `src/assets/screenshots/screenshot-colors-light.png · -dark.png · -dim.png`
- [ ] **Analysis running while editing** (new) - The progress card at the bottom right, the steps panel still open and editable.  
  `src/assets/screenshots/screenshot-analysis-running.png`

## index.mdx

- [ ] **Pipeline preview, light and dark** (update) - The same zoomed-in pipeline preview - nuclei with segmentation overlays - in Light and in Dark, for the compare slider.  
  `src/assets/screenshots/screenshot-pipeline-zoom.png · screenshot-pipeline-dark-zoom.png`

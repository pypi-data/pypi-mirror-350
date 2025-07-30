# twotuft2count

`twotuft2count` is a modular and extensible pipeline for counting tuft cells (or any cell type) in immunofluorescence images. It allows to go from raw TIFF stacks to single-cell data using a **fully scriptable and inspectable CLI**, with napari support for interactive visualization.

---

## Features

- Combine single-channel TIFFs into multi-channel images
- Run **cell segmentation** via InstanSeg 
- Measure **per-cell marker intensities** 
- Export **CSV + FCS** files for each image
- Interactively **gate and threshold** via Napari or FlowJo
- Quantify marker-positive cells (with or without DAPI restriction)
- Share thresholds across datasets for reproducibility
- CLI-friendly: `twotuft2count combine ...` through `quantify ...`

---

## Example Workflow

Assuming your individual single-channel images are in `raw_images/`, and you’ve defined a `panel.csv`:

```bash
twotuft2count combine raw_images img
twotuft2count segment img masks
twotuft2count measure img masks --panel panel.csv
twotuft2count visualize sample1 --panel panel.csv
twotuft2count quantify --panel panel.csv --use-manual-thresholds --threshold-source-image sample1
```

---

## Input Requirements

### `panel.csv`

This file defines which image channel corresponds to which marker:

| channel | marker   |
|---------|----------|
| 0       | DAPI     |
| 1       | EpCAM    |
| 2       | DCLK1    |
| 3       | SiglecF  |

### TIFF images

- Expected format: `.tif` or `.tiff`
- Combined TIFFs should have shape: `(C, H, W)` or `(H, W, C)` depending on backend
- Segmentation masks should be label images with unique integer IDs

---

##  Installation

Install via pip from PyPI:

```bash
pip install twotuft2count
```

Or install in editable mode from source:

```bash
git clone https://github.com/pfluec/twotuft2count.git
cd twotuft2count
pip install -e .
```

---

## Commands

| Command    | Description                                         |
|------------|-----------------------------------------------------|
| `combine`  | Stack single-channel TIFFs into multi-channel images |
| `segment`  | Run segmentation (InstanSeg)                        |
| `measure`  | Extract per-cell intensities + export to CSV/FCS    |
| `visualize`| Napari-based GUI for interactive threshold tuning   |
| `quantify` | Compute marker+ and double-positive cell types      |

Run `twotuft2count [command] --help` to view CLI options.

---

## GUI-Based Thresholding

The `visualize` command launches a Napari window to:
- Adjust marker thresholds interactively
- See point overlays and cell label masks update in real-time
- Save threshold profiles to reuse across images

---

## Outputs

- Per-cell CSVs (intensities, areas, regionprops)
- Individual and merged `.fcs` files for analysis in FlowJo
- Quantification summaries (CSV) per image
- `_thresholds.json` files for reproducible gating

---

## License

MIT License

---

## Citation / Attribution

If you use `twotuft2count` in your work, please cite the GitHub repository.

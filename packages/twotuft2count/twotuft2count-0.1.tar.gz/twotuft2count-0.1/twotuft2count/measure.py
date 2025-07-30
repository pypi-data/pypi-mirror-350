import os
import numpy as np
import tifffile
import pandas as pd
import scipy.ndimage
from skimage.filters import threshold_otsu
from skimage.measure import regionprops_table
from fcswrite import write_fcs


def measure_intensities(image_dir, mask_dir, csv_dir='csv', fcs_dir='fcs', combined_fcs_path='all_images_fcs', panel=None):
    """
    Measures per-cell intensity and morphology features based on segmented masks and multi-channel images.

    Arguments:
    - image_dir: folder with multi-channel TIFF images
    - mask_dir: folder with corresponding label masks
    - csv_dir: directory where per-image CSVs will be saved (default: 'csv')
    - fcs_dir: directory where per-image FCS files will be saved (default: 'fcs')
    - combined_fcs_path: path to write a merged FCS file of all measurements
    - panel: path to panel.csv with two columns: 'channel' (index) and 'marker' (name)

    Note: The panel defines marker names and must match the number of image channels.
    """

    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(fcs_dir, exist_ok=True)
    os.makedirs(os.path.dirname(combined_fcs_path), exist_ok=True)

    all_measurements = []

    for fname in os.listdir(image_dir):
        if not fname.endswith(".tiff") and not fname.endswith(".tif"):
            continue

        image_path = os.path.join(image_dir, fname)
        mask_path = os.path.join(mask_dir, fname)
        if not os.path.exists(mask_path):
            print(f"Warning: mask not found for {fname}, skipping.")
            continue

        output_csv = os.path.join(csv_dir, fname.replace(".tiff", ".csv").replace(".tif", ".csv"))

        # Load image and mask
        image = tifffile.imread(image_path)
        mask = tifffile.imread(mask_path).astype(np.int32)

        if image.ndim == 3 and image.shape[0] < 41:
            channels = image
        elif image.ndim == 3 and image.shape[2] < 41:
            channels = np.moveaxis(image, -1, 0)
        else:
            raise ValueError(f"Image shape not recognized: {image.shape}")

        # Load panel if provided
        if panel is not None:
            try:
                panel_df = pd.read_csv(panel)
            except (UnicodeDecodeError, pd.errors.ParserError):
                panel_df = pd.read_csv(panel, encoding='ISO-8859-1', engine='python')
            panel_df = panel_df.sort_values("channel")
            if len(panel_df) != channels.shape[0]:
                raise ValueError(
                    f"Mismatch between image channels ({channels.shape[0]}) and panel ({len(panel_df)}).")
            channel_names = panel_df["marker"].tolist()
        else:
            channel_names = [f"ch{i}" for i in range(channels.shape[0])]

        # Regionprops
        props = ['label', 'area', 'centroid', 'axis_major_length', 'axis_minor_length']
        props_table = regionprops_table(mask, properties=props)
        region_df = pd.DataFrame(props_table).rename(columns={'label': 'Object'})
        object_ids = region_df['Object'].values

        # Intensities
        intensity_data = {}
        for i, ch in enumerate(channels):
            otsu = threshold_otsu(ch)
            ch_thresh = np.where(ch >= otsu, ch, 1)
            name = channel_names[i]
            # intensity_data[f"{name}_mean"] = scipy.ndimage.mean(ch_thresh, labels=mask, index=object_ids)
            intensity_data[f"{name}_sum"] = scipy.ndimage.sum_labels(ch_thresh, labels=mask, index=object_ids)
            # intensity_data[f"{name}_median"] = scipy.ndimage.median(ch_thresh, labels=mask, index=object_ids)

        intensity_df = pd.DataFrame(intensity_data, index=object_ids).reset_index().rename(columns={'index': 'Object'})
        full_df = pd.merge(region_df, intensity_df, on='Object', how='inner')
        full_df["image"] = fname

        # Save CSV
        full_df.to_csv(output_csv, index=False)
        print(f"Saved CSV: {output_csv}")

        # Save FCS
        fcs_out_path = os.path.join(fcs_dir, fname.replace(".tiff", ".fcs").replace(".tif", ".fcs"))
        numeric_df = full_df.select_dtypes(include=[np.number])
        write_fcs(fcs_out_path, numeric_df.columns.tolist(), numeric_df.values)
        print(f"Saved FCS: {fcs_out_path}")

        all_measurements.append(full_df)

    # Save merged FCS
    if all_measurements:
        full_cat = pd.concat(all_measurements, ignore_index=True)
        numeric_df = full_cat.select_dtypes(include=[np.number])
        write_fcs(combined_fcs_path, numeric_df.columns.tolist(), numeric_df.values)
        print(f"Saved combined FCS: {combined_fcs_path}")

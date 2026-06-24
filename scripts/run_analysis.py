#!/usr/bin/env python3
"""Run coastal water quality analysis on default Tanager scene."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tanager_coastal.indices import compute_water_indices, multispectral_ndwi_approx
from tanager_coastal.stac import asset_href, get_item
from tanager_coastal.viz import load_cloud_mask, load_cog, plot_rgb_and_indices

COLLECTION = "coastal-water-bodies"
SCENE = "20250626_082641_74_4001"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"


def run_hyperspectral() -> dict[str, np.ndarray] | None:
    sr_files = list(DATA_DIR.glob("*_ortho_sr_hdf5.h5"))
    if not sr_files:
        print("No ortho_sr_hdf5 found — run: python scripts/download_scene.py --full")
        return None

    import hypercoast

    item = get_item(COLLECTION, SCENE)
    dataset = hypercoast.read_tanager(sr_files[0], stac_url=asset_href(item, "ortho_sr_hdf5"))
    reflectance = dataset["surface_reflectance"].values
    wavelengths = dataset["wavelength"].values

    udm_files = list(DATA_DIR.glob("*_ortho_beta_udm.tif"))
    nodata_mask = load_cloud_mask(udm_files[0]) if udm_files else None

    indices = compute_water_indices(reflectance, wavelengths, nodata_mask=nodata_mask)
    indices["ndwi_multispectral"] = multispectral_ndwi_approx(
        reflectance, wavelengths, nodata_mask=nodata_mask
    )
    return indices


def run_quick_rgb() -> np.ndarray:
    visual_files = list(DATA_DIR.glob("*_ortho_visual.tif"))
    if not visual_files:
        raise FileNotFoundError("Run: python scripts/download_scene.py")
    rgb, _ = load_cog(visual_files[0])
    return rgb


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rgb = run_quick_rgb()

    indices = run_hyperspectral()
    if indices is None:
        print("Quick mode: saved RGB preview only.")
        fig, ax = plt.subplots(figsize=(10, 8))
        display = np.moveaxis(rgb[:3], 0, -1)
        display = np.clip(display / np.percentile(display, 98), 0, 1)
        ax.imshow(display)
        ax.set_title(f"Tanager {SCENE} — southern Mozambique coast")
        ax.axis("off")
        out = OUTPUT_DIR / "rgb_preview.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        print(f"wrote {out}")
        return

    plot_rgb_and_indices(
        rgb,
        indices,
        title=f"Tanager coastal water quality — {SCENE}",
        output=OUTPUT_DIR / "water_quality_maps.png",
    )

    diff = np.nanmean(np.abs(indices["ndwi"] - indices["ndwi_multispectral"]))
    print(f"Mean |NDWI_hyperspectral - NDWI_8band| = {diff:.4f}")


if __name__ == "__main__":
    main()

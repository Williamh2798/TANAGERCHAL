"""Plotting helpers for Tanager coastal analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.plot import show


def load_cog(path: str | Path) -> tuple[np.ndarray, dict]:
    with rasterio.open(path) as src:
        data = src.read(out_shape=(src.count, 512, 512), resampling=Resampling.bilinear)
        meta = src.meta.copy()
    return data, meta


def load_cloud_mask(path: str | Path) -> np.ndarray:
    with rasterio.open(path) as src:
        mask = src.read(1)
    return mask != 0


def plot_rgb_and_indices(
    rgb: np.ndarray,
    indices: dict[str, np.ndarray],
    *,
    title: str,
    output: str | Path | None = None,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(title, fontsize=14)

    rgb_display = np.moveaxis(rgb[:3], 0, -1)
    rgb_display = np.clip(rgb_display / np.percentile(rgb_display, 98), 0, 1)
    axes[0, 0].imshow(rgb_display)
    axes[0, 0].set_title("True color (ortho_visual)")
    axes[0, 0].axis("off")

    panels = [
        ("NDWI (water extent)", indices["ndwi"], "Blues"),
        ("Turbidity proxy (665/850)", indices["turbidity_proxy"], "YlOrBr"),
        ("Chlorophyll proxy (705/665)", indices["chlorophyll_proxy"], "Greens"),
    ]
    for ax, (label, arr, cmap) in zip(axes.flat[1:], panels):
        im = ax.imshow(arr, cmap=cmap)
        ax.set_title(label)
        ax.axis("off")
        fig.colorbar(im, ax=ax, fraction=0.046)

    plt.tight_layout()
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=150, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()

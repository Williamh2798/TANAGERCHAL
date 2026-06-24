"""Spectral indices for coastal water quality from Tanager surface reflectance."""

from __future__ import annotations

import numpy as np


def band_index_for_wavelength(wavelengths_nm: np.ndarray, target_nm: float) -> int:
    """Return band index closest to target wavelength."""
    return int(np.argmin(np.abs(wavelengths_nm - target_nm)))


def compute_water_indices(
    reflectance: np.ndarray,
    wavelengths_nm: np.ndarray,
    *,
    nodata_mask: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """
    Compute coastal water indices from a hyperspectral cube.

    reflectance shape: (bands, rows, cols) or (rows, cols, bands)
    """
    if reflectance.ndim != 3:
        raise ValueError("reflectance must be a 3D array")

    if reflectance.shape[0] < reflectance.shape[-1]:
        cube = reflectance
    else:
        cube = np.moveaxis(reflectance, -1, 0)

    green = cube[band_index_for_wavelength(wavelengths_nm, 560)]
    red = cube[band_index_for_wavelength(wavelengths_nm, 665)]
    red_edge = cube[band_index_for_wavelength(wavelengths_nm, 705)]
    nir = cube[band_index_for_wavelength(wavelengths_nm, 850)]

    eps = 1e-6
    ndwi = (green - nir) / (green + nir + eps)
    turbidity_proxy = red / (nir + eps)
    chl_proxy = red_edge / (red + eps)

    if nodata_mask is not None:
        for arr in (ndwi, turbidity_proxy, chl_proxy):
            arr[nodata_mask] = np.nan

    return {
        "ndwi": ndwi.astype(np.float32),
        "turbidity_proxy": turbidity_proxy.astype(np.float32),
        "chlorophyll_proxy": chl_proxy.astype(np.float32),
    }


def multispectral_ndwi_approx(
    reflectance: np.ndarray,
    wavelengths_nm: np.ndarray,
    *,
    nodata_mask: np.ndarray | None = None,
) -> np.ndarray:
    """
    Approximate PlanetScope-style NDWI using only ~8 broad bands
    (simulated by picking nearest Tanager bands).
    """
    broad_targets = [490, 560, 665, 705, 740, 783, 842, 865]
    indices = [band_index_for_wavelength(wavelengths_nm, wl) for wl in broad_targets]
    green_idx = indices[1]
    nir_idx = indices[-1]

    if reflectance.shape[0] < reflectance.shape[-1]:
        green = reflectance[green_idx]
        nir = reflectance[nir_idx]
    else:
        green = reflectance[..., green_idx]
        nir = reflectance[..., nir_idx]

    eps = 1e-6
    ndwi = (green - nir) / (green + nir + eps)
    if nodata_mask is not None:
        ndwi = ndwi.astype(np.float32)
        ndwi[nodata_mask] = np.nan
    return ndwi.astype(np.float32)

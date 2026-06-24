# Tanager Coastal Monitor

Hyperspectral coastal water quality analysis using Planet's [Tanager Open STAC catalog](https://www.planet.com/data/stac/browser/tanager-core-imagery/catalog.json).

**Submission type:** Code & scripts (Jupyter notebook + GitHub repo)  
**Competition:** [Tanager Open Data Competition](https://learn.planet.com/2026-Tanager-Open-Data-Competition.html)  
**Deadline:** August 31, 2026

## Project summary

Mozambique's coastline is highly exposed to cyclones, flooding, and sediment plumes that degrade lagoon and estuary water quality. This project demonstrates how **Tanager-1 hyperspectral imagery** can map coastal water extent, turbidity, and chlorophyll proxies at 30 m resolution — and why **426 narrow bands** outperform a simulated 8-band multispectral workflow for separating sediment-laden water from clear ocean and vegetated shoreline.

**Primary scene:** [`20250626_082641_74_4001`](https://www.planet.com/data/stac/browser/tanager-core-imagery/coastal-water-bodies/20250626_082641_74_4001/20250626_082641_74_4001.json) — southern Mozambique coast (coastal-water-bodies collection, CC BY 4.0)

## STAC catalog overview

| Collection | Scenes | Example use |
|------------|--------|-------------|
| [Coastal and Water Bodies](https://www.planet.com/data/stac/browser/tanager-core-imagery/coastal-water-bodies/collection.json) | 43 | Water quality, turbidity, algal blooms |
| [Agriculture](https://www.planet.com/data/stac/browser/tanager-core-imagery/agriculture/collection.json) | 44 | Crop stress, soil |
| [Natural Lands](https://www.planet.com/data/stac/browser/tanager-core-imagery/natural-lands/collection.json) | 72 | Ecosystem health |
| [Urban](https://www.planet.com/data/stac/browser/tanager-core-imagery/urban/collection.json) | 58 | Infrastructure, impervious surface |
| [GHGs and Other Gases](https://www.planet.com/data/stac/browser/tanager-core-imagery/GHG-plumes/collection.json) | 8 | Methane plumes |
| [Fire](https://www.planet.com/data/stac/browser/tanager-core-imagery/fire/collection.json) | 11 | Burn scars |
| [Energy and Mining](https://www.planet.com/data/stac/browser/tanager-core-imagery/energy-mining/collection.json) | 17 | Mineral mapping |
| [Snow and Ice](https://www.planet.com/data/stac/browser/tanager-core-imagery/snow-ice/collection.json) | 7 | Cryosphere |
| [ROCX 2025](https://www.planet.com/data/stac/browser/tanager-core-imagery/ROCX2025/collection.json) | 16 | Conference demo sites |

Each item includes assets such as `ortho_visual` (RGB COG), `ortho_sr_hdf5` (surface reflectance cube), and `ortho_beta_udm` (cloud/nodata mask). See [Planet Tanager documentation](https://docs.planet.com/data/imagery/tanager/).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download RGB + cloud mask (~few MB)
python scripts/download_scene.py

# Optional: full hyperspectral cube for notebook analysis
python scripts/download_scene.py --full

# Find scenes near a location
python scripts/find_scenes.py 34.85 -19.83

# Run analysis notebook
jupyter notebook notebooks/coastal_mozambique.ipynb
```

## Repository layout

```
├── notebooks/coastal_mozambique.ipynb   # Main competition analysis
├── src/tanager_coastal/                 # STAC + index utilities
├── scripts/download_scene.py            # Fetch STAC assets
├── scripts/find_scenes.py               # Search by location
├── SUBMISSION.md                          # Draft survey answers (Q6–Q7)
└── outputs/                               # Generated figures (gitignored)
```

## Methods

1. **Discover** scenes via STAC (`pystac-client` or `tanager_coastal.stac`)
2. **Load** ortho surface reflectance with [HyperCoast](https://hypercoast.org/examples/tanager/) (`read_tanager_stac`)
3. **Mask** clouds using `ortho_beta_udm`
4. **Compute** NDWI, turbidity proxy (665/850 nm), chlorophyll proxy (705/665 nm red-edge)
5. **Compare** full hyperspectral indices vs. simulated PlanetScope 8-band NDWI

## Data license

Tanager Open STAC data is released under **CC BY 4.0**. Cite Planet Labs PBC and link to the [Open STAC catalog](https://www.planet.com/data/stac/browser/tanager-core-imagery/catalog.json).

## References

- Planet Tanager docs: https://docs.planet.com/data/imagery/tanager/
- HyperCoast Tanager example: https://hypercoast.org/examples/tanager/
- Competition terms: https://planet.widen.net/s/mxxxjcppk8/planet-termsconditions-tanagercompetition

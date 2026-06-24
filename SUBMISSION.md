# Draft answers for SurveyMonkey submission

Use these as starting points — personalize names, email, and organization before submitting at  
https://www.surveymonkey.com/r/tanager-competition

---

## Q6 — Project Description (≤300 words)

**Stakeholders:** Coastal resource managers in Mozambique, humanitarian agencies monitoring post-cyclone flooding (e.g., Beira corridor), fisheries cooperatives, and researchers studying Western Indian Ocean lagoon health benefit from repeatable, open water-quality maps.

**Actionable insights:** This project maps coastal water extent (NDWI), turbidity, and chlorophyll proxies from Tanager-1 surface reflectance over southern Mozambique. Outputs support decisions on shellfish harvesting closures, sediment plume tracking after extreme rainfall, and prioritizing field sampling in turbid nearshore zones.

**The Tanager contribution:** Tanager's ~426 bands (380–2500 nm, ~5 nm spacing) enabled red-edge chlorophyll and narrow NIR turbidity indices that a simulated 8-band multispectral stack blurred together. Surface reflectance (`ortho_sr_hdf5`) and cloud masks from the [Open STAC catalog](https://www.planet.com/data/stac/browser/tanager-core-imagery/catalog.json) provided analysis-ready cubes without proprietary API access. HyperCoast streamlined STAC download, gridding, and visualization. The red-edge band near 705 nm was especially valuable for separating vegetated shoreline from turbid water — a distinction that collapsed when we approximated PlanetScope-style broad bands.

---

## Q7 — Next Steps (≤100 words)

With expanded Tanager coverage we would: (1) time-series analysis along the full Mozambique coast including **Beira** and Búzi estuary (featured in competition materials but not yet in open STAC); (2) validate indices against in-situ water samples; (3) automate STAC-driven processing for cyclone-season monitoring; and (4) compare Tanager retrievals with EMIT and Sentinel-2 over overlapping dates. Additional scenes would let us train a lightweight classifier for sediment vs. algal turbidity using full spectral shape rather than three broad indices.

---

## Q8 — Project Materials link

After pushing to GitHub, use:

`https://github.com/YOUR_USERNAME/TANAGERCHAL`

Ensure the repo is public and includes `notebooks/coastal_mozambique.ipynb`, `README.md`, and `outputs/` figures.

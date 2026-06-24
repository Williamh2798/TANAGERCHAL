"""Planet Tanager Open STAC helpers."""

from __future__ import annotations

from typing import Any

import requests

STAC_ROOT = "https://www.planet.com/data/stac/tanager-core-imagery/catalog.json"
BROWSER_ROOT = (
    "https://www.planet.com/data/stac/browser/tanager-core-imagery/catalog.json"
)

COLLECTIONS = {
    "ghg-plumes": "GHG-plumes",
    "energy-mining": "energy-mining",
    "natural-lands": "natural-lands",
    "agriculture": "agriculture",
    "coastal-water-bodies": "coastal-water-bodies",
    "urban": "urban",
    "snow-ice": "snow-ice",
    "fire": "fire",
    "rocx2025": "ROCX2025",
}


def _get_json(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()


def list_collections() -> list[dict[str, str]]:
    catalog = _get_json(STAC_ROOT)
    rows: list[dict[str, str]] = []
    for link in catalog.get("links", []):
        if link.get("rel") != "child":
            continue
        slug = link["href"].rstrip("/").split("/")[-2]
        rows.append({"id": slug, "title": link.get("title", slug), "href": link["href"]})
    return rows


def get_collection(collection_id: str) -> dict[str, Any]:
    slug = COLLECTIONS.get(collection_id, collection_id)
    return _get_json(f"{STAC_ROOT.rsplit('/', 1)[0]}/{slug}/collection.json")


def get_item(collection_id: str, item_id: str) -> dict[str, Any]:
    slug = COLLECTIONS.get(collection_id, collection_id)
    return _get_json(
        f"{STAC_ROOT.rsplit('/', 1)[0]}/{slug}/{item_id}/{item_id}.json"
    )


def search_items(
    collection_id: str,
    *,
    lon: float | None = None,
    lat: float | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return STAC items sorted by distance to (lon, lat) when provided."""
    collection = get_collection(collection_id)
    items: list[dict[str, Any]] = []
    for link in collection.get("links", []):
        if link.get("rel") != "item":
            continue
        item = _get_json(link["href"])
        if lon is not None and lat is not None:
            bbox = item.get("bbox") or []
            if len(bbox) == 4:
                center_lon = (bbox[0] + bbox[2]) / 2
                center_lat = (bbox[1] + bbox[3]) / 2
                item["_distance_deg"] = (
                    (center_lon - lon) ** 2 + (center_lat - lat) ** 2
                ) ** 0.5
        items.append(item)

    if lon is not None and lat is not None:
        items.sort(key=lambda row: row.get("_distance_deg", 999))
    return items[:limit]


def asset_href(item: dict[str, Any], asset_key: str) -> str:
    try:
        return item["assets"][asset_key]["href"]
    except KeyError as exc:
        available = ", ".join(sorted(item.get("assets", {})))
        raise KeyError(f"Asset '{asset_key}' not found. Available: {available}") from exc

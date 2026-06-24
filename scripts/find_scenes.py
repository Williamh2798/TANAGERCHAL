#!/usr/bin/env python3
"""Find Tanager coastal STAC scenes near a target location."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


def fetch_json(url: str) -> dict[str, Any]:
    out = subprocess.check_output(["curl", "-s", url], text=True)
    return json.loads(out)


def main() -> None:
    lon = float(sys.argv[1]) if len(sys.argv) > 1 else 34.85
    lat = float(sys.argv[2]) if len(sys.argv) > 2 else -19.83
    collection_url = (
        "https://www.planet.com/data/stac/tanager-core-imagery/"
        "coastal-water-bodies/collection.json"
    )
    coll = fetch_json(collection_url)
    items = [link["href"] for link in coll["links"] if link.get("rel") == "item"]
    matches: list[tuple[float, str, list[float], str | None]] = []

    for href in items:
        item = fetch_json(href)
        bbox = item.get("bbox") or []
        if len(bbox) != 4:
            continue
        center_lon = (bbox[0] + bbox[2]) / 2
        center_lat = (bbox[1] + bbox[3]) / 2
        dist = ((center_lon - lon) ** 2 + (center_lat - lat) ** 2) ** 0.5
        matches.append((dist, item["id"], bbox, item.get("properties", {}).get("datetime")))

    matches.sort()
    print(f"Target: ({lon}, {lat}) — {len(items)} coastal scenes")
    for dist, scene_id, bbox, dt in matches[:10]:
        print(f"  dist={dist:.2f}°  {scene_id}  {dt}  bbox={bbox}")


if __name__ == "__main__":
    main()

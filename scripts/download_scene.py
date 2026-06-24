#!/usr/bin/env python3
"""Download Tanager assets for a STAC item."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tanager_coastal.stac import asset_href, get_item

DEFAULT_SCENE = "20250626_082641_74_4001"
DEFAULT_COLLECTION = "coastal-water-bodies"

QUICK_ASSETS = ("ortho_visual", "ortho_beta_udm")
FULL_ASSETS = QUICK_ASSETS + ("ortho_sr_hdf5",)


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"skip (exists): {dest.name}")
        return dest

    print(f"downloading: {dest.name}")
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with dest.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--scene", default=DEFAULT_SCENE)
    parser.add_argument("--out-dir", default="data")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Also download ortho_sr_hdf5 (~500MB+) for hyperspectral analysis",
    )
    args = parser.parse_args()

    item = get_item(args.collection, args.scene)
    out_dir = Path(args.out_dir)
    assets = FULL_ASSETS if args.full else QUICK_ASSETS

    for key in assets:
        url = asset_href(item, key)
        filename = url.rsplit("/", 1)[-1]
        download(url, out_dir / filename)

    print(f"done — assets in {out_dir.resolve()}")


if __name__ == "__main__":
    main()

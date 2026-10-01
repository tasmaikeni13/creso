"""Bounded retrieval of primary documents; cache is excluded from Git."""

import concurrent.futures
import hashlib
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / ".source-cache" / "c001"
SOURCES = {
    "statsformer": "https://arxiv.org/html/2601.21410v1",
    "worker-disagreement": "https://arxiv.org/html/2605.27739v1",
    "muon-noise": "https://arxiv.org/html/2609.32861v1",
    "mars-m": "https://arxiv.org/html/2510.21800v3",
    "adaptive-sampling": "https://arxiv.org/abs/1710.11258",
    "kalman-gradient": "https://arxiv.org/abs/1810.12273",
    "bounded-kurtosis": "https://arxiv.org/abs/2607.05226",
}


def fetch(item):
    name, url = item
    row = {
        "id": name,
        "url": url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "CRESO-research/0.2"}
        )
        with urllib.request.urlopen(request, timeout=18) as response:
            blob = response.read()
            path = CACHE / f"{name}.html"
            path.write_bytes(blob)
            row.update(
                status="retrieved",
                bytes=len(blob),
                sha256=hashlib.sha256(blob).hexdigest(),
                cache_path=str(path.relative_to(ROOT)),
                content_type=response.headers.get("Content-Type"),
            )
    except (OSError, ValueError) as error:
        row.update(status="retrieval_failed", error=str(error))
    return row


if __name__ == "__main__":
    CACHE.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, SOURCES.items()))
    output = {
        "date": "2026-10-01",
        "sources": records,
        "scope": "standalone primary source audit",
    }
    (ROOT / "research/c001/source-manifest.json").write_text(
        json.dumps(output, indent=2) + "\n"
    )
    for row in records:
        print(row["id"], row["status"], row.get("sha256", row.get("error")))

"""Retrieve primary-source snapshots with hashes; never execute upstream code."""

import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / ".source-cache" / "r001"
PAPERS = {
    "soap": "2409.11321",
    "adamuon": "2507.11005",
    "variance_muon": "2601.14603",
    "deva": "2602.06880",
    "aro": "2602.09006",
    "spectra_spike": "2602.11185",
    "spectra_framework": "2603.14315",
    "newton_muon": "2604.01472",
    "sage": "2605.07914",
    "mucon": "2605.26459",
    "optmuon": "2606.08783",
    "dion3": "2608.11612",
    "musec": "2609.11655",
    "smoothed_flow": "2608.01911",
    "noise_scale": "2602.03001",
}


def retrieve(item):
    name, url = item
    req = urllib.request.Request(url, headers={"User-Agent": "RASP research audit"})
    at = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = response.read()
            content_type = response.headers.get_content_type()
        suffix = ".pdf" if content_type == "application/pdf" else ".html"
        path = CACHE / (name + suffix)
        path.write_bytes(payload)
        record = {
            "id": name,
            "url": url,
            "retrieved_at": at,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
            "snapshot": str(path.relative_to(ROOT)),
            "content_type": content_type,
        }
        if suffix == ".html":
            soup = BeautifulSoup(payload, "html.parser")
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()
            for math in soup.find_all("math"):
                if math.get("alttext"):
                    math.replace_with(math["alttext"])
            txt = soup.get_text("\n", strip=True)
            path.with_suffix(".txt").write_text(txt)
            record["title"] = soup.title.get_text() if soup.title else ""
            record["official_code_links"] = sorted(
                {
                    a["href"]
                    for a in soup.find_all("a", href=True)
                    if "github.com/" in a["href"]
                }
            )
            record["version_history"] = txt[txt.find("Submission history") :][:2000]
        return record
    except (urllib.error.URLError, TimeoutError) as exc:
        return {"id": name, "url": url, "retrieved_at": at, "error": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore frozen source/code snapshots and verify hashes",
    )
    args = parser.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.restore:
        records = []
        for filename in ("source-manifest.json", "upstream-manifest.json"):
            records.extend(
                json.loads(pathlib.Path(__file__).with_name(filename).read_text())
            )
        for record in records:
            if "sha256" not in record:
                continue
            target = ROOT / record["snapshot"]
            if target.exists():
                payload = target.read_bytes()
            else:
                request = urllib.request.Request(
                    record["url"], headers={"User-Agent": "RASP research audit"}
                )
                with urllib.request.urlopen(request, timeout=60) as response:
                    payload = response.read()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            actual = hashlib.sha256(payload).hexdigest()
            if actual != record["sha256"]:
                raise ValueError(f"Snapshot changed: {record['id']} {actual}")
            print(record["id"], "verified")
        return
    target = pathlib.Path(__file__).with_name("source-manifest.json")
    if target.exists():
        raise FileExistsError("Frozen manifest exists; use --restore or a new revision")
    requests = []
    for name, identifier in PAPERS.items():
        requests.extend(
            [
                (name + "_abs", "https://arxiv.org/abs/" + identifier),
                (name, "https://arxiv.org/html/" + identifier + "v1"),
            ]
        )
    requests.extend(
        [
            (
                "bfo",
                "https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf",
            ),
            (
                "markowitz",
                "https://traders.studentorg.berkeley.edu/papers/Markowitz.pdf",
            ),
            ("shampoo", "https://proceedings.mlr.press/v80/gupta18a.html"),
            ("muon", "https://github.com/KellerJordan/Muon"),
            ("dion", "https://github.com/microsoft/dion"),
        ]
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(retrieve, requests))
    target.write_text(json.dumps(records, indent=2) + "\n")
    for record in records:
        print(record["id"], record.get("bytes", record.get("error")))


if __name__ == "__main__":
    main()

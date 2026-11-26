#!/usr/bin/env python3
"""Check a run of this benchmark against the runs archived with the paper.

    scripts/verify_zenodo.py NEW_OUT [--run out_conda-seed_20-run_1] [--tolerance 0]

The archive is https://doi.org/10.5281/zenodo.18598405: 18 runs (3 backends,
seeds 20, 54 and 85, 2 runs each) of the benchmark as it was before api 0.8.0,
one scores file per dataset, method and metric. NEW_OUT is an api 0.8.0 out
dir, read only through the summary.tsv tables of its `metrics` gather.

Compared: every score of the datasets NEW_OUT has, so a slice can be checked
too. A method that takes a seed (fcps) is compared only when both runs used the
same one: `make run_conda SEED=20`.

Exit 1 if a score differs by more than --tolerance, or is missing on one side
with no recorded failure there. A failure on the missing side is reported, not
fatal: an empty scores file in the archive, a failure.json in NEW_OUT (api
0.8.0, `ob run -k`). Jobs near the 2 h timeout finish in one run and not the
other, whatever the timeout, so a refactor guarantee cannot ask for the same
set of finished jobs; it asks that nothing is lost silently.

The checked-in reference is the conda run: the docker images (ghcr fcps:2.0.0)
have conda's package versions and match it score for score.

The archive (226 MB) is downloaded once, next to this script's --cache, and
read in place: nothing is extracted from it.
"""

import argparse
import csv
import gzip
import hashlib
import json
import sys
import tarfile
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

URL = ("https://zenodo.org/api/records/18598405/files/"
       "clustering_example_18runs_snapshot.tar.gz/content")
MD5 = "c1757e170c794380e9d9765ef316aaae"
POSITIONS = ["k-2", "k-1", "k", "k+1", "k+2"]


def fetch(cache):
    archive = Path(cache) / "clustering_example_18runs_snapshot.tar.gz"
    if not archive.exists():
        print(f"downloading {URL}", file=sys.stderr)
        archive.parent.mkdir(parents=True, exist_ok=True)
        partial = archive.with_suffix(".part")
        urllib.request.urlretrieve(URL, partial)
        partial.rename(archive)
    md5 = hashlib.md5()
    with open(archive, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            md5.update(chunk)
    if md5.hexdigest() != MD5:
        sys.exit(f"{archive}: md5 {md5.hexdigest()}, expected {MD5}; delete it and retry")
    return archive


def label(params):
    """(method_params without the seed, seed): the seed decides comparability."""
    params = dict(params)
    seed = params.pop("seed", None)
    return ";".join(f"{k}={v}" for k, v in sorted(params.items())), seed


def split_scores(text):
    ks, scores = (line.strip().split(",") for line in text.splitlines()[:2])
    return [(pos, k.strip('"').removeprefix("k="), score)
            for pos, k, score in zip(POSITIONS, ks, scores)]


def archived_scores(archive, run):
    """({key: (k, score, seed)}, {key prefix: "failed"}) of one archived run, layout
    data/clustbench/.H/clustering/METHOD/.H/metrics/partition_metrics/.H/"""
    prefix = f"./results/{run}/data/"
    params, scores = {}, {}
    with tarfile.open(archive) as tar:
        for member in tar:
            if not member.name.startswith(prefix) or not member.isfile():
                continue
            path = PurePosixPath(member.name)
            if path.name == "parameters.json":
                params[path.parent] = json.load(tar.extractfile(member))
            elif path.name.endswith(".scores.gz"):
                scores[path.parent] = gzip.decompress(tar.extractfile(member).read()).decode()
    if not scores:
        sys.exit(f"no scores under {prefix} in {archive}; is --run right?")
    table, failed = {}, {}
    for metric_dir, text in scores.items():
        method_dir, data_dir = metric_dir.parents[2], metric_dir.parents[5]
        data, metric = params[data_dir], params[metric_dir]["metric"]
        method_params, seed = label(params[method_dir])
        node = (data["dataset_generator"], data["dataset_name"], method_dir.parent.name,
                method_params, metric)
        if not text.strip():  # the job failed in the archived run
            failed[node] = "failed"
            continue
        for pos, k, score in split_scores(text):
            table[(*node, pos)] = (k, score, seed)
    return table, failed


def new_scores(out):
    table = {}
    for f in Path(out).rglob("summary.tsv"):
        if "by-params" in f.parts:
            continue
        for r in csv.DictReader(open(f), delimiter="\t"):
            method_params, seed = label(p.split("=", 1) for p in r["method_params"].split(";") if p)
            key = (r["dataset_generator"], r["dataset"], r["method"], method_params,
                   r["metric"], r["k_position"])
            assert key not in table, f"duplicate row {key}"
            table[key] = (r["k"], r["score"], seed)
    if not table:
        sys.exit(f"no summary.tsv under {out}")
    return table


def new_failures(out):
    """{key prefix: kind} of the nodes with a failure.json: (generator, dataset)
    for a dataset or its metrics gather, (..., method, params) for a clustering."""
    out, failed = Path(out), {}
    for f in out.rglob("failure.json"):
        parts = f.relative_to(out).parts[:-1]
        if "by-params" in parts or not parts or not parts[0].startswith("data."):
            continue  # the report: no scores hang on it
        data = json.loads((out / parts[0] / "parameters.json").read_text())
        prefix = (data["generator"], data["dataset"])
        if len(parts) > 1 and parts[1].startswith("clustering."):
            method_params, _ = label(json.loads((f.parent / "parameters.json").read_text()))
            prefix += (parts[1].split(".")[1], method_params)
        failed[prefix] = json.loads(f.read_text())["kind"]
    return failed


def failed_on(failed, key):
    """The recorded failure that explains a missing *key*, or None."""
    return next((failed[key[:n]] for n in (5, 4, 2) if key[:n] in failed), None)


def compare(old, new, old_failed, new_failed, tolerance):
    """Counts per method, the rows that fail, and the missing rows a recorded
    failure explains."""
    datasets = {k[:2] for k in new} | {k[:2] for k in new_failed}
    old = {k: v for k, v in old.items() if k[:2] in datasets}
    counts, worst, failures, explained = defaultdict(Counter), Counter(), [], Counter()
    for key in sorted(old.keys() | new.keys()):
        method, a, b = key[2], old.get(key), new.get(key)
        if a is None or b is None:
            side, failed = ("archive", old_failed) if a is None else ("new", new_failed)
            kind = failed_on(failed, key)
            if kind:
                verdict = f"failed in {side}"
                explained[(side, kind, key[:4])] += 1
            else:
                verdict = "only in new" if a is None else "only in archive"
        elif str(a[2]) != str(b[2]):
            verdict = "other seed"
        elif a[0] != b[0]:
            verdict = "different k"
        elif a[1] == b[1] or float(a[1]) == float(b[1]) or (a[1] == b[1] == "nan"):
            verdict = "identical"
        else:
            diff = abs(float(a[1]) - float(b[1]))
            worst[method] = max(worst[method], diff)
            verdict = "within tolerance" if diff <= tolerance else "different"
        counts[method][verdict] += 1
        if verdict in ("only in new", "only in archive", "different k", "different"):
            failures.append((verdict, key, a, b))
    return counts, worst, failures, explained, len(datasets)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("new_out", help="api 0.8.0 out dir")
    parser.add_argument("--run", default="out_conda-seed_20-run_1",
                        help="archived run: out_{conda,oras,envmodules}-seed_{20,54,85}-run_{1,2}")
    parser.add_argument("--tolerance", type=float, default=0.0,
                        help="largest absolute score difference accepted (default: 0)")
    parser.add_argument("--cache", default=Path(__file__).parent / ".zenodo",
                        help="where the archive is kept (default: scripts/.zenodo)")
    args = parser.parse_args()

    old, old_failed = archived_scores(fetch(args.cache), args.run)
    new = new_scores(args.new_out)
    counts, worst, failures, explained, n_datasets = compare(
        old, new, old_failed, new_failures(args.new_out), args.tolerance)

    verdicts = ["identical", "within tolerance", "different", "different k",
                "other seed", "failed in archive", "failed in new",
                "only in archive", "only in new"]
    print(f"{args.run} vs {args.new_out}: {n_datasets} datasets, "
          f"{len({k[:2] for k in old})} in the archive")
    print("\t".join(["method", *verdicts, "max abs diff"]))
    for method in sorted(counts):
        print("\t".join([method, *(str(counts[method][v]) for v in verdicts),
                         f"{worst[method]:.3g}"]))
    for verdict, key, a, b in failures[:20]:
        print(f"  {verdict}: {key} archive={a} new={b}")
    if len(failures) > 20:
        print(f"  ... and {len(failures) - 20} more")
    if explained:
        print("missing on one side, with a recorded failure there (not fatal):")
        for (side, kind, node), n in sorted(explained.items()):
            print(f"  failed in {side} ({kind}): {node} ({n} scores)")
    skipped = sum(c["other seed"] for c in counts.values())
    if skipped:
        print(f"{skipped} scores not compared: seeded with another value than the archived run")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

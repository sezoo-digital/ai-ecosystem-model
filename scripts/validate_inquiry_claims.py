#!/usr/bin/env python3
"""Validate opt-in inquiry claim ledgers.

This is a structural/evidence-hygiene check, NOT an assessment that a
claim is true, that external citations are credible, or that graph edges
establish effective authority. Inquiries without a ledger remain valid.
"""
import argparse
import re
import sys
from pathlib import Path
import yaml

ANCHOR = re.compile(r"<!--\s*claim:\s*([A-Z][A-Z0-9-]*)\s*-->")
KINDS = {"represented", "derived", "externally-evidenced", "unverified"}
CLAIM_ID = re.compile(r"^[A-Z][A-Z0-9-]*$")
MODEL_ID = re.compile(r"^[NELFV]_[A-Z][A-Z0-9_]*$")


def check_document(path, known_ids):
    problems = []
    try:
        source = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}: unreadable: {exc}"]
    if not source.startswith("---\n"):
        return [f"{path}: missing YAML front matter"]
    parts = source.split("---", 2)
    if len(parts) < 3:
        return [f"{path}: unterminated front matter"]
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return [f"{path}: invalid YAML front matter: {exc}"]
    if not isinstance(meta, dict):
        return [f"{path}: front matter must be a mapping"]
    ledger = meta.get("claim_evidence")
    body = parts[2]
    anchors = ANCHOR.findall(body)
    if ledger is None:
        return [f"{path}: claim anchors exist without claim_evidence ledger"] if anchors else []
    if not isinstance(ledger, list) or not ledger:
        return [f"{path}: claim_evidence must be a non-empty list"]
    ids = []
    for index, claim in enumerate(ledger, 1):
        loc = f"{path}:claim_evidence[{index}]"
        if not isinstance(claim, dict):
            problems.append(f"{loc}: expected mapping")
            continue
        cid = claim.get("id")
        if not isinstance(cid, str) or not CLAIM_ID.fullmatch(cid):
            problems.append(f"{loc}: invalid claim id")
            continue
        ids.append(cid)
        category = claim.get("classification")
        if category not in KINDS:
            problems.append(f"{loc}: invalid classification {category!r}")
        refs = claim.get("model_refs", [])
        if not isinstance(refs, list) or any(not isinstance(v, str) or not MODEL_ID.fullmatch(v) for v in refs):
            problems.append(f"{loc}: model_refs must contain canonical ID strings")
        else:
            for ref in refs:
                if ref not in known_ids:
                    problems.append(f"{loc}: unknown canonical ID {ref}")
        if category in ("represented", "derived") and not refs:
            problems.append(f"{loc}: {category} requires model_refs")
        if category == "derived" and not _strings(claim.get("assumptions")):
            problems.append(f"{loc}: derived claim requires explicit assumptions")
        if category == "externally-evidenced":
            sources = claim.get("sources")
            if not _strings(sources) or any(not x.startswith(("https://", "http://")) for x in sources):
                problems.append(f"{loc}: externally-evidenced claim requires source URLs")
        if category == "unverified" and not _strings(claim.get("limitations")):
            problems.append(f"{loc}: unverified claim requires limitations")
        if anchors.count(cid) != 1:
            problems.append(f"{loc}: expected exactly one matching body anchor, found {anchors.count(cid)}")
    for cid in set(ids):
        if ids.count(cid) > 1:
            problems.append(f"{path}: duplicate claim id {cid}")
    for cid in set(anchors) - set(ids):
        problems.append(f"{path}: undeclared claim anchor {cid}")
    return problems


def _strings(value):
    return isinstance(value, list) and bool(value) and all(isinstance(s, str) and bool(s.strip()) for s in value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("documents", nargs="+", type=Path)
    args = parser.parse_args(argv)
    try:
        model = yaml.safe_load(args.model.read_text(encoding="utf-8"))
        known = {item["id"] for group in ("nodes", "edges", "loops", "frames", "views")
                 for item in model.get(group, [])}
    except (OSError, yaml.YAMLError, KeyError, TypeError) as exc:
        parser.error(f"invalid canonical model: {exc}")
    problems = [problem for doc in args.documents for problem in check_document(doc, known)]
    for problem in problems:
        print("ERROR:", problem, file=sys.stderr)
    if problems:
        return 1
    print(f"Claim-ledger structure verified for {len(args.documents)} document(s); semantic accuracy NOT assessed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
import os

import jsonschema


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_schema(cert):
    schema = load_json("schema/triplet_nogo.schema.json")
    jsonschema.validate(cert, schema)


def check_artifact(cert):
    art = cert["artifacts"]

    path = art["edgelist_path"]
    expected = art["edgelist_sha256"]

    if not os.path.exists(path):
        die(f"artifact not found: {path}")

    actual = sha256_file(path)
    if actual != expected:
        die("sha256 mismatch")

    print(json.dumps({
        "path": path,
        "sha256": actual
    }, indent=2))


def find_oblivion_slice_claim(cert):
    for claim in cert["claims"]:
        if claim["name"] == "Oblivion_Slice_k3_D3_R2":
            return claim
    return None


def check_oblivion_slice(cert):
    claim = find_oblivion_slice_claim(cert)
    if claim is None:
        die("Oblivion slice claim not found in claims[]")

    if claim["status"] != "Conditional":
        die("Oblivion slice claim must be Conditional")

    print(json.dumps({
        "claim": claim["name"],
        "status": claim["status"],
        "statement": claim["statement"]
    }, indent=2))

    print("OBLIVION_SLICE_CONDITIONAL_PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", required=True)
    ap.add_argument("--check_oblivion_slice", action="store_true")
    args = ap.parse_args()

    cert = load_json(args.cert)

    validate_schema(cert)
    check_artifact(cert)

    if args.check_oblivion_slice:
        check_oblivion_slice(cert)

    print("VALID")


if __name__ == "__main__":
    main()


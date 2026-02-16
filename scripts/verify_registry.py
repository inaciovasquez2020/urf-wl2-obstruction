import json, hashlib, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    reg = ROOT / "registry" / "wl2_registry.json"
    if not reg.exists():
        print("ERROR: missing registry/wl2_registry.json")
        sys.exit(1)
    regj = json.loads(reg.read_text())

    for item in regj.get("items", []):
        certp = ROOT / item["cert_path"]
        if not certp.exists():
            print(f"ERROR: missing cert {certp}")
            sys.exit(1)
        cert = json.loads(certp.read_text())

        for key in ["A","B"]:
            obj = cert["objects"][key]
            p = ROOT / obj["path"]
            if not p.exists():
                print(f"ERROR: missing object {p}")
                sys.exit(1)
            expected = obj["content_hash"].replace("sha256:","")
            actual = sha256_file(p)
            if expected != actual:
                print(f"ERROR: hash mismatch {key}")
                print(f"  expected: {expected}")
                print(f"  actual:   {actual}")
                sys.exit(1)

        # verify evidence exists (no recomputation in verifier)
        for ep in cert["evidence"]["evidence_paths"]:
            p = ROOT / ep
            if not p.exists():
                print(f"ERROR: missing evidence {p}")
                sys.exit(1)

    print("OK: wl2 registry verified")

if __name__ == "__main__":
    main()

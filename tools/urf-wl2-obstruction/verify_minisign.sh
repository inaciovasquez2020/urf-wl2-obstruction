#!/usr/bin/env sh
set -e

KEY_ID="RWRYSQOcAPcPGowy2ls9e2xh9XL4UP/o5nvmERf6VVP4ssYOIGGvAl2L"

for f in certs/urf-wl2-obstruction/examples/*.json; do
  minisign -Vm "$f" -P "$KEY_ID"
done

echo "URF-WL2 certification signatures verified."

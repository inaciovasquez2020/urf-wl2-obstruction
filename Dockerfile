FROM python:3.11-slim

WORKDIR /work

# Copy repo
COPY . /work

# Minimal dependency for verifier
RUN pip install --no-cache-dir jsonschema==4.26.0

# One-command reproduction:
# 1) regenerate gold instance
# 2) verify certificate
CMD python3 scripts/gen_Tn.py --t 10 --seed 1729 --outdir artifacts --name Tn_gold && \
    python3 verify_triplet.py --cert certs/TRIPLET_NOGO_0001.json



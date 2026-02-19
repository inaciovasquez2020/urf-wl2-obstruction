# WL3 Sampled Obstruction (URF)

Deterministic WL³-style sampling utility used in the URF WL²/WL³ obstruction experiments.

## Purpose

This script performs:
1. Weisfeiler–Leman color refinement on a graph
2. Random sampling of vertex triples (WL³-style signatures)
3. **Collapsed histogram output** (presence-only, no multiplicities)

It is designed to be **CI-safe**, **total**, and **format-robust**.

---

## Usage

```bash
python3 scripts/wl3_sampled.py <edgelist> <depth> <iters> <samples> <seed>


URF–WL2 Certification (Released)

This repository includes URF Certification Artifacts.

A certification release is not a software release.
It makes no performance guarantees, no completeness claims,
and no implications beyond the explicitly stated boundaries.

Certification artifacts are declarative, cryptographically signed,
immutable, and inert with respect to CI and runtime behavior.

Claims are valid only under stated constraints.
All non-claims are explicitly listed in the certification files.

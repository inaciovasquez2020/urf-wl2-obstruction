[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18651031.svg)](https://doi.org/10.5281/zenodo.18651031)

# NCR — New Computational Regime (ISR)

This repository documents the **New Computational Regime (NCR)** based on the **Implicit Superposition Register (ISR)** model.

ISR is a discrete, deterministic computational model whose state is a **reduced ordered decision diagram** representing an exponentially large set of assignments.  
Updates apply constraints by **symbolic conjunction**, without enumerating assignments.

The regime is designed to study **normalization-resistant computation**: systems where standard polynomial normalization techniques fail structurally, not accidentally.

---

## Manuscripts

Primary manuscript:
- `manuscript/ISR_as_a_Normalization_Resistant_Polynomial_Regime.md`

Supplementary minimal note:
- `manuscript/ISR_Normalization_Resistance.md`

These notes provide a structural description of the ISR regime and its resistance to normalization-based reductions.

---

## Model Overview

**ISR = Implicit Superposition Register**

- State: symbolic representation of an exponential assignment space
- Dynamics: constraint application via symbolic conjunction
- No enumeration of assignments
- Deterministic update semantics
- Polynomial-time operations over exponentially large implicit state

This repository is concerned with **structural properties**, not performance claims.

---

## Artifacts

Core materials included here:

- `docs/MODEL.md`
- `docs/INVARIANTS.md`
- `model/isr.py`
- `scripts/run_isr_demo.py`
- `scripts/normalization_attempt.py`
- `scripts/oracle_audit.py`
- `tests/`

These artifacts exist to support inspection, experimentation, and verification of the ISR structure.

---

## Scope

This repository:
- Documents a computational *regime*
- Demonstrates normalization resistance structurally
- Provides reference implementations for inspection

This repository does **not**:
- Claim algorithmic speedups
- Resolve P vs NP
- Provide complexity-theoretic separations
- Assert empirical performance dominance

---

## Certification Boundary

This repository is **NON-CERTIFIED under URF**.

Only **NEGATIVE certification artifacts** may be present.  
No positive NCR claim is asserted.  
All results are research or infrastructure-only.

Certification artifacts, where present, are:
- Declarative
- Cryptographically signed
- Inert with respect to CI and runtime behavior

No guarantees are made beyond explicitly stated theoretical boundaries.


# Einstein Triplet Specification (URF)

Version: triplet/1.0  
Status: Frozen

---

## Objects

The Einstein Triplet consists of three independently verifiable artifacts:

1. **LAW** — a universal invariant inequality.
2. **NOGO** — a canonical task family with a structural obstruction.
3. **VERIFIER** — an executable gate enforcing correctness.

Each artifact must be checkable by a third party without trust in the author.

---

## Canonical Task Family {T_n}

### Base Graph H

Vertices:
{0,1,2,3}

Edges:
(0,1), (1,2), (2,3), (3,0), (0,2)

(4-cycle with a chord)

---

### Deterministic Signed 2-Lift

Given graph G = (V,E) and sign map s : E → {+1,−1}:

Each vertex v ∈ V becomes (v,0),(v,1)

For each edge {u,v}:
- if s(u,v)=+1: connect (u,0)-(v,0), (u,1)-(v,1)
- if s(u,v)=−1: connect (u,0)-(v,1), (u,1)-(v,0)

---

### Definition of T_n

Let G₀ = H.

For i = 1…t:
- Generate deterministic sign map using PRNG(seed + i)
- Set Gᵢ = 2-lift(Gᵢ₋₁)

Output:
Tₙ = G_t  
n = 4 · 2^t

---

## NOGO Structural Invariant

Cycle rank:
r(G) = m − n + c(G)

Gold condition:
r(Tₙ) ≥ ⌊n / 4⌋

This is a **purely structural** certificate.

---

## Conditional Complexity Consequence

If the Oblivion Atom holds at parameters (k, Δ, R), then:

Any FOᵏ-admissible refinement algorithm A satisfies

Cost_A(Tₙ) ≥ α · n log₂ n

This implication **must be labeled Conditional** and must name its dependency.

---

## Acceptance Tests

### TEST-LAW
- Schema-valid
- All numeric fields recomputable
- Any implication beyond invariants tagged Conditional

### TEST-NOGO
- Tₙ regenerates byte-for-byte
- SHA256 matches certificate
- Cycle-rank threshold holds
- Conditional tagging enforced

### TEST-VERIFIER
Command:



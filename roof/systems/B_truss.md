# System B – Planar lattice trusses N–S on pinned SHS posts (mono-pitch, falls north)

**Rev 1: openings at stair/elevator, single-plane slope.** Stair well (x 77.89–81.79, y 29.37–35.37) and elevator shaft (x 77.89–81.99, y 20.17–24.16) left open; roof confirmed as ONE 6 % plane. Roofed area 446 m² (486 m² footprint − 40 m² openings).

## 1. Framing layout

- **One roof plane, 6 % (3.4°) falling north**, no steps. Top-of-steel TOS(y) = 4.52 + 0.06 × (35.87 − y). Bottom chord underside 3.00 m clear at the north edge (y 35.87), 4.22 m at the south edge (y 15.57).

| Position | BC underside | TC centreline | TOS | Roof surface |
|---|---|---|---|---|
| North edge y 35.87 | 3.00 | 4.46 | 4.52 | 4.77 |
| North posts y 35.17–35.77 | 3.01–3.04 | 4.47–4.50 | 4.53–4.56 | – |
| T2 south posts y 20.07 | 3.95 | 5.41 | 5.47 | 5.72 |
| T1 south posts y 15.87 | 4.20 | 5.66 | 5.72 | 5.97 |
| South edge y 15.57 | 4.22 | 5.68 | 5.74 | 5.99 |

- **Parallel-chord Warren trusses, depth 1.40 m c/c**, full-depth N–S, simply supported on pinned posts; no interior posts.

| Truss | Lines x | Supports | Span | Panels |
|---|---|---|---|---|
| T1 | 68.0, 72.1, 77.8 | K25/K6, K26/K5, K27/K7 | 19.3 m | 6 × 3.22 m, mid-span site splice |
| T2 | 81.8, 95.5 | K21/K3, K23/K4 | 15.6 m | 5 × 3.12 m, one piece |
| T2 | 87.2, 92.5 | K1, K2 north / **eave girder** y 20.07 south | 15.6 m | as above |

- Spacing 4.1 / 5.7 / 4.0 / 5.4 / 5.3 / 3.0 m; all trusses sized for 5.4 m tributary.
- **Openings**: T1 at x 77.785 (chord face 77.845) runs along the west edge of both openings; T2 at x 81.84 (chord 81.78–81.90) along the east edge: flush with the stair edge 81.79 but 0.1–0.2 m inside the elevator's notional edge 81.99, i.e. over the 200 mm shaft wall, not the hoistway (client to confirm; T2 cannot move east without leaving post K21). Trimmers **SHS 100×100×4** on the N and S edges (y 20.17, 24.16, 29.37, 35.37) span 4.05 m between the two trusses; E/W edges are the truss top chords. Upstand L100×8 + flashing all round, panels stop at the trimmers. Nothing crosses the openings: 7 purlin lines and 2 tie lines omitted between x 77.8 and 81.8; roof bracing moved from bay 77.8–81.8 to 81.8–87.2.
- **Eave girder IPE 330** along y 20.07, K21–K22–K23 (7.1 + 6.6 m continuous), carries the trusses at x 87.2 and 92.5 (no south column). Re-entrant corner (77.9, 20.07): header IPE 200 from K21 to truss x 77.8, corner mullion hung from it.
- **Purlins Z200×2.0 S350GD @ 1.5 m**, sleeved, independent of truss nodes (chord takes ≤ 5 kNm local bending).
- Posts on 19 columns (13 truss posts + wall posts K24, K19, K15, K8, K18, K14); K9–K13, K16, K17, K20 unused.
- Stability: X-bracing L70×6 in **8 wall bays** (N: K6–K5, K2–K4; S: K25–K26, K22–K23; W: K25–K19, K8–K6; E: K23–K18, K14–K4) and **3 roof bays** at top-chord level (68.0–72.1, 81.8–87.2, 92.5–95.5); eave struts N and S; bottom-chord ties @ ~4.8 m. All joints pinned, bolted.

## 2. Loads (EN 1991, preliminary)

| Load | Value |
|---|---|
| Dead: panel 0.12 + purlins 0.05 + services 0.20 + steel 0.13 | **g_k = 0.50 kN/m²** (0.30 for uplift) |
| Imposed cat. H | **q_k = 0.60 kN/m²**, not with wind |
| Wind v_b 30 m/s, terrain II, z ≈ 10.5 m, c_e 2.35 | **q_p = 1.32 kN/m²** |
| Mono-pitch 5°, high eave windward: c_pe F/G/H −2.3/−1.3/−0.8, c_pi +0.2/−0.3 | net **−1.32 kN/m²** general, −3.3 kN/m² edge strips and around openings |
| Walls c_pe +0.7/−0.3; seismic a_g 0.10 g, q = 4 | drag N–S ≈ 165 kN wind vs ≈ 60 kN seismic |

ULS-1: 1.35 G + 1.5 Q = **1.58 kN/m² down**. ULS-2: 1.0 G + 1.5 W = **1.68 kN/m² up** (anchors, bottom chord, purlin free flange). SLS: trusses L/250, purlins L/200.

## 3. Member sizes (S275; SHS hot-finished EN 10210)

T1 at 5.4 m: w = 8.5 kN/m, M = 396 kNm, V = 82 kN → chord N = M/d = **283 kN**, end diagonal V/sin 43° = **120 kN**. T2: M = 259 kNm → 185 kN. Rev 1: one chord section for all trusses so TOS and bottom-chord planes coincide without cleat packs.

| Member | Section | Check |
|---|---|---|
| Chords, all trusses | SHS 120×120×5 (17.8 kg/m) | 283 kN / N_b,Rd 456 kN (L_cr 2.7 m) + 5 kNm → 0.81; uplift bottom chord 270 kN, ties @ 4.8 m → 331 kN |
| Diagonals (all) | SHS 70×70×4 | 120 / 209 kN; β 0.58 OK for gap K-joints |
| Posts (19) | SHS 150×150×5 | N 95 kN + wind M 24 kNm; N_b,Rd 490 kN, M_pl 40 kNm |
| Eave girder | IPE 330 continuous | M_Ed ≈ 105 kNm (67 kN at 1.7 m from K22) / 221 kNm; deflection governs |
| Purlins | Z200×2.0 sleeved | 7.7 / ≈ 12 kNm; δ ≈ 15 mm |
| Eave struts / trimmers / BC ties | SHS 100×100×4 / 100×100×4 / 60×60×4 | trimmer: 4.05 m, panel strip + upstand, M ≈ 3 kNm, λ̄ < 1.5 |
| Bracing | L70×70×6 crossed, M20 8.8 | bay 41 kN, diagonal 49 kN |
| Splices, caps | 15 mm end plates, 4–6 M20 8.8 | |

**Take-off (446 m² roofed):** trusses 6.3 t, posts 1.8 t, purlins 1.9 t, girder 0.8 t, struts/trimmers/ties 1.6 t, bracing 1.6 t, plates/bolts 1.0 t → **≈ 14.9 t ≈ 33 kg/m² roofed (31 kg/m² of footprint)**, + girts ≈ 1.0 t. Rev 1 change +0.5 t (uniform chords, trimmers).

## 4. Base connection on the hollow-block slab

- Pinned base: plate 300×300×20 on **40 mm non-shrink grout** (screed removed, levelling nuts), 4 × M20 8.8 resin anchors in a **110×300 pattern inside the 200×400 column footprint** (two plate variants for the two orientations), drilled through the solid zone **300 mm into the column head** after rebar scanning; bond pull-out ≈ 120 kN per anchor.
- **Uplift governs**: post ULS uplift ≈ 88 kN vs 95 kN gravity. Global hold-down is fine (slab + column ≈ 150 kN), but anchors in the ribbed slab alone would not work: the through-slab anchor into the column head is essential and must be re-checked once slab thickness and solid-zone extent are confirmed.
- Shear ≤ 41 kN at braced-bay posts via a 20 mm shear key in a grouted pocket; compression goes straight into the column head.

## 5. Pros / cons for this project

**Pros**
- Open hall; 1 truss depth, 1 chord, 1 diagonal, 1 post, 1 purlin section: repetitive, easy to price.
- Trusses fully shop welded, all site work bolted; 14 truss pieces craned onto the slab.
- Openings fall between two trusses: 4 short trimmers, no extra posts, truss family unchanged.
- Light (14 kg/m² trusses), low reactions on the existing columns; irregular grid absorbed by the eave girder.

**Cons (honest)**
- Deepest option: 6.0 m south façade, 4.8 m north: ≈ 20 % more wall cladding than a beam scheme.
- Needs a shop competent in hollow-section K-joints; 19.3 m trusses spliced on site; more small pieces than a rafter scheme.
- Uplift ≈ gravity: ties and anchors are not optional; the anchor detail hinges on the unknown slab.
- IPE 330 eave girder is the one non-repetitive element; T2 at x 81.8 sits over the elevator's east shaft wall.
- Fallback if height matters: support on line y 29.3 → depth 1.0 m, ≈ 15 % less steel, but 7 interior posts and 3 truss types.

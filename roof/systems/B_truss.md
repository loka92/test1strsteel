# System B – Planar lattice trusses N–S on pinned SHS posts (mono-pitch, falls north)

## 1. Framing layout

- **Slope 6 % (3.4°)** north, one roof plane. Bottom chord underside 3.00 m above slab at the north eave, 3.94 m at y 20.07, 4.16 m at y 15.87; roof surface 4.8 m (N) to 6.0 m (S).
- **Parallel-chord Warren trusses, depth 1.40 m**, full-depth N–S, simply supported on pinned posts; no interior posts.

| Truss | Lines x | Supports | Span | Panels |
|---|---|---|---|---|
| T1 | 68.0, 72.1, 77.8 | K25/K6, K26/K5, K27/K7 | 19.3 m | 6 × 3.22 m, mid-span site splice |
| T2 | 81.8, 95.5 | K21/K3, K23/K4 | 15.6 m | 5 × 3.12 m, one piece |
| T2 | 87.2, 92.5 | K1, K2 north / **eave girder** y 20.07 south | 15.6 m | as above |

- Spacing 4.1 / 5.7 / 4.0 / 5.4 / 5.3 / 3.0 m; all trusses sized for 5.4 m tributary (one section set).
- **Eave girder IPE 330** along y 20.07, K21–K22–K23 (7.1 + 6.6 m continuous), carries the trusses at x 87.2 and 92.5 (no south column). Re-entrant corner (77.9, 20.07) has no column: header IPE 200 from K21 to truss x 77.8, corner mullion hung from it.
- **Purlins Z200×2.0 S350GD @ 1.5 m**, sleeved, independent of truss nodes (chord takes ≤ 5 kNm local bending).
- Posts on 19 columns (13 truss posts + wall posts K24, K19, K15, K8, K18, K14); K9–K13, K16, K17, K20 unused.
- Stability: X-bracing L70×6 in **8 wall bays** (N: K6–K5, K2–K4; S: K25–K26, K22–K23; W: K25–K19, K8–K6; E: K23–K18, K14–K4) and **3 roof bays** at top-chord level (68.0–72.1, 77.8–81.8, 92.5–95.5); eave struts on N and S eaves; bottom-chord ties @ ~4.8 m. All joints pinned, bolted.

## 2. Loads (EN 1991, preliminary)

| Load | Value |
|---|---|
| Dead: panel 0.12 + purlins 0.05 + services 0.20 + steel 0.13 | **g_k = 0.50 kN/m²** (0.30 for uplift) |
| Imposed cat. H | **q_k = 0.60 kN/m²**, not combined with wind |
| Wind v_b 30 m/s, terrain II, z ≈ 10.5 m → c_e 2.35 | **q_p = 1.32 kN/m²** |
| Mono-pitch 5°, high eave windward: c_pe F/G/H −2.3/−1.3/−0.8, c_pi +0.2/−0.3 | net **−1.32 kN/m²** general, −3.3 kN/m² in 2.2 m edge strip (purlins, fixings) |
| Walls c_pe +0.7/−0.3 | net 1.32 kN/m²; drag N–S ≈ 165 kN |
| Seismic a_g 0.10 g, q = 4 | ≈ 60 kN, wind governs |

ULS-1: 1.35 G + 1.5 Q = **1.58 kN/m² down**. ULS-2: 1.0 G + 1.5 W = **1.68 kN/m² up** (anchors, bottom chord, purlin free flange). SLS: trusses L/250, purlins L/200.

## 3. Member sizes (S275; SHS hot-finished EN 10210)

T1 at 5.4 m: w = 8.5 kN/m, M = 396 kNm, V = 82 kN → chord N = M/d = **283 kN**, end diagonal V/sin 43° = **120 kN**. T2: M = 259 kNm → 185 kN.

| Member | Section | Check |
|---|---|---|
| T1 chords | SHS 120×120×5 (17.8 kg/m) | 283 kN / N_b,Rd 456 kN (L_cr 2.7 m) + 5 kNm → 0.81; uplift bottom chord 270 kN, ties @ 4.8 m → 331 kN |
| T2 chords | SHS 100×100×5 | 185 / 334 kN; uplift 176 kN with ties @ 3.9 m |
| Diagonals (all) | SHS 70×70×4 | 120 / 209 kN; β 0.58–0.70 OK for gap K-joints |
| Posts (19) | SHS 150×150×5 | N 95 kN + wind M 24 kNm; N_b,Rd 490 kN, M_pl 40 kNm |
| Eave girder | IPE 330 continuous | M_Ed ≈ 105 kNm (67 kN at 1.7 m from K22) / 221 kNm; deflection governs |
| Purlins | Z200×2.0 sleeved | 7.7 / ≈ 12 kNm; δ ≈ 15 mm |
| Eave struts / BC ties | SHS 100×100×4 / 60×60×4 | λ̄ < 1.5 |
| Bracing | L70×70×6 crossed, M20 8.8 | bay 41 kN, diagonal 49 kN |
| Splices, caps | 15 mm end plates, 4–6 M20 8.8 | |

**Take-off (486 m²):** trusses 5.9 t, posts 1.8 t, purlins 2.1 t, girder 0.8 t, struts/ties 1.2 t, bracing 1.8 t, plates/bolts 0.9 t → **≈ 14.4 t ≈ 30 kg/m²** (+ girts ≈ 1.0 t).

## 4. Base connection on the hollow-block slab

- Pinned base: plate 300×300×20 on **40 mm non-shrink grout** (screed removed, levelling nuts), 4 × M20 8.8 resin anchors in a **110×300 pattern inside the 200×400 column footprint** (two plate variants for the two orientations), drilled through the solid zone **300 mm into the column head** after rebar scanning; bond pull-out ≈ 120 kN per anchor.
- **Uplift governs**: post ULS uplift ≈ 88 kN (1.68 × 52 m²) vs 95 kN gravity. Global hold-down is fine (slab + column ≈ 150 kN), but anchors in the 250 mm ribbed slab alone would not work: the through-slab anchor into the column head is essential and must be re-checked once slab thickness and solid-zone extent are confirmed.
- Shear ≤ 41 kN at braced-bay posts via a 20 mm shear key in a grouted pocket; compression goes straight into the column head, no slab punching.

## 5. Pros / cons for this project

**Pros**
- Open hall; 2 truss types, 1 post, 1 diagonal, 1 purlin section: repetitive, easy to price.
- Trusses fully shop welded, all site work bolted; 14 truss pieces craned onto the slab.
- Light (12 kg/m² trusses), low reactions on the existing columns; irregular grid absorbed by the eave girder and constant truss depth; stiff roof.

**Cons (honest)**
- Deepest option: 6.0 m south façade, 4.8 m north: ≈ 20 % more wall cladding than a beam scheme, heavy-looking north eave.
- Needs a shop competent in hollow-section K-joints; 19.3 m trusses spliced on site; more small pieces (ties, vertical bracing, sag rods) than a rafter scheme.
- Uplift ≈ gravity: ties and anchors are not optional; the anchor detail hinges on the unknown slab.
- The IPE 330 eave girder is the one non-repetitive element.
- Fallback if height matters: support on line y 29.3 (spans 13.4/9.2 + 6.4 m) → depth 1.0 m, ≈ 15 % less steel, but 7 interior posts and 3 truss types.

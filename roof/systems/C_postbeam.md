# System C – Post-and-beam braced frame (all pinned)

**Rev 1: openings at stair/elevator, single-plane slope.** Drawings: `C_postbeam_plan.png`, `C_postbeam_section.png`, `C_postbeam.dxf`.

**One roof plane, 6 % falling north:** TOS(y) = 3.28 + 0.06 (35.87 − y); panel top 3.53 m north edge, 4.75 m south. Rafters frame into the level primaries with fin plates, bottoms flush, ends cut at 3.4° – no seats or packs; primary tops sit 0.06 m above the plane. **Cap-plate tops** (TOS − 0.27): y 35.7 **3.00**, y 35.2 **3.03**, y 29.3 **3.39**, y 26.4 **3.56**, y 24.5 **3.68**, y 21.8 **3.84**, y 20.1 **3.94**, y 15.9 **4.19** m.

## 1. Framing layout

**E-W primaries on the column rows, N-S rafters:** 14 of 27 columns sit on the two north rows, so primaries span column-to-column (≤7.1 m, one exception), columns in a row are equal, purlins run parallel to the eave.

| Element | Lines / spans |
|---|---|
| E-W primaries, level, on cap plates | y 35.2: 4.1-5.7; y 35.7: 5.3-5.3-3.1; y 29.3: 4.1-5.8-3.9-5.4-5.3-3.0; y 24.5: K16–K17 4.1; **y 21.8: K19–K20 9.8**; y 20.1: 4.0-7.1-6.6; y 15.9: 4.0-2.9-2.9 |
| N-S rafters/edge beams, 10 lines x = 68.0, 72.1, 74.9, 77.8, 81.8, 84.5, 87.2, 89.9, 92.5, 95.5 | north band 5.9–6.5; west wing 7.5 + 5.9; **east seating x 82–95.5: 9.2 m clear, 4 lines** |
| Z purlins | 1.5 m centres, spans 2.7–4.1 m, none over the openings |

**Notch corner (77.8, 20.1), no column:** the y 20.1 eave beam frames into the edge beam K20–K27 (fin plate, 4.2 m from K27). **Openings (not roofed):** stair well (x 77.89–81.79, y 29.37–35.37), elevator (x 77.89–81.99, y 20.17–24.16). Long edges = rafters x 77.8 / 81.8; stair south edge = y 29.3 primary, north edge = **trimmer T1** IPE 270 at y 35.17, K7 to the x 81.8 rafter (replaces the skewed K7–K3 beam); elevator north edge = **trimmer T2** IPE 270 at y 24.16 (K16–K17 primary stays as tie), south edge = y 20.07 eave beam. 150 mm upstand + flashing all sides, cricket on the uphill side of the stair well. Shaft east wall (81.99) lies 0.1 m outside the K17–K21 beam – fine if the lift stops at the slab.

**Vertical X bracing, 7 bays (must be door-free – client to confirm; alternates in brackets).** E-W: B1 K1–K2 (K3–K1), B2 K5–K7, B3 K22–K23 (K21–K22), B4 K25–K26. N-S: B5 K15–K19 (K19–K25), B6 K14–K18 (K18–K23), B7 K20–K27. Each wing is braced both ways; B2 and B7 are clear of the openings. **Roof-plane X bracing** (green): 3.2 m perimeter strip = horizontal truss feeding B1–B7; at the stair well it jogs south through the panel K10–K11–K17–K16 with the y 29.3 primary as continuous chord.

## 2. Loads (EN 1991, preliminary)

Dead 0.12 + 0.05 + 0.20 + steel 0.12 = **0.49 kN/m²**; walls 0.30. Imposed cat. H **0.60** (ψ₀ = 0). Wind q_b = 0.56, c_e(10 m, II) = 2.35 → **q_p ≈ 1.3 kN/m²**; c_pe (5° mono-pitch) −0.6 to −2.3, c_pi ±0.2 → net **−1.0 (H) to −3.2 kN/m² (F, 1.8 m eave strip)**; walls +1.5. Seismic (0.10 g, q = 2) ≈ 50 kN < wind 80 kN N-S / 65 kN E-W at roof.
ULS1 1.35G + 1.5Q = **1.56 kN/m²**; ULS2 1.0G + 1.5W = **−1.5 (H) to −4.3 (F) uplift**; SLS G + Q = 1.09, δ ≤ L/200.

## 3. Members, S275 – 3 hot-rolled sections + Z + bracing

| Member | Section | Governing check (M = wL²/8, δ = 5wL⁴/384EI) |
|---|---|---|
| Columns ×27, 2.95–4.14 m | **HEA 160** | N_Ed ≤ 70 kN vs N_b,Rd 455 kN |
| Primaries E-W, 96 m | **IPE 330** | K19–K20 9.8 m, w = 10.5 kN/m: M = 126/221 kNm (0.57), δ = 35 mm = L/276. Others ≤0.25 |
| Rafters, edge beams, trimmers T1/T2, 179 m | **IPE 270** | 9.2 m @ 2.7 m: M = 45/133 (0.34), δ = 23 mm = L/407; uplift: fly braces at third points for spans ≥7.5 m |
| Purlins & girts, 620 m | **Z 200×2.0 S350** | 4.1 m: M = 4.9 kNm, δ = L/430 |
| Wall bracing B1–B7 | **2 L 70×7 crossed, tension-only** | N-S bay H = 27 kN → T_Ed = 51 vs 135 kN |
| Roof bracing | M20 rods 8.8 | T ≈ 42 vs 141 kN |

**Weight (Rev 1)**: columns 2.9 t, primaries 4.5 t, rafters/trimmers 6.5 t, upstands 0.15 t, plates 1.5 t → hot-rolled **15.5 t**; + Z 3.7 t + bracing 1.2 t → **20.5 t = 42 kg/m² of footprint (486 m²), 46 kg/m² of roofed area (446 m²)** – unchanged from Rev 0.

## 4. Bases on the hollow-block slab

Pinned base: plate 300×400×20, **4 M20 resin anchors, h_ef 170–200 mm, in the solid column-head zone only** (trial-drill to prove it; ≥100 mm from the slab edge), 40 mm non-shrink grout.
Actions: interior K12 (42 m²) compression 66 kN, **net uplift ULS ≈ 63 kN**; braced-bay columns add ±22 kN (N-S) or ±10 kN (E-W) plus bay shear 27 kN → **worst ≈ 70 kN uplift, 15 kN shear at K15/K19, K22/K23, K14/K18, K20/K27**. 4 M20 at h_ef 200 ≈ 100 kN group tension in cracked C25 – verify with the anchor supplier.

## 5. Pros / cons for this project

**Pros.** Simplest system: 3 hot-rolled sections, 2 connection types, no moment joints or site welding; the irregular grid and the openings are absorbed because rafters and trimmers land anywhere on the primaries; heaviest piece 480 kg; any local fabricator.

**Cons (honest).** Two layers of beams weigh more than a portal or truss (42 vs ~30 kg/m²) and stack 0.6 m at the eave; stability hangs on 7 door-free wall bays; net uplift at every base in a slab of unknown build – the column-head solid zones are the critical unknown; the 9.2 m rafters and 9.8 m primary have little reserve for a future ceiling.

# System C – Post-and-beam braced frame (all pinned)

Drawings: `C_postbeam_plan.png`, `C_postbeam_section.png`. Slope **6 %** falling north; roof top 3.58 m at the north eave, 4.5–4.8 m south.

## 1. Framing layout

**E-W primaries on the column rows, N-S rafters.** 14 of 27 columns sit on the two north rows, so primaries span column-to-column (≤7.1 m, one exception); all columns in a row are equal (caps 3.00 / 3.39 / 3.56 / 3.68 / 3.84 / 3.94 / 4.19 m make the slope); rafters follow the fall, purlins parallel to the eave. N-S primaries would need a skewed 9.3 m beam K12→K22.

| Element | Lines / spans |
|---|---|
| E-W primaries, level, on cap plates | y 35.2/35.7: 4.1-5.7-4.1-5.3-5.3-3.1; y 29.3: 4.1-5.8-3.9-5.4-5.3-3.0; y 24.5: K16–K17 4.1; **y 21.8: K19–K20 9.8**; y 20.1: 4.0-7.1-6.6; y 15.9: 4.0-2.9-2.9 |
| N-S rafters/edge beams, 10 lines x = 68.0, 72.1, 74.9, 77.8, 81.8, 84.5, 87.2, 89.9, 92.5, 95.5 | north band 5.9–6.5; west wing 7.5 + 5.9; **east seating x 82–95.5: 9.2 m clear, 4 lines** |
| Z purlins | 1.5 m centres, spans 2.7–4.1 m |

**Notch corner (77.8, 20.1), no column:** the y 20.1 eave beam runs 4.0 m west from K21 and frames into the edge beam K20–K27 (fin plate, 4.2 m from K27). The 0.5 m north-wall jog is a straight skewed beam K7–K3.

**Vertical X bracing, 7 bays (red; must be door-free – client to confirm; alternates in brackets).** E-W: B1 K1–K2 (K3–K1), B2 K5–K7, B3 K22–K23 (K21–K22), B4 K25–K26. N-S: B5 K15–K19 (K19–K25), B6 K14–K18 (K18–K23), B7 K20–K27. Each wing is braced both ways (torsionally stable L-plan). **Roof-plane X bracing** (green): 3.2 m perimeter strip = horizontal truss feeding B1–B7.

## 2. Loads (EN 1991, preliminary)

Dead: 0.12 + 0.05 + 0.20 + steel ≈0.12 = **0.49 kN/m²**; walls 0.30. Imposed cat. H **0.60** (ψ₀ = 0, never with wind). Wind: q_b = 0.56, c_e(10 m, cat II) = 2.35 → **q_p ≈ 1.3 kN/m²**. Mono-pitch (5° table): c_pe F/G/H = −1.7/−1.2/−0.6 (wind from N), −2.3/−1.3/−0.8 (from S), −2.1/−1.8/−0.6 (E-W); c_pi ±0.2 → net **−1.0 kN/m² (zone H) to −3.2 (F, 1.8 m eave strip)**, downward ≤+0.1. Walls net ≈ +1.5 kN/m². Seismic (0.10 g, q = 2) ≈ 50 kN < wind ≈ 80 kN N-S / 65 kN E-W at roof level.
ULS1 1.35G + 1.5Q = **1.56 kN/m²**; ULS2 1.0G + 1.5W = **−1.5 (H) to −4.3 (F) uplift**; SLS G + Q = 1.09, δ ≤ L/200.

## 3. Members, S275 – 3 hot-rolled sections + Z + bracing

| Member | Section | Governing check (M = wL²/8, δ = 5wL⁴/384EI) |
|---|---|---|
| Columns ×27, 2.95–4.14 m | **HEA 160** | N_Ed ≤ 70 kN vs N_b,Rd 455 kN; wall-wind M 12 ≪ 67 kNm |
| Primaries E-W, 96 m | **IPE 330** | K19–K20 9.8 m, w = 10.5 kN/m: M = 126/221 kNm (0.57), δ = 35 mm = L/276. Others ≤0.25 (IPE 300 fails only here, L/196) |
| Rafters + edge beams, 171 m | **IPE 270** | 9.2 m @ 2.7 m: M = 45/133 (0.34), δ = 23 mm = L/407; uplift M ≈ 43 kNm on the free bottom flange → fly braces at third points for spans ≥7.5 m. |
| Purlins & girts, 620 m | **Z 200×2.0 S350** | 4.1 m: M = 4.9 kNm, δ = L/430 |
| Wall bracing B1–B7 | **2 L 70×7 crossed, tension-only**, 2 M20 per end | N-S bay H = 27 kN → T_Ed = 51 kN vs N_u,Rd ≈ 135 kN |
| Roof bracing | M20 rods 8.8 + turnbuckles | shear ≈ 30 kN ULS/strip → T ≈ 42 vs 141 kN |

Rafters frame into the primary web with **fin plates, bottom flanges flush** (no coping); primaries on 4-bolt **cap plates**; purlins on cleats. Two site details.

**Weight** (486 m²): columns 2.9 t, primaries 4.7 t, rafters 6.2 t, plates +10 % 1.5 t → hot-rolled **15.3 t (32 kg/m²)**; + Z 3.9 t + bracing 1.2 t → **≈20.4 t, 42 kg/m²** (IPE 300/240 saves ~1.5 t).

## 4. Bases on the hollow-block slab

Pinned base: plate 300×400×20 (perimeter columns offset so anchors keep ≥100 mm to the slab edge), **4 M20 resin anchors, h_ef 170–200 mm, in the solid column-head zone only** (trial-drill to prove it; never in block ribs), 40 mm non-shrink grout on levelling nuts.
Actions: interior K12 (42 m²) compression 66 kN, **net uplift ULS ≈ 63 kN**; braced-bay columns add ±22 kN (N-S, h/b = 3.7/4.6) or ±10 kN (E-W) plus bay shear 27 kN → **worst ≈ 70 kN uplift, 15 kN shear at K15/K19, K22/K23, K14/K18, K20/K27**. 4 M20 at h_ef 200 ≈ 100 kN group tension in cracked C25 – verify with the anchor supplier; solid zone under 600 mm → through-bolted spreader plate.

## 5. Pros / cons for this project

**Pros.** Simplest system: 3 hot-rolled sections, 2 connection types, no moment joints or site welding; the irregular grid is absorbed because rafters land anywhere on the primaries; heaviest piece IPE 330 × 9.8 m (480 kg); any local fabricator; erection without propping beyond the first braced bay.

**Cons (honest).** Two layers of beams weigh more than a portal or truss (42 vs ~30 kg/m²) and stack 0.6 m at the eave; stability hangs on 7 door-free wall bays – glazing the terrace sides pushes bracing north/west with higher base uplift; the light roof gives net uplift at every base in a slab of unknown build, so the column-head solid zones are the critical unknown; the 9.2 m rafters and 9.8 m primary have little reserve for a future ceiling.

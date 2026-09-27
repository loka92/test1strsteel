# System A - Hot-rolled mono-pitch portal frames spanning N-S

**Rev 1: openings at stair/elevator, single-plane slope.**

Rigid portal frames on **every N-S column line**: IPE rafters, HEA columns, haunched bolted end-plate knees, pinned bases on the existing slab. **One roof plane**, 6 % (3.4 deg) falling north: top-of-steel TOS = 3.45 + 0.06 x (35.87 - y), i.e. **3.45 m at the north edge** (3.15 m clear under rafter, 3.0 m at haunch) and **4.67 m at the south edge y 15.57**; no steps.

## 1. Framing layout

| Frame | x (m) | Columns | Bays (m) | Rafter |
|---|---|---|---|---|
| F1 west gable | 68.0 | K25 K19 K15 K8 K6 | 5.9 / 4.6 / 3.0 / 5.8 | IPE 240 |
| F2 | 72.1 | K26 K9 K5 | **13.4** / 6.0 | IPE 300 |
| F3 | 77.8 | K27 K20 K16 K10 K7 | 5.9 / 2.7 / 4.8 / 5.9 | IPE 240 |
| F4 | 81.85 | K21 K17 K11 K3 | 4.4 / 4.8 / 6.4 | IPE 240 |
| F5 (propped) | 87.2 | girder, K12 K1 | **9.2 propped** / 6.5 | IPE 300 |
| F6 (propped) | 92.5 | girder, K13 K2 | **9.2 propped** / 6.5 | IPE 300 |
| F7 east gable | 95.55 | K23 K18 K14 K4 | 4.4 / 4.8 / 6.4 | IPE 240 |

- Spacing 4.1 / 5.7 / 4.0 / 5.4 / 5.3 / 3.0 m. K24 and K22 become pinned eave posts HEA 160.
- **Openings (Rev 1)**: stair well (x 77.89-81.79, y 29.37-35.37) and elevator shaft (x 77.89-81.99, y 20.17-24.16) are not roofed. F3 and F4 rafters sit on the shaft walls, beside the voids; no purlin crosses them. **Trimmers IPE 200** at y 20.17, 24.16, 29.37 and 35.37 span F3-F4 (4.05 m); upstand + flashing all sides; the north eave beam jogs to the y 35.37 trimmer.
- **East-wing south edge (y 20.07)**: transfer eave girder IPE 300 on K21-K22-K23 (4.0 / 7.1 / 6.6 m) carries the pinned F5/F6 rafter ends (approx. 35 kN each).
- **Notch corner (77.8, 20.07)**: no column; girder spans K21 to the F3 rafter, corner post SHS 100x100 hung from it.
- **Purlins** Z200x2.0 S350GD @ 1.5 m, sleeved, sag bars per bay; panel overhangs to the gutter at y 35.87. **Eaves beams** IPE 200.
- **Stability**: N-S by portal action. E-W by vertical X bracing (rods M20) in wall bays K6-K5, K2-K4, K25-K26, K22-K23 plus roof X bracing CHS 76.3x3.2 in bays 68.0-72.1, 81.85-87.2 (moved off the openings), 92.5-95.55, plus one panel between the openings.

## 2. Preliminary loads (EN 1991)

| Load | kN/m2 |
|---|---|
| Dead: panel 0.12 + purlins 0.05 + services 0.20 + frames 0.08 | **0.45** |
| Imposed cat. H (psi0 = 0) | **0.60** |

Wind: v_b = 30 m/s, terrain II, z_e approx. 10 m: **q_p = 1.30 kN/m2**. Mono-pitch c_pe (5 deg row): theta 0 F -1.7, G -1.2, H -0.6; theta 180 F -2.3, G -1.3, H -0.8; c_pi +0.2 / -0.3. Net: roof **-1.0 to -1.3 kN/m2** uplift, edge zones and opening edges up to **-3.3 kN/m2**; walls approx. 0.9 / 0.5 kN/m2.

Combinations: 1.35G + 1.5Q; 1.35G + 1.5Q + 0.9W; 1.35G + 1.5W; **1.0G + 1.5W (uplift)**; seismic G only. Design gravity 1.51 kN/m2.

## 3. Members (S275)

| Member | Section | Justification |
|---|---|---|
| Rafters F2, F5, F6 | **IPE 300** | F2: w = 7.4 kN/m, wL2/8 = 166 kNm, knee approx. 105 / midspan 80 kNm; M_pl,Rd = 173 kNm; delta_Q L/380 |
| Rafters F1, F3, F4, F7 | **IPE 240** | bays <= 6.4 m, M <= 35 kNm |
| Columns F2, F5, F6 (7) | **HEA 200** | knee approx. 100 kNm, N approx. 60 kN; M_pl,Rd = 118 kNm |
| Columns others + posts (20) | **HEA 160** | M <= 40 kNm, M_pl,Rd = 68 kNm |
| Haunches | same IPE, 1.0-1.3 m | M20 8.8 end plates |
| Transfer girder y 20.07 | IPE 300 | 35 kN on 7.1 m, M approx. 70 kNm, deflection governs |
| Eaves beams, opening trimmers | IPE 200 | 4-5.7 m; trimmers 4.05 m |
| Purlins / girts | Z200x2.0 / Z150x1.5 @ 1.5 m | 2.3 kN/m on 5.7 m: M approx. 7 < 12 kNm |
| Bracing walls / roof | rods M20 / CHS 76.3x3.2 | 35-45 kN |

Weight: rafters + haunches 4.7 t, columns 3.8 t, eaves beams + trimmers 2.0 t, bracing + posts 1.5 t, +12 % connections: primary **13.3 t = 27 kg/m2** (footprint 484 m2); purlins/girts 3.0 t. **Total approx. 16.3 t = 34 kg/m2** of footprint (37 kg/m2 of 444 m2 roofed). Sections unchanged.

## 4. Base connection on the ribbed slab

Pinned: plate 300x400x20 on **30-50 mm non-shrink grout**, 4 x M20 8.8 chemical anchors h_ef 160-180 mm in the solid zone, 100-150 mm outside the column outline. Per base: N approx. 60 kN, **uplift 25-35 kN**, V 25 kN portal thrust (inward under gravity, 10-15 kN outward under wind), 35-45 kN in braced bays. Cone capacity approx. 100 kN > uplift. Perimeter columns are flush with the slab edge: keep brace shear parallel to the edge, shear lug or through-bolt where outward thrust > 10 kN. Grout pad essential: slab levels vary +-20-30 mm.

## 5. Pros / cons

**Pros**: standard bolted system, 2 rafter + 2 column sections; every column used, one transfer only; low profile (5 m); N-S stability needs no bracing, so north/south facades stay free; openings fall between F3 and F4, only four trimmers added.

**Cons (honest)**: the irregular grid gives **7 different frame geometries**; sections are set by 3 long-span frames, so 34 kg/m2 is heavy for mostly short bays; F5/F6 need a propped end and the notch a hung post; rigid knees push moment towards anchors of limited capacity in a 250 mm slab; the opening bay loses its roof diaphragm, so the wings are tied only through the strip between the openings.

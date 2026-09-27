# System A - Hot-rolled mono-pitch portal frames spanning N-S

Rigid portal frames on **every N-S column line**: IPE rafters, HEA columns, haunched bolted end-plate knees, pinned bases on the existing slab, Z purlins. Roof plane **6 % (3.4 deg) falling north**. North eave rafter centreline +3.45 m (3.0 m clear under haunch); south eave +4.6 m (west) / +4.4 m (east).

## 1. Framing layout

| Frame | x (m) | Columns | Bays (m) | Rafter |
|---|---|---|---|---|
| F1 west gable | 68.0 | K25 K19 K15 K8 K6 | 5.9 / 4.6 / 3.0 / 5.8 | IPE 240 |
| F2 | 72.1 | K26 K9 K5 | **13.4** / 6.0 | IPE 300 |
| F3 interior (roof edge for y < 20.1) | 77.8 | K27 K20 K16 K10 K7 | 5.9 / 2.7 / 4.8 / 5.9 | IPE 240 |
| F4 | 81.85 | K21 K17 K11 K3 | 4.4 / 4.8 / 6.4 | IPE 240 |
| F5 (no column at y 20.1) | 87.2 | girder, K12 K1 | **9.2 propped** / 6.5 | IPE 300 |
| F6 (idem) | 92.5 | girder, K13 K2 | **9.2 propped** / 6.5 | IPE 300 |
| F7 east gable | 95.55 | K23 K18 K14 K4 | 4.4 / 4.8 / 6.4 | IPE 240 |

- Spacing 4.1 / 5.7 / 4.0 / 5.4 / 5.3 / 3.0 m. K24 and K22 become pinned eave posts HEA 160.
- **East-wing south edge (y 20.07)**: transfer eave girder IPE 300 on K21-K22-K23 (4.0 / 7.1 / 6.6 m) carries the pinned south ends of the F5/F6 rafters (approx. 35 kN each).
- **Notch corner (77.8, 20.07)**: no column. Girder spans K21 to the F3 rafter; corner post SHS 100x100 hung from it, base laterally restrained only.
- **Purlins** Z200x2.0 S350GD @ 1.5 m, sleeved, one row of sag bars per bay. North column line steps 0.5 m at x 81.8; panel overhangs to a straight gutter. **Eaves beams** IPE 200.
- **Stability**: N-S by portal action. E-W by vertical X bracing (rods M20) in wall bays K6-K5, K2-K4, K25-K26, K22-K23 plus roof X bracing CHS 76.3x3.2 in bays 68.0-72.1, 77.8-81.85, 92.5-95.55.

## 2. Preliminary loads (EN 1991)

| Load | kN/m2 |
|---|---|
| Dead: panel 0.12 + purlins 0.05 + services 0.20 + frames 0.08 | **0.45** |
| Imposed cat. H (psi0 = 0) | **0.60** |
| Wall cladding | 0.30 per m2 wall |

Wind: v_b = 30 m/s, terrain II, z_e approx. 10 m: **q_p = 1.30 kN/m2**. Mono-pitch c_pe (5 deg row): theta 0 F -1.7, G -1.2, H -0.6; theta 180 F -2.3, G -1.3, H -0.8; c_pi +0.2 / -0.3. Net: roof **-1.0 to -1.3 kN/m2** uplift, edge zones up to **-3.3 kN/m2**; frames -1.1 uniform; walls approx. 0.9 / 0.5 kN/m2.

Combinations: 1.35G + 1.5Q; 1.35G + 1.5Q + 0.9W; 1.35G + 1.5W; **1.0G + 1.5W (uplift)**; seismic G only (added mass approx. 37 t). SLS rafters L/200. Design gravity 1.51 kN/m2.

## 3. Members (S275)

| Member | Section | Justification |
|---|---|---|
| Rafters F2, F5, F6 | **IPE 300** | F2: w = 7.4 kN/m, wL2/8 = 166 kNm, knee approx. 105 / midspan 80 kNm; M_pl,Rd = 173 kNm; L/d 45; delta_Q L/380 |
| Rafters F1, F3, F4, F7 | **IPE 240** | bays <= 6.4 m, M <= 35 kNm; stiffness governs |
| Columns F2, F5, F6 (7) | **HEA 200** | knee approx. 100 kNm, N approx. 60 kN; M_pl,Rd = 118 kNm |
| Columns others + posts (20) | **HEA 160** | M <= 40 kNm, M_pl,Rd = 68 kNm |
| Haunches | same IPE, 1.0-1.3 m | M20 8.8 end plates |
| Transfer girder y 20.07 | IPE 300 | 35 kN on 7.1 m, M approx. 70 kNm, deflection governs |
| Other eaves beams | IPE 200 | 4-5.7 m |
| Purlins / girts | Z200x2.0 / Z150x1.5 @ 1.5 m | 2.3 kN/m on 5.7 m: M approx. 7 < 12 kNm |
| Bracing walls / roof | rods M20 / CHS 76.3x3.2 | 35-45 kN per diagonal |

Weight: rafters + haunches 4.7 t, columns 3.8 t, eaves beams 1.6 t, bracing + posts 1.4 t, +12 % connections: primary **12.9 t = 27 kg/m2**; purlins/girts 3.1 t. **Total approx. 16 t = 33 kg/m2** on 484 m2.

## 4. Base connection on the ribbed slab

Pinned: plate 300x400x20 on **30-50 mm non-shrink grout** (strip screed locally, bush-hammer, re-seal), 4 x M20 8.8 chemical anchors h_ef 160-180 mm in the 250 mm solid zone, 100-150 mm outside the 20x40 column outline. Per base: N approx. 60 kN, **uplift 25-35 kN**, V approx. 25 kN portal thrust (inward under gravity, 10-15 kN outward under wind), 35-45 kN along the wall in braced bays. Group cone capacity approx. 100 kN > uplift; global uplift nil. Perimeter columns sit flush with the slab edge, so outward shear has little edge distance: keep brace shear parallel to the edge, add a shear lug or through-bolt where outward thrust > 10 kN. The grout pad is essential: 27 slab levels will vary +-20-30 mm.

## 5. Pros / cons

**Pros**: standard bolted system, 2 rafter + 2 column sections; every column used, one transfer only; low profile (5 m); N-S stability needs no bracing, so north/south facades stay free; pieces max 13.4 m, small crane; near-square HEA columns indifferent to concrete column orientation.

**Cons (honest)**: the irregular grid gives **7 different frame geometries**; sections are set by 3 frames while two thirds of the bays are under 6.5 m, so 33 kg/m2 is heavy for the spans; F5/F6 need a propped end and the notch a hung post; rigid knees on short columns push moment towards anchors of limited capacity in a 250 mm slab; haunches cost 0.3-0.4 m of eave height; E-W stiffness rests on 4 rod-braced bays.

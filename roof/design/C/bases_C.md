# Alternative C - base and anchor design note, Rev 4 (bases_C.md)

Self-contained note for the base reviewer, replacing Rev 3 after the sign-off check (S1-S4). Loads from `calc/run_all.py` (reactions_C.csv: every column and load case with concurrent N, V_x, V_y, base type and utilisation); anchorage basis `../load_basis.md` Rev 2. Units kN, mm, MPa.

**Rev 4 in one paragraph.** The slab edge is now modelled where it is: 100 mm from the centre of every perimeter column (column flush with the building face) and at the stair / shaft openings (treated as free slab edges). With the real edges the concentric 4-anchor group has only 50 kN (one edge) / 38 kN (corner) of cone resistance and Key A next to the face has only 18-24 kN parallel-to-edge resistance, so the base type is now chosen per column: **B1** (concentric resin anchors + Key A + Key B) where the real-edge cone and the parallel-edge check pass at <= 0.90 (15 bases: K3, K4, K5, K6, K7, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26), **B2** (through-bolts + inboard key pair, the Rev 3 fallback made primary with corrected lever statics) at the 11 perimeter and edge-adjacent bases that do not (K1, K2, K10, K15, K18, K19, K20, K22, K23, K25, K27), and **P** at the K21 pier. Nothing is drilled into a column head except the K21 pier anchors.

## 1. Base details

**B1 - concentric anchors (interior and lightly loaded edge bases):** plate 300 x 400 x 25 S275 (350 across at near-edge bases, 100 outboard / 250 inboard) on 25 mm non-shrink grout; **4 M20 8.8 resin anchors at 80 x 280, h_ef 200 in the slab**, 280 along the concrete column's long axis, 26 mm clearance holes (tension only); **Key A** SHS 90x90x8 stub, 180 embedded in a 140 mm cored pocket 200 deep under the column centre (along-axis and inward shear; compressible strip on the outboard face where an edge is closer than 0.25 m); **Key B** 60 mm bar (f_y 335), 180 embedded in a 110 mm pocket 200 deep, 180 mm inboard on the outward axis (c1 250) where an outward shear > 3 kN points to an edge closer than 0.25 m. The cone is evaluated with the concrete actually there: outboard row 60 mm from the face at K3, K4, K6, K7, K8, K11, K14 (N_Rd,c 50 / 38 at corners, psi_s 0.76), 160-360 mm at K16, K17, K24, K26, full 800 at K5, K9, K12, K13. Key A parallel-to-edge breakout (2 V_Rk,c at c1 = distance - 45) is checked wherever an edge is closer than 0.6 m.

**B2 - through-bolts and inboard key pair (perimeter / edge-adjacent bases with uplift or along-wall shear beyond B1):** plate **700 (along the wall) x 550 (across: 100 outboard, 450 inboard) x 30 S275** with two 120 x 10 stiffeners from the column flange tips to the inboard plate end (stiffened section M_Rd 48 kNm, plastic); **2 M24 8.8 through-bolts** (F_t,Rd 203 kN) in a row 250 mm inboard of the column centre, 280 apart along the wall, both >= 300 mm from every slab edge (row shifted along the wall at corners and next to openings, table in section 3), bearing on a **400 x 200 x 20 plate under the slab** (cut to the solid zone soffit beside the column; ceiling access at each base); the bolts sit in 26 mm clearance holes (no shear). Uplift is carried by **lever action**: the bolts hold the plate down at the row (centroid distance c from the column), the inboard plate tip (b = c + 180) bears on the grout: T = N_t b/(b - c), C = T - N_t. Shear is carried by a **pair of SHS 90x90x8 keys** (140 pockets, 200 deep) 200 mm inboard of the column line and +/- 300 mm along the wall (both keys >= 300 mm from every edge, c1 >= 255): each key takes half the shear plus the torque of the eccentric shear (V x 0.2 m about the pair centroid, arm 0.6 m); outward components are checked as plain-concrete edge breakout at their own c1, resultants as bearing at 1.5 f_cd. No anchor cone and no anchor shear at B2 bases; the slab is not relied on for tension (through-bolts) and the shear keys sit in confined concrete.

**P - K21 (200 mm pier between the notch edge and the shaft opening):** plate 300 x 400 x 25; **4 M16 8.8 resin anchors at 70 x 280, h_ef 400 into the pier** (the only place where the client's permission to drill a column head is used: the pier has no inboard side and no soffit access); EN 1992-4 gives no cone in a 200 mm wall, so the anchors are designed as a lap with the pier's vertical bars (EN 1992-1-1 8.7 logic): bond 4 x pi x 16 x 400 x 10 = 804 kN / 1.5 = 536 kN, steel 323 kN, splitting of the pier restrained by two dia6 links (4 legs, f_yd 435) = 49 kN over the 400 mm lap; **saddle** of two 15 mm plates 400 x 150 on the pier faces for the N-S shear (82 kN). Rebar scan mandatory (links at <= 200 and 6 dia14 confirmed).

**Wind post WP1** (notch corner, no concrete column): post moved 280 mm inboard on both axes to (77.61, 20.25), plate 250 x 250 x 15, one centred 60 mm key (c1 250 both ways), 2 M12 for location, no uplift (slotted top connection). Demand 11.8 / 8.8 kN (E-W / N-S) vs 38.2 kN -> 0.31.

## 2. Resistances (EN 1992-4 with the basis values; EN 1993-1-8 and EN 1992-1-1 6.7 for plates and keys)

| Item | Formula / factors | Value |
|---|---|---|
| B1 anchor steel, per M20 | 196 / 1.4 | 140.0 kN |
| B1 cone, single, slab | k 7.2 (cracked) sqrt(25) 200^1.5 | N0_Rk,c = 101.8 kN |
| B1 cone group, interior (800 zone) | A_c,N/A0 = 800 x 680 / 600^2 = 1.511, psi_s 0.96 | N_Rd,c = 98.5 kN |
| B1 cone group, one edge at 100 mm from the column centre | outboard row 60 mm from the face: A = (60+80+300)(300+280+300) = 0.978 x 600^2, psi_s = 0.7 + 0.3 x 60/300 = 0.76 | **N_Rd,c = 50.4 kN** |
| B1 cone group, corner (two edges at 100 mm) | A = 440 x 640 | **37.8 kN** |
| B1 bond group | pi 20 x 200 x 10 = 125.7 kN single, s_cr,Np 462, A_p,N/A0 1.88 | N_Rd,p = 157.9 kN |
| Eccentric tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key/N_t (key moment V x 85 mm); max anchor N_t/4 + M/(2 s) | per case |
| Plate bearing (compression) | c = 76 mm, A_eff = 934 cm2 at 10 MPa | 934 kN |
| B1 plate T-stub under uplift, per row | m = 55, l_eff 300, t 25 | 934 kN |
| Key A bearing (B1 centre key and B2 pair) | rigid stub, z0 = 113 mm, p_max = V z0/(b(z0 D - D^2/2)), b 90, D 180, sigma_Rd 1.5 f_cd = 25 MPa (confined, >= 250 mm from a face) | **V_Rd,A = 83.8 kN** per key |
| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3 f_y 355 -> 26.6 kNm at lever 85; a = 8 | 313 / 673 kN |
| Key A parallel to an edge (B1, EN 1992-4 7.2.2.5 with psi_alpha = 2) | c1 = edge distance - 45: c1 55 -> 18.5 kN, c1 155 -> 56.6 kN, c1 255 -> 83.0 kN | used at K3, K4, K6, K7, K8, K11, K14, K16, K17, K24, K26 |
| Key towards an edge (Key B c1 250; B2 pair c1 >= 255; Key A 0.25-0.6 m) | 7.2.2.5, k9 1.7 cracked, d_nom 60 / 90, l_f 180, A_c,V/A0, psi_h | c1 250 (d 60): **38.2 kN**; c1 255 (d 90): **41.5 kN**; c1 355 (d 90): 53.1 kN |
| Key B bearing / bending | 60 mm bar, plain f_cd; W_pl d^3/6, f_y 335 | 37.2 / 142 kN |
| B2 through-bolt | M24 8.8, 0.9 x 800 x 353 / 1.25 | 203.3 kN each |
| B2 lever | T = N_t b/(b - c), C = T - N_t, c = bolt-row centroid distance, b = c + 180 (plate tip); bolt tension per M24 = T/2 + M_key/(2 x 0.28) | per base, section 3 |
| B2 tip bearing | 350 x 60 strip at 10 MPa | 210 kN |
| B2 stiffened plate | 350 x 30 plate + 2 stiffeners 120 x 10, plastic | M_Rd 48 kNm vs N_t c + M_key |
| B2 under-slab plate | 400 x 200 on the solid-zone soffit at 10 MPa | 800 kN |
| P (K21) | bond 536 kN, steel 323 kN, splitting (links) 49 kN; saddle 82.5 kN | |

Anchors and through-bolts carry no shear (clearance holes); keys and saddle carry no tension; the key moments enter the anchor group (B1: psi_ec,N and max anchor) or the bolt row and plate (B2). B2 base plates are checked for the lever moment N_t c + M_key on the stiffened section.

## 3. Final base-type table (ULS envelope; reactions_C.csv has every case)

| Col | Type | Long axis | Bays | Near edges (< 0.25 m) | Keys | Bolts / anchors (mm from the column centre) | N_c max (case) | N_t max (case) | V max (case) | Tension util. | Key util. | Plate util. | **Governing** | Min. inboard zone |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | **B2** | E-W | B1 | +y | A-pair at (-300, -200) / (300, -200) | 2 M24 through at (-140, -250) / (140, -250), lever 2.39 | 54.7 (ULS2E) | 34.0 (ULS3N) | 33.5 (ULS2W) | 0.21 | 0.42 | 0.22 | **0.42** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K2 | **B2** | E-W | B1 | +y | A-pair at (-300, -200) / (300, -200) | 2 M24 through at (-140, -250) / (140, -250), lever 2.39 | 46.9 (ULS2W) | 36.1 (ULS3N) | 34.4 (ULS2E) | 0.24 | 0.45 | 0.25 | **0.45** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K3 | **B1** | N-S | - | +y | A centre + B +y | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 31.1 (ULS1) | 15.1 (ULS3N) | 15.0 (ULS2N) | 0.33 | 0.37 | 0.03 | **0.37** (Key B outward +y) | outboard to the face, inboard >= 300, along +/- 300 |
| K4 | **B1** | N-S | - | +x,+y | A centre + B +x,+y | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 19.8 (ULS1) | 14.6 (ULS3E) | 14.8 (ULS2N) | 0.53 | 0.37 | 0.02 | **0.53** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K5 | **B1** | E-W | B2 | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 57.6 (ULS2E) | 42.1 (ULS3W) | 41.6 (ULS2W) | 0.59 | 0.50 | 0.06 | **0.59** (anchor group cone, real edges) | >= 600 x 600 centred |
| K6 | **B1** | N-S | - | -x | A centre + B -x | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 25.2 (ULS1) | 18.0 (ULS3W) | 16.3 (ULS2N) | 0.48 | 0.48 | 0.03 | **0.48** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K7 | **B1** | N-S | B2 | +x | A centre | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 52.0 (ULS2W) | 26.4 (ULS3E) | 41.6 (ULS2E) | 0.86 | 0.85 | 0.06 | **0.86** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K8 | **B1** | N-S | - | -x | A centre + B -x | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 30.1 (ULS1) | 26.4 (ULS3W) | 15.8 (ULS2W) | 0.61 | 0.39 | 0.03 | **0.61** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K9 | **B1** | E-W | - | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 57.2 (ULS1) | 52.2 (ULS3N) | 0.0 (ULS1) | 0.53 | 0.00 | 0.06 | **0.53** (anchor group cone, real edges) | >= 600 x 600 centred |
| K10 | **B2** | E-W | B8 | +y | A-pair at (-300, -200) / (300, -200) | 2 M24 through at (-140, -250) / (140, -250), lever 2.39 | 78.8 (ULS2S) | 58.1 (ULS3N) | 33.2 (ULS2N) | 0.37 | 0.20 | 0.38 | **0.38** (B2 tip bearing) | >= 550 from the face (bolts + under-slab plate) |
| K11 | **B1** | E-W | - | +y | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 43.6 (ULS1) | 33.9 (ULS3N) | 0.0 (ULS1) | 0.67 | 0.00 | 0.05 | **0.67** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K12 | **B1** | E-W | - | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 70.5 (ULS1) | 66.7 (ULS3N) | 0.0 (ULS1) | 0.68 | 0.00 | 0.08 | **0.68** (anchor group cone, real edges) | >= 650 x 650 centred |
| K13 | **B1** | E-W | - | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 55.7 (ULS1) | 54.0 (ULS3N) | 0.0 (ULS1) | 0.55 | 0.00 | 0.06 | **0.55** (anchor group cone, real edges) | >= 600 x 600 centred |
| K14 | **B1** | E-W | B6 | +x | A centre + B +x | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 56.7 (ULS2S) | 26.4 (ULS3N) | 30.8 (ULS2N) | 0.66 | 0.49 | 0.06 | **0.66** (anchor group cone, real edges) | outboard to the face, inboard >= 300, along +/- 300 |
| K15 | **B2** | N-S | B5 | -x | A-pair at (200, -300) / (200, 300) | 2 M24 through at (250, -140) / (250, 140), lever 2.39 | 43.6 (ULS2S) | 16.7 (ULS3N) | 23.5 (ULS2N) | 0.12 | 0.31 | 0.13 | **0.31** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K16 | **B1** | N-S | B8 | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 43.8 (ULS2N) | 58.4 (ULS3S) | 57.3 (ULS2S) | 0.76 | 0.68 | 0.05 | **0.76** (anchor group cone, real edges) | >= 700 x 700 centred |
| K17 | **B1** | N-S | - | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 23.2 (ULS1) | 15.7 (ULS3S) | 0.0 (ULS1) | 0.20 | 0.00 | 0.02 | **0.20** (anchor group cone, real edges) | >= 400 x 400 centred |
| K18 | **B2** | N-S | B6,B9 | +x | A-pair at (-200, -300) / (-200, 300) | 2 M24 through at (-250, -140) / (-250, 140), lever 2.39 | 54.2 (ULS2S) | 39.5 (ULS3S) | 45.5 (ULS2S) | 0.27 | 0.54 | 0.29 | **0.54** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K19 | **B2** | N-S | B5,B10 | -x | A-pair at (200, -300) / (200, 300) | 2 M24 through at (250, -140) / (250, 140), lever 2.39 | 79.9 (ULS2S) | 73.1 (ULS3S) | 40.2 (ULS2S) | 0.46 | 0.52 | 0.48 | **0.52** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K20 | **B2** | N-S | B7 | +x | A-pair at (-200, -300) / (-200, 300) | 2 M24 through at (-250, -140) / (-250, 140), lever 2.39 | 82.3 (ULS2S) | 64.0 (ULS3N) | 29.5 (ULS2N) | 0.40 | 0.23 | 0.42 | **0.42** (B2 tip bearing) | >= 550 from the face (bolts + under-slab plate) |
| K21 | **P** | E-W | - | +y,-y | saddle | 4 M16 h_ef 400 in the pier, 70 x 280 | 39.8 (ULS1) | 19.8 (ULS3S) | 29.3 (ULS2W) | 0.53 | 0.36 | 0.04 | **0.53** (P pier anchors: splitting of the 200 pier restrained by the dia6/200 links) | pier 200 x >= 800 |
| K22 | **B2** | E-W | B3 | -y | A-pair at (-300, 200) / (300, 200) | 2 M24 through at (-140, 250) / (140, 250), lever 2.39 | 90.6 (ULS2E) | 56.3 (ULS3S) | 59.0 (ULS2W) | 0.35 | 0.74 | 0.37 | **0.74** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K23 | **B2** | E-W | B3,B9 | +x,-y | A-pair at (-700, 200) / (-100, 200) | 2 M24 through at (-380, 250) / (-100, 250), lever 2.93 | 63.7 (ULS2W) | 62.1 (ULS3S) | 63.7 (ULS2E) | 0.49 | 0.80 | 0.57 | **0.80** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K24 | **B1** | E-W | - | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 E-W) | 23.9 (ULS1) | 23.6 (ULS3S) | 16.4 (ULS2E) | 0.28 | 0.31 | 0.03 | **0.31** (Key A towards edge -y) | >= 450 x 450 centred |
| K25 | **B2** | N-S | B4,B10 | -x | A-pair at (200, 0) / (200, 600) | 2 M24 through at (250, 0) / (250, 280), lever 2.59 | 47.8 (ULS2E) | 42.6 (ULS3W) | 47.0 (ULS2S) | 0.30 | 0.83 | 0.32 | **0.83** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| K26 | **B1** | N-S | B4 | - | A centre | 4 M20 h_ef 200, 80 x 280 (280 N-S) | 50.1 (ULS2W) | 30.5 (ULS3E) | 26.7 (ULS2E) | 0.54 | 0.34 | 0.05 | **0.54** (anchor group cone, real edges) | >= 550 x 550 centred |
| K27 | **B2** | N-S | B7 | +x | A-pair at (-200, 0) / (-200, 600) | 2 M24 through at (-250, 0) / (-250, 280), lever 2.59 | 38.8 (ULS2N) | 44.1 (ULS3S) | 59.3 (ULS2S) | 0.33 | 0.76 | 0.37 | **0.76** (B2 key pair outward) | >= 550 from the face (bolts + under-slab plate) |
| WP1 | post | - | - | +x,-y | one 60 mm key centred, c1 250 | 2 M12 location | 1.7 | 0 | 11.8 | - | 0.31 | - | **0.31** (key edge) | notch edge beam |

Worst base **K7 (B1): 0.86 (anchor group cone, real edges (N_Rd,c 50, psi_ec 0.61), ULS3E)**; worst tension 0.86 at K7; worst key 0.85 at K7; worst plate 0.57 at K23. All 27 bases and WP1 <= 1.0 with the real slab edges.

## 4. Worked checks

**K12 (B1)** - concrete beyond the anchor rows (across-, across+, along-, along+) = 360, 360, 260, 260 mm -> A_c,N/A0 1.511, psi_s 0.96, N_Rd,c 98.5 kN. Governing tension case ULS3N: N_t 66.7 kN with V = (0.0, 0.0), key moments 0.0 / 0.0 kNm, psi_ec 1.00: Key A SHS bearing 0.00; anchor group cone, real edges (N_Rd,c 98, psi_ec 1.00) 0.68; anchor group bond 0.42; anchor steel (max anchor 17 kN) 0.12; plate T-stub 0.04; plate strip at key moment 0.00.

**K7 (B1)** - concrete beyond the anchor rows (across-, across+, along-, along+) = 360, 60, 260, 260 mm -> A_c,N/A0 0.978, psi_s 0.76, N_Rd,c 50.4 kN. Governing tension case ULS3E: N_t 26.4 kN with V = (-39.1, 14.3), key moments 1.2 / 3.3 kNm, psi_ec 0.61: Key A SHS bearing 0.50; Key A parallel to edge +x (c1 55) 0.78; anchor group cone, real edges (N_Rd,c 50, psi_ec 0.61) 0.86; anchor group bond 0.17; anchor steel (max anchor 30 kN) 0.21; plate T-stub 0.02; plate strip at key moment 0.35.

**K23 (B2)** - bolts at (-380, 250) / (-100, 250) (c = 347 mm, tip b = 527 mm, lever 2.93); keys at (-700, 200) / (-100, 200). Governing tension case ULS3E: N_t 59.3 kN with V = (-62.8, -10.4): B2 key pair bearing 0.54; B2 key pair outward (c1 >= 255) 0.80; B2 through-bolt tension (lever 2.93, 96 kN each) 0.47; B2 tip bearing (114 kN) 0.54; B2 stiffened plate (M 26 kNm) 0.54; B2 under-slab plate bearing 0.22. Max shear case ULS2E: 63.7 kN.

**K19 (B2)** - bolts at (250, -140) / (250, 140) (c = 250 mm, tip b = 430 mm, lever 2.39); keys at (200, -300) / (200, 300). Governing tension case ULS3S: N_t 73.1 kN with V = (-19.5, 35.1): B2 key pair bearing 0.33; B2 key pair outward (c1 >= 255) 0.52; B2 through-bolt tension (lever 2.39, 93 kN each) 0.46; B2 tip bearing (102 kN) 0.48; B2 stiffened plate (M 22 kNm) 0.45; B2 under-slab plate bearing 0.22. Max shear case ULS2S: 40.2 kN.

## 5. Coring acceptance criterion (one-sided at edge heads) and what happens if it fails

- **B1 heads:** solid concrete (no blocks, no voids, full depth >= 250 mm, C25 by rebound + core) over the zone in the last column of the table: interior heads centred (>= 650 x 650 at K12, K9, K13 600, others <= 550); edge heads one-sided - outboard to the building face (100 mm), inboard >= 300 from the column centre, +/- 300 along the wall - which is what an edge beam or column-head solid zone normally provides. A B1 head that fails the criterion is built as B2 (the B2 detail needs no cone).
- **B2 heads:** solid concrete from the face to >= 550 mm inboard and +/- 400 along the wall (bolts at 300-450 from the face, under-slab plate, key pockets), soffit accessible from below (ceiling opening ~600 x 600 at each of the 11 bases). If the soffit is not accessible at a head, the alternative is the basis Rev 2 concept (anchors through the slab into the column head, h_ef >= 300, rebar scan) at that head only - to be agreed with the reviewer.
- **K21:** rebar scan confirming 6 dia14 and links at <= 200 in the top 500 mm of the pier; pier faces accessible for the saddle.
- Cores at 3 heads first (one B1 interior, one B1 edge, one B2), then every head by 60 mm core or GPR against its own line of the table.

## 6. Before anchor installation

1. Rebar scan of the slab top bars at every head; place the 140 / 110 mm pockets and the through-bolt holes to cut at most one top bar.
2. Pull-out test on 3 sacrificial M20 resin anchors (h_ef 200) to 1.3 x max B1 anchor = 45 kN; ETA group verification by the supplier (basis open item).
3. B2: torque the M24 through-bolts to snug + 1/4 turn after the grout has cured; check the under-slab plate seating (dry-pack).

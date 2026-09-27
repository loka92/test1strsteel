# Alternative C - base and anchor design note, Rev 3 (bases_C.md)

Self-contained note for the base reviewer, replacing Rev 2 after the focused review (R1-R7). Loads from `calc/run_all.py` (reactions_C.csv: every column and load case with concurrent N, V_x, V_y and the base utilisation); anchorage basis `../load_basis.md` Rev 2. Units kN, mm, MPa.

**Rev 3 in one paragraph.** Nothing is drilled into the column heads any more (R4): the client had permitted it, but the review showed it is unnecessary (h_ef 200 in the slab gives the same 98 kN) and risky (5-11 mm to the column bars). All anchors and keys stay within the 250 mm slab solid zone. The "column cage" shear resistance of Rev 2 is withdrawn (R1); outward shear towards a free slab edge is taken by a second key placed 180 mm inboard so that c1 = 250 mm, checked as plain-concrete edge breakout (cracked), or by a saddle at the K21 pier; the key moments V x 85 mm are carried into the anchor group as eccentric tension (psi_ec,N) and into the max anchor (R2); the minimum solid zone per base is tabulated with a coring acceptance criterion and a through-bolt fallback (R3). Minor items R5-R7 are in the tables.

## 1. Base details

**Type S (standard, 26 bases K1-K20, K22-K27):**
- Base plate **300 x 400 x 25 S275**, long side along the concrete column's 400 mm axis; at near-edge bases the plate is 350 wide across the wall, placed 100 mm outboard / 250 mm inboard of the column centre (corners 350 x 350 the same way). HEA 160 welded a = 6 all round, web across the concrete column's short axis. **25 mm** non-shrink grout (C50 class) on levelling shims.
- **4 M20 8.8 resin anchors, h_ef = 200 mm in the slab solid zone only**, pattern **80 x 280 with the 280 along the concrete column's long axis** (table in section 3: E-W for the 0.4 x 0.2 columns, N-S for the 0.2 x 0.4 columns); the anchors sit over the column head footprint (60 mm inside its faces) but stop 50 mm above the column top. Plate holes 26 mm (clearance): the anchors carry tension only. ETA h_min = h_ef + 2 d0 = 248 <= 250 OK.
- **Key A** under the column centre: SHS 90x90x8 S355 stub, 180 mm embedded (20 mm grout under its toe), welded to the plate a = 8 all round, in a **140 mm cored pocket 200 mm deep** (25 mm grout annulus, pocket position set after the rebar scan so that no more than one slab top bar is cut). It carries the shear along the column's long axis (bay shear along the wall) and the inward shear across; at near-edge bases a 25 mm compressible strip on the outboard face of the pocket stops it from taking outward shear.
- **Key B** (only where the table in section 3 says so: 14 bases with an outward demand towards a free slab edge closer than 0.25 m): 60 mm round bar S355 (f_y 335), 180 embedded, welded a = 8, in a **110 mm cored pocket 200 deep**, centred **180 mm inboard of the column centre on the outward axis**, so that c1 = 250 mm to the slab edge (350 at K3 where the edge is 0.2 m away). Corner bases K4, K6, K23, K25 have two Key B (one per edge). Key B lies on the axis of the outward force through the column, so the eccentric key adds no in-plane torque; the plate carries the force to the column as a deep beam (in-plane).
- Erection: level, grout the pockets and the bed, then set the resin anchors through the plate; nuts snug + 1/4 turn (no preload relied upon).

**Type P (K21, 200 mm pier between the notch edge y 19.97 and the shaft opening y 20.17):** no key; a **saddle** of two 15 mm S275 plates 400 x 150 welded to the plate edges, hanging down the north and south faces of the pier and grouted against them, carries the N-S base shear by bearing on the pier faces (400 x 150 each); E-W shear is negligible (no E-W bay, no E-W wall). Same plate and 4 anchors (h_ef 200 in the pier top; the pier is a wall element 200 thick - the cone is limited to the 200 x 800 concrete available, see section 3). Requires the pier faces to be accessible from the notch (outside) and the shaft top; to be confirmed on site.

**Wind post WP1** (notch corner, no concrete column): the post is moved **280 mm inboard on both axes** to (77.61, 20.25) so that a single centred 60 mm key has c1 = 250 to both slab edges; plate 250 x 250 x 15, 2 M12 for location only (no uplift: slotted top connection); the corner girts cantilever 280 mm to the wall line. Demand 11.8 kN (E-W) / 8.8 kN (N-S) vs 38.2 kN (edge breakout, either direction) -> 0.31.

## 2. Resistances (EN 1992-4 with the basis values; EN 1993-1-8 and EN 1992-1-1 6.7 for the plate and keys)

| Item | Formula / factors | Value |
|---|---|---|
| Anchor steel, per anchor | N_Rk,s 196 / gamma_Ms 1.4 | 140.0 kN |
| Concrete cone, single, slab | k 7.2 (cracked) sqrt(25) x 200^1.5 | N0_Rk,c = 101.8 kN |
| Cone group, zone 800 | s_cr,N 600, c_cr,N 300; group 80 x 280: A_c,N/A0 = 800 x 680 / 600^2 = 1.511; psi_s,N = 0.96; psi_re = 1; psi_ec,N per case (section 3) | N_Rk,c,g = 147.7 -> **N_Rd,c = 98.5 kN** |
| Cone group, zone 750 / 700 / 600 | same, boundary of the solid zone as free edges | N_Rd,c = 89.9 / 81.7 / 58.4 kN |
| Bond, single | pi x 20 x 200 x tau_Rk 10 (cracked) | N0_Rk,p = 125.7 kN |
| Bond group | s_cr,Np = 7.3 d sqrt(tau) = 462; A_p,N/A0 = 1.88; psi_s,Np = 1.00; psi_g,Np = 1.0 | N_Rd,p = 157.9 kN |
| Eccentric group tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key / N_t; max anchor = N_t/4 + M_along/(2 x 0.28) + M_across/(2 x 0.08) | per case |
| Bearing under the plate | c = t sqrt(f_y / 3 f_jd) = 76 mm, A_eff = 934 cm2 at f_jd 10 MPa | 934 kN |
| Plate T-stub under uplift, per anchor row | cantilever from the flange tips m = 55 mm, l_eff 300, t 25 | 934 kN |
| Key shear resultant | rigid stub in a grouted pocket, pressure linear with rotation point z0 = 113 mm below the slab top; resultant 85 mm below the plate (25 grout + 180/3) | M_key = V x 0.085 |
| Key A bearing | p_max = V z0 / (b (z0 D - D^2/2)), b = 90, D = 180 -> p_max = V x 0.298 MPa/kN; sigma_Rd = 1.5 f_cd = 25 MPa (partially loaded area in the solid zone) | **V_Rd,A = 83.8 kN** |
| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3, f_y 355 -> M_Rd 26.6 kNm at lever 85 mm; a = 8 all round | 313 / 673 kN |
| Key B bearing | 60 mm bar, plain f_cd 16.7 | 37.2 kN |
| Key B bending / weld | W_pl = d^3/6, f_y 335 -> M_Rd 12.1 kNm | 142 / 352 kN |
| **Key B concrete edge breakout, c1 = 250** | EN 1992-4 7.2.2.5, k9 1.7 (cracked), d_nom 60, l_f 180: V0_Rk,c = 70.3 kN; A_c,V/A0 = 750 x 250 / (4.5 x 250^2) = 0.667; psi_h = sqrt(375/250) = 1.22; psi_s = psi_alpha = psi_re = 1; / gamma_Mc 1.5 | **V_Rd,c = 38.2 kN** (c1 350: 49.5 kN) |
| Key A towards an edge 0.25-0.6 m away (no Key B) | same formula with d_nom 90, c1 = edge distance - 45 | e.g. c1 355: 53.1 kN |
| Saddle (K21) | bearing 400 x 150 on the pier faces; plate cantilever 150, t 15: M_Rd 6.2 kNm / 0.075 | 82.5 kN |
| Plate strip at the key moment | 300 mm strip, t 25 | 12.9 kNm |

Shear parallel to a slab edge at Key A (bay shear along the wall line, e.g. K23 68 kN at 70 mm from the notch edge) bears on concrete that is continuous along the wall (column head / edge beam / solid strip); it is checked as bearing (Key A), not as edge breakout, and the edge beam under every wall line is part of the coring scope (section 5). The anchors take no shear, so there is no anchor N-V interaction; the key moments enter the anchor group through psi_ec,N and the max-anchor check.

## 3. Every base: pattern, keys, governing actions, utilisation, minimum solid zone (ULS envelope; reactions_C.csv has all cases)

| Col | Long axis (280 spacing) | Bays | Near edges | Key B | N_c max (case) | N_t max (case) | V max (case) | M_key max kNm | psi_ec at N_t max | Max anchor kN | Governing check | **Util. (zone 800)** | Util. cone 750 / 700 / 600 | Min. zone mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | E-W | B1 | +y | +y | 54.7 (ULS2E) | 34.0 (ULS3N) | 33.5 (ULS2W) | 3.8 | 0.87 | 20 | anchor group cone (psi_ec 0.69) | **0.45** | 0.49 / 0.54 / 0.76 | 550 |
| K2 | E-W | B1 | +y | +y | 46.9 (ULS2W) | 36.1 (ULS3N) | 34.4 (ULS2E) | 4.0 | 0.90 | 23 | anchor group cone (psi_ec 0.71) | **0.51** | 0.56 / 0.62 / 0.86 | 600 |
| K3 | N-S | - | +y | +y | 31.1 (ULS1) | 15.1 (ULS3N) | 15.0 (ULS2N) | 1.3 | 0.78 | 6 | Key B outward +y (c1 250) | **0.37** | 0.21 / 0.24 / 0.33 | 400 |
| K4 | N-S | - | +x,+y | +x,+y | 19.8 (ULS1) | 14.6 (ULS3E) | 14.8 (ULS2N) | 1.6 | 0.73 | 11 | Key B outward +x (c1 250) | **0.37** | 0.22 / 0.24 / 0.34 | 400 |
| K5 | E-W | B2 | - | - | 57.6 (ULS2E) | 42.1 (ULS3W) | 41.6 (ULS2W) | 4.5 | 0.72 | 24 | anchor group cone (psi_ec 0.72) | **0.59** | 0.65 / 0.71 / 1.00 | 600 |
| K6 | N-S | - | -x | -x | 25.2 (ULS1) | 18.0 (ULS3W) | 16.3 (ULS2N) | 1.8 | 0.74 | 13 | Key B outward -x (c1 250) | **0.40** | 0.27 / 0.30 / 0.42 | 450 |
| K7 | N-S | B2 | +x | - | 52.0 (ULS2W) | 26.4 (ULS3E) | 41.6 (ULS2E) | 4.5 | 0.61 | 30 | Key A SHS bearing | **0.50** | 0.48 / 0.53 / 0.74 | 550 |
| K8 | N-S | - | -x | -x | 30.1 (ULS1) | 26.4 (ULS3W) | 15.8 (ULS2W) | 1.3 | 0.85 | 15 | Key B outward -x (c1 250) | **0.39** | 0.34 / 0.38 / 0.53 | 500 |
| K9 | E-W | - | - | - | 57.2 (ULS1) | 52.2 (ULS3N) | 0.0 (ULS1) | 0.0 | 1.00 | 13 | anchor group cone (psi_ec 1.00) | **0.53** | 0.58 / 0.64 / 0.89 | 600 |
| K10 | E-W | B8 | +x,+y | - | 78.8 (ULS2S) | 58.1 (ULS3N) | 33.2 (ULS2N) | 2.8 | 0.86 | 32 | anchor group cone (psi_ec 0.86) | **0.69** | 0.75 / 0.83 / 1.16 | 650 |
| K11 | E-W | - | +y | - | 43.6 (ULS1) | 33.9 (ULS3N) | 0.0 (ULS1) | 0.0 | 1.00 | 8 | anchor group cone (psi_ec 1.00) | **0.34** | 0.38 / 0.41 / 0.58 | 500 |
| K12 | E-W | - | - | - | 70.5 (ULS1) | 66.7 (ULS3N) | 0.0 (ULS1) | 0.0 | 1.00 | 17 | anchor group cone (psi_ec 1.00) | **0.68** | 0.74 / 0.82 / 1.14 | 650 |
| K13 | E-W | - | - | - | 55.7 (ULS1) | 54.0 (ULS3N) | 0.0 (ULS1) | 0.0 | 1.00 | 13 | anchor group cone (psi_ec 1.00) | **0.55** | 0.60 / 0.66 / 0.92 | 600 |
| K14 | E-W | B6 | +x | +x | 56.7 (ULS2S) | 26.4 (ULS3N) | 30.8 (ULS2N) | 3.7 | 0.66 | 23 | Key B outward +x (c1 250) | **0.49** | 0.45 / 0.49 / 0.69 | 550 |
| K15 | N-S | B5 | -x | -x | 43.6 (ULS2S) | 16.7 (ULS3N) | 23.5 (ULS2N) | 2.8 | 0.61 | 14 | Key B outward -x (c1 250) | **0.35** | 0.30 / 0.33 / 0.47 | 450 |
| K16 | N-S | B8 | +x | - | 43.8 (ULS2N) | 58.4 (ULS3S) | 57.3 (ULS2S) | 4.9 | 0.78 | 23 | anchor group cone (psi_ec 0.78) | **0.76** | 0.83 / 0.91 / 1.28 | 700 |
| K17 | N-S | - | - | - | 23.2 (ULS1) | 15.7 (ULS3S) | 0.0 (ULS1) | 0.0 | 1.00 | 4 | anchor group cone (psi_ec 1.00) | **0.16** | 0.17 / 0.19 / 0.27 | 400 |
| K18 | N-S | B6,B9 | +x | +x | 54.2 (ULS2S) | 39.5 (ULS3S) | 45.5 (ULS2S) | 5.0 | 0.69 | 25 | anchor group cone (psi_ec 0.69) | **0.58** | 0.64 / 0.70 / 0.99 | 600 |
| K19 | N-S | B5,B10 | -x | -x | 79.9 (ULS2S) | 73.1 (ULS3S) | 40.2 (ULS2S) | 4.6 | 0.82 | 34 | anchor group cone (psi_ec 0.82) | **0.91** | 0.99 / 1.09 / 1.53 | 750 |
| K20 | N-S | B7 | +x | - | 82.3 (ULS2S) | 64.0 (ULS3N) | 29.5 (ULS2N) | 2.5 | 0.88 | 20 | anchor group cone (psi_ec 0.88) | **0.73** | 0.80 / 0.89 / 1.24 | 700 |
| K21 | E-W | - | +y,-y | saddle | 39.8 (ULS1) | 19.8 (ULS3S) | 29.3 (ULS2W) | 2.2 | 0.78 | 8 | saddle plates (N-S) | **0.36** | 0.28 / 0.31 / 0.44 | 450 |
| K22 | E-W | B3 | -y | -y | 90.6 (ULS2E) | 56.3 (ULS3S) | 59.0 (ULS2W) | 6.7 | 0.87 | 35 | anchor group cone (psi_ec 0.68) | **0.78** | 0.85 / 0.94 / 1.31 | 700 |
| K23 | E-W | B3,B9 | +x,-y | +x,-y | 63.7 (ULS2W) | 62.1 (ULS3S) | 63.7 (ULS2E) | 6.2 | 0.76 | 46 | anchor group cone (psi_ec 0.76) | **0.83** | 0.91 / 1.00 / 1.40 | 750 |
| K24 | E-W | - | - | - | 23.9 (ULS1) | 23.6 (ULS3S) | 16.4 (ULS2E) | 1.4 | 0.87 | 13 | Key A towards edge -y (c1 355) | **0.31** | 0.30 / 0.33 / 0.47 | 450 |
| K25 | N-S | B4,B10 | -x | -x | 47.8 (ULS2E) | 42.6 (ULS3W) | 47.0 (ULS2S) | 5.3 | 0.78 | 31 | anchor group cone (psi_ec 0.65) | **0.57** | 0.63 / 0.69 / 0.96 | 600 |
| K26 | N-S | B4 | - | - | 50.1 (ULS2W) | 30.5 (ULS3E) | 26.7 (ULS2E) | 3.1 | 0.73 | 22 | anchor group cone (psi_ec 0.73) | **0.42** | 0.46 / 0.51 / 0.72 | 550 |
| K27 | N-S | B7 | +x | +x | 38.8 (ULS2N) | 44.1 (ULS3S) | 59.3 (ULS2S) | 6.0 | 0.67 | 27 | Key A SHS bearing | **0.69** | 0.73 / 0.80 / 1.12 | 650 |

Worst base **K19: 0.91 (anchor group cone (psi_ec 0.82), ULS3S)**; max uplift 73.1 kN at K19; max shear 63.7 kN at K23 (Key A 0.76). All 27 bases and WP1 <= 1.0 with the 800 x 800 solid zone; the cone group is the governing mode at the braced and interior bases, the Key B edge breakout at the lightly loaded perimeter bases.

## 4. Worked check, three representative bases

**K12 (long axis E-W, bays -, near edges none, Key B none)** - governing tension case ULS3N: N_t 66.7 kN with V = (0.0, 0.0) kN; Key A 0.0 kN along / 0.0 kN across, Key B none; key moments M_along 0.0 + M_across 0.0 kNm -> e_N 0 / 0 mm -> psi_ec 1.00 -> N_Rd,c = 98.5 x 1.00 = 98.5 kN -> **0.68**; max anchor 17 kN (steel 0.12); bond 0.42; plate row 0.04. Compression max 70.5 kN (ULS1): bearing 0.08. Shear max 0.0 kN (ULS1): Key A 0.00. Minimum solid zone 650 mm.

**K23 (long axis E-W, bays B3,B9, near edges +x,-y, Key B +x,-y)** - governing tension case ULS3S: N_t 62.1 kN with V = (12.2, 52.7) kN; Key A 0.0 kN along / 52.7 kN across, Key B +x 13.6 kN; key moments M_along 1.2 + M_across 4.5 kNm -> e_N 19 / 72 mm -> psi_ec 0.76 -> N_Rd,c = 98.5 x 0.76 = 74.7 kN -> **0.83**; max anchor 46 kN (steel 0.33); bond 0.39; plate row 0.04. Compression max 63.7 kN (ULS2W): bearing 0.07. Shear max 63.7 kN (ULS2E): Key A 0.76. Minimum solid zone 750 mm.

**K19 (long axis N-S, bays B5,B10, near edges -x, Key B -x)** - governing tension case ULS3S: N_t 73.1 kN with V = (-19.5, 35.1) kN; Key A 35.1 kN along / 0.0 kN across, Key B -x 19.5 kN; key moments M_along 3.0 + M_across 1.7 kNm -> e_N 41 / 23 mm -> psi_ec 0.82 -> N_Rd,c = 98.5 x 0.82 = 80.6 kN -> **0.91**; max anchor 34 kN (steel 0.24); bond 0.46; plate row 0.05. Compression max 79.9 kN (ULS2S): bearing 0.09. Shear max 40.2 kN (ULS2S): Key A 0.48. Minimum solid zone 750 mm.

## 5. Coring acceptance criterion and fallback (R3)

- Cores (100 mm) at 3 column heads first, then a 60 mm core or GPR confirmation at every head: **solid concrete (no blocks, no voids) over at least the minimum zone of section 3, in all cases >= 750 x 750 mm, full slab depth >= 250 mm, C25 or better (rebound + core), and an edge/drop beam under every perimeter wall line**. A head that meets this is built as Type S / P above. K19 and K23 need 750; K16, K20, K22 need 700; all others 650 or less.
- **Fallback for a head whose solid zone is smaller than its minimum**: 4 M20 8.8 through-bolts at 500 (along) x 300 (across) around the column footprint, bearing on a 300 x 400 x 15 plate under the slab (cut around the 200 x 400 column, i.e. two 400 x 50 strips joined by 100 wide cross plates, or four 100 x 100 x 15 plate washers on the solid concrete beside the column), base plate 400 x 450; at a perimeter head both rows go inboard (150 and 350 mm from the column centre, +/- 250 along) and the 250 mm eccentricity of N_t is resisted by the couple of the two rows (e.g. K19: 73 kN x 0.25 / 0.20 = 91 kN row force, 2 M20 per row, 141 kN each). Tension then goes to the under-slab plate (no cone, no bond); shear stays with the keys (their bearing is on the solid concrete of the head, present in every case). Nine bases carry the fallback on the drawings from the start: K9, K10, K12, K13, K16, K19, K20, K22, K23.
- No coring or drilling into a column head in any case (R4); if neither the solid zone nor the fallback can be built at a head, the bay layout (section 8 of the report) is revised, not the anchorage.

## 6. Site verification before anchor installation

1. Cores as above; rebar scan of the slab top bars at every head to place the 140 mm (Key A) and 110 mm (Key B) pockets so that at most one top bar is cut, and to keep the anchors 20 mm clear of the slab bars.
2. Pull-out test on 3 sacrificial anchors (h_ef 200) to 1.3 x max anchor = 60 kN before production drilling; anchor supplier's ETA group verification (basis open item).
3. K21: confirm access to the pier faces; WP1: confirm the notch edge beam (or use the Type S plate with two Key B).

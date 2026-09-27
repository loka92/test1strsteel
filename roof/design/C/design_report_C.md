# Alternative C - post-and-beam braced frame: design report, Rev 2 (bases Rev 4)

System C: E-W IPE 330 primaries on the column rows, N-S IPE 270 rafters, pinned HEA 160 columns, vertical X bracing for all lateral load, roof-plane X bracing as the diaphragm. All numbers come from `calc/` (`python3 run_all.py; python3 write_report.py`); ULS design values unless stated. Companion note: `bases_C.md` (bases and anchors, self-contained).

## 0. Change log Rev 1 -> Rev 2 (basis Rev 2 and independent review, every finding addressed)

| Ref | Change |
|---|---|
| Basis: wind zones | e = 20 m: F/G strip 2.0 m deep, F corners 5.0 m along the eave; zone sets kept as the envelope (theta = 180 values for both N and S wind, F5). Roof uplift total W_S -669 kN incl. gutter (Rev 1 -614). |
| Basis / F4 | Horizontal component of the roof suction added: 39.1 kN char. northward for S wind (resultant at x 81.0, y 26.0), also as an N-S load under E/W wind; S-wind roof-level force 108.7 -> **148.3 kN** (+36 %); no friction term. Bracing, braced columns and bases re-run. |
| Basis: anchorage / F1, F2, F3 | New base for all 27 columns: 4 M20 through the slab into the column head (h_ef 300, 80 x 280 in the core), bond + cracked cone in the slab, **grouted shear key** for all shear (no anchor shear, so the cracked-edge question F2 disappears), plate 25 mm. Wall shear wL/2 is at the column base in every case (F1); base struts deleted, every base carries its full concurrent H + V_wall (F3). |
| Bracing layout | K17-K21 (Rev 1 B8) dropped - K21 is a 200 mm pier between the notch edge and the shaft opening. N-S bracing now on three lines with two bays in series each: B5 K15-K19 + **B10 K19-K25**, B7 K20-K27 + **B8 K10-K16**, B6 K14-K18 + **B9 K18-K23**; E-W B1-B4 unchanged. 10 bays; no braced-bay base has its bay shear towards a free edge < 0.25 m. |
| F6 | Gutter/fascia 0.25 kN/m (G) and -0.50 kN/m (W) on the north eave in the take-down (rafter cantilevers, eave beams, fin plates). West-block north edge kept at y 35.87 (wall line); drainage's gutter line y 35.37 to be coordinated (open item 6). |
| F7 | Column interaction with k_zy from Annex B Table B.2 (0.97-1.00): K25 0.72, K23 0.70, K22 0.63. HEA 160 confirmed. |
| F8 | Purlin uplift re-run with the 2.0 m / 5.0 m zones: corner spans (3.07 m, zone F) 8.3 kNm, stair strip 4.07 m 8.6 kNm; mid-span anti-sag row on all spans; supplier uplift capacity before order (open item 3). |
| F9 | Seismic: ULS-4 rows (1.0 G +/- 1.0 E, both directions, 5 % eccentricity) added to reactions_C.csv; floor amplification through the existing building stated as open item 5. |
| F10 | Roof diaphragm re-modelled with the rods in the drawn cells; east/west edge trusses now use diagonals over two rafter bays (depth 5.65 / 4.10 m) and posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) at the wall-column lines; M24 rods throughout; truss deflection by virtual work: east wall drift 10.4 mm, west 9.3 mm (SLS, incl. bay sway) vs h/150 = 26-28 mm. |
| F11 | TOS(35.87) = 3.30 m, primary top at TOS + 0.05: clear height 3.03 m, rafter/primary bottom-flange clearance 18 mm nominal, 13 mm at the down-slope flange tip. T1 at y 35.44 and T2 at y 24.09 (half a flange inside the opening edges). R82 at x 81.85 over the shaft east wall line: client to confirm (open item 7). |
| F12 | Cap-plate bolts at pitch 200 (plate 200 x 280 x 20); primaries bolted before the rafters are landed. |
| F13 | reactions_C.csv now one row per column and load case (594 rows: ULS-1, ULS-2/3 x 4 wind directions, ULS-4 x 4, SLS) with concurrent N, V_x, V_y, near-edge flags and the base utilisation; WP1 included; envelope in section 9. |
| F14 | Angle bearing with e2 = 30 mm (124 kN per bolt): B8 gusset 0.57. |
| F15 | Base struts and wall-rail anchorage deleted; the lateral system is 10 wall bays + 24 rod panels + 2 posts. |
| **Bases Rev 3 / R1-R7** | Section 6 and `bases_C.md` re-issued after the base re-review: R1 column-cage resistance withdrawn, outward shear at the 14 near-edge bases (Rev 3 count) through a second key 180 mm inboard (c1 = 250, plain-concrete edge breakout 38.2 kN) and a saddle at the K21 pier, WP1 moved 280 mm inboard; R2 key moments V x 85 mm carried into the anchor group (psi_ec,N) and the max anchor; R3 minimum solid zone per base, coring acceptance criterion (>= 750 x 750 x 250, C25, edge beams) and a through-bolt fallback pre-designed at 9 bases; R4 anchors h_ef 200 and pockets 200 deep in the slab only, no drilling into the column heads (permitted by the client, shown unnecessary and risky); R5 f_y 335 for the bar, Key A edge check to 0.6 m; R6/R7 tables with spacing orientation, key moment, max anchor, minimum zone. Worst base at Rev 3: K19 0.91 (superseded by Rev 4). |
| **Bases Rev 4 / S1-S4** | Real slab edges modelled (column flush with the face: outboard anchor row 60 mm from the edge; shaft and stair openings as free edges): concentric cone 50 / 38 kN at edge / corner heads, Key A parallel-to-edge 18-24 kN. Base type chosen per column: **B1** concentric anchors at 15 bases (K3, K4, K5, K6, K7, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26), **B2** through-bolts + inboard key pair (corrected lever statics T = N_t b/(b-c), stiffened 30 mm plate) at 11 bases (K1, K2, K10, K15, K18, K19, K20, K22, K23, K25, K27), **P** pier anchors + saddle at K21. One-sided coring criterion at edge heads. Worst base K7 0.86. |

## 1. Basis and assumptions

- Loads, combinations and resistances exactly per `../load_basis.md` Rev 2; geometry per `../../geometry.json` (27 columns, L-shape less the notch, stair and elevator openings not roofed; roofed area 446.2 m2 from the grid).
- One roof plane at 6 % falling north, TOS(y) = 3.30 + 0.06 (35.87 - y); level primaries with their top at TOS + 0.05; cap-plate top = TOS - 0.28; column length = TOS - 0.34 (25 mm plate + 40 mm grout), 2.97 m (north rows) to 4.16 m (south row).
- Statics: all beams are chains of simple spans (fin plates, cap plates), purlins simple spans between rafters, columns pinned-pinned; girts span horizontally between columns, so each column delivers wL/2 of its wall to the roof and wL/2 to its base. The take-down integrates the roof on a 0.1 m grid (exact tributary, openings excluded) -> rafters -> primaries -> columns. Section tables IPE 200-360 / HEA 140-200 in `calc/sections.py`.
- Wind post WP1 (HEA 160) at the notch corner (77.89, 19.97): wall wind only, slotted top connection, base 2 M16 in the notch edge beam (shear 11.8 kN, no uplift).
- Slab: 250 mm ribbed, solid zone >= 800 x 800 at every column head, C25 cracked, column cage 6 dia14 + dia6/200 - all to be confirmed by cores and a rebar scan before drilling (bases_C.md section 6).

## 2. Loads and combinations (kN, m)

| Action | Value | Used for |
|---|---|---|
| Panel + purlins + services G | 0.12 + 0.05 + 0.20 = 0.37 kN/m2 + member self-weight; gutter 0.25 kN/m on the north eave | gravity |
| G_min (uplift) | 0.17 kN/m2 + member self-weight | ULS-3 |
| Imposed cat. H Q | 0.60 kN/m2, psi_0 = 0 (never with wind) | ULS-1, SLS |
| Wind q_p | 1.30 kN/m2 (Tripoli, binding) | all wind cases |
| Roof net uplift, c_pi +0.2, e = 20 m | H -1.30, G -1.95, F -3.25 kN/m2 (N and S wind, F/G strip 2.0 m, F corners 5.0 m); along the ridge F -2.99, G -2.60, H -1.04, I -0.91; gutter -0.50 kN/m | ULS-3, purlins, fly braces |
| Roof pressure case, c_pi -0.3 | +0.39 kN/m2 (never governs over Q) | ULS-2 |
| Walls, net | D +1.1 (c_pi -0.3); A -1.4 / B -1.0 / C -0.7 / E -0.7 (c_pi +0.2); x 1.3 -> up to 1.82 kN/m2 char. | column bending and base shear |
| Global horizontal wind at roof level | 1.3 q_p on the projected wall area, half to the roof, plus the roof-suction component (39.1 kN, S wind; 30 kN N-S under E/W wind): **N 84.6, S 148.3, E/W 72 (+30 N-S) kN** char. | bracing, diaphragm |
| Wall self-weight | 0.30 kN/m2 x wall height (3.60 m N ... 4.82 m S) x column trib | column axial |
| Seismic (EN 1998-1, a_g 0.10 g, S 1.2, q 1.5, S_d 0.20 g) | seismic weight 383 kN -> F_b = **76.5 kN** (1.0 E) with 5 % eccentricity -> max bay force 37.0 kN (E-W) / 18.7 kN (N-S) vs wind 53 / 57 kN: wind governs; ULS-4 in the reaction table | ULS-4 |

Combinations (EN 1990 6.10): ULS-1 1.35 G + 1.5 Q; ULS-2 1.35 G + 1.5 W (pressure, wall D/E with c_pi -0.3, roof +0.39, bracing compression); ULS-3 1.0 G_min + 1.5 W (uplift, c_pi +0.2, four wind directions, bracing tension); ULS-4 1.0 G +/- 1.0 E; SLS G + Q (L/200, purlins L/150) and G + W (sway H/150).

## 3. Load take-down and bracing analysis results

**Take-down (`takedown.py`).** 11 N-S rafter lines (x = 68.0, 70.0, 72.1, 74.9, 77.8, 81.85, 84.5, 87.2, 89.9, 92.5, 95.5), rafter spans 2.7-9.2 m, purlin spans 2.05-3.1 m (4.07 m over the north strip of the stair well). Example column loads (characteristic, kN): K12 interior G 24.5, Q 25.0, W_N -55.2; K19 (braced, west wall) G 28.1, Q 19.1, W_S -43.7. Sum of column loads: G 443 (incl. gutter), Q 268 (= 0.60 x 446), W_S -669 kN.

**Bracing (`bracing.py`).** The roof force of each windward face (and the roof-suction component at its centroid) is distributed to the bays twice: (a) rigid diaphragm, 3 DOF, bay stiffness k = E A cos^2(alpha)/L_d of one L70x7 diagonal (15.6-24 kN/mm), centre of rigidity and torsion included; (b) flexible-diaphragm tributary to the bracing lines, then to the bays of a line by stiffness. **The envelope of (a) and (b) is used** (sum of bay forces 1.2-1.4 x the applied force). Wind from S, characteristic: rigid B5 23.4 / B10 22.0 / B7 23.1 / B8 26.1 / B6 28.3 / B9 25.4 kN, tributary 15.2 / 14.3 / 33.9 / 38.2 / 24.9 / 22.3 kN; wind from E: rigid B1 20.0 / B2 19.5 / B3 17.5 / B4 15.2, tributary 1.3 / 26.1 / 35.5 / 9.8 kN.

Bay forces at ULS (1.5 W), tension-only diagonal T = H L_d/w, column axial N = H h/w, base shear H at the tension-diagonal base (windward column) concurrent with that column's wall shear:

| Bay | Columns | w m | h m | Wind | H_Ed kN (ULS) | H seismic (1.0 E) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | h/150 mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | K1-K2 | 5.29 | 3.14 | E | 30.0 | 22.3 | 34.8 | 17.8 | 189.3 | 0.18 | 0.28 | 2.8 | 20.9 |
| B2 | K5-K7 | 5.70 | 3.17 | W | 39.1 | 34.0 | 44.7 | 21.7 | 189.3 | 0.24 | 0.36 | 3.1 | 21.1 |
| B3 | K22-K23 | 6.61 | 4.08 | E | 53.2 | 37.0 | 62.5 | 32.8 | 189.3 | 0.33 | 0.51 | 3.9 | 27.2 |
| B4 | K25-K26 | 4.00 | 4.33 | W | 22.9 | 16.2 | 33.8 | 24.8 | 189.3 | 0.18 | 0.27 | 3.0 | 28.9 |
| B5 | K15-K19 | 4.61 | 3.84 | S | 35.1 | 13.7 | 45.7 | 29.2 | 189.3 | 0.24 | 0.37 | 3.2 | 25.6 |
| B6 | K14-K18 | 4.81 | 3.67 | S | 42.4 | 15.7 | 53.4 | 32.4 | 189.3 | 0.28 | 0.43 | 3.4 | 24.5 |
| B7 | K20-K27 | 5.89 | 4.15 | S | 50.9 | 16.6 | 62.2 | 35.9 | 189.3 | 0.33 | 0.50 | 3.9 | 27.7 |
| B8 | K10-K16 | 4.81 | 3.67 | S | 57.3 | 18.7 | 72.1 | 43.7 | 189.3 | 0.38 | 0.58 | 3.9 | 24.5 |
| B9 | K18-K23 | 4.39 | 3.95 | S | 38.1 | 14.1 | 51.2 | 34.2 | 189.3 | 0.27 | 0.41 | 3.4 | 26.3 |
| B10 | K19-K25 | 5.89 | 4.15 | S | 33.1 | 12.9 | 40.5 | 23.3 | 189.3 | 0.21 | 0.33 | 3.2 | 27.7 |

## 4. Member checks (EN 1993-1-1)

Checks per span: bending 6.2.5 (M_pl,Rd IPE 270 = 133 kNm, IPE 330 = 221 kNm), shear 6.2.6 (V_pl,Rd 351 / 489 kN; V_Ed < 0.5 V_pl everywhere), LTB 6.3.2 with M_cr from I_w, I_t and C1 per restraint segment (C1 = 1.88 - 1.40 psi + 0.52 psi^2 for linear segments, 1.0 when the maximum lies inside the segment), curve b, deflection G + Q <= L/200 by numerical double integration.

Restraints: rafters - top flange held by purlins @ 1.5 m (gravity, chi_LT = 1.0); under uplift the free bottom flange is held by **fly braces to the purlins at mid-span for spans <= 6.6 m and at the third points for 7.5 and 9.2 m spans** (segments 2.2-3.25 m). Primaries - both flanges restrained at every rafter fin plate (plate over the full rafter web depth) and at the columns, segments <= 4.1 m; the K19-K20 LTB check is governed by its 2.8 m middle segment (C1 1.07).

| Member (span) | Section | L m | M_Ed kNm | V_Ed kN | 6.2.5 M | 6.2.6 V | 6.3.2 LTB gravity | 6.3.2 LTB uplift | SLS L/200 | Util. | Governs | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P_K19K20/K19-K20 | IPE 330 | 9.79 | 131.3 | 44.8 | 0.59 | 0.09 | 0.73 | 0.72 | 0.74 | **0.74** | defl | OK |
| R92/P_K22K23-K13 | IPE 270 | 9.20 | 57.0 | 35.2 | 0.43 | 0.1 | 0.36 | 0.57 | 0.52 | **0.57** | LTBu | OK |
| R87/P_K21K22-K12 | IPE 270 | 9.20 | 49.5 | 25.0 | 0.37 | 0.07 | 0.35 | 0.49 | 0.5 | **0.5** | defl | OK |
| R85/P_K21K22-P_K11K12 | IPE 270 | 9.20 | 49.3 | 25.3 | 0.37 | 0.07 | 0.35 | 0.49 | 0.49 | **0.49** | defl | OK |
| R90/P_K22K23-P_K12K13 | IPE 270 | 9.20 | 49.6 | 26.5 | 0.37 | 0.08 | 0.34 | 0.49 | 0.49 | **0.49** | LTBu | OK |
| P_K22K23/K22-K23 | IPE 330 | 6.67 | 70.2 | 38.8 | 0.32 | 0.08 | 0.25 | 0.36 | 0.17 | **0.36** | LTBu | OK |
| P_K21K22/K21-K22 | IPE 330 | 7.03 | 56.6 | 28.5 | 0.26 | 0.06 | 0.27 | 0.31 | 0.2 | **0.31** | LTBu | OK |
| R75/P_K19K20-P_K9K10 | IPE 270 | 7.51 | 33.2 | 17.7 | 0.25 | 0.05 | 0.25 | 0.3 | 0.28 | **0.3** | LTBu | OK |
| R70/P_K19K20-P_K8K9 | IPE 270 | 7.56 | 32.6 | 17.2 | 0.24 | 0.05 | 0.19 | 0.29 | 0.22 | **0.29** | LTBu | OK |
| R92/K13-K2 | IPE 270 | 6.50 | 32.5 | 28.4 | 0.24 | 0.08 | 0.18 | 0.28 | 0.18 | **0.28** | LTBu | OK |
| R95/K14-K4 | IPE 270 | 6.40 | 31.1 | 19.6 | 0.23 | 0.06 | 0.11 | 0.27 | 0.11 | **0.27** | LTBu | OK |
| R72/P_K19K20-K9 | IPE 270 | 7.51 | 28.0 | 14.9 | 0.21 | 0.04 | 0.21 | 0.25 | 0.25 | **0.25** | LTBu | OK |
| R90/P_K12K13-P_K1K2 | IPE 270 | 6.50 | 26.5 | 20.5 | 0.2 | 0.06 | 0.17 | 0.23 | 0.17 | **0.23** | LTBu | OK |
| R87/K12-K1 | IPE 270 | 6.50 | 25.9 | 19.0 | 0.19 | 0.05 | 0.17 | 0.22 | 0.17 | **0.22** | LTBu | OK |
| P_K9K10/K9-K10 | IPE 330 | 5.69 | 44.9 | 17.0 | 0.2 | 0.03 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| P_K11K12/K11-K12 | IPE 330 | 5.34 | 46.1 | 18.3 | 0.21 | 0.04 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| P_K12K13/K12-K13 | IPE 330 | 5.29 | 45.4 | 18.5 | 0.21 | 0.04 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| R75/K24-P_K19K20 | IPE 270 | 5.79 | 25.5 | 25.2 | 0.19 | 0.07 | 0.14 | 0.21 | 0.13 | **0.21** | LTBu | OK |
| R85/P_K11K12-P_K3K1 | IPE 270 | 6.40 | 24.7 | 18.1 | 0.19 | 0.05 | 0.17 | 0.21 | 0.17 | **0.21** | LTBu | OK |
| R72/K26-P_K19K20 | IPE 270 | 5.89 | 22.7 | 22.0 | 0.17 | 0.06 | 0.13 | 0.19 | 0.12 | **0.19** | LTBu | OK |
| R70/P_K25K26-P_K19K20 | IPE 270 | 5.89 | 21.8 | 18.4 | 0.16 | 0.05 | 0.11 | 0.18 | 0.1 | **0.18** | LTBu | OK |
| R70/P_K8K9-P_K6K5 | IPE 270 | 5.90 | 21.8 | 16.9 | 0.16 | 0.05 | 0.11 | 0.18 | 0.1 | **0.18** | LTBu | OK |
| R75/P_K9K10-P_K5K7 | IPE 270 | 5.93 | 22.0 | 17.5 | 0.17 | 0.05 | 0.15 | 0.18 | 0.14 | **0.18** | LTBu | OK |
| R78/K27-K20 | IPE 270 | 5.89 | 21.0 | 15.6 | 0.16 | 0.04 | 0.11 | 0.18 | 0.1 | **0.18** | LTBu | OK |
| R72/K9-K5 | IPE 270 | 6.00 | 20.7 | 18.9 | 0.16 | 0.05 | 0.13 | 0.17 | 0.13 | **0.17** | LTBu | OK |
| R68/K25-K19 | IPE 270 | 5.89 | 19.2 | 13.1 | 0.14 | 0.04 | 0.07 | 0.16 | 0.06 | **0.16** | LTBu | OK |
| P_K5K7/K5-K7 | IPE 330 | 5.69 | 32.0 | 12.1 | 0.14 | 0.02 | 0.13 | 0.16 | 0.07 | **0.16** | LTBu | OK |
| R68/K8-K6 | IPE 270 | 5.80 | 18.5 | 12.9 | 0.14 | 0.04 | 0.07 | 0.15 | 0.06 | **0.15** | LTBu | OK |
| P_K1K2/K1-K2 | IPE 330 | 5.29 | 28.1 | 11.6 | 0.13 | 0.02 | 0.11 | 0.14 | 0.06 | **0.14** | LTBu | OK |
| P_K8K9/K8-K9 | IPE 330 | 4.10 | 31.3 | 15.7 | 0.14 | 0.03 | 0.11 | 0.14 | 0.05 | **0.14** | LTBu | OK |
| R78/K16-K10 | IPE 270 | 4.81 | 16.9 | 14.0 | 0.13 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| R82/K17-K11 | IPE 270 | 4.81 | 16.3 | 13.5 | 0.12 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| P_K3K1/K3-K1 | IPE 330 | 5.34 | 26.1 | 10.5 | 0.12 | 0.02 | 0.11 | 0.13 | 0.06 | **0.13** | LTBu | OK |
| R95/K23-K18 | IPE 270 | 4.39 | 14.9 | 13.6 | 0.11 | 0.04 | 0.05 | 0.12 | 0.04 | **0.12** | LTBu | OK |
| R95/K18-K14 | IPE 270 | 4.81 | 15.5 | 13.2 | 0.12 | 0.04 | 0.06 | 0.12 | 0.05 | **0.12** | LTBu | OK |
| R82/K11-K3 | IPE 270 | 6.40 | 14.7 | 11.4 | 0.11 | 0.03 | 0.11 | 0.09 | 0.11 | **0.11** | defl | OK |
| P_K6K5/K6-K5 | IPE 330 | 4.10 | 23.5 | 12.0 | 0.11 | 0.02 | 0.07 | 0.11 | 0.03 | **0.11** | LTBu | OK |
| ST1 | IPE 270 | 5.65 | 0 |  |  |  | 0.11 |  |  | **0.11** | 6.3.1 | OK |
| R78/K10-K7 | IPE 270 | 5.90 | 13.3 | 9.2 | 0.1 | 0.03 | 0.1 | 0.08 | 0.09 | **0.1** | LTBg | OK |
| 15 further spans (eave beams, trimmers, short edge-beam spans, ST2) | IPE 330 / IPE 270 | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |

Governing members: primary **K19-K20 (9.79 m)** at 0.74 (deflection 36 mm = L/271; M_Ed 131 kNm = 0.59 M_pl; LTB 0.73); 9.2 m rafters at 0.49-0.52 (deflection 22-24 mm = L/390-410, M 0.35, LTB uplift 0.51). Max beam utilisation 0.74. Alternatives run with the same scripts: IPE 240 rafters pass strength (M 0.58, LTB uplift 0.71) but give L/265 on the 9.2 m spans with no reserve for a future ceiling, so IPE 270 is kept; IPE 300 primaries put K19-K20 at L/194 (1.03): IPE 330 confirmed.

Rafters as roof-truss posts: N_Ed = 37.7 kN with N_b,Rd = 624 kN (L_y 9.2, L_z 3.07 m) -> 0.06; new posts ST1 (IPE 270, 5.65 m, N 25.0 kN vs 231) and ST2 (4.10 m, 20.1 vs 404); eave primaries as struts <= 57 kN vs N_b,Rd >= 800 kN. Purlins are not used as struts.

**Columns** (6.3.1 pinned-pinned, L_cr = L both axes, HEA 160 curve b/c; 6.3.3 Annex B method 2, Table B.2 for the LTB-susceptible member, C_m = C_mLT = 0.95 for the wall-wind UDL, web normal to the wall it supports, corners biaxial). N_b,Rd = 461 kN (L 4.16 m) to 667 kN (L 2.97 m).

| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | k_zy (B.2) | 6.3.1 N/N_b,Rd | 6.3.3 | Util. | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| K25 | HEA 160 | 4.16 | 47.8 (ULS2E) | 42.6 (ULS3W) | 15.1 / 12.4 | 0.99 | 0.1 | 0.72 | **0.72** | OK |
| K23 | HEA 160 | 3.91 | 63.7 (ULS2W) | 62.1 (ULS3S) | 14.4 / 12.0 | 0.99 | 0.13 | 0.7 | **0.7** | OK |
| K22 | HEA 160 | 3.91 | 90.6 (ULS2E) | 56.3 (ULS3S) | 25.5 / 0.0 | 0.97 | 0.18 | 0.63 | **0.63** | OK |
| K21 | HEA 160 | 3.91 | 39.8 (ULS1) | 19.8 (ULS3S) | 28.6 / 0.0 | 0.99 | 0.08 | 0.58 | **0.58** | OK |
| K27 | HEA 160 | 4.16 | 38.8 (ULS2N) | 44.1 (ULS3S) | 10.9 / 9.2 | 0.99 | 0.08 | 0.52 | **0.52** | OK |
| K19 | HEA 160 | 3.81 | 79.9 (ULS2S) | 73.1 (ULS3S) | 18.5 / 0.0 | 0.98 | 0.15 | 0.48 | **0.48** | OK |
| K6 | HEA 160 | 3.00 | 25.2 (ULS1) | 18.0 (ULS3W) | 8.7 / 6.6 | 1.00 | 0.04 | 0.38 | **0.38** | OK |
| K26 | HEA 160 | 4.16 | 50.1 (ULS2W) | 30.5 (ULS3E) | 14.6 / 0.0 | 0.98 | 0.11 | 0.37 | **0.37** | OK |
| K14 | HEA 160 | 3.36 | 56.7 (ULS2S) | 26.4 (ULS3N) | 15.4 / 0.0 | 0.99 | 0.1 | 0.36 | **0.36** | OK |
| K18 | HEA 160 | 3.64 | 54.2 (ULS2S) | 39.5 (ULS3S) | 14.9 / 0.0 | 0.99 | 0.1 | 0.36 | **0.36** | OK |
| other 17 columns | HEA 160 | 2.97-4.16 | <= 58 | <= 58 | <= 15 | 0.98-1.00 | <= 0.12 | <= 0.38 | <= 0.38 | OK |

Max column utilisation 0.72 (K25, SW corner). Wind post WP1 HEA 160, L 4.21 m: M_y 9.3, M_z 9.8 kNm -> 0.47. HEA 140 reaches 1.06 at K25 with Table B.2: **HEA 160 confirmed**.

**Purlins Z200x2.0 @ 1.5 m** (basis: M_Rd 12.5 kNm single span, 16 sleeved; I = 3.9e6 mm4): worst gravity M_Ed = 4.3 kNm; worst uplift M_Ed = **8.6 kNm** on the 4.07 m stair strip (x 77.8-81.8, y 35.6, zone G) and 8.3 kNm on the 3.07 m corner spans (zone F, w = -7.1 kN/m), i.e. 0.66-0.69 of the single-span gravity value. Because the free-flange uplift capacity of a Z200x2.0 is typically 55-70 % of the gravity value, **a mid-span anti-sag row is specified on every span and the supplier's uplift capacity (>= 9 kNm single span with one anti-sag row, or sleeved) is required before order** (open item 3). Deflection G + Q on 4.07 m: 6.3 mm < L/150 = 27.1 mm. Girts (wall net 2.15 kN/m2, zone A 2.73 within 2.4 m of a corner): 1.5 m rows single-span for bays <= 5.3 m (<= 11.3 kNm); 1.2 m rows sleeved on K5-K7, K25-K19, K8-K6 (<= 14.2 kNm); 1.0 m rows sleeved on K21-K22, K22-K23, K14-K4 (<= 14.9 kNm, 0.93).

## 5. Connections (EN 1993-1-8)

- **Rafter to primary fin plate**, one type: 100 x 150 x 10 S275, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web, 2 x 6 mm fillets. Max rafter end reaction 35.2 kN (envelope ULS-1 / reversed ULS-3 incl. the gutter): bolt shear incl. eccentricity 0.33, bearing on the 6.6 mm rafter web **0.45** (governs), plate bearing 0.29, plate shear 0.17, plate bending 0.17, weld 0.19, web block tearing 0.31. 9.2 m rafters: 3 bolts, plate 220 (0.14 at 20.4 kN). No copes. T1/T2, ST1/ST2 and the notch eave beam use the same detail.
- **Primary to column cap plate** 200 x 280 x 20, a = 6 all round, 4 M20 through the primary bottom flange (gauge 90, **pitch 200** so the nuts clear the passing rafter flange; primaries bolted before the rafters). Tension = roof uplift 66.7 kN (K12, ULS-3N; the bracing vertical component enters below the cap through the gusset): bolt tension 0.12, shear + tension interaction with the chord/strut force 60.9 kN 0.25, IPE 330 flange T-stub 0.16, cap plate 0.05, weld 0.07. Chord continuity across a column (<= 61 kN): 10 mm tie plate between the primary bottom flanges on the lines y 29.3 and y 20.1.
- **Bracing gussets**: 10 mm plates welded to the column web and base plate; each L70x7 with 2 M20 (e1 40, p1 110, e2 30): angle net section 189 kN, bolt shear 188 kN, gusset bearing 2 x 124 kN; max T_Ed 72.1 kN (B8) -> 0.38 angle, 0.57 bolts.
- **Roof bracing** M24 rods 8.8 (F_t,Rd 203 kN) with turnbuckles to 8 mm gussets on the rafter and primary webs at the bottom flange level; on the east and west edge trusses the rods span two rafter bays and pass the intermediate rafter (R92 / R70) through a slotted web clip; sag ties to the purlins at the crossing and at 3 m centres.
- Trimmers T1 (y 35.44) and T2 (y 24.09) IPE 270 between the rafters x 77.8 / 81.85 carry only the 150 mm upstand (0.3 kN/m, M_Ed 1.8 kNm); upstand framing 100 x 50 x 3 cold-formed C on the trimmers and along the rafters beside the openings, cricket on the south side of the stair well.

## 6. Bases and anchors, Rev 4 (EN 1993-1-8 6.2.5, EN 1992-4 with the Rev 2 basis) - full note in `bases_C.md`

The slab edge is 100 mm from the centre of every perimeter column and the stair / shaft openings are free edges, so the base type is chosen per column from the real-edge checks:

- **B1, concentric resin anchors (15 bases: K3, K4, K5, K6, K7, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26)**: plate 300 x 400 x 25, 4 M20 at 80 x 280 (280 along the concrete column's long axis), h_ef 200 in the slab, clearance holes; Key A SHS 90x90x8 under the column (along-axis and inward shear, 25 MPa confined bearing, V_Rd 83.8 kN; parallel-to-edge breakout 2 V_Rk,c = 18.5 kN at c1 55 where an edge is 100 mm from the column, checked at K3, K4, K6, K7, K8, K11, K14); Key B 60 mm bar 180 mm inboard (c1 250, 38.2 kN) for outward shear at K3, K4, K6, K8, K14. Cone with the concrete actually there: interior 98.5 kN, one edge 50.4 kN, corner 37.8 kN, times psi_ec,N from the key moments. Worst B1: K7 0.86 (cone 50 x 0.61, N_t 26.4; Key A parallel 0.85), K16 0.76, K12 0.68.
- **B2, through-bolts and inboard key pair (11 bases: K1, K2, K10, K15, K18, K19, K20, K22, K23, K25, K27)**: plate 700 x 550 x 30 with two 120 x 10 stiffeners; 2 M24 8.8 through-bolts 250 mm inboard of the column, 280 apart, all >= 300 mm from every slab edge (rows shifted along the wall at K23, K25, K27), on a 400 x 200 x 20 under-slab plate; uplift by lever action about the inboard plate tip, T = N_t b/(b - c) = 2.39-2.93 N_t (K19: 175 kN, 87 kN per M24 = 0.46; tip bearing C = 1.39-1.93 N_t on a 350 x 60 strip <= 0.57; stiffened plate M = N_t c + M_key <= 27 kNm vs 48); shear by two SHS 90x90x8 keys 200 mm inboard, +/- 300 along the wall, each taking half the shear plus the torque of the eccentric shear (arm 0.6 m), outward components checked as edge breakout at c1 >= 255 (41.5 kN): K25 0.83, K23 0.80, K27 0.76, K22 0.74. No cone, no anchor shear.
- **P, K21** (200 mm pier): 4 M16 h_ef 400 into the pier lapped with its bars (splitting restrained by the dia6 links, 49 kN -> 0.53), saddle plates for the N-S shear (0.36). The only base where the client's permission to drill a column head is used.
- WP1: post 280 mm inboard, one centred key, 0.31. Compression bearing <= 0.10 everywhere.

Worst base **K7: 0.86 (anchor group cone, real edges (N_Rd,c 50, psi_ec 0.61), ULS3E)**; all 27 bases and WP1 <= 1.0 with the real edges. Coring acceptance is one-sided at edge heads (outboard to the face, inboard >= 300-550 mm, +/- 300-400 along; interior B1 heads >= 400-700 centred); a B1 head that fails is built as B2; B2 needs soffit access at 11 locations.

## 7. Deflections and sway

- Roof members SLS G + Q: worst primary K19-K20 36 mm = L/271 (limit 49 mm); 9.2 m rafters 22-24 mm = L/390; 7.5 m rafters L/700-820; purlins L/640.
- Braced-bay sway under SLS wind (diagonal elongation + 2 mm bolt-slip allowance): 2.8-3.9 mm vs h/150 = 20-28 mm. Column bending under wall wind (K22, 9.8 kN/m on 3.91 m) 8.5 mm = h/460.
- **Roof diaphragm drift** at the mid-length of the east / west walls (truss deflection by virtual work over the M24 rods, SLS, plus bay sway): **10.4 / 9.3 mm** vs h/150 = 26-28 mm (0.40).

## 8. Bracing

Vertical bays (X, one L70x7 per diagonal, tension-only), **final list for the client - these bays must stay door-free**: E-W **B1 K1-K2** (north wall, 5.3 m), **B2 K5-K7** (north wall, 5.7 m), **B3 K22-K23** (notch south wall, 6.6 m), **B4 K25-K26** (south wall, 4.0 m); N-S **B5 K15-K19** and **B10 K19-K25** (west wall, 4.6 + 5.9 m), **B6 K14-K18** and **B9 K18-K23** (east wall, 4.8 + 4.4 m), **B7 K20-K27** (notch west wall / shaft west line, 5.9 m) and **B8 K10-K16** (core west line between the stair well and the shaft, inside the hall, 4.8 m). Max diagonal utilisation 0.38 (B8), gusset bolts 0.57. Reason for the layout: at every braced-bay base the bay shear enters the concrete along the column's long axis or towards the slab interior, never towards a free edge < 0.25 m; the middle columns K19, K18, K20 of the three N-S lines carry no net bracing uplift. Alternates if a bay is not door-free: B1 -> K3-K1, B3 -> K21-K22 (K21 base then needs a supplier-verified edge detail), B5/B10 -> single bay K15-K25 not possible (7.5 m), B8 -> none (K17-K21 and K11-K17 are excluded by the K21 / K11 edge condition).

Roof-plane bracing: M24 rods in 24 rafter cells (full rafter depth, primaries as chords, rafters as posts), east/west edge trusses with rods over two bays and posts ST1/ST2 at the wall-column lines; the north-band shear passes the stair well through the jog panel x 77.8-81.85 / y 24.5-29.3 (y 29.3 primary as continuous chord, tie plates at K10, K11).

| Roof truss | Wind | Span m | Depth m | Panels | Shear V kN | Diagonal T kN (M24, 203) | Chord kN | Post kN | Util. rod | Truss defl. ULS mm |
|---|---|---|---|---|---|---|---|---|---|---|
| RT-N-W (N band west, chords y 29.3 / 35.2) | N-S | 9.8 | 5.9 | 4 | 21.7 | 23.0 | 11.2 | 21.7 | 0.11 | 2.8 |
| RT-N-E (N band east, chords y 29.3 / 35.7) | N-S | 13.7 | 6.4 | 5 | 31.0 | 33.6 | 20.6 | 31.0 | 0.17 | 5.1 |
| RT-S-E (S band east, chords y 20.1 / 29.3) | N-S | 13.7 | 9.2 | 5 | 37.7 | 39.3 | 17.4 | 37.7 | 0.19 | 7.9 |
| RT-S-W (S band west, chords y 15.9 / 21.8) | N-S | 9.8 | 5.9 | 4 | 27.7 | 29.3 | 14.3 | 27.7 | 0.14 | 3.6 |
| RT-W (west edge, chords R68 / R72 (rods over two bays)) | E-W | 19.4 | 4.1 | 3 | 27.2 | 47.6 | 60.9 | 27.2 | 0.23 | 8.1 |
| RT-E (east edge, chords R90 / R95 (rods over two bays)) | E-W | 15.6 | 5.7 | 2 | 31.3 | 47.5 | 23.2 | 31.3 | 0.23 | 9.7 |
| RT-JOG (jog panel x 77.8-81.9 / y 24.5-29.3) | N-S | 4.1 | 4.8 | 1 | 0.0 | 0.0 | 2.0 | 0.0 | 0.00 | 0.0 |

## 9. Reactions at the column bases (kN, ULS envelope with concurrent values; reactions_C.csv gives every column and case: ULS-1, ULS-2/3 for N, S, E, W wind, ULS-4 +/-x, +/-y, SLS, with N, V_x, V_y, near-edge flags and base utilisation)

| Col | Type | Bays | Near edges | Keys | N_c max kN (case) | N_t max kN (case) | V max kN (case) | N_c SLS | N_t SLS | Base governs | Util. | Min. zone |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | B2 | B1 | +y | A-pair | 54.7 (ULS2E) | 34.0 (ULS3N) | 33.5 (ULS2W) | 30.4 | 13.7 | B2 key pair outward | **0.42** | B2: 550 from face |
| K2 | B2 | B1 | +y | A-pair | 46.9 (ULS2W) | 36.1 (ULS3N) | 34.4 (ULS2E) | 24.0 | 17.0 | B2 key pair outward | **0.45** | B2: 550 from face |
| K3 | B1 | - | +y | A,B+y | 31.1 (ULS1) | 15.1 (ULS3N) | 15.0 (ULS2N) | 22.4 | 3.3 | Key B outward +y | **0.37** | 400 |
| K4 | B1 | - | +x,+y | A,B+x,+y | 19.8 (ULS1) | 14.6 (ULS3E) | 14.8 (ULS2N) | 14.3 | 5.3 | anchor group cone, real edges | **0.53** | 400 |
| K5 | B1 | B2 | - | A | 57.6 (ULS2E) | 42.1 (ULS3W) | 41.6 (ULS2W) | 29.5 | 19.4 | anchor group cone, real edges | **0.59** | 600 |
| K6 | B1 | - | -x | A,B-x | 25.2 (ULS1) | 18.0 (ULS3W) | 16.3 (ULS2N) | 18.1 | 6.5 | anchor group cone, real edges | **0.48** | 450 |
| K7 | B1 | B2 | +x | A | 52.0 (ULS2W) | 26.4 (ULS3E) | 41.6 (ULS2E) | 24.4 | 10.3 | anchor group cone, real edges | **0.86** | 550 |
| K8 | B1 | - | -x | A,B-x | 30.1 (ULS1) | 26.4 (ULS3W) | 15.8 (ULS2W) | 21.5 | 11.2 | anchor group cone, real edges | **0.61** | 500 |
| K9 | B1 | - | - | A | 57.2 (ULS1) | 52.2 (ULS3N) | 0.0 (ULS1) | 40.1 | 23.6 | anchor group cone, real edges | **0.53** | 600 |
| K10 | B2 | B8 | +y | A-pair | 78.8 (ULS2S) | 58.1 (ULS3N) | 33.2 (ULS2N) | 29.7 | 30.3 | B2 tip bearing | **0.38** | B2: 550 from face |
| K11 | B1 | - | +y | A | 43.6 (ULS1) | 33.9 (ULS3N) | 0.0 (ULS1) | 30.8 | 13.9 | anchor group cone, real edges | **0.67** | 500 |
| K12 | B1 | - | - | A | 70.5 (ULS1) | 66.7 (ULS3N) | 0.0 (ULS1) | 49.5 | 30.7 | anchor group cone, real edges | **0.68** | 650 |
| K13 | B1 | - | - | A | 55.7 (ULS1) | 54.0 (ULS3N) | 0.0 (ULS1) | 39.0 | 25.1 | anchor group cone, real edges | **0.55** | 600 |
| K14 | B1 | B6 | +x | A,B+x | 56.7 (ULS2S) | 26.4 (ULS3N) | 30.8 (ULS2N) | 19.6 | 11.7 | anchor group cone, real edges | **0.66** | 550 |
| K15 | B2 | B5 | -x | A-pair | 43.6 (ULS2S) | 16.7 (ULS3N) | 23.5 (ULS2N) | 11.3 | 7.7 | B2 key pair outward | **0.31** | B2: 550 from face |
| K16 | B1 | B8 | - | A | 43.8 (ULS2N) | 58.4 (ULS3S) | 57.3 (ULS2S) | 15.5 | 34.5 | anchor group cone, real edges | **0.76** | 700 |
| K17 | B1 | - | - | A | 23.2 (ULS1) | 15.7 (ULS3S) | 0.0 (ULS1) | 16.5 | 5.7 | anchor group cone, real edges | **0.20** | 400 |
| K18 | B2 | B6,B9 | +x | A-pair | 54.2 (ULS2S) | 39.5 (ULS3S) | 45.5 (ULS2S) | 16.1 | 21.5 | B2 key pair outward | **0.54** | B2: 550 from face |
| K19 | B2 | B5,B10 | -x | A-pair | 79.9 (ULS2S) | 73.1 (ULS3S) | 40.2 (ULS2S) | 47.2 | 35.1 | B2 key pair outward | **0.52** | B2: 550 from face |
| K20 | B2 | B7 | +x | A-pair | 82.3 (ULS2S) | 64.0 (ULS3N) | 29.5 (ULS2N) | 39.4 | 31.5 | B2 tip bearing | **0.42** | B2: 550 from face |
| K21 | P | - | +y,-y | saddle | 39.8 (ULS1) | 19.8 (ULS3S) | 29.3 (ULS2W) | 28.6 | 4.6 | P pier anchors: splitting of the 200 pier restrained by the dia6/200 links | **0.53** | B2: 550 from face |
| K22 | B2 | B3 | -y | A-pair | 90.6 (ULS2E) | 56.3 (ULS3S) | 59.0 (ULS2W) | 48.0 | 23.6 | B2 key pair outward | **0.74** | B2: 550 from face |
| K23 | B2 | B3,B9 | +x,-y | A-pair | 63.7 (ULS2W) | 62.1 (ULS3S) | 63.7 (ULS2E) | 25.2 | 33.8 | B2 key pair outward | **0.80** | B2: 550 from face |
| K24 | B1 | - | - | A | 23.9 (ULS1) | 23.6 (ULS3S) | 16.4 (ULS2E) | 17.1 | 10.7 | Key A towards edge -y | **0.31** | 450 |
| K25 | B2 | B4,B10 | -x | A-pair | 47.8 (ULS2E) | 42.6 (ULS3W) | 47.0 (ULS2S) | 18.3 | 22.8 | B2 key pair outward | **0.83** | B2: 550 from face |
| K26 | B1 | B4 | - | A | 50.1 (ULS2W) | 30.5 (ULS3E) | 26.7 (ULS2E) | 20.6 | 14.2 | anchor group cone, real edges | **0.54** | 550 |
| K27 | B2 | B7 | +x | A-pair | 38.8 (ULS2N) | 44.1 (ULS3S) | 59.3 (ULS2S) | 14.2 | 25.0 | B2 key pair outward | **0.76** | B2: 550 from face |
| WP1 (offset 280 inboard) | post | - | +x,-y | B centred | 1.7 (self weight) | 0 | 11.8 (ULS2 E / S) | - | - | key edge breakout c1 250 | 0.31 | - |

## 10. Weight and section list

| Item | Section | Length m | Weight t |
|---|---|---|---|
| Rafters / edge beams / trimmers / posts ST1-ST2 | IPE 270 | 214.8 | 7.75 |
| Primaries / eave beams | IPE 330 | 92.5 | 4.54 |
| Columns (27) + wind post WP1 | HEA 160 | 99.0 | 3.01 |
| Plates, fin/cap/base plates, shear keys, bolts (10 %) | S275 / S355 keys | - | 1.53 |
| **Hot-rolled total** | | | **16.8** |
| Wall bracing, 10 bays x 2 diagonals | L 70x7 | 129.5 | 0.96 |
| Roof bracing, 24 panels x 2 diagonals | M24 rods 8.8 | 365.6 | 1.30 |
| Purlins 372 m + girts 359 m | Z 200x2.0 S350GD | 731 | 4.31 |
| **Total** | | | **23.4** (48 kg/m2 of footprint 486 m2, 52 kg/m2 of roofed 446 m2) |

Sections: **IPE 330** (all E-W primaries and eave beams on the column rows, 92.5 m), **IPE 270** (rafters, edge beams, trimmers, truss posts ST1/ST2, 215 m), **HEA 160** (27 columns, WP1), plus L70x7 wall bracing, M24 rod roof bracing, Z200x2.0 purlins/girts. Three hot-rolled sections kept. Weight 23.4 t against Rev 1 23.6 t (struts -1.3 t, two more bays and M24 rods +0.8 t, posts +0.4 t) and the scheme's 20.5 t.

## 11. Open items / risks

1. **Slab verification** (bases_C.md sections 5-6): cores at 3 heads then every head against its own one-sided criterion; rebar scan of the slab top bars for the pockets and through-bolt holes; pull-out tests on 3 anchors to 45 kN; supplier ETA group verification; soffit access for the 11 B2 under-slab plates (ceiling openings) and the K21 pier faces. A B1 head that fails its criterion becomes B2; if a B2 soffit is inaccessible, the basis Rev 2 column-head anchorage is the agreed alternative at that head.
2. Wind: q_p 1.30 to be confirmed with the Libyan National Meteorological Centre; a 10 % increase raises the worst B1 base (K7) to about 0.95 and the B2 key pair at K25 to 0.91.
3. Purlin uplift capacity (>= 9 kNm single span with one anti-sag row) and the sleeved girt capacities to be confirmed with the supplier before order.
4. BoardX product data (0.30 kN/m2, girt rows per section 4) and its drift limit (h/150 assumed; diaphragm drift 10 mm, bay sway 4 mm).
5. Seismic: F_b 77 kN on the roof mass alone is below the wind bay forces; floor amplification through the existing building (S_a up to ~0.6 g / q) could bring the E-W seismic bay forces to the wind level - two-mass check once the building period is known; the bracing has 2.5 x reserve.
6. Drainage coordination: the drainage layout puts the west gutter at y 35.37; the structure roofs and walls the west block to y 35.87. Confirm the north edge; if 35.37, the north eave beam K6-K5-K7 and wall move 0.5 m south (no member change).
7. Client confirmations: door-free bays B1-B10 (section 8), B8 visible inside the hall along the core line, rafter R82 over the shaft east wall line (x 81.85 vs shaft face 81.99).
8. Temperature: slotted holes in the fin plates on the y 29.3 line (27.8 m).

Files: `design_report_C.md` (this), `bases_C.md` (Rev 4), `members_C.csv` (99 rows), `reactions_C.csv` (595 rows, with base type, keys, psi_ec, max anchor/bolt and minimum zone per case), `framing_C.png`, `calc/` (sections.py, model.py, loads.py, statics.py, takedown.py, bracing.py, members.py, connections.py, bases_note.py, run_all.py, write_report.py, report_text.md, summary_C.json).

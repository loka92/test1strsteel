# Alternative C - post-and-beam braced frame: design report, Rev 3 (bases Rev 4b)

System C: E-W IPE 330 primaries on the column rows, N-S IPE 270 rafters, pinned HEA 160 columns, vertical X bracing for all lateral load, roof-plane X bracing as the diaphragm. All numbers come from `calc/` (`python3 run_all.py; python3 write_report.py`); ULS design values unless stated. Companion note: `bases_C.md` (bases and anchors, self-contained).

## 0. Change log Rev 1 -> Rev 2 (basis Rev 2 and independent review, every finding addressed)

| Ref | Change |
|---|---|
| Basis: wind zones | e = 20 m: F/G strip 2.0 m deep, F corners 5.0 m along the eave; zone sets kept as the envelope (theta = 180 values for both N and S wind, F5). Roof uplift total W_S -669 kN incl. gutter (Rev 1 -614). |
| Basis / F4 | Horizontal component of the roof suction added: 38.6 kN char. northward for S wind (resultant at x 81.1, y 25.8), also as an N-S load under E/W wind; S-wind roof-level force 108.7 -> **148.5 kN** (+36 %); no friction term. Bracing, braced columns and bases re-run. |
| Basis: anchorage / F1, F2, F3 | New base for all 27 columns: 4 M20 through the slab into the column head (h_ef 300, 80 x 280 in the core), bond + cracked cone in the slab, **grouted shear key** for all shear (no anchor shear, so the cracked-edge question F2 disappears), plate 25 mm. Wall shear wL/2 is at the column base in every case (F1); base struts deleted, every base carries its full concurrent H + V_wall (F3). |
| Bracing layout | K17-K21 (Rev 1 B8) dropped - K21 is a 200 mm pier between the notch edge and the shaft opening. N-S bracing now on three lines with two bays in series each: B5 K15-K19 + **B10 K19-K25**, B7 K20-K27 + **B8 K10-K16**, B6 K14-K18 + **B9 K18-K23**; E-W B1-B4 unchanged. 10 bays; no braced-bay base has its bay shear towards a free edge < 0.25 m. |
| F6 | Gutter/fascia 0.25 kN/m (G) and -0.50 kN/m (W) on the north eave in the take-down (rafter cantilevers, eave beams, fin plates). West-block north edge kept at y 35.87 (wall line); drainage's gutter line y 35.37 to be coordinated (open item 6). |
| F7 | Column interaction with k_zy from Annex B Table B.2 (0.97-1.00): K25 0.72, K23 0.71, K22 0.64. HEA 160 confirmed. |
| F8 | Purlin uplift re-run with the 2.0 m / 5.0 m zones: corner spans (3.07 m, zone F) 8.3 kNm, stair strip 4.07 m 8.6 kNm; mid-span anti-sag row on all spans; supplier uplift capacity before order (open item 3). |
| F9 | Seismic: ULS-4 rows (1.0 G +/- 1.0 E, both directions, 5 % eccentricity) added to reactions_C.csv; floor amplification through the existing building stated as open item 5. |
| F10 | Roof diaphragm re-modelled with the rods in the drawn cells; east/west edge trusses now use diagonals over two rafter bays (depth 5.65 / 4.10 m) and posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) at the wall-column lines; M24 rods throughout; truss deflection by virtual work: east wall drift 10.5 mm, west 9.5 mm (SLS, incl. bay sway) vs h/150 = 26-28 mm. |
| F11 | (superseded by Rev 3: TOS(35.87) = 3.33, 3.02 m clear under the cap nuts) TOS(35.87) = 3.30 m, primary top at TOS + 0.05: clear height 3.03 m, rafter/primary bottom-flange clearance 18 mm nominal, 13 mm at the down-slope flange tip. T1 at y 35.44 and T2 at y 24.09 (half a flange inside the opening edges). R82 at x 81.85 over the shaft east wall line: client to confirm (open item 7). |
| F12 | Cap-plate bolts at pitch 200 (plate 200 x 280 x 20); primaries bolted before the rafters are landed. |
| F13 | reactions_C.csv now one row per column and load case (594 rows: ULS-1, ULS-2/3 x 4 wind directions, ULS-4 x 4, SLS) with concurrent N, V_x, V_y, near-edge flags and the base utilisation; WP1 included; envelope in section 9. |
| F14 | Angle bearing with e2 = 30 mm (124 kN per bolt): B8 gusset 0.57. |
| F15 | Base struts and wall-rail anchorage deleted; the lateral system is 10 wall bays + 24 rod panels + 2 posts. |
| **Bases Rev 3 / R1-R7** | Section 6 and `bases_C.md` re-issued after the base re-review: R1 column-cage resistance withdrawn, outward shear at the 14 near-edge bases (Rev 3 count) through a second key 180 mm inboard (c1 = 250, plain-concrete edge breakout 38.2 kN) and a saddle at the K21 pier, WP1 moved 280 mm inboard; R2 key moments V x 85 mm carried into the anchor group (psi_ec,N) and the max anchor; R3 minimum solid zone per base, coring acceptance criterion (>= 750 x 750 x 250, C25, edge beams) and a through-bolt fallback pre-designed at 9 bases; R4 anchors h_ef 200 and pockets 200 deep in the slab only, no drilling into the column heads (permitted by the client, shown unnecessary and risky); R5 f_y 335 for the bar, Key A edge check to 0.6 m; R6/R7 tables with spacing orientation, key moment, max anchor, minimum zone. Worst base at Rev 3: K19 0.91 (superseded by Rev 4). |
| **Bases Rev 4 / S1-S4** | Real slab edges modelled (column flush with the face: outboard anchor row 60 mm from the edge; shaft and stair openings as free edges): concentric cone 50 / 38 kN at edge / corner heads, Key A parallel-to-edge 18-24 kN. Base type chosen per column: **B1** concentric anchors at 13 bases (K3, K4, K6, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26), **B2** through-bolts + inboard key pair (corrected lever statics T = N_t b/(b-c), stiffened 30 mm plate) at 13 bases (K1, K2, K5, K7, K10, K15, K18, K19, K20, K22, K23, K25, K27), **P** pier anchors + saddle at K21. One-sided coring criterion at edge heads. |
| **Bases Rev 4a / T1-T6** | Per-base B2 plate lengths and coring zones for the shifted layouts (K23 1000 x 550 plate, zone -1100..+250 along; K25 550 x 900 and K27 600 x 900, zone to +1000; standard 800 x 550, zone +/- 700); coring criterion made identical to the cone extents used (B1 edge heads: inboard >= 340, +/- 400 along); ONE key-moment model - rigid post in the grouted pocket - for every key (psi_ec dropped; K7 now 0.85 on the Key A parallel-edge check, cone 0.52; K14 0.49); 8 % cone reduction at the diagonal opening corners K3, K16, K17; under-slab plate 25 mm, class-3 stiffeners, skewed levers at K23/K25/K27 and the T/C couple for the slab designer stated; bond quoted with the real extents. Worst base at Rev 4a: K7 0.85 (superseded). |
| **Design Rev 3 / final critique C1-C14** | C1 north-face jog modelled: wall and roof edge at y 35.37 for x 67.89-81.79 (K6, K5, K7 on that wall), 35.87 east of x 81.79; the stair well reaches the north face, so no roof, no T1 and no eave beam across it (wall header only); 0.5 m wall return at x 81.79 on brackets from K3; rafters R68-R78 end at 35.37 (0.10-0.20 m cantilevers); gutters G-W at 35.37 and G-E at 35.87 with stop ends; roofed area 439.3 m2; loads, bracing (S-wind roof force 148.5 kN), reactions, CSVs and figure re-run. C3 plane raised 30 mm, TOS(35.87) = 3.33: **3.02 m clear under the cap-plate nuts at K1/K2**, one figure; C2 column length TOS - 0.35 (B2 0.355). C4 slotted fin plates deleted; conditioned-hall range +/-20 K, erection state +/-30 K; E-W chord path B2-RT-N-W-y 29.3-RT-N-E-B1 checked: k_eff 2.8 kN/mm, locked-in 10 kN service, ULS +9 kN with wind and 23 kN thermal-leading; K1, K2, K5, K7 checked - **K7 (and K5, whose north edge is now 0.1 m) built as B2**. C7 B2 plate extents to the slab face (100 outboard), one standard length 800; C8 drawing BOM weight quoted (25.4 t at closing sign-off, X1); C10 purlin cleat check (10.8 kN per cleat in zone F, 0.66) and panel fastener schedule from the supplier; C11 RT-JOG corrected (50.6 kN rod, 0.25); C13 K21 pattern fixed on site by the scan; C14 superseded figures removed. Worst base K25 0.83. |

## 1. Basis and assumptions

- Loads, combinations and resistances exactly per `../load_basis.md` Rev 2; geometry per `../../geometry.json`: 27 columns, L-shape less the notch, **north face at y 35.37 for x 67.89-81.79 and at 35.87 for x 81.79-95.69** (interior_walls_y 35.37, K6/K5/K7 on that wall; 0.5 m wall return at x 81.79), stair well x 77.89-81.79 / y 29.37-35.37 open to the north wall (no roof, no eave beam: a wall header carries wall and gutter stop-ends), elevator opening not roofed; roofed area 439.3 m2 from the grid.
- One roof plane at 6 % falling north, **TOS(y) = 3.33 + 0.06 (35.87 - y)** (TOS 3.33 at y 35.87, 3.36 at the west north edge 35.37, 4.55 at 15.57); level primaries with their top at TOS + 0.05; column top = cap-plate underside = TOS - 0.30, cap-plate top TOS - 0.28; column length TOS - 0.35 (B1: 25 mm plate + 25 mm grout; B2 plates 30 mm: TOS - 0.355), 2.99 m (y 35.77) to 4.18 m (y 15.87). **Clear height: 3.02 m under the lowest steel (cap-plate nuts at K1/K2, y 35.77); 3.06 m under the eave primary and under the rafters at the north edge.**
- Statics: all beams are chains of simple spans (fin plates, cap plates), purlins simple spans between rafters, columns pinned-pinned; girts span horizontally between columns, so each column delivers wL/2 of its wall to the roof and wL/2 to its base. The take-down integrates the roof on a 0.1 m grid (exact tributary, openings excluded) -> rafters -> primaries -> columns. Section tables IPE 200-360 / HEA 140-200 in `calc/sections.py`.
- Wind post WP1 (HEA 160) at the notch corner, set 280 mm inboard of both faces at (77.61, 20.25): wall wind only, slotted top connection, no uplift, base 250 x 250 x 15 with one centred 60 mm key (11.9 kN shear, 0.31).
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
| Global horizontal wind at roof level | 1.3 q_p on the projected wall area, half to the roof, plus the roof-suction component (38.6 kN, S wind; 30 kN N-S under E/W wind): **N 85.6, S 148.5, E/W 72 (+30 N-S) kN** char. | bracing, diaphragm |
| Wall self-weight | 0.30 kN/m2 x wall height (3.60 m N ... 4.82 m S) x column trib | column axial |
| Temperature (C4) | conditioned hall +/-20 K in service, +/-30 K erection/unconditioned state; E-W north bay pair B2-B1 restrained through the roof trusses: k_eff 2.8 kN/mm x 3.6 / 5.4 mm = 10 / 15 kN char.; ULS +9 kN on B1/B2 with wind (psi_0 0.6), 23 kN thermal-leading without wind; south pair released by the weak-axis bending of R78 (0.3 kN/mm), N-S lines by the fin-plate clearances | B1/B2 bays, bases K1, K2, K5, K7 |
| Seismic (EN 1998-1, a_g 0.10 g, S 1.2, q 1.5, S_d 0.20 g) | seismic weight 379 kN -> F_b = **75.9 kN** (1.0 E) with 5 % eccentricity -> max bay force 37.2 kN (E-W) / 18.4 kN (N-S) vs wind 53 / 57 kN: wind governs; ULS-4 in the reaction table | ULS-4 |

Combinations (EN 1990 6.10): ULS-1 1.35 G + 1.5 Q; ULS-2 1.35 G + 1.5 W (pressure, wall D/E with c_pi -0.3, roof +0.39, bracing compression); ULS-3 1.0 G_min + 1.5 W (uplift, c_pi +0.2, four wind directions, bracing tension); ULS-4 1.0 G +/- 1.0 E; SLS G + Q (L/200, purlins L/150) and G + W (sway H/150).

## 3. Load take-down and bracing analysis results

**Take-down (`takedown.py`).** 11 N-S rafter lines (x = 68.0, 70.0, 72.1, 74.9, 77.8, 81.85, 84.5, 87.2, 89.9, 92.5, 95.5), rafter spans 2.7-9.2 m, purlin spans 2.05-3.1 m; the west-block rafters end at the north wall y 35.37 (0.10-0.20 m cantilevers carrying gutter G-W), the east ones at 35.87 (gutter G-E); nothing spans the stair well. Example column loads (characteristic, kN): K12 interior G 24.5, Q 25.0, W_N -56.0; K19 (braced, west wall) G 28.1, Q 19.1, W_S -43.7. Sum of column loads: G 439 (incl. gutters), Q 264 (= 0.60 x 439.3), W_S -660 kN.

**Bracing (`bracing.py`).** The roof force of each windward face (and the roof-suction component at its centroid) is distributed to the bays twice: (a) rigid diaphragm, 3 DOF, bay stiffness k = E A cos^2(alpha)/L_d of one L70x7 diagonal (15.6-24 kN/mm), centre of rigidity and torsion included; (b) flexible-diaphragm tributary to the bracing lines, then to the bays of a line by stiffness. **The envelope of (a) and (b) is used** (sum of bay forces 1.2-1.4 x the applied force). Wind from S, characteristic: rigid B5 23.4 / B10 22.0 / B7 23.1 / B8 26.1 / B6 28.3 / B9 25.4 kN, tributary 15.2 / 14.3 / 33.9 / 38.2 / 24.9 / 22.3 kN; wind from E: rigid B1 20.0 / B2 19.5 / B3 17.5 / B4 15.2, tributary 1.3 / 26.1 / 35.5 / 9.8 kN.

Bay forces at ULS (1.5 W), tension-only diagonal T = H L_d/w, column axial N = H h/w, base shear H at the tension-diagonal base (windward column) concurrent with that column's wall shear:

| Bay | Columns | w m | h m | Wind | H_Ed kN (ULS) | H seismic (1.0 E) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | h/150 mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | K1-K2 | 5.29 | 3.16 | W | 30.7 | 22.0 | 35.8 | 18.3 | 189.3 | 0.19 | 0.29 | 2.9 | 21.0 |
| B2 | K5-K7 | 5.70 | 3.19 | W | 40.1 | 33.8 | 46.0 | 22.4 | 189.3 | 0.24 | 0.37 | 3.2 | 21.3 |
| B3 | K22-K23 | 6.61 | 4.10 | E | 53.6 | 37.2 | 63.1 | 33.2 | 189.3 | 0.33 | 0.51 | 3.9 | 27.3 |
| B4 | K25-K26 | 4.00 | 4.35 | W | 23.4 | 16.2 | 34.6 | 25.4 | 189.3 | 0.18 | 0.28 | 3.0 | 29.0 |
| B5 | K15-K19 | 4.61 | 3.86 | S | 35.1 | 13.4 | 45.7 | 29.3 | 189.3 | 0.24 | 0.37 | 3.2 | 25.7 |
| B6 | K14-K18 | 4.81 | 3.69 | S | 42.6 | 15.7 | 53.6 | 32.7 | 189.3 | 0.28 | 0.43 | 3.4 | 24.6 |
| B7 | K20-K27 | 5.89 | 4.17 | S | 50.9 | 16.4 | 62.4 | 36.1 | 189.3 | 0.33 | 0.50 | 3.9 | 27.8 |
| B8 | K10-K16 | 4.81 | 3.69 | S | 57.3 | 18.4 | 72.2 | 44.0 | 189.3 | 0.38 | 0.58 | 3.9 | 24.6 |
| B9 | K18-K23 | 4.39 | 3.97 | S | 38.1 | 14.1 | 51.4 | 34.5 | 189.3 | 0.27 | 0.42 | 3.4 | 26.4 |
| B10 | K19-K25 | 5.89 | 4.17 | S | 33.1 | 12.7 | 40.5 | 23.4 | 189.3 | 0.21 | 0.33 | 3.2 | 27.8 |

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
| R85/P_K11K12-P_K3K1 | IPE 270 | 6.40 | 29.3 | 26.1 | 0.22 | 0.07 | 0.17 | 0.25 | 0.17 | **0.25** | LTBu | OK |
| R87/K12-K1 | IPE 270 | 6.50 | 27.8 | 22.0 | 0.21 | 0.06 | 0.17 | 0.24 | 0.17 | **0.24** | LTBu | OK |
| R90/P_K12K13-P_K1K2 | IPE 270 | 6.50 | 26.5 | 20.5 | 0.2 | 0.06 | 0.17 | 0.23 | 0.17 | **0.23** | LTBu | OK |
| P_K11K12/K11-K12 | IPE 330 | 5.34 | 46.6 | 18.3 | 0.21 | 0.04 | 0.22 | 0.23 | 0.12 | **0.23** | LTBu | OK |
| P_K9K10/K9-K10 | IPE 330 | 5.69 | 44.9 | 17.0 | 0.2 | 0.03 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| P_K12K13/K12-K13 | IPE 330 | 5.29 | 45.4 | 18.5 | 0.21 | 0.04 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| R75/K24-P_K19K20 | IPE 270 | 5.79 | 25.5 | 25.2 | 0.19 | 0.07 | 0.14 | 0.21 | 0.13 | **0.21** | LTBu | OK |
| R72/K9-K5 | IPE 270 | 6.00 | 23.4 | 21.2 | 0.18 | 0.06 | 0.13 | 0.2 | 0.13 | **0.2** | LTBu | OK |
| R75/P_K9K10-P_K5K7 | IPE 270 | 5.93 | 23.6 | 19.1 | 0.18 | 0.05 | 0.15 | 0.2 | 0.14 | **0.2** | LTBu | OK |
| R70/P_K8K9-P_K6K5 | IPE 270 | 5.90 | 21.9 | 19.1 | 0.16 | 0.05 | 0.11 | 0.19 | 0.1 | **0.19** | LTBu | OK |
| R72/K26-P_K19K20 | IPE 270 | 5.89 | 22.7 | 22.0 | 0.17 | 0.06 | 0.13 | 0.19 | 0.12 | **0.19** | LTBu | OK |
| P_K3K1/K3-K1 | IPE 330 | 5.34 | 38.1 | 15.0 | 0.17 | 0.03 | 0.11 | 0.19 | 0.06 | **0.19** | LTBu | OK |
| R70/P_K25K26-P_K19K20 | IPE 270 | 5.89 | 21.8 | 18.4 | 0.16 | 0.05 | 0.11 | 0.18 | 0.1 | **0.18** | LTBu | OK |
| R78/K27-K20 | IPE 270 | 5.89 | 21.0 | 15.6 | 0.16 | 0.04 | 0.11 | 0.18 | 0.1 | **0.18** | LTBu | OK |
| R68/K25-K19 | IPE 270 | 5.89 | 19.2 | 13.1 | 0.14 | 0.04 | 0.07 | 0.16 | 0.06 | **0.16** | LTBu | OK |
| R68/K8-K6 | IPE 270 | 5.80 | 18.7 | 12.9 | 0.14 | 0.04 | 0.07 | 0.16 | 0.06 | **0.16** | LTBu | OK |
| P_K5K7/K5-K7 | IPE 330 | 5.69 | 28.9 | 11.0 | 0.13 | 0.02 | 0.12 | 0.14 | 0.07 | **0.14** | LTBu | OK |
| P_K1K2/K1-K2 | IPE 330 | 5.29 | 28.1 | 11.6 | 0.13 | 0.02 | 0.11 | 0.14 | 0.06 | **0.14** | LTBu | OK |
| P_K8K9/K8-K9 | IPE 330 | 4.10 | 31.5 | 15.8 | 0.14 | 0.03 | 0.11 | 0.14 | 0.05 | **0.14** | LTBu | OK |
| R78/K16-K10 | IPE 270 | 4.81 | 16.9 | 14.0 | 0.13 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| R82/K17-K11 | IPE 270 | 4.81 | 16.3 | 13.7 | 0.12 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| R82/K11-K3 | IPE 270 | 6.40 | 14.5 | 12.2 | 0.11 | 0.03 | 0.11 | 0.13 | 0.11 | **0.13** | LTBu | OK |
| R95/K23-K18 | IPE 270 | 4.39 | 14.9 | 13.6 | 0.11 | 0.04 | 0.05 | 0.12 | 0.04 | **0.12** | LTBu | OK |
| R95/K18-K14 | IPE 270 | 4.81 | 15.5 | 13.2 | 0.12 | 0.04 | 0.06 | 0.12 | 0.05 | **0.12** | LTBu | OK |
| ST1 | IPE 270 | 5.65 | 0 |  |  |  | 0.11 |  |  | **0.11** | 6.3.1 | OK |
| R78/K10-K7 | IPE 270 | 5.90 | 13.3 | 11.3 | 0.1 | 0.03 | 0.1 | 0.1 | 0.1 | **0.1** | LTBg | OK |
| P_K6K5/K6-K5 | IPE 330 | 4.10 | 21.0 | 10.7 | 0.09 | 0.02 | 0.06 | 0.1 | 0.03 | **0.1** | LTBu | OK |
| 14 further spans (eave beams, trimmers, short edge-beam spans, ST2) | IPE 330 / IPE 270 | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |

Governing members: primary **K19-K20 (9.79 m)** at 0.74 (deflection 36 mm = L/271; M_Ed 131 kNm = 0.59 M_pl; LTB 0.73); 9.2 m rafters at 0.49-0.52 (deflection 22-24 mm = L/390-410, M 0.35, LTB uplift 0.51). Max beam utilisation 0.74. Alternatives run with the same scripts: IPE 240 rafters pass strength (M 0.58, LTB uplift 0.71) but give L/265 on the 9.2 m spans with no reserve for a future ceiling, so IPE 270 is kept; IPE 300 primaries put K19-K20 at L/194 (1.03): IPE 330 confirmed.

Rafters as roof-truss posts: N_Ed = 38.6 kN with N_b,Rd = 624 kN (L_y 9.2, L_z 3.07 m) -> 0.06; new posts ST1 (IPE 270, 5.65 m, N 25.2 kN vs 231) and ST2 (4.10 m, 20.3 vs 404); eave primaries as struts <= 57 kN vs N_b,Rd >= 800 kN. Purlins are not used as struts.

**Columns** (6.3.1 pinned-pinned, L_cr = L both axes, HEA 160 curve b/c; 6.3.3 Annex B method 2, Table B.2 for the LTB-susceptible member, C_m = C_mLT = 0.95 for the wall-wind UDL, web normal to the wall it supports, corners biaxial). N_b,Rd = 461 kN (L 4.16 m) to 667 kN (L 2.97 m).

| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | k_zy (B.2) | 6.3.1 N/N_b,Rd | 6.3.3 | Util. | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| K25 | HEA 160 | 4.18 | 48.0 (ULS2E) | 43.1 (ULS3W) | 15.2 / 12.5 | 0.99 | 0.1 | 0.72 | **0.72** | OK |
| K23 | HEA 160 | 3.93 | 64.2 (ULS2W) | 62.3 (ULS3S) | 14.5 / 12.1 | 0.99 | 0.13 | 0.71 | **0.71** | OK |
| K22 | HEA 160 | 3.93 | 91.1 (ULS2E) | 56.3 (ULS3S) | 25.8 / 0.0 | 0.97 | 0.18 | 0.64 | **0.64** | OK |
| K21 | HEA 160 | 3.93 | 39.9 (ULS1) | 19.8 (ULS3S) | 28.9 / 0.0 | 0.99 | 0.08 | 0.59 | **0.59** | OK |
| K27 | HEA 160 | 4.18 | 39.4 (ULS2N) | 44.2 (ULS3S) | 11.0 / 9.3 | 0.99 | 0.09 | 0.53 | **0.53** | OK |
| K19 | HEA 160 | 3.83 | 80.0 (ULS2S) | 73.2 (ULS3S) | 18.7 / 0.0 | 0.98 | 0.16 | 0.48 | **0.48** | OK |
| K6 | HEA 160 | 3.02 | 23.4 (ULS1) | 14.5 (ULS3W) | 8.8 / 6.7 | 1.00 | 0.04 | 0.38 | **0.38** | OK |
| K26 | HEA 160 | 4.18 | 50.7 (ULS2W) | 30.7 (ULS3E) | 14.7 / 0.0 | 0.98 | 0.11 | 0.38 | **0.38** | OK |
| K14 | HEA 160 | 3.38 | 57.0 (ULS2S) | 26.7 (ULS3N) | 15.6 / 0.0 | 0.99 | 0.1 | 0.36 | **0.36** | OK |
| K18 | HEA 160 | 3.66 | 54.5 (ULS2S) | 39.7 (ULS3S) | 15.1 / 0.0 | 0.99 | 0.1 | 0.36 | **0.36** | OK |
| other 17 columns | HEA 160 | 2.97-4.16 | <= 58 | <= 58 | <= 15 | 0.98-1.00 | <= 0.12 | <= 0.38 | <= 0.38 | OK |

Max column utilisation 0.72 (K25, SW corner). Wind post WP1 HEA 160, L 4.24 m: M_y 9.4, M_z 9.9 kNm -> 0.48. HEA 140 reaches 1.06 at K25 with Table B.2: **HEA 160 confirmed**.

**Purlins Z200x2.0 @ 1.5 m** (basis: M_Rd 12.5 kNm single span, 16 sleeved; I = 3.9e6 mm4): worst gravity M_Ed = 4.3 kNm; worst uplift M_Ed = **8.3 kNm** on the 3.07 m corner spans (x 92.5-95.5, y 35.6, zone F, w = -7.1 kN/m), 0.66 of the single-span gravity value. Purlin cleats (C10): zone-F end reaction 10.8 kN per cleat -> 2 M12 8.8 in tension 0.11, cleat plate 120 x 10 bending 0.66; the panel fastener schedule in zones F/G comes from the panel supplier. Because the free-flange uplift capacity of a Z200x2.0 is typically 55-70 % of the gravity value, **a mid-span anti-sag row is specified on every span and the supplier's uplift capacity (>= 9 kNm single span with one anti-sag row, or sleeved) is required before order** (open item 3). Deflection G + Q on 4.07 m: 6.3 mm < L/150 = 27.1 mm. Girts (wall net 2.15 kN/m2, zone A 2.73 within 2.4 m of a corner): 1.5 m rows single-span for bays <= 5.3 m (<= 11.3 kNm); 1.2 m rows sleeved on K5-K7, K25-K19, K8-K6 (<= 14.2 kNm); 1.0 m rows sleeved on K21-K22, K22-K23, K14-K4 (<= 14.9 kNm, 0.93).

## 5. Connections (EN 1993-1-8)

- **Rafter to primary fin plate**, one type: 100 x 150 x 10 S275, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web, 2 x 6 mm fillets. Max rafter end reaction 35.2 kN (envelope ULS-1 / reversed ULS-3 incl. the gutter): bolt shear incl. eccentricity 0.33, bearing on the 6.6 mm rafter web **0.45** (governs), plate bearing 0.29, plate shear 0.17, plate bending 0.17, weld 0.19, web block tearing 0.31. 9.2 m rafters: 3 bolts, plate 220 (0.14 at 20.4 kN). No copes. T1/T2, ST1/ST2 and the notch eave beam use the same detail.
- **Primary to column cap plate** 200 x 280 x 20, a = 6 all round, 4 M20 through the primary bottom flange (gauge 90, **pitch 200** so the nuts clear the passing rafter flange; primaries bolted before the rafters). Tension = roof uplift 67.8 kN (K12, ULS-3N; the bracing vertical component enters below the cap through the gusset): bolt tension 0.12, shear + tension interaction with the chord/strut force 61.3 kN 0.25, IPE 330 flange T-stub 0.16, cap plate 0.05, weld 0.07. Chord continuity across a column (<= 61 kN): 10 mm tie plate between the primary bottom flanges on the lines y 29.3 and y 20.1.
- **Bracing gussets**: 10 mm plates welded to the column web and base plate; each L70x7 with 2 M20 (e1 40, p1 110, e2 30): angle net section 189 kN, bolt shear 188 kN, gusset bearing 2 x 124 kN; max T_Ed 72.2 kN (B8) -> 0.38 angle, 0.57 bolts.
- **Roof bracing** M24 rods 8.8 (F_t,Rd 203 kN) with turnbuckles to 8 mm gussets shop-welded to the primary webs and bolted (2 M16) to the rafter webs at the bottom flange level (no site welding, C9; rod hole in the rafter web shown on D5); on the east and west edge trusses the rods span two rafter bays and pass the intermediate rafter (R92 / R70) through a bolted web clip; sag ties to the purlins at the crossing and at 3 m centres.
- Trimmer T2 (y 24.09) IPE 270 between the rafters x 77.8 / 81.85 carries only the 150 mm upstand (0.3 kN/m, M_Ed 1.8 kNm); upstand framing 100 x 50 x 3 cold-formed C on the trimmers and along the rafters beside the openings, cricket on the south side of the stair well; the well's north edge is the wall itself (header with gutter stop-ends), T1 deleted.

## 6. Bases and anchors, Rev 4 (EN 1993-1-8 6.2.5, EN 1992-4 with the Rev 2 basis) - full note in `bases_C.md`

The slab edge is 100 mm from the centre of every perimeter column and the stair / shaft openings are free edges, so the base type is chosen per column from the real-edge checks:

- **B1, concentric resin anchors (13 bases: K3, K4, K6, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26)**: plate 300 x 400 x 25, 4 M20 at 80 x 280 (280 along the concrete column's long axis), h_ef 200 in the slab, clearance holes; Key A SHS 90x90x8 under the column (along-axis and inward shear, 25 MPa confined bearing, V_Rd 83.8 kN; parallel-to-edge breakout 2 V_Rk,c = 18.5 kN at c1 55 where an edge is 100 mm from the column, checked at K3, K4, K6, K7, K8, K11, K14); Key B 60 mm bar 180 mm inboard (c1 250, 38.2 kN) for outward shear at K3, K4, K6, K8, K14. Cone with the concrete actually there: interior 98.5 kN, one edge 50.4 kN, corner 37.8 kN, times psi_ec,N from the key moments. Key moments stay in the grouted pockets (rigid-post model, one model for all keys). Worst B1: K12 0.68, K16 0.68 (cone x 0.92 at the diagonal opening corner), K11 0.67. Thermal (C4): the locked-in E-W force (9 kN with wind, 23 kN thermal-leading) is applied to B1/B2 and their bases K1, K2, K5, K7 - all B2, max 0.76 (K7).
- **B2, through-bolts and inboard key pair (13 bases: K1, K2, K5, K7, K10, K15, K18, K19, K20, K22, K23, K25, K27; K7 by decision after the thermal check, K5 because its north edge is 0.1 m away)**: plate 550 x 800 x 30, 100 outboard to the slab face (per-base extents in bases_C.md: K7 500 x 1000, K23 1000 x 550, K25 550 x 900, K27 600 x 900) with two 120 x 10 stiffeners; 2 M24 8.8 through-bolts 250 mm inboard of the column, 280 apart, all >= 300 mm from every slab edge (rows shifted along the wall at K23, K25, K27), on a 400 x 200 x 25 under-slab plate; uplift by lever action about the inboard plate tip, T = N_t b/(b - c) = 2.39-2.93 N_t (K19: 175 kN, 87 kN per M24 = 0.43; tip bearing C = 1.39-1.93 N_t on a 350 x 60 strip <= 0.57; stiffened class-3 plate M = N_t c <= 26 kNm vs 48; per-base plate lengths 800-1000 mm along the wall, bases_C.md section 3); shear by two SHS 90x90x8 keys 200 mm inboard, +/- 300 along the wall, each taking half the shear plus the torque of the eccentric shear (arm 0.6 m), outward components checked as edge breakout at c1 >= 255 (41.5 kN): K25 0.83, K23 0.80, K27 0.76, K22 0.74. No cone, no anchor shear.
- **P, K21** (200 mm pier): 4 M16 h_ef 400 into the pier lapped with its bars (splitting restrained by the dia6 links, 49 kN -> 0.53), saddle plates for the N-S shear (0.36). The only base where the client's permission to drill a column head is used.
- WP1: post 280 mm inboard, one centred key, 0.31. Compression bearing <= 0.10 everywhere.
- Setting-out (X2): **columns are cut to the surveyed plate-top level; grout bed 25 +/- 5 mm** (the slab survey and the plate-top datum on S00 come before the column cut list).

Worst base **K25: 0.83 (B2 key pair outward (c1 >= 255), ULS2S)**; all 27 bases and WP1 <= 1.0 with the real edges. Coring acceptance equals the concrete the checks use: B1 edge heads outboard to the face, inboard >= 340 mm, +/- 400 along; interior B1 heads 400-650 centred; B2 heads the key breakout bodies (+/- 700 along for the standard layout, K23 to -1100, K25/K27 to +1000) and the under-slab plate zone, with soffit access at 13 locations; a B1 head that fails is built as B2.

## 7. Deflections and sway

- Roof members SLS G + Q: worst primary K19-K20 36 mm = L/271 (limit 49 mm); 9.2 m rafters 22-24 mm = L/390; 7.5 m rafters L/700-820; purlins L/640.
- Braced-bay sway under SLS wind (diagonal elongation + 2 mm bolt-slip allowance): 2.8-3.9 mm vs h/150 = 20-28 mm. Column bending under wall wind (K22, 9.8 kN/m on 3.91 m) 8.5 mm = h/460.
- **Roof diaphragm drift** at the mid-length of the east / west walls (truss deflection by virtual work over the M24 rods, SLS, plus bay sway): **10.5 / 9.5 mm** vs h/150 = 26-28 mm (0.40).

## 8. Bracing

Vertical bays (X, one L70x7 per diagonal, tension-only), **final list for the client - these bays must stay door-free**: E-W **B1 K1-K2** (north wall, 5.3 m), **B2 K5-K7** (north wall, 5.7 m), **B3 K22-K23** (notch south wall, 6.6 m), **B4 K25-K26** (south wall, 4.0 m); N-S **B5 K15-K19** and **B10 K19-K25** (west wall, 4.6 + 5.9 m), **B6 K14-K18** and **B9 K18-K23** (east wall, 4.8 + 4.4 m), **B7 K20-K27** (notch west wall / shaft west line, 5.9 m) and **B8 K10-K16** (core west line between the stair well and the shaft, inside the hall, 4.8 m). Max diagonal utilisation 0.38 (B8), gusset bolts 0.57. Reason for the layout: at every braced-bay base the bay shear enters the concrete along the column's long axis or towards the slab interior, never towards a free edge < 0.25 m; the middle columns K19, K18, K20 of the three N-S lines carry no net bracing uplift. Alternates if a bay is not door-free: B1 -> K3-K1, B3 -> K21-K22 (K21 base then needs a supplier-verified edge detail), B5/B10 -> single bay K15-K25 not possible (7.5 m), B8 -> none (K17-K21 and K11-K17 are excluded by the K21 / K11 edge condition).

Roof-plane bracing: M24 rods in 24 rafter cells (full rafter depth, primaries as chords, rafters as posts), east/west edge trusses with rods over two bays and posts ST1/ST2 at the wall-column lines; the west-end reaction of the north-band-east truss (38.6 kN) is carried by the single jog panel x 77.8-81.85 / y 24.5-29.3 (rod 50.6 kN, 0.25) into bay B8 (K10-K16), the y 29.3 primary being the continuous chord (tie plates at K10, K11).

| Roof truss | Wind | Span m | Depth m | Panels | Shear V kN | Diagonal T kN (M24, 203) | Chord kN | Post kN | Util. rod | Truss defl. ULS mm |
|---|---|---|---|---|---|---|---|---|---|---|
| RT-N-W (N band west, chords y 29.3 / 35.2) | N-S | 9.8 | 5.9 | 4 | 22.0 | 23.3 | 11.4 | 22.0 | 0.11 | 2.8 |
| RT-N-E (N band east, chords y 29.3 / 35.7) | N-S | 13.7 | 6.4 | 5 | 31.2 | 33.7 | 20.7 | 31.2 | 0.17 | 5.1 |
| RT-S-E (S band east, chords y 20.1 / 29.3) | N-S | 13.7 | 9.2 | 5 | 37.8 | 39.4 | 17.5 | 37.8 | 0.19 | 7.9 |
| RT-S-W (S band west, chords y 15.9 / 21.8) | N-S | 9.8 | 5.9 | 4 | 27.8 | 29.4 | 14.4 | 27.8 | 0.14 | 3.6 |
| RT-W (west edge, chords R68 / R72 (rods over two bays)) | E-W | 19.4 | 4.1 | 3 | 27.9 | 48.9 | 61.3 | 27.9 | 0.24 | 8.3 |
| RT-E (east edge, chords R90 / R95 (rods over two bays)) | E-W | 15.6 | 5.7 | 2 | 31.5 | 47.8 | 23.4 | 31.5 | 0.24 | 9.8 |
| RT-JOG (jog panel x 77.8-81.9 / y 24.5-29.3, carries the RT-N-E west reaction into B8) | N-S | 4.1 | 4.8 | 1 | 38.6 | 50.6 | 32.7 | 38.6 | 0.25 | 5.6 |

## 9. Reactions at the column bases (kN, ULS envelope with concurrent values; reactions_C.csv gives every column and case: ULS-1, ULS-2/3 for N, S, E, W wind, ULS-4 +/-x, +/-y, SLS, with N, V_x, V_y, near-edge flags and base utilisation)

| Col | Type | Bays | Near edges | Keys | N_c max kN (case) | N_t max kN (case) | V max kN (case) | N_c SLS | N_t SLS | Base governs | Util. | Min. zone |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | B2 | B1 | +y | A-pair | 60.4 (ULS2E) | 41.7 (ULS3N) | 42.7 (ULS2W) | 30.4 | 18.9 | B2 key pair outward | **0.51** | B2: 550 from face |
| K2 | B2 | B1 | +y | A-pair | 53.1 (ULS2W) | 41.5 (ULS3E) | 42.8 (ULS2E) | 24.1 | 20.6 | B2 key pair outward | **0.52** | B2: 550 from face |
| K3 | B1 | - | +y | A,B+y | 28.2 (ULS1) | 21.3 (ULS3N) | 17.0 (ULS2W) | 20.2 | 8.1 | Key B outward +y | **0.45** | 400 |
| K4 | B1 | - | +x,+y | A,B+x,+y | 19.8 (ULS1) | 14.5 (ULS3E) | 14.9 (ULS2N) | 14.3 | 5.3 | anchor group cone, real edges | **0.38** | 400 |
| K5 | B2 | B2 | +y | A-pair | 60.0 (ULS2E) | 44.4 (ULS3W) | 51.2 (ULS2W) | 26.9 | 21.6 | B2 key pair outward | **0.57** | B2: 550 from face |
| K6 | B1 | - | -x,+y | A,B-x,+y | 23.4 (ULS1) | 14.5 (ULS3W) | 16.4 (ULS2N) | 16.9 | 4.5 | Key B outward -x | **0.40** | 400 |
| K7 | B2 | B2 | +x,+y | A-pair | 52.4 (ULS2W) | 29.4 (ULS3E) | 52.5 (ULS2E) | 20.0 | 13.5 | B2 key pair bearing | **0.76** | B2: 550 from face |
| K8 | B1 | - | -x | A,B-x | 30.1 (ULS1) | 26.7 (ULS3W) | 15.9 (ULS2W) | 21.5 | 11.4 | anchor group cone, real edges | **0.53** | 450 |
| K9 | B1 | - | - | A | 57.2 (ULS1) | 53.6 (ULS3N) | 0.0 (ULS1) | 40.2 | 24.6 | anchor group cone, real edges | **0.54** | 600 |
| K10 | B2 | B8 | +y | A-pair | 79.6 (ULS2S) | 60.5 (ULS3N) | 33.8 (ULS2N) | 30.2 | 31.8 | B2 tip bearing | **0.40** | B2: 550 from face |
| K11 | B1 | - | +y | A | 44.4 (ULS1) | 36.4 (ULS3N) | 0.0 (ULS1) | 31.3 | 15.4 | anchor group cone, real edges | **0.72** | 500 |
| K12 | B1 | - | - | A | 70.5 (ULS1) | 67.8 (ULS3N) | 0.0 (ULS1) | 49.5 | 31.5 | anchor group cone, real edges | **0.69** | 650 |
| K13 | B1 | - | - | A | 55.7 (ULS1) | 54.0 (ULS3N) | 0.0 (ULS1) | 39.1 | 25.1 | anchor group cone, real edges | **0.55** | 600 |
| K14 | B1 | B6 | +x | A,B+x | 57.0 (ULS2S) | 26.7 (ULS3N) | 31.1 (ULS2N) | 19.6 | 11.9 | Key B outward +x | **0.50** | 450 |
| K15 | B2 | B5 | -x | A-pair | 43.7 (ULS2S) | 17.0 (ULS3N) | 23.8 (ULS2N) | 11.4 | 7.8 | B2 key pair outward | **0.32** | B2: 550 from face |
| K16 | B1 | B8 | - | A | 44.4 (ULS2N) | 58.7 (ULS3S) | 57.3 (ULS2S) | 15.5 | 34.7 | Key A SHS bearing | **0.68** | 650 |
| K17 | B1 | - | - | A | 23.3 (ULS1) | 15.7 (ULS3S) | 0.0 (ULS1) | 16.5 | 5.7 | anchor group cone, real edges, -8 % diagonal corner | **0.22** | 400 |
| K18 | B2 | B6,B9 | +x | A-pair | 54.5 (ULS2S) | 39.7 (ULS3S) | 45.6 (ULS2S) | 16.2 | 21.6 | B2 key pair outward | **0.54** | B2: 550 from face |
| K19 | B2 | B5,B10 | -x | A-pair | 80.0 (ULS2S) | 73.2 (ULS3S) | 40.2 (ULS2S) | 47.2 | 35.1 | B2 key pair outward | **0.52** | B2: 550 from face |
| K20 | B2 | B7 | +x | A-pair | 82.5 (ULS2S) | 64.4 (ULS3N) | 30.0 (ULS2N) | 39.4 | 31.8 | B2 tip bearing | **0.43** | B2: 550 from face |
| K21 | P | - | +y,-y | saddle | 39.9 (ULS1) | 19.8 (ULS3S) | 29.5 (ULS2W) | 28.6 | 4.6 | P pier anchors: splitting of the 200 pier restrained by the dia6/200 links | **0.53** | B2: 550 from face |
| K22 | B2 | B3 | -y | A-pair | 91.1 (ULS2E) | 56.3 (ULS3S) | 59.4 (ULS2W) | 48.0 | 23.6 | B2 key pair outward | **0.74** | B2: 550 from face |
| K23 | B2 | B3,B9 | +x,-y | A-pair | 64.2 (ULS2W) | 62.3 (ULS3S) | 64.1 (ULS2E) | 25.2 | 34.0 | B2 key pair outward | **0.80** | B2: 550 from face |
| K24 | B1 | - | - | A | 23.9 (ULS1) | 23.5 (ULS3S) | 16.5 (ULS2E) | 17.1 | 10.6 | Key A towards edge -y | **0.31** | 450 |
| K25 | B2 | B4,B10 | -x | A-pair | 48.0 (ULS2E) | 43.1 (ULS3W) | 47.1 (ULS2S) | 18.4 | 23.1 | B2 key pair outward | **0.83** | B2: 550 from face |
| K26 | B1 | B4 | - | A | 50.7 (ULS2W) | 30.7 (ULS3E) | 26.8 (ULS2E) | 20.6 | 14.3 | anchor group cone, real edges | **0.40** | 500 |
| K27 | B2 | B7 | +x | A-pair | 39.4 (ULS2N) | 44.2 (ULS3S) | 59.4 (ULS2S) | 14.2 | 25.1 | B2 key pair outward | **0.77** | B2: 550 from face |
| WP1 (offset 280 inboard) | post | - | +x,-y | B centred | 1.7 (self weight) | 0 | 11.9 (ULS2 E / S) | - | - | key edge breakout c1 250 | 0.31 | - |

## 10. Weight and section list

| Item | Section | Length m | Weight t |
|---|---|---|---|
| Rafters / edge beams / trimmers / posts ST1-ST2 | IPE 270 | 208.2 | 7.52 |
| Primaries / eave beams | IPE 330 | 92.5 | 4.54 |
| Columns (27) + wind post WP1 | HEA 160 | 99.6 | 3.03 |
| Plates, stiffeners, keys, bolts (BOM take-off) | S275 / S355 keys | - | 3.40 |
| **Hot-rolled total** | | | **18.5** |
| Wall bracing, 10 bays x 2 diagonals | L 70x7 | 129.7 | 0.96 |
| Roof bracing, 24 panels x 2 diagonals | M24 rods 8.8 | 365.6 | 1.30 |
| Purlins 300 m + girts 271 m (BOM lengths) | Z 200x2.0 S350GD | 571 | 3.37 |
| Calculation take-off | | | 24.1 |
| **BOM total (S06, for cost)** | | | **25.4 t** (52 kg/m2 of footprint 486 m2, 58 kg/m2 of roofed 439 m2) |

Sections: **IPE 330** (all E-W primaries and eave beams on the column rows, 92.5 m), **IPE 270** (rafters, edge beams, trimmer T2, truss posts ST1/ST2, 208 m), **HEA 160** (27 columns, WP1), plus L70x7 wall bracing, M24 rod roof bracing, Z200x2.0 purlins/girts. Three hot-rolled sections kept. **Weight: 25.4 t per the drawing bill of materials (S06 Rev 4b: includes the sill rail 0.40 t, the well header 0.22 t and the Rev 4b base plates), used for cost**; the calculation take-off above gives 24.1 t with the BOM's plates (3.4 t) and purlin/girt length (571 m), the balance being the sill rail, well header and the BOM's cut-length and connection allowances. Cost basis: 25.4 t fabricated and erected at the indicative MENA rate (about 51,800 $ incl. the heavy base plates, i.e. about 1,000 $ above the 24.9 t figure of the final critique).

## 11. Open items / risks

1. **Slab verification** (bases_C.md sections 5-6): cores at 3 heads then every head against its own one-sided criterion; rebar scan of the slab top bars for the pockets and through-bolt holes; pull-out tests on 3 anchors to 45 kN; supplier ETA group verification; soffit access for the 13 B2 under-slab plates (ceiling openings) and the K21 pier faces. A B1 head that fails its criterion becomes B2; if a B2 soffit is inaccessible, the basis Rev 2 column-head anchorage is the agreed alternative at that head.
2. Wind: q_p 1.30 to be confirmed with the Libyan National Meteorological Centre; a 10 % increase raises the worst B1 base (K7) to about 0.95 and the B2 key pair at K25 to 0.91.
3. Purlin uplift capacity (>= 9 kNm single span with one anti-sag row) and the sleeved girt capacities to be confirmed with the supplier before order.
4. BoardX product data (0.30 kN/m2, girt rows per section 4) and its drift limit (h/150 assumed; diaphragm drift 10 mm, bay sway 4 mm).
5. Seismic: F_b 77 kN on the roof mass alone is below the wind bay forces; floor amplification through the existing building (S_a up to ~0.6 g / q) could bring the E-W seismic bay forces to the wind level - two-mass check once the building period is known; the bracing has 2.5 x reserve.
6. Existing structure (C5): the roof adds about 439 kN of characteristic gravity load and 148.5 kN of characteristic roof-level wind (N-S) into the 27 pinned 20 x 40 concrete columns and their foundations; as-builts, a one-page adequacy statement of the existing columns/foundations, a roof survey (screed thickness = datum for the 3.02 m and the base seating) and the slab-top datum on S00 are required before cores.
7. Client confirmations: door-free bays B1-B10 (section 8), B8 visible inside the hall along the core line, rafter R82 over the shaft east wall line (x 81.85 vs shaft face 81.99).
8. Thermal: no slotted holes; the locked-in E-W force is designed for (section 2); the panel supplier confirms the sandwich-panel fastening for +/-30 K. Client option (C15): all 27 bases as B2 (16 more soffit openings) removes every cone check and the B1 coring criterion.

Files: `design_report_C.md` (this, Rev 3), `bases_C.md` (Rev 4b), `members_C.csv` (99 rows), `reactions_C.csv` (595 rows, with base type, keys, psi_ec, max anchor/bolt and minimum zone per case), `framing_C.png`, `calc/` (sections.py, model.py, loads.py, statics.py, takedown.py, bracing.py, members.py, connections.py, bases_note.py, run_all.py, write_report.py, report_text.md, summary_C.json).

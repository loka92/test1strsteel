# Alternative C - post-and-beam braced frame: design report (Rev 1 geometry)

System C: E-W primaries on the column rows, N-S rafters, pinned HEA columns, vertical X bracing for all lateral load, roof-plane X bracing as the diaphragm. All numbers come from the scripts in `calc/` (`python3 run_all.py; python3 write_report.py`); ULS design values unless stated.

## 1. Basis and assumptions

- Loads, combinations and resistances exactly per the binding `../load_basis.md`; geometry per `../../geometry.json` (27 columns, L-shape less the notch, stair and elevator openings not roofed; roofed area 446.2 m2 from the grid).
- One roof plane at 6 % falling north, TOS(y) = 3.28 + 0.06 (35.87 - y). **Detail change vs the scheme:** the level primaries have their top at TOS + 0.04 (scheme: + 0.06), so the IPE 270 rafter bottom flange sits 20 mm above the IPE 330 bottom flange and clears it on the 3.4 deg cut without a cope; panel underside (TOS + 0.20) clears the primary top by 160 mm. Cap-plate top = TOS - 0.29, column length = TOS - 0.35 (plate + grout), 2.94 m (north) to 4.13 m (south); 3.01 m clear at the north eave.
- Statics: all beams are chains of simple spans, purlins simple spans between rafters, columns pinned-pinned. The take-down integrates the roof on a 0.1 m grid (exact tributary, openings excluded) -> rafters -> primaries -> columns. Section tables IPE 200-360 / HEA 140-200 in `calc/sections.py`.
- Wind zone note: the basis labels theta = 0 as wind from S; in EN 1991-1-4 Fig. 7.6 theta = 0 is the wind blowing onto the low (north) eave. To remove the ambiguity the larger set (F -2.3, G -1.3, H -0.8) is applied for **both** N and S wind with the F/G strip (e/10 = 1.2 m, F over e/4 = 3 m at the corners) on the windward edge; wind along the ridge uses F -2.1, G -1.8, H -0.6, I -0.5 with e = 12 m. c_pi = +0.2 (uplift) and -0.3 (pressure) both applied.
- Walls: BoardX on Z girts spanning between columns; girt reactions load the columns, half to the cap and half to the base. **The wall base rail is assumed anchored to the slab (M10 @ 600), so the lower half of the wall wind goes to the slab directly and the column bases see the bracing shear only**; the wall base shear is listed separately (V_wall) in the reaction table.
- Wind post WP1 (HEA 160) added at the notch corner (77.89, 19.97): wall wind only, slotted top connection, no uplift, base 2 M16 in a solid rib (5 kN shear).

## 2. Loads and combinations (kN, m)

| Action | Value | Used for |
|---|---|---|
| Panel + purlins + services G | 0.12 + 0.05 + 0.20 = 0.37 kN/m2 + member self-weight from the sections | gravity |
| G_min (uplift) | 0.17 kN/m2 + member self-weight | ULS-3 |
| Imposed cat. H Q | 0.60 kN/m2, psi_0 = 0 (never with wind) | ULS-1, SLS |
| Wind q_p | 1.30 kN/m2 at z_e = 10 m | all wind cases |
| Roof net uplift, c_pi +0.2 | H zone -(0.8+0.2) 1.3 = **-1.30**; G -1.95; F **-3.25** kN/m2 (N/S wind); along ridge G -2.6, F -2.99, H -1.04, I -0.91 | ULS-3, purlins, fly braces |
| Roof pressure case, c_pi -0.3 | (0.0 + 0.3) 1.3 = +0.39 kN/m2 (never governs over Q) | ULS-2 |
| Walls, net | D +1.1 (c_pi -0.3), A -1.4 / B -1.0 / C -0.7 / E -0.7 (c_pi +0.2), x 1.3 -> up to 1.82 kN/m2 char. | column bending, base V_wall |
| Global horizontal wind at roof level | 1.3 q_p on the projected wall area above the slab, half to the roof: **N 84.1, S 108.7, E 71.9, W 71.9 kN** (char.) | bracing, diaphragm |
| Wall self-weight | 0.30 kN/m2 x wall height (3.58 m N ... 4.80 m S) x column trib | column axial |
| Seismic check (EN 1998-1, a_g 0.10 g, S 1.2, q 1.5, plateau S_d = 0.20 g) | seismic weight 382 kN (roof G + steel + half walls) -> F_b = **76.4 kN** (1.0 E) versus 1.5 W = 163.1 kN (N-S) and 107.8 kN (E-W): **wind governs both directions**, no seismic design of the bracing needed | ULS-4 |

Combinations (EN 1990 6.10): ULS-1 1.35 G + 1.5 Q; ULS-2 1.35 G + 1.5 W (pressure case, wall D/E with c_pi -0.3, roof +0.39, bracing compression); ULS-3 1.0 G_min + 1.5 W (uplift, c_pi +0.2, four wind directions, bracing tension); ULS-4 1.0 G +/- 1.0 E check only; SLS G + Q (deflection L/200, purlins L/150) and G + W (sway H/150). Uniform ULS-1 roof load 1.35 x 0.37 + 1.5 x 0.60 = 1.40 kN/m2 plus steel.

## 3. Load take-down and bracing analysis results

**Take-down (scripts `takedown.py`).** 11 N-S rafter lines (x = 68.0, **70.0 (added)**, 72.1, 74.9, 77.8, 81.85, 84.5, 87.2, 89.9, 92.5, 95.5), rafter spans 2.7-9.2 m; purlin spans now 2.05-3.1 m (4.07 m only over the north strip of the stair well). Example column loads (characteristic, kN): K12 interior G 24.5 (incl. 0.20 services), Q 25.0, W_N -54.5; K19 (braced, west wall) G 28.0, Q 19.1, W_S -41.9. Sum of column loads: G 428 kN, Q 268 kN (= 0.60 x 446 m2, check), W_N -610 kN (mean -1.37 kN/m2 with edge zones).

**Bracing (script `bracing.py`).** The roof force of each windward face is distributed to the braced bays twice: (a) rigid diaphragm, 3-DOF, bay stiffness k = E A cos^2(alpha)/L_d of one tension diagonal (k = 15.6-23.9 kN/mm), centre of rigidity and torsion included; (b) flexible-diaphragm tributary (each eave strip to the two adjacent bracing lines). **The envelope of (a) and (b) is used** (sum of bay forces 1.2-1.5 x the applied force, deliberately conservative). Characteristic bay shears for wind from S: rigid B5 26.4 / B6 30.5 / B7 25.6 / B8 26.3 kN, tributary 20.4 / 27.0 / 27.9 / 34.0 kN; for wind from E: rigid B1 18.4 / B2 18.1 / B3 18.7 / B4 16.7, tributary 1.3 / 25.9 / 35.4 / 9.6 kN. Bay B8 (K17-K21, x = 81.85, along the elevator shaft east wall) was **added** to the scheme's seven bays: without it B7 collected 54 kN char. (81 kN ULS) and 102 kN uplift at K20/K27, which the 4-anchor group cannot take.

Bay forces at ULS (1.5 W), tension-only diagonal T = H L_d/w, column axial N = H h/w, base shear H shared by the two bases through an HEA 160 base strut (see section 6):

| Bay | Columns | w m | h m | Governing wind | H_Ed kN (ULS) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | Limit h/150 mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | K1-K2 | 5.29 | 3.11 | E | 27.6 | 32.0 | 16.2 | 189.3 | 0.17 | 0.22 | 2.8 | 20.7 |
| B2 | K5-K7 | 5.70 | 3.14 | E | 38.9 | 44.4 | 21.4 | 189.3 | 0.23 | 0.30 | 3.1 | 20.9 |
| B3 | K22-K23 | 6.61 | 4.05 | E | 53.1 | 62.3 | 32.5 | 189.3 | 0.33 | 0.43 | 3.9 | 27.0 |
| B4 | K25-K26 | 4.00 | 4.30 | W | 25.1 | 36.8 | 27.0 | 189.3 | 0.19 | 0.25 | 3.1 | 28.7 |
| B5 | K15-K19 | 4.61 | 3.81 | S | 39.6 | 51.4 | 32.7 | 189.3 | 0.27 | 0.35 | 3.3 | 25.4 |
| B6 | K14-K18 | 4.81 | 3.64 | S | 45.7 | 57.4 | 34.6 | 189.3 | 0.30 | 0.39 | 3.5 | 24.3 |
| B7 | K20-K27 | 5.89 | 4.12 | S | 41.9 | 51.1 | 29.3 | 189.3 | 0.27 | 0.35 | 3.5 | 27.5 |
| B8 | K17-K21 | 4.39 | 3.92 | S | 51.0 | 68.4 | 45.5 | 189.3 | 0.36 | 0.47 | 3.8 | 26.1 |

## 4. Member checks (EN 1993-1-1)

Checks per span: bending 6.2.5 (M_pl,Rd IPE 270 = 133 kNm, IPE 330 = 221 kNm), shear 6.2.6 (V_pl,Rd 351 / 489 kN; V_Ed < 0.5 V_pl everywhere so no M-V interaction), LTB 6.3.2 with M_cr from I_w, I_t and C1 per restraint segment (C1 = 1.88 - 1.40 psi + 0.52 psi^2 for linear segments, 1.0 when the maximum lies inside the segment), curve b, and deflection G + Q <= L/200 by numerical double integration.

Restraint assumptions: rafters - top flange held by purlins @ 1.5 m (gravity, chi_LT = 1.0); under uplift the free bottom flange is held by **fly braces to the purlins at mid-span for spans <= 6.6 m and at the third points for 7.5 and 9.2 m spans** (segment 2.2-3.25 m, M_b,Rd >= 98 kNm for IPE 270). Primaries - both flanges restrained at the rafter fin plates (plate over the full rafter web depth, bottoms 20 mm apart) and at the columns, segments <= 4.1 m (eave beams without rafters: full span).

| Member (span) | Section | L m | M_Ed kNm | V_Ed kN | 6.2.5 M | 6.2.6 V | 6.3.2 LTB gravity | 6.3.2 LTB uplift | SLS L/200 | Util. | Governs | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P_K19K20/K19-K20 | IPE 330 | 9.79 | 131.3 | 44.8 | 0.59 | 0.09 | 0.73 | 0.68 | 0.74 | **0.74** | defl | OK |
| R92/P_K22K23-K13 | IPE 270 | 9.20 | 51.0 | 26.9 | 0.38 | 0.08 | 0.36 | 0.51 | 0.52 | **0.52** | defl | OK |
| R87/P_K21K22-K12 | IPE 270 | 9.20 | 47.9 | 23.2 | 0.36 | 0.07 | 0.35 | 0.48 | 0.5 | **0.5** | defl | OK |
| R85/P_K21K22-P_K11K12 | IPE 270 | 9.20 | 47.3 | 22.9 | 0.36 | 0.07 | 0.35 | 0.47 | 0.49 | **0.49** | defl | OK |
| R90/P_K22K23-P_K12K13 | IPE 270 | 9.20 | 46.8 | 22.7 | 0.35 | 0.06 | 0.34 | 0.46 | 0.49 | **0.49** | defl | OK |
| R75/P_K19K20-P_K9K10 | IPE 270 | 7.51 | 33.2 | 17.7 | 0.25 | 0.05 | 0.25 | 0.3 | 0.28 | **0.3** | LTBu | OK |
| P_K21K22/K21-K22 | IPE 330 | 7.03 | 51.3 | 26.1 | 0.23 | 0.05 | 0.27 | 0.28 | 0.2 | **0.28** | LTBu | OK |
| P_K22K23/K22-K23 | IPE 330 | 6.67 | 54.2 | 31.5 | 0.25 | 0.06 | 0.25 | 0.28 | 0.17 | **0.28** | LTBu | OK |
| R72/P_K19K20-K9 | IPE 270 | 7.51 | 28.0 | 14.9 | 0.21 | 0.04 | 0.21 | 0.25 | 0.25 | **0.25** | LTBu | OK |
| R92/K13-K2 | IPE 270 | 6.50 | 26.3 | 20.5 | 0.2 | 0.06 | 0.18 | 0.23 | 0.18 | **0.23** | LTBu | OK |
| R70/P_K19K20-P_K8K9 | IPE 270 | 7.56 | 23.9 | 12.7 | 0.18 | 0.04 | 0.19 | 0.21 | 0.22 | **0.22** | defl | OK |
| P_K9K10/K9-K10 | IPE 330 | 5.69 | 44.9 | 17.0 | 0.2 | 0.03 | 0.22 | 0.21 | 0.12 | **0.22** | LTBg | OK |
| P_K11K12/K11-K12 | IPE 330 | 5.34 | 46.1 | 18.3 | 0.21 | 0.04 | 0.22 | 0.22 | 0.12 | **0.22** | LTBg | OK |
| P_K12K13/K12-K13 | IPE 330 | 5.29 | 45.4 | 18.5 | 0.21 | 0.04 | 0.22 | 0.21 | 0.12 | **0.22** | LTBg | OK |
| R87/K12-K1 | IPE 270 | 6.50 | 24.3 | 17.1 | 0.18 | 0.05 | 0.17 | 0.21 | 0.17 | **0.21** | LTBu | OK |
| R85/P_K11K12-P_K3K1 | IPE 270 | 6.40 | 23.2 | 16.5 | 0.17 | 0.05 | 0.17 | 0.2 | 0.17 | **0.2** | LTBu | OK |
| R90/P_K12K13-P_K1K2 | IPE 270 | 6.50 | 23.8 | 16.7 | 0.18 | 0.05 | 0.17 | 0.2 | 0.17 | **0.2** | LTBu | OK |
| R95/K14-K4 | IPE 270 | 6.40 | 23.5 | 15.2 | 0.18 | 0.04 | 0.11 | 0.2 | 0.11 | **0.2** | LTBu | OK |
| R75/K24-P_K19K20 | IPE 270 | 5.79 | 20.6 | 17.8 | 0.16 | 0.05 | 0.14 | 0.17 | 0.13 | **0.17** | LTBu | OK |
| R75/P_K9K10-P_K5K7 | IPE 270 | 5.93 | 20.9 | 15.3 | 0.16 | 0.04 | 0.15 | 0.17 | 0.14 | **0.17** | LTBu | OK |
| R72/K26-P_K19K20 | IPE 270 | 5.89 | 17.8 | 13.9 | 0.13 | 0.04 | 0.13 | 0.15 | 0.12 | **0.15** | LTBu | OK |
| R72/K9-K5 | IPE 270 | 6.00 | 18.1 | 13.5 | 0.14 | 0.04 | 0.13 | 0.15 | 0.13 | **0.15** | LTBu | OK |
| R78/K27-K20 | IPE 270 | 5.89 | 16.9 | 12.6 | 0.13 | 0.04 | 0.11 | 0.14 | 0.1 | **0.14** | LTBu | OK |
| R68/K25-K19 | IPE 270 | 5.89 | 15.4 | 10.9 | 0.12 | 0.03 | 0.07 | 0.13 | 0.06 | **0.13** | LTBu | OK |
| R70/P_K25K26-P_K19K20 | IPE 270 | 5.89 | 15.4 | 14.1 | 0.12 | 0.04 | 0.11 | 0.13 | 0.1 | **0.13** | LTBu | OK |
| R78/K16-K10 | IPE 270 | 4.81 | 16.9 | 14.0 | 0.13 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| R82/K17-K11 | IPE 270 | 4.81 | 16.3 | 13.5 | 0.12 | 0.04 | 0.12 | 0.13 | 0.09 | **0.13** | LTBu | OK |
| P_K5K7/K5-K7 | IPE 330 | 5.69 | 26.8 | 10.3 | 0.12 | 0.02 | 0.13 | 0.13 | 0.07 | **0.13** | LTBu | OK |
| R68/K8-K6 | IPE 270 | 5.80 | 14.7 | 10.6 | 0.11 | 0.03 | 0.07 | 0.12 | 0.06 | **0.12** | LTBu | OK |
| R70/P_K8K9-P_K6K5 | IPE 270 | 5.90 | 14.7 | 12.5 | 0.11 | 0.04 | 0.11 | 0.12 | 0.1 | **0.12** | LTBu | OK |
| R82/K11-K3 | IPE 270 | 6.40 | 14.8 | 11.4 | 0.11 | 0.03 | 0.11 | 0.08 | 0.12 | **0.12** | defl | OK |
| P_K3K1/K3-K1 | IPE 330 | 5.34 | 22.1 | 9.0 | 0.1 | 0.02 | 0.1 | 0.11 | 0.06 | **0.11** | LTBu | OK |
| P_K8K9/K8-K9 | IPE 330 | 4.10 | 24.5 | 12.6 | 0.11 | 0.03 | 0.11 | 0.1 | 0.05 | **0.11** | LTBg | OK |
| R78/K10-K7 | IPE 270 | 5.90 | 13.3 | 9.2 | 0.1 | 0.03 | 0.1 | 0.08 | 0.09 | **0.1** | LTBg | OK |
| R95/K18-K14 | IPE 270 | 4.81 | 12.6 | 10.5 | 0.09 | 0.03 | 0.06 | 0.1 | 0.05 | **0.1** | LTBu | OK |
| P_K1K2/K1-K2 | IPE 330 | 5.29 | 21.2 | 8.9 | 0.1 | 0.02 | 0.1 | 0.1 | 0.05 | **0.1** | LTBu | OK |
| 16 further spans (eave beams, trimmers, short edge-beam spans) | IPE 330 / IPE 270 | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |

Governing members: primary **K19-K20 (9.79 m)** at 0.74 (deflection 36 mm = L/271; M_Ed 131 kNm = 0.59 M_pl; LTB 0.73 with C1 = 1.86 on the 4.1 m end segment); 9.2 m rafters at 0.49-0.52 (deflection 22-24 mm = L/390-410, M 0.35, LTB uplift 0.51). Max beam utilisation 0.74. Alternatives run with the same scripts: IPE 240 rafters pass strength (M 0.58, LTB uplift 0.71) but give L/265 on the 9.2 m spans with no reserve for a future ceiling, so IPE 270 is kept; IPE 300 primaries put K19-K20 at L/194 (1.03): IPE 330 confirmed.

Rafters as roof-truss posts: N_Ed = 53.1 kN with N_b,Rd = 624 kN (L_y 9.2, L_z 3.07 m) -> 0.09; eave primaries as struts <= 53 kN vs N_b,Rd >= 800 kN. Purlins are not used as struts.

**Columns** (6.3.1 pinned-pinned, L_cr = L both axes, HEA 160 curve b/c; 6.3.3 Annex B method 2 with C_m = 0.95 for the wall-wind UDL, orientation web perpendicular to the wall it supports, corners biaxial). N_b,Rd = 465 kN (L 4.13 m) to 673 kN (L 2.94 m).

| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | 6.3.1 N/N_b,Rd | 6.3.3 interaction | Util. | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| K25 | HEA 160 | 4.13 | 50.1 (ULS2W) | 34.4 (ULS3W) | 14.8 / 12.2 | 0.11 | 0.68 | **0.68** | OK |
| K23 | HEA 160 | 3.88 | 63.6 (ULS2E) | 45.6 (ULS3E) | 18.0 / 9.3 | 0.13 | 0.64 | **0.64** | OK |
| K22 | HEA 160 | 3.88 | 90.2 (ULS2E) | 55.2 (ULS3E) | 25.1 / 0.0 | 0.18 | 0.56 | **0.56** | OK |
| K21 | HEA 160 | 3.88 | 80.8 (ULS2S) | 60.3 (ULS3S) | 22.2 / 0.0 | 0.16 | 0.49 | **0.49** | OK |
| K27 | HEA 160 | 4.13 | 47.3 (ULS2S) | 34.7 (ULS3S) | 13.7 / 7.1 | 0.1 | 0.49 | **0.49** | OK |
| K19 | HEA 160 | 3.78 | 89.2 (ULS2S) | 73.8 (ULS3S) | 18.3 / 0.0 | 0.17 | 0.43 | **0.43** | OK |
| K6 | HEA 160 | 2.97 | 24.4 (ULS1) | 11.2 (ULS3W) | 8.5 / 6.5 | 0.04 | 0.35 | **0.35** | OK |
| K14 | HEA 160 | 3.33 | 58.8 (ULS2S) | 40.9 (ULS3S) | 15.1 / 0.0 | 0.1 | 0.32 | **0.32** | OK |
| K26 | HEA 160 | 4.13 | 52.2 (ULS2W) | 34.3 (ULS3W) | 14.3 / 0.0 | 0.11 | 0.32 | **0.32** | OK |
| K18 | HEA 160 | 3.61 | 54.6 (ULS2S) | 40.4 (ULS3S) | 14.6 / 0.0 | 0.1 | 0.31 | **0.31** | OK |
| other 17 columns | HEA 160 | 2.94-4.13 | <= 57 | <= 52 | <= 15 | <= 0.10 | <= 0.35 | <= 0.35 | OK |

Max column utilisation 0.68 (K25, SW corner: N 50 kN, M_y 14.8 + M_z 12.2 kNm). Wind post WP1 HEA 160, L 4.18 m: M_y 9.2, M_z 9.6 kNm -> 0.47. HEA 140 was run and reaches 1.00 at K25: **HEA 160 confirmed**.

**Purlins Z200x2.0 @ 1.5 m** (basis: M_Rd 12.5 kNm single span, 16 sleeved; I = 3.9e6 mm4; capacity assumed valid for uplift with the free flange braced by the anti-sag bar at mid-span - to be confirmed by the supplier): worst gravity M_Ed = 4.3 kNm, worst uplift M_Ed = **8.6 kNm** (4.07 m span over the north strip of the stair well, x 77.8-81.8, y 35.6, G zone), i.e. 0.68 of the single-span value; elsewhere spans <= 3.1 m give <= 6.5 kNm (0.52). Deflection G + Q on 4.07 m: 6.3 mm < L/150 = 27.1 mm. Single-span cleated purlins are sufficient everywhere (sleeves optional). Girts (same section, wall net pressure 1.5 x 1.1 x 1.3 = 2.15 kN/m2, zone A 2.73 kN/m2 within 2.4 m of a corner): bays <= 5.3 m take 1.5 m rows single-span (M_Ed <= 11.3 kNm); **K5-K7, K25-K19 and K8-K6 (5.7-5.9 m) need 1.2 m rows sleeved (<= 14.2 kNm); K21-K22, K22-K23 and K14-K4 (6.4-7.1 m) need 1.0 m rows sleeved (<= 14.9 kNm, 0.93)**. The girt length in section 10 follows this rule.

## 5. Connections (EN 1993-1-8)

- **Rafter to primary fin plate**, one type: 100 x 150 x 10 S275, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web, 2 x 6 mm fillets. Max rafter end reaction 26.9 kN (envelope ULS-1 / reversed ULS-3): bolt shear incl. eccentricity 0.25, bearing on the 6.6 mm rafter web **0.34** (governs), plate bearing 0.23, plate shear 0.13, plate bending 0.13, weld 0.14, web block tearing 0.24. 9.2 m rafters: 3 bolts, plate 220 (0.14 at 20.4 kN). No copes. T1/T2 and the notch eave beam use the same detail.
- **Primary to column cap plate** 200 x 240 x 20, a = 6 all round, 4 M20 through the primary bottom flange (gauge 90, pitch 140). Tension = roof uplift 65.5 kN (K12, ULS-3N; the bracing vertical component enters below the cap through the gusset): bolt tension 0.12, shear + tension interaction with the chord/strut force 53.1 kN 0.22, IPE 330 flange T-stub 0.17, cap plate 0.06, weld 0.07. Chord continuity across a column (<= 46 kN): 10 mm tie plate between the primary bottom flanges on the lines y 29.3 and y 20.1.
- **Bracing gussets**: 10 mm plates welded to the column web and base plate; each L70x7 with 2 M20 (e1 40, p1 110): angle net section 0.7 A_net f_u/gamma_M2 = 189 kN, bolt shear 188 kN, gusset bearing 2 x 98 kN; max T_Ed 68 kN (B8) -> 0.36 / 0.36 / 0.35.
- **Roof bracing** M20 rods 8.8 with turnbuckles, F_t,Rd 141 kN, to 8 mm gussets on the rafter and primary webs at the bottom flange level; sag ties to the purlins at the crossing and at 3 m centres on the 9.6 m diagonals.
- Trimmers T1 (y 35.37) and T2 (y 24.16) IPE 270 between the rafters x 77.8 / 81.85 carry only the 150 mm upstand (0.3 kN/m, M_Ed 1.8 kNm); upstand framing 100 x 50 x 3 cold-formed C on the trimmers and along the rafters beside the openings, cricket on the south side of the stair well.

## 6. Bases and anchors (EN 1993-1-8 6.2.5, EN 1992-4 with the basis values)

Base plate 300 x 400 x 20 S275 on 40 mm non-shrink grout, 4 M20 resin anchors at 200 x 300, h_ef 170 mm, in the assumed 800 x 800 solid zone (>= 100 mm from its edge in the plate's short direction; **cores to prove the solid zone before drilling**). In each braced bay an **HEA 160 base strut** lies on the slab between the two base plates (bolted to a side gusset on each plate, under the wall base rail), so the bay shear H is shared by the two 4-anchor groups (H/2 each in the table of section 9).

- Bearing: effective area 763 cm2 (c = 60 mm), 10 MPa -> 763 kN; max N_c 90 kN (K22) -> 0.12. Plate under uplift (T-stub cantilever m = 69 mm): 0.08.
- Anchor tension group: cone A_c,N/A_c,N0 = 2.18 (i.e. 0.55 per anchor, edge to the solid zone 250 mm, psi_s 0.99) -> N_Rd,c = **115.8 kN**; bond N_Rd,p = 168.6 kN; steel 4 x 140 kN. Worst uplift 74 kN at K20/K19 (ULS-3S, roof + bracing) -> cone 0.64.
- Anchor shear group: steel 4 x 70 kN, pry-out 231.6 kN, concrete edge failure towards the solid-zone boundary (treated as a free edge, k = 2.4 uncracked, A_c,V limited by the 250 mm slab) V_Rd,c = **48.1 kN**; V = 26.6 kN at K22/K23 (B3) -> 0.55, 20.9 kN at K20 -> 0.44. N-V interaction (exponent 1.5): **0.80 at K20**; all bases <= 0.80 (table in section 9).
- Without the base strut the braced-bay bases would see 51-53 kN shear (1.1 of V_Rd,c) and fail the interaction; without the anchored wall rail a further 13-29 kN. Both details are therefore mandatory.

## 7. Deflections and sway

- Roof members SLS G + Q: worst primary K19-K20 36 mm = L/271 (limit L/200 = 49 mm); 9.2 m rafters 22-24 mm = L/390; 7.5 m rafters L/700-820, all other spans > L/1000. Purlins L/640.
- Sway of the braced bays under SLS wind (elastic diagonal elongation + 2 mm bolt-slip allowance): 2.8-3.9 mm against h/150 = 20.7-28.7 mm (utilisation <= 0.15). Column bending deflection under wall wind (SLS, K22: 9.8 kN/m on 3.88 m) 8.2 mm = h/470. 

## 8. Bracing

Vertical bays (X, single L70x7 per diagonal, tension-only, 8 bays): E-W B1 K1-K2, B2 K5-K7, B3 K22-K23, B4 K25-K26; N-S B5 K15-K19, B6 K14-K18, B7 K20-K27, **B8 K17-K21 (new)**. Max diagonal utilisation 0.36 (B8); L60x6 would also pass, L70x7 kept for stiffness. Bays must stay door-free (alternates: B1 -> K3-K1, B3 -> K21-K22, B5 -> K19-K25, B6 -> K18-K23, B8 -> K11-K17).

Roof-plane bracing: X of M20 rods in 20 rafter bays (full rafter depth, primaries as chords, rafters as posts) forming the horizontal trusses below; the north band shear passes the stair well through the jog panel x 77.8-81.85 / y 24.5-29.3 with the y 29.3 primary as continuous chord (tie plates at K10, K11).

| Roof truss | Wind | Span m | Depth m | Shear V kN | Diagonal T kN (M20 rod, 141) | Chord kN | Post kN | Util. rod |
|---|---|---|---|---|---|---|---|---|
| RT-N-W (N band west, chords y 29.3 / 35.2) | N-S | 9.8 | 5.9 | 22.2 | 24.7 | 9.2 | 22.2 | 0.18 |
| RT-N-E (N band east, chords y 29.3 / 35.7) | N-S | 13.7 | 6.4 | 31.1 | 34.5 | 16.6 | 31.1 | 0.24 |
| RT-S-E (S band east, chords y 20.1 / 29.3) | N-S | 13.7 | 9.2 | 39.4 | 41.5 | 14.7 | 39.4 | 0.29 |
| RT-S-W (S band west, chords y 15.9 / 21.8) | N-S | 9.8 | 5.9 | 29.8 | 33.1 | 12.4 | 29.8 | 0.24 |
| RT-W (west edge, chords x 68.0 / 72.1) | E-W | 19.4 | 4.1 | 38.9 | 81.6 | 45.9 | 38.9 | 0.58 |
| RT-E (east edge, chords x 89.9 / 95.5) | E-W | 15.6 | 5.7 | 53.1 | 101.5 | 36.8 | 53.1 | 0.72 |
| RT-JOG (jog panel x 77.8-81.9, y 24.5-29.3) | N-S | 4.1 | 4.8 | 51.0 | 66.8 | 10.8 | 51.0 | 0.47 |

## 9. Reactions at the column bases (kN; + compression, uplift listed positive in its own column; V from bracing shared by the base strut; V_wall = wall base shear taken by the anchored wall rail)

| Col | x | y | Bay | N_c ULS (case) | N_t ULS (case) | V_x ULS | V_y ULS | N_c SLS | N_t SLS | V_x SLS | V_y SLS | V_wall,x | V_wall,y | Anchor util. (governs) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 87.19 | 35.77 | B1 | 51.1 (ULS2E) | 26.8 (ULS3N) | 13.8 | 0 | 35.9 | 13.0 | 9.2 | 0 | 0.0 | 16.7 | 0.29 (group edge) |
| K2 | 92.48 | 35.77 | B1 | 43.8 (ULS2E) | 27.7 (ULS3E) | 13.8 | 0 | 30.6 | 14.6 | 9.2 | 0 | 0.0 | 13.2 | 0.29 (group edge) |
| K3 | 81.89 | 35.67 | - | 29.4 (ULS1) | 11.1 (ULS3N) | 0 | 0 | 21.1 | 3.1 | 0 | 0 | 0.0 | 14.8 | 0.1 (group cone) |
| K4 | 95.59 | 35.67 | - | 19.1 (ULS1) | 9.2 (ULS3E) | 0 | 0 | 13.8 | 3.0 | 0 | 0 | 13.7 | 6.6 | 0.08 (group cone) |
| K5 | 72.09 | 35.27 | B2 | 55.6 (ULS2E) | 35.4 (ULS3W) | 19.5 | 0 | 38.8 | 18.9 | 13.0 | 0 | 0.0 | 15.6 | 0.43 (N-V interaction) |
| K6 | 67.99 | 35.17 | - | 24.4 (ULS1) | 11.2 (ULS3W) | 0 | 0 | 17.5 | 3.7 | 0 | 0 | 14.6 | 8.7 | 0.1 (group cone) |
| K7 | 77.79 | 35.17 | B2 | 50.0 (ULS2E) | 23.9 (ULS3W) | 19.5 | 0 | 35.0 | 11.3 | 13.0 | 0 | 0.0 | 15.6 | 0.4 (group edge) |
| K8 | 67.99 | 29.37 | - | 30.0 (ULS1) | 18.4 (ULS3W) | 0 | 0 | 21.5 | 8.3 | 0 | 0 | 15.7 | 0.0 | 0.16 (group cone) |
| K9 | 72.09 | 29.27 | - | 57.2 (ULS1) | 50.8 (ULS3N) | 0 | 0 | 40.1 | 29.3 | 0 | 0 | 0.0 | 0.0 | 0.44 (group cone) |
| K10 | 77.89 | 29.27 | - | 42.2 (ULS1) | 32.4 (ULS3N) | 0 | 0 | 29.7 | 17.7 | 0 | 0 | 0.0 | 0.0 | 0.28 (group cone) |
| K11 | 81.78 | 29.27 | - | 43.6 (ULS1) | 33.4 (ULS3N) | 0 | 0 | 30.8 | 18.2 | 0 | 0 | 0.0 | 0.0 | 0.29 (group cone) |
| K12 | 87.19 | 29.27 | - | 70.5 (ULS1) | 65.5 (ULS3N) | 0 | 0 | 49.5 | 38.3 | 0 | 0 | 0.0 | 0.0 | 0.57 (group cone) |
| K13 | 92.48 | 29.27 | - | 55.7 (ULS1) | 51.8 (ULS3N) | 0 | 0 | 39.0 | 30.3 | 0 | 0 | 0.0 | 0.0 | 0.45 (group cone) |
| K14 | 95.48 | 29.27 | B6 | 58.8 (ULS2S) | 40.9 (ULS3S) | 0 | 22.9 | 40.6 | 23.3 | 0 | 15.2 | 20.0 | 0.0 | 0.54 (N-V interaction) |
| K15 | 67.99 | 26.37 | B5 | 47.0 (ULS2S) | 33.2 (ULS3S) | 0 | 19.8 | 32.2 | 19.5 | 0 | 13.2 | 14.3 | 0.0 | 0.42 (N-V interaction) |
| K16 | 77.78 | 24.46 | - | 21.9 (ULS1) | 14.7 (ULS3N) | 0 | 0 | 15.5 | 7.5 | 0 | 0 | 0.0 | 0.0 | 0.13 (group cone) |
| K17 | 81.89 | 24.46 | B8 | 65.2 (ULS2S) | 60.3 (ULS3S) | 0 | 25.5 | 44.4 | 37.7 | 0 | 17.0 | 0.0 | 0.0 | 0.76 (N-V interaction) |
| K18 | 95.59 | 24.46 | B6 | 54.6 (ULS2S) | 40.4 (ULS3S) | 0 | 22.9 | 37.5 | 23.6 | 0 | 15.2 | 17.8 | 0.0 | 0.53 (N-V interaction) |
| K19 | 67.99 | 21.76 | B5 | 89.2 (ULS2S) | 73.8 (ULS3S) | 0 | 19.8 | 62.3 | 42.0 | 0 | 13.2 | 21.3 | 0.0 | 0.77 (N-V interaction) |
| K20 | 77.78 | 21.76 | B7 | 75.7 (ULS2S) | 74.0 (ULS3S) | 0 | 20.9 | 52.6 | 44.2 | 0 | 14.0 | 0.0 | 0.0 | 0.8 (N-V interaction) |
| K21 | 81.79 | 20.07 | B8 | 80.8 (ULS2S) | 60.3 (ULS3S) | 0 | 25.5 | 55.9 | 34.4 | 0 | 17.0 | 0.0 | 22.9 | 0.76 (N-V interaction) |
| K22 | 88.88 | 20.07 | B3 | 90.2 (ULS2E) | 55.2 (ULS3E) | 26.6 | 0 | 63.1 | 29.1 | 17.7 | 0 | 0.0 | 28.5 | 0.74 (N-V interaction) |
| K23 | 95.49 | 20.07 | B3 | 63.6 (ULS2E) | 45.6 (ULS3E) | 26.6 | 0 | 44.1 | 25.5 | 17.7 | 0 | 12.1 | 18.6 | 0.66 (N-V interaction) |
| K24 | 74.89 | 15.97 | - | 23.8 (ULS1) | 15.1 (ULS3S) | 0 | 0 | 17.0 | 6.9 | 0 | 0 | 0.0 | 12.8 | 0.13 (group cone) |
| K25 | 67.99 | 15.87 | B4 | 50.1 (ULS2W) | 34.4 (ULS3W) | 12.5 | 0 | 34.8 | 18.7 | 8.4 | 0 | 18.3 | 11.8 | 0.3 (group cone) |
| K26 | 71.99 | 15.87 | B4 | 52.2 (ULS2W) | 34.3 (ULS3W) | 12.5 | 0 | 36.1 | 19.1 | 8.4 | 0 | 0.0 | 15.3 | 0.3 (group cone) |
| K27 | 77.78 | 15.87 | B7 | 47.3 (ULS2S) | 34.7 (ULS3S) | 0 | 20.9 | 32.6 | 19.8 | 0 | 14.0 | 13.2 | 8.8 | 0.45 (N-V interaction) |

## 10. Weight and section list

| Item | Section | Length m | Weight t |
|---|---|---|---|
| Rafters / edge beams / trimmers | IPE 270 | 205.0 | 7.40 |
| Primaries / eave beams | IPE 330 | 92.5 | 4.54 |
| Columns (27) + wind post WP1 | HEA 160 | 98.2 | 2.98 |
| Base struts in the 8 braced bays | HEA 160 | 41.3 | 1.26 |
| Plates, fin/cap/base plates, bolts (10 %) | S275 | - | 1.62 |
| **Hot-rolled total** | | | **17.8** |
| Wall bracing, 8 bays x 2 diagonals | L 70x7 | 102.7 | 0.76 |
| Roof bracing, 20 panels x 2 diagonals | M20 rods 8.8 | 298.1 | 0.74 |
| Purlins 372 m + girts 359 m | Z 200x2.0 S350GD | 731 | 4.31 |
| **Total** | | | **23.6** (49 kg/m2 of footprint 486 m2, 53 kg/m2 of roofed 446 m2) |

Sections: **IPE 330** (all E-W primaries and eave beams on the column rows, 92.5 m), **IPE 270** (rafters, edge beams, trimmers, 205 m), **HEA 160** (27 columns, WP1, base struts), plus L70x7 wall bracing, M20 rod roof bracing, Z200x2.0 purlins/girts. Three hot-rolled sections as in the scheme; the weight is 23.6 t against the scheme's 20.5 t (added rafter line +0.7 t, base struts +1.3 t, 10 % plates instead of 1.5 t, full girt count).

## 11. Open items / risks

1. **Slab solid zones**: the anchor group results assume an 800 x 800 solid zone at every column head and treat its boundary as a free edge for shear (V_Rd,c 48 kN). Core 3-4 column heads before final design; a larger zone or a drop beam lowers the utilisations, a smaller one means supplier-verified anchors or a second bay on the same line for the braced-bay bases. EN 1992-4 group verification with the supplier software remains open (basis).
2. Wind coefficients: the roof zones were enveloped (theta = 180 values for both N and S); local wind speed and the city are unconfirmed - a 10 % higher q_p raises uplift utilisations proportionally (anchor cone at K20 -> 0.72).
3. Purlin uplift capacity with the free flange in compression (Z200x2.0, 8.6 kNm required on the 4.07 m strip, 6.5 kNm elsewhere) and the girt capacity on the 7.1 m bay (sleeved) to be confirmed with the purlin supplier's tables.
4. Wall base rail anchorage to the slab (M10 @ 600) and the BoardX product data (0.30 kN/m2, girt rows per section 4) to be confirmed; otherwise add V_wall to the column bases.
5. Door-free braced bays B1-B8 to be confirmed by the client; B8 lies along the elevator shaft east wall inside the hall (hidden by the shaft enclosure if the lift stops at the slab).
6. Temperature: slotted holes in the fin plates on the y 29.3 line (27.8 m) and at the base struts.
7. Ponding: the 6 % slope and L/271 deflection give no risk; the cricket on the south side of the stair well must keep the 6 % fall to the trimmer.

Files: `design_report_C.md` (this), `members_C.csv` (96 rows: spans, columns, bracing), `reactions_C.csv`, `framing_C.png`, `calc/` (sections.py, model.py, loads.py, statics.py, takedown.py, bracing.py, members.py, connections.py, run_all.py, write_report.py, summary_C.json).

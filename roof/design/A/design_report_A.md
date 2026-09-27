# Alternative A - mono-pitch portal frames: steel design report (Rev 1 scheme, calculated)

Project: steel and sandwich-panel roof over the existing restaurant slab. Basis: `roof/brief.md` (incl. Revision 1), `roof/design/load_basis.md` (binding), `roof/geometry.json`, scheme `roof/systems/A_portal.md`. Codes EN 1990 / 1991-1-4 / 1993-1-1 / 1993-1-8 / 1992-4. Units kN, m, kNm. All numbers below come from the scripts in `calc/` (`python3 calc/run_all.py` re-runs everything in about 1 minute).

**Result in one line:** the scheme works with ONE rafter section (IPE 300, 1.3 m haunches at every column), ONE column section (HEA 200 for all 27 columns incl. both eave posts), IPE 200 for all secondary members (eaves beams, trimmers, wind posts), the IPE 300 transfer girder, CHS 76.3x3.2 roof bracing and M20 rods in nine wall bays. Governing utilisations: rafter 0.66, column 0.70, knee connection 0.90, girder 0.75, purlin 0.67, anchors 0.87 (with 300 mm deep anchors), sway h/177, deflection L/339. Total steel 18.9 t (38.9 kg/m2 of footprint).

## 1. Basis and assumptions

- Geometry as scheme A Rev 1: 7 portal frames spanning N-S on x = 68.0 / 72.1 / 77.8 / 81.85 / 87.2 / 92.5 / 95.55; single roof plane TOS = 3.45 + 0.06 (35.87 - y), rafter centreline 150 mm below TOS; column lengths 3.31 m (K1/K2) to 4.50 m (K25-K27). F1/F3 rafters y 15.57-35.87, F4/F7 y 19.97-35.87, F5/F6 propped at y 20.07 on the transfer girder K21-K22-K23. The stair and elevator openings carry no roof load; their strips are removed from F3/F4 and trimmed by IPE 200 at y 20.17, 24.16, 29.37, 35.37.
- System: rigid frames in plane (bolted haunched end plates at every column, column passing through at internal columns), pinned bases, E-W stability by vertical X-bracing in wall bays plus roof X-bracing; column tops held by the eaves beams / purlin line.
- Haunches: stepped section 1.5 h = 450 mm over 1.3 m each side of the column centreline (cutting from the same IPE 300); one-sided in bays < 3.5 m (K15-K8, K20-K16).
- F5/F6 prop modelled as a vertical spring (7560 kN/m at x 87.2, 3980 kN/m at x 92.5 from the 2-span IPE 300 girder) and as a rigid pin; checks use the envelope.
- Materials, factors, bolt, purlin and anchor values exactly as `load_basis.md`. One deviation: anchor embedment 300 mm into the solid column head instead of 170 mm (section 6 reports both).
- Section properties hard-coded from the European tables (`calc/sections.py`). Analysis with the 2D stiffness solver `calc/frame2d.py` (consistent geometric stiffness for alpha_cr), cross-checked against PyNiteFEA 3.2 on F2 (`calc/pynite_check.py`: peak moment 140.63 vs 140.63 kNm, reactions and sway identical).
- Second order: alpha_cr by eigenvalue for every ULS combination, cross-checked with the H/V formula; all > 10, so no amplification (the script would apply 1/(1 - 1/alpha_cr) to the horizontal loads otherwise). EHF phi V (phi = alpha_h alpha_m / 200, 0.0041 for F2) in every ULS combination.
- Buckling lengths: columns L_cr,y = L_cr,z = column length (non-sway, top held); rafter top flange held by purlins at 1.5 m, bottom flange by fly braces at 3.0 m and at every haunch tip and column line.

## 2. Loads and combinations

Surface loads (kN/m2): roof G = 0.12 + 0.05 + 0.20 = 0.37 (G_min = 0.17); rafter self-weight 0.414 kN/m x 1.10 for plates (0.65 kN/m in the haunch); Q_k = 0.60 (psi_0 = 0); wall 0.30 kN/m2 on perimeter columns (H_wall = TOS + 0.20 m); upstand 0.3 kN/m at opening edges; q_p = 1.30 kN/m2.

Tributary widths (m): F1 2.16, F2 4.90, F3 2.85 (+2.025 only outside the openings), F4 2.675 (+2.025 idem), F5 5.325, F6 4.175, F7 1.665. Line loads on F2 (kN/m): G 2.27, Q 2.94, wind N zone H with c_pi +0.2 = -(0.8 + 0.2) x 1.30 x 4.90 = -6.37; ULS-1 = 7.47 down, ULS-3 = 1.29 - 9.55 = -8.26 up: uplift governs the F2 rafter and the K9 knee.

Roof c_pe (e = 12 m, F/G strip 1.2 m from the windward eave, H beyond): from N -2.3/-1.3/-0.8, from S -1.7/-1.2/-0.6 or 0.0, along the ridge -1.3 (F1, F7, area-weighted G/H), -0.6 (F2, F6), -0.5 (F3-F5); F/G values kept for purlins, eaves members and trimmers (net up to -3.3 kN/m2). c_pi +0.2 and -0.3. Walls: +0.8 / -0.5 / side -0.8, net 1.43 / -0.26 kN/m2 (c_pi -0.3) and 0.78 / -0.91 (c_pi +0.2), as UDLs over the column height with wall tributaries 2.1-5.3 m; for F5/F6 the south-wall wind enters at the propped end via the wind posts. Gable walls load the F1/F7 columns about the weak axis (M_z = w h^2/8, 24 kNm at K19) and the bracing (146 kN characteristic on 86 m2, 73 kN at roof level).

Combinations per frame: ULS-1 1.35 G + 1.5 Q (EHF both ways); ULS-2 1.35 G + 1.5 W, c_pi -0.3, wind from N, S, S with zero roof pressure (max sway), along the ridge; ULS-3 G_min + 1.5 W, c_pi +0.2, from N, S, along the ridge; SLS G + Q, Q, G + W (four cases). Seismic check-only (section 8).

## 3. Analysis model and results per frame

Model: rafter elements <= 0.4 m long along the slope, 4 elements per column, pinned supports, spring/pin at the girder for F5/F6, all loads as element UDLs or column-top point loads. `frames_A.png` shows the seven frames with the ULS-1 (red) and ULS-3 wind-N (blue) moment diagrams.

| Frame | rafter | columns | alpha_cr ULS-1 | alpha_cr min (combo) | alpha_cr H/V | M_sag max (kNm) | M_hog max at column face (kNm) | V max (kN) | N rafter (kN) | col M_top max (kNm) | col N max (kN) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | IPE300 | HEA 200 | 50.2 | 50.2 (ULS1+) | 58.2 | 20 | -16 | 17 | -12 / +13 | 15 | 37 |
| F2 | IPE300 | HEA 200 | 20.6 | 20.6 (ULS1+) | 24.0 | 163 | -141 | 63 | -28 / +31 | 80 | 99 |
| F3 | IPE300 | HEA 200 | 42.7 | 42.7 (ULS1+) | 49.6 | 30 | -24 | 25 | -15 / +17 | 21 | 43 |
| F4 | IPE300 | HEA 200 | 43.0 | 43.0 (ULS1+) | 49.8 | 34 | -33 | 26 | -22 / +23 | 33 | 41 |
| F5 | IPE300 | HEA 200 | 25.2 | 25.2 (ULS1+) | 29.3 | 99 | -78 | 52 | -20 / +18 | 41 | 87 |
| F6 | IPE300 | HEA 200 | 31.1 | 31.1 (ULS1+) | 36.1 | 80 | -64 | 40 | -18 / +17 | 36 | 70 |
| F7 | IPE300 | HEA 200 | 59.3 | 59.3 (ULS1+) | 68.1 | 17 | -14 | 14 | -8 / +9 | 13 | 32 |

Key points: F2 (13.4 m bay) governs everything: 163 kNm sagging at the K9 face under uplift, 141 kNm hogging under ULS-1, column K9 top moment 80 kNm, 99 kN compression / 96 kN uplift at K9. F5/F6 propped bays: 99 / 80 kNm, girder reactions 29 kN down (ULS-1) and 33 kN up (ULS-3) at x 87.2. Frames F1, F3, F4, F7 (bays <= 6.4 m) stay below 35 kNm. alpha_cr (eigenvalue) is 20.6 at worst (F2, ULS-1); the H/V method gives 24.0, i.e. the simplified formula is 15 % less conservative here, and both confirm that second-order sway is negligible (amplification would be 1.05).

Moments at every column face (design values for the knee connections; both signs occur, uplift governs on K9, K12, K13):

| column | M hog (combo) | M sag (combo) | V (kN) | dM panel (kNm) |
|---|---|---|---|---|
| K25 | 4 (ULS2_N) | 10 (ULS3_R) | 14 | 10 |
| K19 | 15 (ULS1+) | 19 (ULS3_R) | 17 | 10 |
| K15 | 7 (ULS2_S0) | 6 (ULS3_N) | 9 | 11 |
| K8 | 11 (ULS1-) | 14 (ULS3_S) | 15 | 12 |
| K6 | 14 (ULS2_S0) | 13 (ULS3_N) | 15 | 14 |
| K26 | 52 (ULS1-) | 54 (ULS3_R) | 46 | 54 |
| K9 | 136 (ULS1+) | 157 (ULS3_N) | 63 | 77 |
| K5 | 36 (ULS2_S0) | 34 (ULS3_N) | 18 | 35 |
| K27 | 10 (ULS2_N) | 13 (ULS3_R) | 12 | 13 |
| K20 | 17 (ULS1+) | 21 (ULS3_N) | 17 | 16 |
| K16 | 8 (ULS2_S0) | 13 (ULS3_S) | 15 | 16 |
| K10 | 22 (ULS1-) | 28 (ULS3_N) | 25 | 20 |
| K7 | 13 (ULS2_S0) | 14 (ULS3_N) | 14 | 12 |
| K21 | 14 (ULS2_N) | 13 (ULS3_R) | 12 | 14 |
| K17 | 19 (ULS2_S0) | 22 (ULS3_N) | 18 | 25 |
| K11 | 28 (ULS2_S0) | 32 (ULS3_S) | 25 | 30 |
| K3 | 31 (ULS2_S0) | 25 (ULS3_N) | 19 | 31 |
| K12 | 74 (ULS1+) | 95 (ULS3_S) | 51 | 40 |
| K1 | 40 (ULS3_S) | 34 (ULS2_N) | 31 | 40 |
| K13 | 60 (ULS1+) | 77 (ULS3_S) | 39 | 34 |
| K2 | 34 (ULS3_S) | 28 (ULS2_N) | 25 | 34 |
| K23 | 5 (ULS2_N) | 6 (ULS3_R) | 8 | 6 |
| K18 | 8 (ULS2_S0) | 8 (ULS3_S) | 8 | 9 |
| K14 | 13 (ULS2_S0) | 15 (ULS3_R) | 14 | 11 |
| K4 | 13 (ULS2_S0) | 10 (ULS3_N) | 12 | 13 |

## 4. Member checks

Checks to EN 1993-1-1 (`calc/checks_members.py`): class (Table 5.2 with the actual N/M), 6.2.9 M + N (N < 0.25 N_pl everywhere, M_pl governs), shear (V < 0.5 V_pl,Rd), haunch as class-3 elastic section (M_el = 247 kNm) at the column face, LTB 6.3.2.3 (curve b, C1 from the end-moment ratio of each segment between bottom-flange restraints, 1.13 with the peak inside) and 6.3.3 with Annex B factors (C_my 0.9 for wall-loaded, 0.6 for internal columns). E/W-wall columns include the out-of-plane wind moment and the bracing vertical (30 kN) in the along-ridge combinations. All sections class 1.

| member | section | L (m) | N_Ed (kN) | M_Ed (kNm) | Mz (kNm) | V_Ed (kN) | class | M+N 6.2.9 | shear | haunch Mel | buckling 6.3.3 | LTB | u | governing (combo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K25 (F1) | HEA200 | 4.50 | 32 | 5 | 18 | 6 | 1 | 0.36 | 0.02 | - | 0.39 | - | **0.39** | 6.3.3 (6.62) (ULS2_R) |
| K19 (F1) | HEA200 | 4.15 | 0 | 1 | 24 | 0 | 1 | 0.44 | 0.00 | - | 0.40 | - | **0.44** | 6.2.9 M+N (ULS2_R) |
| K15 (F1) | HEA200 | 3.87 | 3 | 1 | 15 | 0 | 1 | 0.28 | 0.00 | - | 0.26 | - | **0.28** | 6.2.9 M+N (ULS2_R) |
| K8 (F1) | HEA200 | 3.69 | 0 | 0 | 16 | 0 | 1 | 0.29 | 0.00 | - | 0.26 | - | **0.29** | 6.2.9 M+N (ULS2_R) |
| K6 (F1) | HEA200 | 3.34 | 28 | 6 | 11 | 5 | 1 | 0.24 | 0.02 | - | 0.25 | - | **0.25** | 6.3.3 (6.62) (ULS2_R) |
| F1 rafter bay 1 | IPE300 + haunch | 5.89 | 0 | 8 | - | 17 | 1 | 0.05 | 0.04 | 0.08 | - | 0.06 (L 3.0, C1 1.13, chi 0.83) | **0.08** | haunch Mel (ULS3_R) |
| F1 rafter bay 2 | IPE300 + haunch | 4.61 | 0 | 4 | - | 17 | 1 | 0.02 | 0.04 | 0.08 | - | 0.02 (L 2.0, C1 1.13, chi 0.94) | **0.08** | haunch Mel (ULS3_R) |
| F1 rafter bay 3 | IPE300 + haunch | 3.00 | 0 | 13 | - | 16 | 1 | 0.08 | 0.04 | 0.06 | - | 0.00 (L 0.0, C1 1.00, chi 1.00) | **0.08** | 6.2.9 M+N (ULS3_R) |
| F1 rafter bay 4 | IPE300 + haunch | 5.80 | 0 | 13 | - | 16 | 1 | 0.08 | 0.04 | 0.06 | - | 0.07 (L 3.0, C1 1.13, chi 0.83) | **0.08** | 6.2.9 M+N (ULS3_R) |
| F1 rafter cant N | IPE300 + haunch | 0.70 | 4 | 15 | - | 11 | 1 | 0.00 | 0.03 | 0.06 | - | 0.08 (L 0.7, C1 1.88, chi 1.00) | **0.08** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| K26 (F2) | HEA200 | 4.50 | 55 | 56 | 0 | 12 | 1 | 0.47 | 0.04 | - | 0.57 | - | **0.57** | 6.3.3 (6.62) (ULS1-) |
| K9 (F2) | HEA200 | 3.70 | 0 | 80 | 0 | 22 | 1 | 0.68 | 0.08 | - | 0.70 | - | **0.70** | 6.3.3 (6.62) (ULS3_N) |
| K5 (F2) | HEA200 | 3.34 | 30 | 37 | 0 | 14 | 1 | 0.31 | 0.05 | - | 0.35 | - | **0.35** | 6.3.3 (6.62) (ULS2_S0) |
| F2 rafter bay 1 | IPE300 + haunch | 13.40 | 1 | 87 | - | 63 | 1 | 0.50 | 0.16 | 0.66 | - | 0.58 (L 3.0, C1 1.13, chi 0.83) | **0.66** | haunch Mel (ULS3_N) |
| F2 rafter bay 2 | IPE300 + haunch | 6.00 | 1 | 47 | - | 63 | 1 | 0.27 | 0.16 | 0.66 | - | 0.00 (L 0.0, C1 1.00, chi 1.00) | **0.66** | haunch Mel (ULS3_N) |
| F2 rafter cant N | IPE300 + haunch | 0.60 | 9 | 38 | - | 16 | 1 | 0.01 | 0.04 | 0.16 | - | 0.18 (L 0.6, C1 1.88, chi 1.00) | **0.18** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| K27 (F3) | HEA200 | 4.50 | 38 | 5 | 11 | 5 | 1 | 0.25 | 0.02 | - | 0.29 | - | **0.29** | 6.3.3 (6.62) (ULS2_R) |
| K20 (F3) | HEA200 | 4.15 | 3 | 17 | 0 | 4 | 1 | 0.14 | 0.01 | - | 0.16 | - | **0.16** | 6.3.3 (6.62) (ULS2_N) |
| K16 (F3) | HEA200 | 3.98 | 0 | 17 | 0 | 4 | 1 | 0.14 | 0.01 | - | 0.15 | - | **0.15** | 6.3.3 (6.62) (ULS2_N) |
| K10 (F3) | HEA200 | 3.70 | 0 | 21 | 0 | 6 | 1 | 0.17 | 0.02 | - | 0.18 | - | **0.18** | 6.3.3 (6.62) (ULS2_N) |
| K7 (F3) | HEA200 | 3.34 | 1 | 20 | 0 | 20 | 1 | 0.17 | 0.07 | - | 0.17 | - | **0.17** | 6.3.3 (6.62) (ULS2_N) |
| F3 rafter bay 1 | IPE300 + haunch | 5.89 | 0 | 11 | - | 18 | 1 | 0.06 | 0.04 | 0.09 | - | 0.08 (L 3.0, C1 1.13, chi 0.83) | **0.09** | haunch Mel (ULS3_N) |
| F3 rafter bay 2 | IPE300 + haunch | 2.70 | 2 | 12 | - | 18 | 1 | 0.07 | 0.04 | 0.09 | - | 0.00 (L 0.0, C1 1.00, chi 1.00) | **0.09** | haunch Mel (ULS3_N) |
| F3 rafter bay 3 | IPE300 + haunch | 4.81 | 7 | 12 | - | 25 | 1 | 0.07 | 0.06 | 0.13 | - | 0.07 (L 2.2, C1 1.13, chi 0.92) | **0.13** | haunch Mel (ULS3_N) |
| F3 rafter bay 4 | IPE300 + haunch | 5.90 | 7 | 5 | - | 25 | 1 | 0.03 | 0.06 | 0.13 | - | 0.04 (L 3.0, C1 1.13, chi 0.83) | **0.13** | haunch Mel (ULS3_N) |
| F3 rafter cant N | IPE300 + haunch | 0.70 | 1 | 14 | - | 13 | 1 | 0.01 | 0.03 | 0.06 | - | 0.07 (L 0.7, C1 1.88, chi 1.00) | **0.07** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| K21 (F4) | HEA200 | 4.25 | 15 | 23 | 0 | 22 | 1 | 0.20 | 0.08 | - | 0.23 | - | **0.23** | 6.3.3 (6.62) (ULS2_S0) |
| K17 (F4) | HEA200 | 3.98 | 24 | 25 | 0 | 6 | 1 | 0.21 | 0.02 | - | 0.25 | - | **0.25** | 6.3.3 (6.62) (ULS2_S0) |
| K11 (F4) | HEA200 | 3.70 | 32 | 30 | 0 | 8 | 1 | 0.25 | 0.03 | - | 0.29 | - | **0.29** | 6.3.3 (6.62) (ULS2_S0) |
| K3 (F4) | HEA200 | 3.31 | 29 | 33 | 0 | 13 | 1 | 0.28 | 0.04 | - | 0.31 | - | **0.31** | 6.3.3 (6.62) (ULS2_S0) |
| F4 rafter bay 1 | IPE300 + haunch | 4.39 | 22 | 21 | - | 15 | 1 | 0.03 | 0.04 | 0.09 | - | 0.10 (L 1.3, C1 1.52, chi 1.00) | **0.10** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| F4 rafter bay 2 | IPE300 + haunch | 4.81 | 9 | 5 | - | 19 | 1 | 0.03 | 0.05 | 0.14 | - | 0.04 (L 2.2, C1 1.13, chi 0.92) | **0.14** | haunch Mel (ULS3_S) |
| F4 rafter bay 3 | IPE300 + haunch | 6.40 | 16 | 33 | - | 21 | 1 | 0.07 | 0.05 | 0.14 | - | 0.14 (L 1.3, C1 1.41, chi 1.00) | **0.14** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| K12 (F5) | HEA200 | 3.70 | 59 | 39 | 0 | 11 | 1 | 0.33 | 0.04 | - | 0.40 | - | **0.40** | 6.3.3 (6.62) (ULS2_S0) |
| K1 (F5) | HEA200 | 3.31 | 22 | 38 | 0 | 15 | 1 | 0.32 | 0.05 | - | 0.35 | - | **0.35** | 6.3.3 (6.62) (ULS2_S) |
| F5 rafter bay 1 | IPE300 + haunch | 9.20 | 2 | 92 | - | 52 | 1 | 0.54 | 0.13 | 0.21 | - | 0.39 (L 3.0, C1 1.13, chi 0.83) | **0.54** | 6.2.9 M+N (ULS3_N) |
| F5 rafter bay 2 | IPE300 + haunch | 6.50 | 2 | 92 | - | 52 | 1 | 0.54 | 0.13 | 0.21 | - | 0.05 (L 3.0, C1 1.13, chi 0.83) | **0.54** | 6.2.9 M+N (ULS3_N) |
| K13 (F6) | HEA200 | 3.70 | 48 | 35 | 0 | 10 | 1 | 0.30 | 0.03 | - | 0.36 | - | **0.36** | 6.3.3 (6.62) (ULS2_S0) |
| K2 (F6) | HEA200 | 3.31 | 20 | 34 | 0 | 13 | 1 | 0.29 | 0.05 | - | 0.32 | - | **0.32** | 6.3.3 (6.62) (ULS2_S) |
| F6 rafter bay 1 | IPE300 + haunch | 9.20 | 1 | 73 | - | 40 | 1 | 0.42 | 0.10 | 0.15 | - | 0.29 (L 3.0, C1 1.13, chi 0.83) | **0.42** | 6.2.9 M+N (ULS3_N) |
| F6 rafter bay 2 | IPE300 + haunch | 6.50 | 1 | 73 | - | 40 | 1 | 0.42 | 0.10 | 0.15 | - | 0.03 (L 3.0, C1 1.13, chi 0.83) | **0.42** | 6.2.9 M+N (ULS3_N) |
| K23 (F7) | HEA200 | 4.25 | 34 | 3 | 13 | 4 | 1 | 0.26 | 0.01 | - | 0.29 | - | **0.29** | 6.3.3 (6.62) (ULS2_R) |
| K18 (F7) | HEA200 | 3.98 | 4 | 1 | 20 | 0 | 1 | 0.36 | 0.00 | - | 0.33 | - | **0.36** | 6.2.9 M+N (ULS2_R) |
| K14 (F7) | HEA200 | 3.70 | 1 | 0 | 21 | 0 | 1 | 0.37 | 0.00 | - | 0.33 | - | **0.37** | 6.2.9 M+N (ULS2_R) |
| K4 (F7) | HEA200 | 3.31 | 1 | 4 | 10 | 4 | 1 | 0.22 | 0.01 | - | 0.20 | - | **0.22** | 6.2.9 M+N (ULS2_R) |
| F7 rafter bay 1 | IPE300 + haunch | 4.39 | 8 | 9 | - | 8 | 1 | 0.01 | 0.02 | 0.04 | - | 0.04 (L 1.3, C1 1.72, chi 1.00) | **0.04** | LTB 6.3.2/6.3.3 (ULS2_S0) |
| F7 rafter bay 2 | IPE300 + haunch | 4.81 | 0 | 4 | - | 14 | 1 | 0.02 | 0.03 | 0.07 | - | 0.01 (L 2.2, C1 1.13, chi 0.92) | **0.07** | haunch Mel (ULS3_R) |
| F7 rafter bay 3 | IPE300 + haunch | 6.40 | 0 | 8 | - | 14 | 1 | 0.05 | 0.03 | 0.07 | - | 0.06 (L 3.0, C1 1.13, chi 0.83) | **0.07** | haunch Mel (ULS3_R) |

Secondary members (`calc/checks_secondary.py`):

| member | section | L (m) | N (kN) | M (kNm) | V (kN) | u | governing |
|---|---|---|---|---|---|---|---|
| purlin F1-F2 | Z200x2.0 S350GD | 4.10 | 0 | 8.4 | 0 | **0.67** | uplift edge purlin |
| purlin F2-F3 | Z200x2.0 S350GD | 5.70 | 0 | 10.1 | 0 | **0.63** | uplift edge purlin |
| purlin F3-F4 | Z200x2.0 S350GD | 4.05 | 0 | 5.1 | 0 | **0.32** | uplift edge purlin |
| purlin F4-F5 | Z200x2.0 S350GD | 5.35 | 0 | 8.9 | 0 | **0.56** | uplift edge purlin |
| purlin F5-F6 | Z200x2.0 S350GD | 5.30 | 0 | 8.7 | 0 | **0.55** | uplift edge purlin |
| purlin F6-F7 | Z200x2.0 S350GD | 3.05 | 0 | 4.6 | 0 | **0.37** | uplift edge purlin |
| eaves beam N K6-K5 | IPE200 | 4.10 | 0 | 8.9 | 9 | **0.33** | uplift LTB + strut |
| eaves beam N K5-K7 | IPE200 | 5.70 | 28 | 10.1 | 7 | **0.69** | uplift LTB + strut |
| eaves beam N K7-K3 | IPE200 | 4.10 | 0 | 8.9 | 9 | **0.33** | uplift LTB + strut |
| eaves beam N K3-K1 | IPE200 | 5.30 | 28 | 8.7 | 7 | **0.62** | uplift LTB + strut |
| eaves beam N K1-K2 | IPE200 | 5.30 | 28 | 8.7 | 7 | **0.62** | uplift LTB + strut |
| eaves beam N K2-K4 | IPE200 | 3.05 | 0 | 4.9 | 6 | **0.26** | uplift LTB + strut |
| eaves beam S K25-K26 | IPE200 | 4.00 | 18 | 6.4 | 6 | **0.45** | uplift LTB + strut |
| eaves beam S K26-K24 | IPE200 | 2.90 | 18 | 3.3 | 5 | **0.35** | uplift LTB + strut |
| eaves beam S K24-K27 | IPE200 | 2.90 | 18 | 3.3 | 5 | **0.35** | uplift LTB + strut |
| transfer girder K21-K22-K23 (+hanger to F3) | IPE300 | 17.70 | 0 | 48.4 | 41 | **0.75** | LTB (L 5.4 m) + weak-axis wind (eaves ties @ 2 m) |
| trimmer y=20.17 | IPE200 | 4.05 | 0 | 7.4 | 7 | **0.21** | uplift LTB (L 4.05 m) |
| trimmer y=24.16 | IPE200 | 4.05 | 0 | 7.4 | 7 | **0.21** | uplift LTB (L 4.05 m) |
| trimmer y=29.37 | IPE200 | 4.05 | 0 | 7.4 | 7 | **0.21** | uplift LTB (L 4.05 m) |
| trimmer y=35.37 | IPE200 | 4.05 | 0 | 7.4 | 7 | **0.21** | uplift LTB (L 4.05 m) |
| wind post x=77.89 (notch corner) | IPE200 | 4.40 | 0 | 10.1 | 9 | **0.31** | wind bending (pinned-pinned) |
| wind post x=87.2 | IPE200 | 4.60 | 0 | 20.1 | 18 | **0.64** | wind bending (pinned-pinned) |
| wind post x=92.5 | IPE200 | 4.60 | 0 | 18.7 | 16 | **0.60** | wind bending (pinned-pinned) |
| eave post K24 | HEA200 | 4.60 | 12 | 16.5 | 14 | **0.18** | wind bending (pinned-pinned) |
| eave post K22 | HEA200 | 4.60 | 52 | 15.0 | 13 | **0.22** | wind bending (pinned-pinned) |
| wall bracing K6-K5 | rod M20 8.8 (X) | 5.36 | 36 | 0.0 | 0 | **0.25** | tension rod |
| wall bracing K5-K7 | rod M20 8.8 (X) | 6.67 | 32 | 0.0 | 0 | **0.23** | tension rod |
| wall bracing K25-K26 | rod M20 8.8 (X) | 6.13 | 28 | 0.0 | 0 | **0.20** | tension rod |
| wall bracing K26-K24 | rod M20 8.8 (X) | 5.48 | 35 | 0.0 | 0 | **0.24** | tension rod |
| wall bracing K24-K27 | rod M20 8.8 (X) | 5.48 | 35 | 0.0 | 0 | **0.24** | tension rod |
| wall bracing K3-K1 | rod M20 8.8 (X) | 6.33 | 33 | 0.0 | 0 | **0.23** | tension rod |
| wall bracing K1-K2 | rod M20 8.8 (X) | 6.32 | 33 | 0.0 | 0 | **0.23** | tension rod |
| wall bracing K21-K22 | rod M20 8.8 (X) | 8.34 | 32 | 0.0 | 0 | **0.23** | tension rod |
| wall bracing K22-K23 | rod M20 8.8 (X) | 7.94 | 33 | 0.0 | 0 | **0.23** | tension rod |
| roof bracing W bay 68.0-72.1 | CHS 76.3x3.2 | 7.18 | 96 | 0.0 | 0 | **0.48** | tension-only diagonal |
| roof bracing E bay 92.5-95.55 | CHS 76.3x3.2 | 7.09 | 127 | 0.0 | 0 | **0.63** | tension-only diagonal |
| roof bracing E bay 81.85-87.2 (diaphragm tie) | CHS 76.3x3.2 | 8.34 | 43 | 0.0 | 0 | **0.21** | tension-only diagonal |
| roof bracing mid panel 77.8-81.85 (y 24.2-29.3) | CHS 76.3x3.2 | 6.59 | 22 | 0.0 | 0 | **0.11** | tension-only diagonal |

Purlins Z200x2.0 @ 1.5 m, sleeved (M_Rd 16 kNm, wL^2/10), single-span gable bays (12.5 kNm): gravity 2.10 kN/m -> 6.8 kNm on 5.7 m; zone-H uplift 2.67 kN/m -> 8.7 kNm; first purlin from an eave (0.45 m in the F/G strip) 10.1 kNm on 5.7 m, 8.4 kNm on the 4.1 m gable bay: 0.67. Deflection 14.7 mm < L/150 = 38 mm. One row of sag bars per bay > 4.5 m; the supplier's uplift capacity must cover the free-flange compression. Fly braces (angle 50x5 from purlin web to rafter bottom flange) at every second purlin (3.0 m) and at each haunch tip; restraint force 2.5 % of the flange force = 12 kN at K9.

Eaves beams IPE 200: uplift 8.7-10.1 kNm with the bottom flange held at 2.0 m by eaves ties to the first purlin, plus the bracing strut force along the eave (27.5 kN on K5-K7, K3-K1, K1-K2): 0.69. Trimmers IPE 200 (4.05 m): 7.4 kNm under -3.3 kN/m2, 0.21. Wind posts IPE 200 at the notch corner, x 87.2 and x 92.5 (pinned, slotted top so they carry no roof load): 0.64, 7.3 mm < h/150. Eave posts K24/K22 HEA 200: 0.22 incl. the 52 kN girder reaction on K22.

Transfer girder IPE 300, 3-span continuous 77.8 (hanger on the F3 rafter) - K21 - K22 - K23 (3.99 / 7.09 / 6.61 m): M = 30 / -37 kNm (ULS-1), 48 / -37 kNm (ULS-3), V = 41 kN; M_b,Rd = 99 kNm with the compression flange held only at supports and rafter connections (L 5.41 m, lambda_LT 1.10); weak-axis 9 kNm with eaves ties at 2 m: 0.75. Deflection G + Q 3.1 mm (limit 35). Reactions K21 14 / -25, K22 52 / -70, K23 12 / -17 kN (gravity / uplift ULS), hanger on F3 0.5 / -2.3 kN.

## 5. Connections

Knee / column connection, one detail for all 27 columns (`calc/checks_connections.py`, EN 1993-1-8 component method, individual bolt rows with the column-flange group limit): the 450 mm haunched rafter end is bolted with a symmetric extended end plate 200 x 680 x 20 S275 to the HEA 200 flange, 12 x M20 8.8 in two lines at gauge 100, rows at -45 / 55 / 155 / 295 / 395 / 495 mm from the rafter top; two pairs of column stiffeners 95 x 10 at the rafter top-flange and haunch bottom-flange levels; welds flange 8 mm, web 5 mm double fillet.

- Row resistances: extension row 173 kN (column flange mode 1 next to the stiffener; plate 225, bolts 282), row adjacent to the flange 173 kN, inner row 163 kN limited by the two-row group on the column flange (248 kN) to 75 kN. Compression: haunch flange + web 562 kN, stiffened column web 880 kN.
- M_j,Rd = 173 x 0.490 + 173 x 0.390 + 75 x 0.290 = 174 kNm hogging and, by symmetry, 174 kNm sagging. M_Ed at the column face: 136 kNm hogging (K9, ULS-1) -> 0.78; 157 kNm sagging (K9, ULS-3 uplift) -> 0.90; all other knees < 95 kNm (0.55).
- Column web panel: V_wp,Ed = (M_left - M_right)/z = 77 / 0.44 = 175 kN at K9 vs V_wp,Rd = 0.9 f_y A_vc / sqrt 3 = 258 kN -> 0.68. Vertical shear 63 kN on the four compression-side bolts: 0.17. The stiffened joint is taken as rigid.
- Rafter-to-girder pin (F5/F6): 12 mm rafter end plate on a 10 mm vertical T-stiffener welded to the girder top flange, 4 x M20 8.8; resultant 34 kN (33 kN uplift + 8 kN wind) -> 0.09; not slotted, so the south-wall wind reaches the roof plane.
- Bracing: CHS flattened ends with 2 x M20 (188 kN > 127 kN); rods M20 8.8 with turnbuckles on 10 mm gussets.

## 6. Bases and anchors

Base plate 300 x 400 x 20 S275 on 30-50 mm non-shrink grout, pinned: c = t sqrt(f_y / 3 f_jd) = 61 mm, A_eff = 90 400 mm2, N_Rd = 904 kN at f_jd = 10 MPa (max N_Ed 99 kN, 0.11); plate bending under uplift (anchor row 55 mm from the flange face) 0.56 at K22.

Anchors: 4 x M20 8.8 resin anchors per base, group 300 x 150 mm; centred at interior columns. Perimeter columns are flush with the slab edge (centre 100 mm from the edge), so the group sits inboard with rows at 100 and 250 mm from the edge, eccentric by 75 mm; the plate extends 300 mm inboard. EN 1992-4 group factors with the basis formulas (N0_Rk,c = 7.2 sqrt(25) h_ef^1.5, uncracked, psi_s,N = 0.7 + 0.3 c/c_cr, psi_ec,N = 1/(1 + 2 e/s_cr), near row of two anchors carrying the tension of eccentric groups):

| h_ef | single N_Rk,c | interior group N_Rd (A_c/A_c0) | edge group N_Rd | corner group N_Rd | N_Rd,s (2 anchors) | N_Rd,p (2 anchors) | V_Rd edge breakout (c1 = 100, toward / parallel) |
|---|---|---|---|---|---|---|---|
| 170 mm (basis) | 80 kN | 109 kN (2.06) | 53 kN (1.57 x 0.82 x 0.77) | 46 kN | 280 kN | 143 kN | 34 / 68 kN |
| 300 mm (adopted) | 187 kN | 194 kN (1.56) | 85 kN | 64 kN | 280 kN | 251 kN | 34 / 68 kN |

With 170 mm the K22 post base (70 kN uplift from the girder) and corner K6 (42 kN incl. bracing) fail (1.65, 1.12) and six more bases exceed 0.8; 300 mm embedment into the solid column head is therefore adopted for all 27 bases (one anchor type, 24 mm hole, rebar scan before drilling). Utilisations with N + V interaction ((N/N_Rd)^1.5 + (V/V_Rd)^1.5, per combination) are in section 9: worst K22 0.87, K6 0.79, K23 0.64, K1 0.60 (24 kN shear toward the edge vs 34 kN). Steel and pull-out are never critical.

## 7. Deflections and sway

| frame | bay | L (m) | delta G+Q (mm) | delta Q (mm) | limit L/200 (mm) | ratio |
|---|---|---|---|---|---|---|
| F1 | 15.87-21.76 | 5.89 | 0.7 | 0.4 | 29 | L/7964 |
| F1 | 21.76-26.37 | 4.61 | 0.1 | 0.0 | 23 | L/46100 |
| F1 | 26.37-29.37 | 3.00 | -0.0 | -0.0 | 15 | L/30000 |
| F1 | 29.37-35.17 | 5.80 | 0.8 | 0.4 | 29 | L/7140 |
| F1 | cant N | 0.70 | -0.3 | -0.1 | 7 | L/7000 |
| F2 | 15.87-29.27 | 13.40 | 39.5 | 22.3 | 67 | L/339 |
| F2 | 29.27-35.27 | 6.00 | -0.0 | -0.0 | 30 | L/60000 |
| F2 | cant N | 0.60 | 0.8 | 0.4 | 6 | L/789 |
| F3 | 15.87-21.76 | 5.89 | 1.1 | 0.6 | 29 | L/5557 |
| F3 | 21.76-24.46 | 2.70 | -0.0 | -0.0 | 13 | L/27000 |
| F3 | 24.46-29.27 | 4.81 | 0.4 | 0.3 | 24 | L/12086 |
| F3 | 29.27-35.17 | 5.90 | 0.8 | 0.3 | 30 | L/7692 |
| F3 | cant N | 0.70 | -0.3 | -0.1 | 7 | L/7000 |
| F4 | 20.07-24.46 | 4.39 | 0.2 | 0.1 | 22 | L/17724 |
| F4 | 24.46-29.27 | 4.81 | 0.1 | 0.1 | 24 | L/48100 |
| F4 | 29.27-35.67 | 6.40 | 1.3 | 0.6 | 32 | L/5012 |
| F5 | 20.07-29.27 | 9.20 | 13.9 | 7.9 | 46 | L/660 |
| F5 | 29.27-35.77 | 6.50 | 0.8 | 0.4 | 33 | L/8249 |
| F6 | 20.07-29.27 | 9.20 | 10.9 | 6.1 | 46 | L/843 |
| F6 | 29.27-35.77 | 6.50 | 0.6 | 0.3 | 33 | L/10973 |
| F7 | 20.07-24.46 | 4.39 | 0.2 | 0.1 | 22 | L/20118 |
| F7 | 24.46-29.27 | 4.81 | -0.0 | -0.0 | 24 | L/48100 |
| F7 | 29.27-35.67 | 6.40 | 0.9 | 0.4 | 32 | L/7236 |

Sway under SLS G + W (worst column of each frame):

| frame | column | u (mm) | h (m) | ratio | combo |
|---|---|---|---|---|---|
| F1 | K6 | 4.9 | 3.49 | h/708 | SLS_WS |
| F2 | K5 | 19.7 | 3.49 | h/177 | SLS_WNp |
| F3 | K7 | 8.5 | 3.49 | h/412 | SLS_WN |
| F4 | K3 | 12.3 | 3.46 | h/282 | SLS_WS |
| F5 | K1 | 18.1 | 3.46 | h/191 | SLS_WN |
| F6 | K2 | 14.7 | 3.46 | h/234 | SLS_WN |
| F7 | K4 | 4.4 | 3.46 | h/790 | SLS_WS |

All rafters satisfy L/200 under G + Q; F2 has 39.5 mm on 13.4 m (L/339, 22 mm from Q alone), no precamber needed. Sway is within h/150 for all frames; F2 (h/177) and F5 (h/191) are the closest, both with HEA 200 columns (with HEA 180 they reached h/131 and h/134, which fixed the column section). If the BoardX supplier needs less than h/150, the roof plane between frames (not counted here) or HEA 220 in F2/F5 only would reduce it.

## 8. Bracing

E-W: wind on the gable elevation 1.3 x 1.30 x 86.5 m2 = 146 kN characteristic, 73 kN at roof level (110 kN ULS). Roof X-bracing CHS 76.3x3.2 (tension-only, N_t,Rd 202 kN) in bay 68.0-72.1 (4 panels, diagonal 96 kN, 0.48), 92.5-95.55 (3 panels, 127 kN, 0.63), 81.85-87.2 as diaphragm tie of the east wing (43 kN) and one panel between the openings (77.8-81.85, y 24.2-29.3, 22 kN). Chord forces 64-70 kN in the F1/F2 and F6/F7 rafters (< 0.05 N_pl). Vertical X-bracing, M20 8.8 rods with turnbuckles, in nine wall bays arranged in series so that the bracing uplift at any base stays <= 29 kN: north K6-K5 + K5-K7 and K3-K1 + K1-K2; south K25-K26 + K26-K24 + K24-K27 and K21-K22 + K22-K23; rod forces 28-36 kN (0.25); eaves beams / girder are the struts between bays (27.5 kN, in their check). Bays K7-K3 and K2-K4 stay free; braced bays must be door-free. N-S: portal action, no bracing.

Seismic check-only (a_g 0.10 g, soil B, S 1.2, plateau 2.5, mass 316 kN): F_b = 63 kN E-W (q 1.5), 24 kN N-S (q 4) against wind base shears of 146 kN (E-W) and 171 kN (N-S): wind governs.

## 9. Reactions

Reaction table for the slab check (`reactions_A.csv`). Nc = compression on the base, Nt = uplift, Vx = E-W shear (bracing or gable-wall wind), Vy = N-S shear (frame), ULS design values and SLS characteristic values; "Vy to edge" is the shear directed toward the free slab edge at perimeter columns. K21/K22/K23 include the girder reactions, K24 the eaves beam. The last two columns give the anchor utilisation with the adopted 300 mm and with the basis 170 mm embedment.

| column | position | Nc ULS | Nt ULS | Vx ULS | Vy ULS | Vy to edge | Nc SLS | Nt SLS | Vx SLS | Vy SLS | anchor u (h_ef 300) | anchor u (h_ef 170) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | edge | 34 | 32 | 27 | 30 | 24 | 24 | 20 | 18 | 20 | 0.60 | 0.60 |
| K2 | edge | 29 | 28 | 27 | 24 | 20 | 20 | 16 | 18 | 16 | 0.59 | 0.64 |
| K3 | edge | 29 | 29 | 27 | 22 | 16 | 20 | 13 | 18 | 14 | 0.46 | 0.67 |
| K4 | corner | 17 | 13 | 13 | 8 | 8 | 12 | 7 | 8 | 5 | 0.19 | 0.24 |
| K5 | edge | 30 | 26 | 27 | 26 | 19 | 21 | 16 | 18 | 17 | 0.57 | 0.57 |
| K6 | corner | 22 | 42 | 27 | 9 | 9 | 15 | 16 | 18 | 6 | 0.79 | 1.12 |
| K7 | edge | 30 | 25 | 27 | 20 | 15 | 21 | 12 | 18 | 14 | 0.47 | 0.64 |
| K8 | edge | 30 | 26 | 18 | 3 | 12 | 21 | 9 | 12 | 2 | 0.37 | 0.54 |
| K9 | interior | 99 | 96 | 0 | 22 | 0 | 69 | 57 | 0 | 14 | 0.37 | 0.85 |
| K10 | interior | 43 | 38 | 0 | 6 | 0 | 30 | 22 | 0 | 4 | 0.09 | 0.21 |
| K11 | interior | 41 | 35 | 0 | 8 | 0 | 29 | 21 | 0 | 5 | 0.08 | 0.19 |
| K12 | interior | 87 | 83 | 0 | 11 | 0 | 60 | 50 | 0 | 7 | 0.29 | 0.67 |
| K13 | interior | 70 | 63 | 0 | 10 | 0 | 49 | 37 | 0 | 6 | 0.19 | 0.45 |
| K14 | edge | 32 | 24 | 23 | 3 | 15 | 23 | 7 | 15 | 2 | 0.44 | 0.60 |
| K15 | edge | 18 | 12 | 16 | 3 | 10 | 13 | 2 | 11 | 2 | 0.23 | 0.29 |
| K16 | interior | 21 | 21 | 0 | 4 | 0 | 14 | 12 | 0 | 3 | 0.04 | 0.08 |
| K17 | interior | 32 | 28 | 0 | 6 | 0 | 23 | 16 | 0 | 4 | 0.06 | 0.13 |
| K18 | edge | 25 | 14 | 20 | 2 | 13 | 18 | 4 | 14 | 2 | 0.31 | 0.38 |
| K19 | edge | 37 | 31 | 24 | 2 | 15 | 26 | 9 | 16 | 2 | 0.53 | 0.75 |
| K20 | interior | 32 | 21 | 0 | 4 | 0 | 22 | 11 | 0 | 3 | 0.04 | 0.09 |
| K21 | edge | 44 | 38 | 27 | 22 | 16 | 24 | 16 | 18 | 14 | 0.58 | 0.85 |
| K22 | edge | 54 | 70 | 27 | 13 | 8 | 35 | 47 | 18 | 9 | 0.87 | 1.65 |
| K23 | corner | 34 | 34 | 27 | 8 | 8 | 18 | 11 | 18 | 5 | 0.64 | 0.88 |
| K24 | edge | 12 | 5 | 18 | 14 | 9 | 8 | 0 | 12 | 10 | 0.27 | 0.27 |
| K25 | corner | 24 | 34 | 18 | 10 | 10 | 17 | 12 | 12 | 6 | 0.57 | 0.82 |
| K26 | edge | 55 | 46 | 18 | 22 | 12 | 39 | 27 | 12 | 8 | 0.52 | 0.91 |
| K27 | corner | 38 | 38 | 18 | 8 | 7 | 26 | 13 | 12 | 4 | 0.60 | 0.88 |

Maximum values: compression 99 kN (K9, ULS-1), uplift 96 kN (K9, ULS-3) and 70 kN at the K22 post, N-S shear 30 kN (K1), E-W shear 27 kN (braced-bay columns). The largest uplift falls on interior columns with the 800 x 800 solid zone; at the perimeter it does not exceed 46 kN except K22.

## 10. Weight and section list

| Member | Section | Pieces / length | Note |
|---|---|---|---|
| Rafters, all 7 frames | IPE 300 S275 | 125 m, haunches 1.3 m from the same section (36 cuttings) | one knee detail |
| Columns K1-K27 incl. eave posts K22, K24 | HEA 200 S275 | 27 pieces, 108 m | one base detail |
| Eaves beams, trimmers, wind posts | IPE 200 S275 | 37.8 + 16.2 + 13.5 m | |
| Transfer eave girder y 20.07 | IPE 300 S275 | 17.7 m (77.8-95.49) | |
| Roof bracing | CHS 76.3x3.2 | approx. 150 m | tension-only X |
| Wall bracing | rods M20 8.8 + turnbuckles | 9 bays, approx. 110 m | |
| Purlins / girts | Z200x2.0 / Z150x1.5 S350GD @ 1.5 m | 300 m / 290 m | sleeved |
| Knee end plates | 200 x 680 x 20, 12 x M20 8.8 | 36 | column stiffeners 95 x 10 |
| Base plates | 300 x 400 x 20, 4 x M20 resin anchors h_ef 300 | 27 | |

| item | kg |
|---|---|
| rafters IPE 300 (125 m) | 5255 |
| haunch cuttings (36) | 494 |
| columns HEA 200 (27, 108 m) | 4570 |
| eaves beams IPE 200 (37.8 m) | 847 |
| transfer girder IPE 300 (17.7 m) | 747 |
| trimmers IPE 200 (4 x 4.05 m) | 363 |
| wind posts IPE 200 (3 x 4.5 m) | 302 |
| roof bracing CHS 76.3x3.2 (approx. 150 m) | 862 |
| wall bracing rods M20 (9 bays, approx. 110 m) | 275 |
| eaves ties, fly braces, sag rods (allowance) | 250 |
| end plates, stiffeners, base plates, bolts (+12 %) | 1676 |
| purlins Z200x2.0 @ 1.5 m (approx. 300 m incl. sleeves) | 1950 |
| girts Z150x1.5 (perimeter 96 m x 3 rows) | 1305 |
| **total** | **18895** |

Total 18.9 t = 38.9 kg/m2 of footprint (42.4 kg/m2 of roofed area); hot-rolled primary steel incl. connections 15.6 t. This is 2.6 t above the scheme estimate (16.3 t): about 1.8 t is the price of the single-section choice (IPE 240 on F1/F3/F4/F7 and HEA 160 on the 20 lightly loaded columns would save 0.9 t each, at the cost of two extra sections, two knee details and h/131 sway on F4 - not recommended); the rest is the wind posts, the longer bracing and the 12 % connection allowance.

## 11. Open items / risks

1. Anchor embedment 300 mm into the column heads deviates from the basis (170 mm); needs trial cores / rebar scan of the column-head zone and the supplier's group verification (ETA, cracked/uncracked). With 170 mm K22 and K6 fail and six bases exceed 0.8.
2. Shear toward the free slab edge relies on a 100 mm edge distance (V_Rd 34 kN, K1 at 0.71); if the edge is not solid over the full depth, a shear key into the edge beam or an inboard column offset is needed.
3. K22 post base: 70 kN ULS uplift from the transfer girder, the most loaded perimeter anchor group (0.87).
4. Purlin uplift capacity and sag-bar layout taken as the basis values (12.5 / 16 kNm); confirm with the supplier, including the fly-brace connection.
5. Frames analysed individually, no sharing of sway through the roof diaphragm (conservative); braced wall bays must remain door-free.
6. Knee: rows checked individually with the column-flange group limit, joint assumed rigid; full EN 1993-1-8 check before fabrication. The F5/F6 prop connection must not be slotted.
7. F/G wind zones applied to purlins, eaves members and trimmers only; frames use G/H (area-weighted on F1/F7).
8. K24/K22 eaves reactions approximated (12 kN); girder hanger on F3 (2 kN) neglected in the frame model. Slotted holes for temperature in the eaves beam and girder splices.

Files: `design_report_A.md`, `members_A.csv`, `reactions_A.csv`, `frames_A.png`, `calc/` (frame2d.py, sections.py, loads.py, frames_model.py, checks_members.py, checks_secondary.py, checks_connections.py, report_build.py, report_text.md, report_assemble.py, pynite_check.py, run_all.py).

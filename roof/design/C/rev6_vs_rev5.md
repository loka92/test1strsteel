# Design C: Rev 6a (IPE 300 / IPE 240 / HEA 140, P13 IPE 330, levels per A1) versus Rev 5a (IPE 330 / IPE 270 / HEA 160) - one-page comparison

Same scripts (`calc/run_all.py`), load basis Rev 3, Rev 5a bracing; Rev 5a values from `calc/summary_rev5_baseline.json`, Rev 6 from `calc/summary_C.json`. ULS unless stated; kN, kNm, mm.

| Item | Rev 5a | Rev 6 | Note |
|---|---|---|---|
| Sections primaries / rafters / columns | IPE 330 / IPE 270 / HEA 160 | IPE 300 / IPE 240 / HEA 140, P13 (K19-K20) IPE 330 | brief Rev 7, client decision; Rev 6a: P13 kept IPE 330 (review A2) |
| Levels: primary top / column top / column length | TOS + 0.05 / TOS - 0.30 / TOS - 0.35 | TOS + 0.03 / TOS - 0.29 / TOS - 0.335 exact (K19, K20: - 0.32 / - 0.365) | Rev 6a (A1): the TOS + 0.05 of Rev 3-6 put the rafter flange 0.7-4.3 mm below the primary flange; now 19.3 mm clear |
| Clear height under the cap nuts (y 35.77) / eave primary / rafters at the north edge, m | 3.02 / 3.06 / 3.06 (as printed; the true Rev 5 values were 3.00 / 3.04 / 3.06 with the flange clash) | 3.03 / 3.07 / 3.09 |  |
| Seismic mass W_a kN / F E-W / F N-S kN (two-mass, q 1.5) | 335 / 145 / 146 | 312 / 137 / 137 | lighter roof steel |
| Max beam utilisation (K19-K20 primary) | 0.68 (LTB gravity) | 0.69 (defl) | Rev 6 envelopes G + Q and G + 0.5 q_p (pressure case) for L/200; P13 IPE 330 (Rev 6a) |
| K19-K20 (9.79 m): LTB gravity / deflection mm (L/x) [case] | 0.68 / 26.9 (L/364) [G+Q] | 0.67 / 33.0 (L/297) [G+W_D] as IPE 330; as IPE 300: 0.82 / 46.0 (L/213) | Rev 5 checked G + Q only |
| 9.2 m rafters: utilisation (governs) / LTB uplift / deflection mm (L/x) | 0.55 (M) / 0.47 / 25.4 (L/362) | 0.69 (defl) / 0.55 / 31.8 (L/289) [G+W_D] | two fly braces at the third points, unchanged |
| Max column utilisation (K25, corner, biaxial) | 0.56 | 0.80 (ULS2W, k_zy 0.99) | HEA 140: 1.06 only at load basis Rev 2 wind |
| Column N_b,Rd range kN | 461-667 (HEA 160) | 310-475 |  |
| Wind post WP1 | 0.46 | 0.65 |  |
| Posts ST1 / ST2 | 0.10 / 0.05 | 0.15 / 0.07 |  |
| Bay B1: H_Ed kN (seismic) / diagonal | 41.9 / 0.26 | 39.8 / 0.25 |  |
| Bay B2: H_Ed kN (seismic) / diagonal | 64.4 / 0.39 | 61.2 / 0.37 |  |
| Bay B3: H_Ed kN (seismic) / diagonal | 70.9 / 0.44 | 67.3 / 0.42 |  |
| Bay B5: H_Ed kN (seismic) / diagonal | 49.2 / 0.34 | 46.4 / 0.32 |  |
| Bay B7: H_Ed kN (seismic) / diagonal | 66.8 / 0.43 | 63.1 / 0.41 |  |
| Roof rods: worst (jog) / RT-W chord kN in the rafters | 0.43 / 76.1 | 0.41 / 72.2 |  |
| Strut / chord members (axial + bending): rafter chord / rafter N-S strut / primary chord | 0.36 / 0.38 / 0.29 | 0.47 / 0.48 / 0.37 |  |
| Fin plates: web bearing per M20 (one row) / worst strut splice / chord splices | 68.8 kN / 0.55 (R78, 2 M20) / 3 M20 <= 0.46 | 64.6 kN / 0.56 (R78, 2 M20) / 2 x 2 M20 <= 0.41 | IPE 240 web 6.2 mm, 190 clear: no 3-bolt row |
| Gravity fin plate (2 M20) / cap plate worst / cap-plate cantilever | 0.27 / 0.26 / - | 0.29 / 0.25 / 0.11 | HEA 140: gauge 90 inside the 140 flange, pitch 200 outside the 133 depth |
| Seismic drift nu d_r vs 0.005 h, west wall / x 77.8 line, mm | 13.3 / 10.8 vs 19.7 | 12.7 / 10.5 vs 19.7 |  |
| Thermal path k_eff kN/mm / F ULS wind / erection kN | 3.1 / 15 / 37 | 3.0 / 15 / 37 |  |
| Sum G on the bases, char. kN | 279 | 258 |  |
| K7: N_t max kN (case) / N_c max / V max / base util. | 27.9 (ULS4-x) / 44.2 / 64.4 / 0.90 | 27.4 (ULS4-x) / 43.5 / 63.0 / 0.88 |  |
| K19: N_t max kN (case) / N_c max / V max / base util. | 49.0 (ULS3W) / 77.1 / 49.2 / 0.36 | 50.2 (ULS3W) / 76.0 / 48.3 / 0.50 |  |
| K23: N_t max kN (case) / N_c max / V max / base util. | 43.9 (ULS3E) / 56.2 / 71.0 / 0.53 | 45.1 (ULS3E) / 54.8 / 70.2 / 0.72 |  |
| K22: N_t max kN (case) / N_c max / V max / base util. | 27.1 (ULS4+x) / 71.8 / 70.9 / 0.52 | 27.4 (ULS3W) / 70.3 / 69.0 / 0.71 |  |
| K20: N_t max kN (case) / N_c max / V max / base util. | 41.7 (ULS3N) / 85.1 / 66.8 / 0.48 | 43.2 (ULS3N) / 84.2 / 63.8 / 0.66 |  |
| K27: N_t max kN (case) / N_c max / V max / base util. | 42.4 (ULS4+y) / 52.3 / 66.8 / 0.52 | 40.9 (ULS4+y) / 50.4 / 63.8 / 0.66 |  |
| K14: N_t max kN (case) / N_c max / V max / base util. | 26.9 (ULS3N) / 33.5 / 35.5 / 0.58 | 27.8 (ULS3N) / 33.0 / 35.0 / 0.57 |  |
| K25: N_t max kN (case) / N_c max / V max / base util. | 28.6 (ULS4+x) / 40.2 / 31.6 / 0.38 | 27.8 (ULS4+x) / 40.4 / 31.9 / 0.38 |  |
| Bases: tension max / key max / plate max / worst | 0.36 / 0.90 / 0.09 / 0.90 (K7) | 0.37 / 0.88 / 0.13 / 0.88 (K7) | base plates 25 -> 20 mm; rebars and keys unchanged |
| Weight t: rafters / primaries / columns / bracing / plates | 7.52 / 4.54 / 3.03 / 1.43 / 3.40 | 6.39 / 3.97 / 2.47 / 1.44 / 3.27 |  |
| Weight: calc take-off / BOM basis t | 23.3 / 24.6 (25.4 less the Rev 5 bracing) | 20.9 / **22.2** | sections -2.25 t (P13 IPE 330 kept, +0.07), bracing -0.83 t, plates -0.13 t |

Exceptions: P13 (K19-K20, 9.79 m) kept as IPE 330 on the reviewer's recommendation (Rev 6a) - as IPE 300 it passed at 0.94 with a precamber; every other member, connection and base passes with the lighter section, no precamber anywhere (P13 L/297 under the pressure case); the SW corner column K25 (0.80) is the member closest to its limit. Not changed: geometry and roof plane, bracing layout (13 panels, 8 bays), rods and angles, the base detail (rebars, keys, key pairs), the detailing package (S00-S06 to be re-issued for the new sections, levels and plates).

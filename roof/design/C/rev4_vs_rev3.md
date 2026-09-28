# Design C: Rev 4 (load basis Rev 3) versus Rev 3 (load basis Rev 2) - one-page comparison

Both columns come from the same scripts (`calc/run_all.py`); Rev 3 values from `calc/summary_rev3_baseline.json`, Rev 4 from `calc/summary_C.json`. ULS values unless stated; kN, kNm, mm.

| Item | Rev 3 | Rev 4 | Note |
|---|---|---|---|
| Basis | load basis Rev 2 | load basis Rev 3 (independent load critique) |  |
| Services / imposed Q (kN/m2) | 0.20 / 0.60 | 0.10 / 0.40 |  |
| Wall self-weight in G, G_min | 0.30 kN/m2 x height (in both) | none (wall mass in the seismic mass only) |  |
| Wind q_p (kN/m2) N / S / E / W | 1.30 all directions, z_e 10 | 1.25 / 0.75 / 1.05 / 1.05, z_e 9 m, terrain I / III / II / II |  |
| Roof zones | mono-pitch Table 7.3a theta 180 set (-2.3/-1.3/-0.8) enveloped, e 20 | flat roof Table 7.2 (-1.8/-1.2/-0.7/-0.2, I +0.2), e 18 |  |
| Global wall factor | 1.3 (D 0.8 + E 0.5) | 0.98 (0.85 x (0.75 + 0.40)) |  |
| Roofed area m2 | 439.3 | 439.3 |  |
| Sum G on the bases, char. kN | 439 | 279 | no walls, services 0.10 |
| Sum Q, char. kN | 264 | 176 |  |
| Sum roof uplift W_N / W_S, char. kN | -659 / -660 | -423 / -262 |  |
| Roof-level wind N / S / E / W, char. kN | 85.6 / 148.5 / 102.7 / 103.9 | 61.9 / 62.5 / 63.0 / 63.5 |  |
| Roof-suction horizontal component (S), kN | 38.6 | 14.8 |  |
| Seismic force at roof level, kN | 75.9 (roof mass, 0.20 g, unamplified) | 145 E-W / 136 N-S (two-mass, S_a 0.65 / 0.61 g, q 1.5) |  |
| Bay B1: governing H_Ed kN (case) / diagonal util. | 30.7 (W) / 0.19 | 42.0 (seismic) / 0.26 |  |
| Bay B2: governing H_Ed kN (case) / diagonal util. | 40.1 (W) / 0.24 | 64.4 (seismic) / 0.39 |  |
| Bay B3: governing H_Ed kN (case) / diagonal util. | 53.6 (E) / 0.33 | 70.9 (seismic) / 0.44 |  |
| Bay B5: governing H_Ed kN (case) / diagonal util. | 35.1 (S) / 0.24 | 24.1 (seismic) / 0.17 |  |
| Bay B6: governing H_Ed kN (case) / diagonal util. | 42.6 (S) / 0.28 | 28.2 (seismic) / 0.19 |  |
| Bay B7: governing H_Ed kN (case) / diagonal util. | 50.9 (S) / 0.33 | 29.4 (seismic) / 0.19 |  |
| Bay B8: governing H_Ed kN (case) / diagonal util. | 57.3 (S) / 0.38 | 33.1 (seismic) / 0.22 |  |
| Thermal locked-in force B1/B2, ULS with wind / erection, kN | 9 / 23 | 14 / 34 |  |
| Sections (primaries / rafters / columns) | IPE 330 / IPE 270 / HEA 160 | IPE 330 / IPE 270 / HEA 160 (kept; IPE 300 / IPE 240 / HEA 140 passes at 0.82 / 0.69 / 0.79, not adopted) |  |
| Max beam utilisation (K19-K20) | 0.74 | 0.68 | now LTB under the flat-roof pressure case |
| Max column utilisation (K25) | 0.72 | 0.56 |  |
| Purlin uplift M_Ed, kNm (3.07 m corner span) | 8.3 | 6.3 |  |
| Cap-plate uplift, max kN | 67.8 | 43.2 |  |
| K19: uplift max kN (case) / compression max kN / shear max kN | 73.2 (ULS3S) / 80.0 / 40.2 | 40.9 (ULS3W) / 65.7 / 24.1 |  |
| K12: uplift max kN (case) / compression max kN / shear max kN | 67.8 (ULS3N) / 70.5 / 0.0 | 43.2 (ULS3N) / 62.2 / 0.0 |  |
| K23: uplift max kN (case) / compression max kN / shear max kN | 62.3 (ULS3S) / 64.2 / 64.1 | 43.9 (ULS3E) / 56.5 / 71.1 |  |
| K22: uplift max kN (case) / compression max kN / shear max kN | 56.3 (ULS3S) / 91.1 / 59.4 | 27.1 (ULS4+x) / 71.8 / 70.9 |  |
| K20: uplift max kN (case) / compression max kN / shear max kN | 64.4 (ULS3N) / 82.5 / 30.0 | 24.4 (ULS3N) / 67.9 / 29.4 |  |
| K10: uplift max kN (case) / compression max kN / shear max kN | 60.5 (ULS3N) / 79.6 / 33.8 | 43.9 (ULS3N) / 56.2 / 33.1 |  |
| K7: uplift max kN (case) / compression max kN / shear max kN | 29.4 (ULS3E) / 52.4 / 52.5 | 27.9 (ULS4-x) / 44.2 / 64.4 |  |
| Base utilisation: tension max / key max / worst base | 0.54 / 0.80 / 0.80 (K23) | 0.32 / 0.90 / 0.90 (K7) | seismic-governed E-W bay bases |
| Weight (BOM t / calc take-off t) | 25.4 / 24.1 | 25.4 / 24.1 | unchanged sections |
| Existing-structure loads: G char. / roof-level wind char. / roof-level seismic design | 439 kN / 148.5 kN / 75.9 kN | 279 kN (+116 if the walls are counted) / 63.5 kN / 145 kN E-W, 136 kN N-S |  |

What did not change: geometry (north-face jog, TOS 3.33, 11 rafter lines), sections, bracing layout (10 bays), roof-plane rods, connections, the base detail (type E post-installed rebar at all 27 columns, keys and plates), the detailing package. What changed: every load-derived number above, the governing case of every braced bay (seismic, two-mass), and the base and bay utilisations.

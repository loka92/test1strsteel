# Alternative C - design Rev 6 (IPE 300 / IPE 240 / HEA 140, load basis Rev 3, Rev 5a bracing): sign-off

Scripts re-run: report, members, reactions and `bases_C.md` (Rev 8) regenerate byte-identical. Units kN, m, mm.

## 1. Hand checks

- **K19-K20 primary, IPE 300, 9.79 m**: M 119.4 / 172.8 = 0.69; LTB on the 2.81 m rafter segment (C1 1.07, curve c) M_b,Rd 144.9 -> **0.82**; deflection 36.7 mm (G + Q), **46.0 mm = L/213 under G + W_D**: reproduced. L/213 is inside the L/200 basis and W_D is a rare short-term case, so the envelope is conservative; a 15 mm precamber (about three quarters of the ~20 mm dead-load sag) is standard and sensible. **Opinion:** keep this one member (mark P13) as IPE 330 - one extra mark, +70 kg, LTB 0.57, L/258, no precamber to specify and inspect; if one section everywhere is wanted, 0.94 with the precamber is acceptable.
- **9.2 m rafters, IPE 240**: M 0.42, uplift LTB with third-point fly braces (3.07 m, M_b,Rd 72.6) 0.55, deflection 31.8 mm = L/289 under G + W_D. Keep IPE 240.
- **Columns HEA 140**: K25 ULS2W: 0.043 + 0.994 x 11.9/36.8 + 1.007 x 10.3/23.3 = **0.81**; K23 0.79. Acceptable at the Rev 3 wind; the uncredited girt restraint is a reserve. Keep HEA 140.
- **Cap plate** 200 x 280 x 20: gauge 90 inside the 140 flange, rows 33 mm outside the 133 depth, cantilever 11.2 x 0.033 = 0.37 kNm vs 2.75 -> 0.13 (they 0.11). Fine.
- **Fin plates**: 64.6 kN per M20 on the 6.2 mm web (e2 40), 54.8 at the two-row splices (e2 30): 4 bolts 219 vs 70.2 -> 0.32; R78 strut 61.7 on 2 M20 -> 0.55. Z1 closed.
- **Seismic**: W_a 312, T_a 0.126 / 0.130 s, S_a 0.64 / 0.65 g, F 133 / 134 kN reproduced; the 0.66 g bound (Y2) still applies. **Base plates 20 mm**: strip 5.6 / 8.25 = 0.68 (85 mm lever), T-stub 0.13: fine.

## 2. Findings

**A1 - MAJOR - Rafter / primary bottom-flange clash.** With the primary top at TOS + 0.05 the IPE 240 bottom flange (TOS - 0.240) sits 0.7 mm **below** the IPE 300 bottom-flange top face (TOS - 0.239), 4.3 mm below at the down-slope tip: the rafter cannot land on the fin plate without a cope. The same arithmetic gives -1.5 mm for IPE 330 / IPE 270, so the "18 mm nominal" printed since Rev 3 was never true - my Rev 1 finding F11 asked for +0.05 with the wrong sign, withdrawn here. Fix: **primary top at TOS + 0.03** (19.3 mm clear top and bottom, 15.7 at the tip); cap-plate top TOS - 0.27, column top TOS - 0.29, column length TOS - 0.335 (exact, not 0.32); clear height 3.03 m under the cap nuts, 3.07 m under the eave primary - still above 3.0. Re-issue the S01-S03 levels and schedule.

**A2 - MINOR** - P13 as IPE 330 rather than precambered; its cap-plate tops then 30 mm lower (columns are cut to survey).

**A3 - MINOR** - L = TOS - 0.32 printed for 0.315; superseded by A1.

**A4 - MINOR** - Still open, unchanged by Rev 6: Y1-Y3, Y5, Y6, Z2-Z6.

| ID | Severity | Item | Fix |
|---|---|---|---|
| A1 | MAJOR | Rafter bottom flange 0.7 mm below the primary flange top at TOS + 0.05; "18 mm" wrong since Rev 3 (reviewer's F11 sign error) | Primary top TOS + 0.03; cap TOS - 0.27, column top TOS - 0.29, L TOS - 0.335; clear 3.03 m |
| A2 | MINOR | K19-K20 at 0.94 with 15 mm precamber | Prefer IPE 330 for P13 only |
| A3 | MINOR | L rounded to 0.32 | Exact; superseded by A1 |
| A4 | MINOR | Y1-Y3, Y5, Y6, Z2-Z6 open | Close with the Rev 6 drawings |

## 3. Verdict

**ACCEPTABLE WITH FIXES.** The lighter sections pass with acceptable margins (0.94 deflection-governed under a rare case, LTB 0.82, corner column 0.81); no member must stay heavier, though IPE 330 is recommended for the single primary P13. A1 changes every rafter joint level and the column schedule and must be applied before S01-S06 are re-issued for Rev 6.

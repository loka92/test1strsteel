# Alternative C - bases Rev 5a: confirmation of V1-V6 (written with the Rev 4 review)

Checked on the Rev 5a files before the Rev 4 / Rev 6 re-issue (scripts regenerated them byte-identical) and re-confirmed on Rev 6, which keeps the detail unchanged. Units kN, mm.

- **V1 closed** - post-installed rebar connection (EAD 330087, EN 1992-1-1 8.4 / 8.7): 4 x dia 16 B500 with M16 threaded ends, f_bd 2.7 MPa; capacity 4 x 33.9 = 136 kN at the 250 mm minimum embedment, 163 kN at the 300 mm target; 1:1 lap with the corner dia14 bars (268 kN receiving). Rev 5a: K19 0.54, K23 0.80 (key pair) reproduced; Rev 6: K23 tension 0.32, K7 key 0.90.
- **V5 closed / l_0 statement** - at K19 sigma_sd 91 MPa gives l_0 = 1.5 x 135 = 203 < l_0,min = 15 d = 240 <= 250 provided, 300 targeted; the note prints "l_0 240 mm vs 250 provided" per base: correct.
- **V2 closed** - top 300 mm debonded by a sleeve, resin in the column part only; the slab cone and slab bond are never loaded; the bar tip sits 250-300 mm inside a column that continues downward, so no cone exists. Logic sound.
- **V3 closed** - pattern 70 x 240 with the 240 along the concrete column's long axis: (+/-120, +/-35) at the E-W columns (K1, K2, K5, K9-K14, K21-K24), (+/-35, +/-120) at the N-S ones; rod at (35, 120) to the corner bar at (57, 157): 43 - 7 - 10 = **26 mm clear**, as stated. Procedure: cover-meter scan of the column faces from below (+/-3-5 mm) plus GPR from above, 10 mm pilot with feed monitoring, relocation within +/-15 mm, 30 mm plate holes with plate washers or match-drilling.
- **V4 closed** - proof test of 3 production bars (interior, edge, corner head) to >= 60 kN held 2 min, displacement <= 1 mm; EAD 330087 injection system, certified installer.
- **V6 closed** - all 27 bases type E (K21 E + saddle); B1 kept only as an appendix option with its solid-zone condition.

**Verdict: Rev 5a bases ACCEPTABLE.** Superseded numerically by Rev 6 (load basis Rev 3), which is signed off in `review_C_rev4.md`.

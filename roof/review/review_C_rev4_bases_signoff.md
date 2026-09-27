# Alternative C - bases Rev 4: final sign-off check

Scripts re-run: report, reactions and `bases_C.md` regenerate byte-identical; S1-S4 answered. Units kN, mm.

## Hand checks that agree

- **K7 (B1)**: extents (300, 60, 260, 260) -> A/A0 0.978, psi_s 0.76, N_Rd,c 50.4; ULS3E N_t 26.4, psi_ec 0.61 -> **0.86**; Key A parallel to the +x edge 15.8 / 18.5 = **0.85**. Reproduced, but see T3.
- **K19 (B2)**: T = 73.1 x 430/180 = 174.6; per M24 87.3 + 3.4/0.56 = **93 kN** (0.46); C 101.5 / 210 (**0.48**); plate 21.7 kNm (0.45; plastic section 70 kNm, 48 conservative). Key pair: torque 35.1 x 0.2 m over 0.6 m -> 21 kN outward at c1 255 -> **0.52**.
- **K23 (B2)**: c 347, lever 2.93, bolt 96 kN, C 114, plate 26 kNm; torque -16.7 kNm -> 33.1 kN towards the notch edge, **0.80**. **K25**: key 1 outward 9.2 + 23.3 = 32.5 kN -> 0.78-0.83. Both agree.
- **K21 (P)**: 6.5 kN per M16 needs ~50 mm bond of 400; links 49 vs 26 -> 0.53. Acceptable; scan-adjusted pattern (12 mm to the corner bars).
- **Adjacency**: K20, K7, K10, K11, K21 adjacent; K16, K3, K17 not - agreed (T4).

## Findings

**T1 - MAJOR - B2 layouts outside plate and coring zone.** Shifted keys at 700 (K23) and 600 mm (K25, K27) and a bolt at 380 (K23) lie beyond the 700 x 550 plate and the +/-400 criterion; standard keys reach the plate edge (345 of 350). Fix: per-base plate length (K23 1100, K25 / K27 950, others 750) and criterion.

**T2 - MAJOR - B1 criterion smaller than the concrete the cone uses.** Calculation 340 inboard / +/-400 along, criterion 300 / +/-300: with the criterion N_Rd,c = 34.4 not 50.4 (K7 1.26, K11 0.98, K14 0.97); B2 key breakout bodies need +/-683 along. Fix: criterion 340 / +/-400 (B1), +/-700 (B2).

**T3 - MAJOR - Key-moment model at B1.** psi_ec is applied across the 80 mm spacing with e = 126 mm at K7, outside the group; the tension row alone gives 59 vs 41.3 kN (1.43). The rigid-post model already used for bearing (z0 113, pocket 200) keeps the moment in the pocket: K7 0.52. Apply one model consistently (recommend rigid-post), or make K7 and K14 B2.

**T4 - MINOR** - Diagonal opening corners at K3, K16, K17 cut ~8 % of the cone area (K16 0.76 -> ~0.82); slab openings remain an assumption.

**T5 - MINOR** - B2: under-slab plate 400 x 200 x 20 at 0.8 (use 25); stiffeners class 3 (elastic ~50 >= 48); skewed bolt centroids at K23 / K25 / K27 (14 vs 34 kNm); slab designer to get the 175 / 114 kN couple. **T6 - MINOR** - B1 bond quoted with the 800 zone; not governing.

| ID | Severity | Item | Fix |
|---|---|---|---|
| T1 | MAJOR | K23 / K25 / K27 keys and bolts outside plate and zone | Per-base plate length and criterion |
| T2 | MAJOR | Criterion 300 / +/-300 vs calc 340 / +/-400: 34.4 vs 50.4 kN | Align criterion; B2 +/-700 |
| T3 | MAJOR | psi_ec outside the group at K7 (row alone 1.43) | Rigid-post model, or K7 / K14 as B2 |
| T4 | MINOR | Diagonal opening corners | Reduce A_c,N ~8 % |
| T5 | MINOR | Under-slab plate 0.8; stiffeners; skewed levers; slab couple | 25 mm plate; note; slab check |
| T6 | MINOR | Bond with 800 zone | Update table |

## Verdict

**ACCEPTABLE WITH FIXES.** The B2 through-bolt and key-pair concept, the pier detail and WP1 are sound and correctly checked; T1-T3 are consistency fixes to close before base drawings issue. Detailing may start for B2 bases (per-base plate lengths), the pier, WP1 and interior B1 bases; K7 and K14 wait for T3; the coring criterion goes to site after T2.

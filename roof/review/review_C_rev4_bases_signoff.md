# Alternative C - bases Rev 4: final sign-off check

Scripts re-run: report, reactions and `bases_C.md` regenerate byte-identical. S1-S4 are answered: real edges in `edge_distances`, per-base type B1 / B2 / P, corrected lever statics. Units kN, mm.

## Hand checks that agree

- **K7 (B1)**: extents (300, 60, 260, 260) -> A/A0 0.978, psi_s 0.76, N_Rd,c 50.4; ULS3E N_t 26.4, V (-39.1, 14.3), M 1.2 / 3.3 kNm, psi_ec 0.867 x 0.704 = 0.61 -> **0.86**; Key A parallel to the +x edge: 2 V_Rk,c(c1 55) = 18.5 kN, 15.8/18.5 = **0.85**. Reproduced - but see T3.
- **K19 (B2)**: T = 73.1 x 430/180 = 174.6, per M24 87.3 + 3.4/0.56 = **93 kN** (0.46); C = 101.5 vs 210 (**0.48**); plate 73.1 x 0.25 + 3.4 = 21.7 kNm (0.45; my plastic M_Rd of the stiffened section is 70 kNm, 48 is conservative). Key pair: torque 35.1 x 0.2 m over 0.6 m -> 12 kN across per key: outward 21 kN at c1 255 (41.5) -> **0.52**.
- **K23 (B2)**: c = 347, lever 2.93, bolt 96 kN (0.47), C 114 (0.54), plate 26 kNm; key pair torque -16.7 kNm -> key 2 sees 33.1 kN towards the notch edge, 33.1/41.5 = **0.80**, resultant 45.6/83.8 = 0.54. Agrees.
- **K25**: torque of the 42.4 kN along-wall shear at 0.2 m -> key 1 outward 9.2 + 23.3 = 32.5 kN at c1 255 -> 0.78-0.83. Agrees.
- **K21 (P)**: bond needed for 6.5 kN per M16 at f_bd 2.7 is ~50 mm of 400; links 49 kN vs 26 -> 0.53. Lap logic acceptable at this load level; scan-adjusted pattern (12 mm nominal to the corner bars).
- **Adjacency rule**: K20, K7, K10, K11, K21 adjacent and K16, K3, K17 not - agreed, with T4.

## Findings

**T1 - MAJOR - B2 layouts outside the plate and the coring zone.** The shifted layouts put keys at 700 (K23) and 600 mm (K25, K27) along the wall and a bolt at 380 (K23), beyond the 700 x 550 plate (+/-350) and the +/-400 coring criterion; the standard key at +/-300 reaches the plate edge (345 of 350). Fix: per-base plate length (K23 1100, K25 / K27 950, others 750) and criterion.

**T2 - MAJOR - B1 coring criterion does not match the calculation.** The cone uses concrete to 340 inboard and +/-400 along; the criterion says inboard >= 300, along +/-300. With the criterion's extents N_Rd,c = 34.4 kN, not 50.4: K7 1.26, K11 0.98, K14 0.97. For B2 the key breakout body needs +/-683 along (300 + 1.5 c1). Fix: criterion inboard >= 340, along +/-400 (B1) and +/-700 (B2), or recompute with the criterion.

**T3 - MAJOR - Key-moment model at B1.** psi_ec is applied across the 80 mm spacing with e = 126 mm (K7), outside the group; EN 1992-4 then requires the tension row alone: 2 x 29.6 = 59 kN vs 41.3 kN (1.43). The rigid-post model already used for bearing (z0 113 mm, pocket 200 deep, anchor couple over 80 mm negligible) keeps that moment in the pocket, giving K7 0.52. State one model and apply it consistently (recommend rigid-post), or make K7 and K14 B2.

**T4 - MINOR** - Diagonal opening corners at K3, K16, K17 cut ~8 % of the cone area not captured by the rule (K16 0.76 -> ~0.82). Stair / shaft slab openings remain an assumption (conservative).

**T5 - MINOR** - B2: under-slab plate 400 x 200 x 20 at 0.8 in bending (use 25); 120 x 10 stiffeners are class 3 (elastic M_Rd ~50, still >= 48); at K23 / K25 / K27 the bolt centroid is 140-240 mm off-axis (plate 14 kNm vs 34, state it); hand the slab designer the 175 kN pull / 114 kN push couple 180 mm apart.

**T6 - MINOR** - Note: bond N_Rd,p for B1 still quotes the 800 zone (157.9); not governing.

| ID | Severity | Item | Fix |
|---|---|---|---|
| T1 | MAJOR | K23 / K25 / K27 keys and bolts outside plate and coring zone | Per-base plate length and criterion |
| T2 | MAJOR | B1 criterion (300 / +/-300) vs calculation (340 / +/-400): 34.4 vs 50.4 kN | Align criterion; B2 +/-700 along |
| T3 | MAJOR | psi_ec outside the group at K7 (row alone 1.43) | Rigid-post model consistently, or K7 / K14 as B2 |
| T4 | MINOR | Diagonal opening corners | Reduce A_c,N ~8 % at K3, K16, K17 |
| T5 | MINOR | Under-slab plate 0.8; stiffener class; skewed levers; slab couple | 25 mm plate; note; slab check |
| T6 | MINOR | Bond quoted with 800 zone | Update table |

## Verdict

**ACCEPTABLE WITH FIXES.** The B2 through-bolt and key-pair concept, the P pier detail and WP1 are sound and checked correctly; T1-T3 are consistency fixes to be closed before base drawings issue. Detailing may start for the B2 bases (with per-base plate lengths) and the interior B1 bases; K7 and K14 wait for T3; the coring criterion goes to site only after T2.

# Alternative C - design Rev 4 (load basis Rev 3) / bases Rev 6: review

Scripts re-run: report, members, reactions and `bases_C.md` regenerate byte-identical. The critic's harness (`scratchpad/recalc.py`, patched only where its `round()` meets the new two-mass dict) run on its "recommended" scenario against the Rev 4 code gives G 278.9 / Q 175.7 / W_N -422.5 / W_S -262.1 kN, K12 uplift 43.2, K19 40.9, K19-K20 M 122.7 kNm at 0.68 - identical to the report; its hall forces (68.7-70.0) exceed the report's 61.9-63.5 only by the D/E update the basis adopted (1.105 vs 0.98 q_p). Units kN, m, kN/m2.

## 1. Rev 3 loads as written

Confirmed in `loads.py`, `bracing.py`, `members.py`: services 0.10 (G 0.27 + steel), Q 0.40 with psi 0, G_WALL 0 in G and G_min with 0.30 in the seismic mass, gutter 0.25 / 0.10 / -0.50, q_p N 1.25 / E-W 1.05 / S 0.75 at z_e 9, e 18, flat-roof Table 7.2 (F -1.8, G -1.2, H -0.7, I -0.2) with the I +0.2 / c_pi -0.3 pressure case (+0.625 on the far half, governing K19-K20 through LTB), walls 0.75 / -0.40 with 0.85 on the resultant (C_GLOBAL 0.98, no friction), roof-suction component 14.8 kN, bracing uplift net per line, temperature 30 / 45 K (thermal 15 / 23 kN char.). Bay forces from wind fall to 10-25 kN char.; every bay is now governed by seismic.

## 2. Seismic two-mass / appendage check

- Formula: EN 1998-1 4.3.5.2 with z = H: S_a = 0.12 [6/(1 + (1 - T_a/T_1)^2) - 0.5]; at T_a 0.13, T_1 0.15: 5.40 x 0.12 = 0.648 g, reproduced. The scan 0.15-0.35 s misses the exact resonance T_1 = T_a, where S_a = 5.5 alpha S = **0.66 g** (+2 %). Use the bound, no scan needed. Applying the non-structural formula to a storey of mass ratio ~0.12 is a conservative simplification (a two-DOF modal analysis would give less); acceptable.
- q = 1.5 is right: DCL for tension-only X bracing (6.1.2, Table 6.2); DCM q = 4 would require slenderness limits and connection / base overstrength 1.1 gamma_ov N_pl = 355 kN, which this slab cannot take. Caveat: a_g S = 0.12 g exceeds the 0.10 g "low seismicity" limit of 3.2.1(4), so a checker may question DCL; cite the Libyan zonation for Tripoli in the report.
- 1.0 G +/- 1.0 E: psi_2 Q = 0 for a category H roof, vertical component not required (a_vg 0.09 g < 0.25 g): correct. **Missing: the orthogonal combination E_x +/- 0.3 E_y (4.3.3.5.1(3))** for the columns shared by two bays (K19, K18, K23): K23 compression 44 + 0.3 x 22.8 = 51 (+15 %), shear resultant +0.5 %; K7 unaffected. Utilisations stay <= 0.6; add it.
- Realism: with a_g 0.10, S 1.2 and resonance assumed, 145 kN E-W is a defensible upper bound, close to the old wind force by coincidence; an ambient-vibration measurement of T_1 could bring S_a towards the 0.30 g plateau (67 kN). The 145 / 136 kN also go into the existing columns (C5 statement).

## 3. Sections - opinion for the client

Keep IPE 330 / IPE 270 / HEA 160. The lighter set saves 2.3 t (~4,700 $, about 4 % of the project) and buys: a 9.8 m primary at 0.82 and L/266 under a Q of only 0.40, corner columns at 0.79 (the report itself says HEA 140 reaches 1.06 at K25 with Table B.2 - the two statements must be reconciled), and a re-opened detailing package. The margin kept is worth more to this client than the saving: services could go back to 0.20 and Q to 0.60 (a ceiling, a wind revision at 27 m/s) without touching a drawing.

## 4. Bases Rev 6 and the Rev 5a items

- K7: pair at (-200, -700) / (-200, -100), centroid 400 mm south of the column; ULS4-x V 64.4 -> torque 25.8 kNm over 0.6 m: near key 32.2 + 42.9 = 75.1 kN / 83.8 = **0.90**, reproduced; reversible under seismic. K23: 0.52 reproduced. Tension 43.9 / 136 = 0.32. The 18.5 kN parallel-edge value is not in play at K7 (pair >= 300 from every edge).
- Rev 5a items closed: post-installed rebar to EAD 330087 / EC2 8.4-8.7, dia 16 B500 threaded ends, f_bd 2.7, 136 kN at 250 / 163 at 300 (V1); top 300 debonded, column part only injected (V2); 70 x 240 with the 240 along the long axis - (+/-120, +/-35) for the E-W columns, (+/-35, +/-120) for the N-S ones - 26 mm clear to the corner bars, face scan from below, pilot, relocation +/-15, 30 mm plate holes (V3); proof test 60 kN / <= 1 mm (V4); l_0 240 <= 250 min / 300 target (V5); all 27 as E (V6). Separate confirmation in `review_C_rev5a_bases_signoff.md`.

## 5. Unconservative items

Only the two above (30 % rule; resonance bound), both a few per cent at utilisations far from 1.0. Terrain III for the south sector (0.75) presumes >= 1 km of continuous urban roughness upwind (Annex A.2); if the map shows less, category II (1.05) applies - it changes no governing case now.

| ID | Severity | Item | Fix |
|---|---|---|---|
| Y1 | MINOR | E_x +/- 0.3 E_y not applied (K19, K18, K23 shared columns, +15 % N) | Add the combination |
| Y2 | MINOR | T_1 scan misses resonance: S_a 0.66 g not 0.648 | Use the 5.5 alpha S bound |
| Y3 | MINOR | DCL with a_g S 0.12 g; report inconsistent on HEA 140 (0.79 vs 1.06) | Cite Tripoli zonation; reconcile the text |
| Y4 | MINOR | K7 key pair 0.90 under a seismic envelope | Accept, or SHS 100x100x8 at K7 / K23 for margin |
| Y5 | MINOR | South-sector terrain III to be confirmed on the map | Confirm; no governing change |
| Y6 | MINOR | Existing structure now receives 145 / 136 kN design seismic at roof level | Include in the C5 adequacy statement |

## 6. Verdict

**ACCEPTABLE WITH FIXES** (Y1-Y3 are text and a small combination update; no member, bracing, base or drawing changes). Bases Rev 6 signed off; Rev 5a items V1-V6 closed.

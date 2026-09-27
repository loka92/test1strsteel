# Independent review - Alternative C (post-and-beam braced frame, all pinned)

Independent check, 2026-09-27, of `design/C/`. `run_all.py` and `write_report.py` re-run: report, CSVs and PNG regenerate byte-identical, so every figure below is traceable to the code. Units kN, m, kNm.

## 1. Verified and agreeing

- **Loads** as the basis. Column-load sums G 435 / Q 268 / W_N -609 reconcile with my integration (roof G 165 + spans 115 + columns 28 + walls 114 + upstands 11 = 433; Q = 0.60 x 446.2; W_N mean -1.37 kN/m2).
- **Wind directions.** `loads.py` applies F -2.3 / G -1.3 / H -0.8 for both N and S wind, F/G strip on the windward edge each time (e = 12 m), theta = 90 set along the ridge, both cpi, wall D windward. The mislabelling changed nothing in C (F5).
- **Take-down.** Tributary widths of the 11 lines (2.05 ... 3.5 ... 1.6 m) re-derived; K19 G 28.0 rebuilt (15.9 + 4.0 + wall 7.0 + column 1.1).
- **Primary K19-K20 (9.79 m).** Rafter reactions 22.5 / 26.0 / 29.7 at 2.05 / 4.10 / 6.91 m: R_K19 44.9 (44.8), M 132.5 (131.3), delta 36.4 mm = L/269 (L/271, meets L/200; 21 mm variable). LTB on the 2.81 m segment (C1 1.07, curve c) M_b,Rd 179 -> 0.74 (0.73); "4.1 m end segment" in the text is a leftover, the code restrains at every rafter via the fin plates - state it.
- **9.2 m rafter.** M 46.9 gravity, 51.1 uplift with the F/G strip (51.0); delta 23.7 mm = L/388; uplift LTB with third-point fly braces: M_cr(3.07 m) 162, chi 0.76, M_b,Rd 100.7 -> 0.51.
- **Columns.** N_b,Rd(4.13 m) 465 correct; K25 M_y 14.8 / M_z 12.2 re-derived.
- **Bracing.** Centre of rigidity (81.0, 28.2), bay stiffness 15.6-24 kN/mm, B6 30.6 reproduced; L-shape torsion (65-208 kNm) included; rigid/tributary envelope conservative (1.2-1.5 x). L70x7 N_u 189, bolts 188.
- **Connections.** Fin plate 23.4 kN/bolt -> 0.25, web bearing 68.8 -> 0.34; cap-plate T-stub mode 1 379 / mode 2 398 kN (prying covered); anchor cone ratio 2.18 -> 115.8, bond 168.6, pry-out 231.6 reproduced.
- **Brief.** Openings not roofed, one plane at 6 %, three hot-rolled sections, columns centred on the 27 concrete columns, door-free bay list given.

## 2. Findings

**F1 - BLOCKER - Braced-bay bases fail once the wall shear is put where it belongs.** The report sends the lower half of the wall wind "to the slab through the anchored wall rail". BoardX spans on girts between columns, so a pinned-pinned column delivers wL/2 to its base plate; the rail only carries the strip below the lowest girt. Designer's own anchor check with V_wall restored (same wind as the bay shear), their H/2 strut share and uncracked V_Rd,c 48.1: K21 **1.38** (V 48.4, edge alone 1.01), K23 1.02, K22 1.01, K19 0.95. With the cracked edge value (F2): K21 2.07, K23 1.55, K22 1.47, K19 1.24, K17 1.03, K27 1.03, K14 1.01. Without a proven strut (F3) the compression base takes H + V_wall: K21 74 kN vs 34 (2.2). Fix: a base that does not rely on post-installed anchor shear near the solid-zone edge (through-bolts with a plate under the slab, grouted shear lug in a cored pocket) or 2-3 more bays per direction so H + V_wall <= ~25 kN per base; re-run all 27 bases with V_wall in V.

**F2 - MAJOR - Cracked/uncracked inconsistency.** Cone uses k = 7.2 (cracked), edge shear k9 = 2.4 (uncracked). Anchors sit in the slab top over a column head, the hogging tension zone: cracked applies, V_Rd,c = 34.0 not 48.1.

**F3 - MAJOR - Strut sharing H/2 unproven.** Two anchor groups linked by an HEA 160 on side gussets in 2 mm clearance holes share by slip, not stiffness: one group carries H until it moves 2 mm. Fitted/injection bolts or welded ends plus a compatibility check, or full H per base. The struts add 1.26 t and floor obstructions (B8 is inside the hall).

**F4 - MAJOR (basis, both alternatives) - Horizontal component of roof suction missing.** Uplift acts normal to the 3.43 deg plane: 614 x sin 3.43 deg = 36.8 kN char northwards, +34 % on the S-wind roof force (108.7 -> 145.5). B8 T 68 -> 92 (angle 0.48, OK), N_col 45.5 -> 61, K17/K21 uplift 60 -> 76 (cone 0.66). "Friction included in 1.3" is also wrong (0.8 + 0.5 = 1.3; friction ~6 kN). Feeds F1.

**F5 - MINOR** - Correct the basis text (theta = 0 = wind from N onto the low eave, F -1.7/G -1.2/H -0.6; theta = 180 from S, -2.3/-1.3/-0.8) so it cannot propagate to A.

**F6 - MINOR** - Gutter loads (0.25 / -0.50 kN/m, 0.05 kNm/m) are in no script: < 2 % on members, but needed for the eave rail, fascia and 0.6-0.7 m rafter cantilevers. Drainage puts the west gutter at y 35.37; the model roofs and walls the whole north edge at 35.87 (eave beam 35.22). Confirm the west-block north edge.

**F7 - MINOR** - Column interaction uses k_zy = 0.6 k_yy (Table B.1) although the column is treated as LTB-susceptible; Table B.2 (k_zy ~0.98) gives K25 0.79, K23 0.76, K22 0.62 (report 0.68 / 0.64 / 0.56). HEA 160 still adequate.

**F8 - MINOR** - Purlin uplift: the same routine gives 8.3 kNm on the 3.07 m corner spans (zone F), not "<= 6.5 elsewhere". 8.6 on the 4.07 m strip is 0.68 of a gravity capacity; free-flange uplift capacity of Z200x2.0 is typically 55-70 % of it. Anti-sag row there and supplier confirmation before order.

**F9 - MINOR** - Seismic 76 kN (roof mass alone) vs 108 kN E-W wind ignores floor amplification through the existing building (S_a up to ~0.6 g / q_a). Two-mass check when the building period is known.

**F10 - MINOR** - Diaphragm deflection unchecked: RT-E rods at 0.72 give ~20 mm at the east wall mid-length (h/165-180) plus 4 mm bay sway, close to h/150. RT-E/RT-W are computed as single 5.65 / 4.1 m panels with 10.8 / 8.6 m rods, but the drawn rods sit in 3.07 / 2.05 m cells (~84 kN in 9.7 m rods - fine); correct geometry, lengths and weight; consider M24 on the east band.

**F11 - MINOR** - Primary bottom at y 35.77 = 2.996 m (4 mm under 3.0); rafter/primary bottom-flange clearance 8.5 mm nominal, 3.7 mm at the down-slope flange tip - rolling tolerance eats it. Primary top at TOS + 0.05, TOS(35.87) = 3.30. T1 (y 35.37) and T2 (y 24.16) are centred on the opening edges (half a flange over the opening); R82 at x 81.85 lies inside the brief's elevator limit 81.99 - client to confirm.

**F12 - MINOR** - Cap-plate nuts (gauge 90, pitch 140) sit under the passing rafter bottom flange (135 wide, 20 mm above): primaries bolted before rafters, or pitch >= 200.

**F13 - MINOR** - Reactions table: no concurrent N-V pairs, WP1 base and ULS-4 missing, V_wall to be merged into V; add anchor layout and solid-zone size.

**F14 - MINOR** - Angle bearing with e2 = 35; the 40 gauge on a 70 leg gives e2 = 30 -> 124 kN, B8 0.55 (0.74 with F4). OK.

**F15 - MINOR** - Three hot-rolled sections hold, but the lateral system is 8 X-bays + 8 floor struts + rail anchors + 20 rod panels + fly braces + tie plates; 23.6 t is +15 % on the scheme, 1.3 t of it struts of doubtful value.

## 3. Findings table

| ID | Severity | Item | Mine vs theirs | Fix |
|---|---|---|---|---|
| F1 | BLOCKER | Braced-bay anchors, wall shear removed from bases | K21 1.38 (2.07 cracked) vs 0.76 | Through-bolts / shear lug / more bays; re-run with V_wall |
| F2 | MAJOR | Edge shear uncracked k9 | V_Rd,c 34.0 vs 48.1 | Use cracked |
| F3 | MAJOR | Strut H/2 sharing via clearance-hole bolts | Not reliable | Fitted bolts + compatibility, or full H per base |
| F4 | MAJOR | Roof-suction horizontal component (basis) | +36.8 kN char, +34 % N-S | Add to basis and bracing/base loads |
| F5 | MINOR | Basis wind-direction labels | Enveloped in C | Correct text |
| F6 | MINOR | Gutter loads absent; north edge 35.37 vs 35.87 | 0 vs 0.25/-0.50 kN/m | Add; coordinate with drainage |
| F7 | MINOR | k_zy Table B.1 vs B.2 | K25 0.79 vs 0.68 | Use B.2 |
| F8 | MINOR | Purlin uplift corner spans | 8.3 vs "<= 6.5" | Anti-sag row, supplier check |
| F9 | MINOR | Seismic without floor amplification | 76 vs 108 kN | Two-mass check |
| F10 | MINOR | Diaphragm deflection / RT-E geometry | ~20 mm (h/170) unchecked | Check; M24 east band |
| F11 | MINOR | 2.996 m clear; 8.5 mm flange clearance; trimmer lines | vs 3.0 m / "no cope" | TOS + 0.05, TOS(35.87) 3.30 |
| F12 | MINOR | Cap nuts under rafter flange | clash | Sequence or pitch 200 |
| F13 | MINOR | Reactions table incomplete | - | Concurrent pairs, WP1, ULS-4 |
| F14 | MINOR | Angle bearing e2 | 0.55 vs 0.47 | Note |
| F15 | MINOR | Complexity / weight | 23.6 t vs 20.5 t | Drop struts once F1 solved |

## 4. Verdict

**NOT ACCEPTABLE** as submitted. The superstructure (IPE 330 / IPE 270 / HEA 160, L70x7, M20 rods) is sound and acceptable with the minor fixes, but the load path from the braced bays into the hollow-block slab fails by 1.4-2.2 x once two unjustified assumptions (wall shear to the rail, strut sharing) and one inconsistency (uncracked edge factor) are removed - the one thing this scheme must get right on an existing slab.

**Five biggest risks:** (1) anchor edge/cone failure at the 16 braced-bay bases (F1-F3); (2) the 800 x 800 solid zone is an assumption - core before anchor design; (3) N-S wind under-estimated ~34 % in the basis (F4), also affecting A; (4) Z200x2.0 uplift capacity unconfirmed (F8); (5) east-face diaphragm drift and seismic amplification (F9, F10).

**Fitness for this client.** The pinned post-and-beam frame is genuinely simple in members and connections, and every gravity load lands centred on a concrete column. Its weakness is that it concentrates the whole lateral load into eight bays - sixteen small anchor groups near the edge of an assumed solid zone in a hollow-block slab - and the designer already had to add a bay, floor struts and a wall-rail anchorage to close the numbers. For an occupied restaurant on an unknown slab, C is fit only with a base detail that does not rely on post-installed anchor shear/cone resistance (through-bolting where ceiling access exists) or with roughly twice the braced bays; the client should see this before choosing between A and C.

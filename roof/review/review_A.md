# Independent structural review - Alternative A (mono-pitch portal frames)

Reviewer: independent check, 2026-09-27. Reviewed: `roof/brief.md` (Rev 1), `roof/design/load_basis.md`, `roof/geometry.json`, `roof/drainage/drainage_loads.json`, `roof/design/A/` (report, members_A.csv, reactions_A.csv, frames_A.png, calc/*.py).

## 0. Reproducibility

`python3 calc/run_all.py` (copy in scratch, PyNiteFEA 3.2 present) re-creates `design_report_A.md`, `members_A.csv` and `reactions_A.csv` byte-identical; the PyNite cross-check on F2 (140.63 kNm both) runs. All report numbers come from the scripts. My hand values agree with the scripts wherever the *inputs* agree: q_p 1.32, F2 ULS-1 w 7.47 kN/m, haunch M_el 247 kNm, IPE 300 chi_LT 0.83 at L 3.0 m, HEA 200 column 80/(0.96 x 118) = 0.70, knee rows 173/173/75 kN -> M_j,Rd 174 kNm, V_wp,Rd 258 kN, anchor edge-shear V_Rd 34 kN, cone values 80/187 kN. The solver and the checks are sound; the problems are in the inputs and in the bases.

## 1. Wind direction (known issue) - checked first

`loads.py`: `ROOF_CPE = {'N': F-2.3 G-1.3 H-0.8, 'S': F-1.7 G-1.2 H-0.6}`. Per EN 1991-1-4 Fig. 7.7 / Table 7.3a this is reversed: wind from the NORTH (low eave windward, theta = 0) is -1.7/-1.2/-0.6 (+0.0 alternative); wind from the SOUTH (high eave windward, theta = 180) is -2.3/-1.3/-0.8. The wall pressures (D on the windward wall) and c_pi are paired correctly with the *direction*, so the strong roof set is combined with the wrong wall side and the F/G strip is on the wrong eave. The zero-roof case "S0" (the +0.0 alternative) belongs to theta = 0, i.e. wind from N, not S. The secondary checks hard-code 2.3 (N eave) / 1.7 (S eave) - also reversed: the S eave (K25-K26-K24-K27) and the transfer-girder edge strip at y 19.97 are the high eave and must use -2.3/-1.3.

I re-ran the model with the pairing corrected (everything else unchanged):

| item | report | corrected pairing |
|---|---|---|
| K9 knee sagging (ULS-3) | 157 kNm (0.90) | 141 kNm (0.81) |
| K12 / K13 knee sagging | 95 / 77 | 113 / 91 (0.65 / 0.52) |
| F2 rafter, K9 column, K26 column | 0.66 / 0.70 / 0.57 | 0.60 / 0.61 / 0.65 |
| sway F2 / F5 | h/177 / h/191 | h/189 / **h/163** |
| base uplift K9 / K12 / K13 (ULS) | 96 / 83 / 63 kN | **111 / 102 / 81 kN** |
| girder prop uplift F5 / F6 | 33 / 26 kN | 39 / 30 kN; girder M 55 kNm, u 0.81 |
| K22 base uplift / anchor u (h_ef 300) | 70 kN / 0.87 | **79 kN / 1.02** |
| anchor u with basis h_ef 170: K22, K9, K26, K6 | 1.65, 0.85, 0.91, 1.12 | **1.95, 1.02, 1.09, 1.12** |

So the error is harmless for the steel members (knee even improves) but it **does** change the verdict at the bases: uplift on every base rises 10-25 % and K22 fails even with the designer's 300 mm anchors.

## 2. Findings

| # | Sev. | Item | Evidence (mine vs theirs) | Required fix |
|---|---|---|---|---|
| 1 | BLOCKER | 300 mm anchor embedment in a 250 mm slab | Group 300 x 150 on a 200 x 400 column: anchors 25 mm from the column face, on the dia14 corner bars / stirrups; at perimeter bases the inner row (250 mm from the edge) is outside the 200 mm column. EN 1992-4 needs member thickness about h_ef + 2 d_0 = 348 mm > 250; the cone model with s_cr 900 mm is meaningless in a column head. Drilling 50 mm into the column head with a 24 mm bit cuts stirrups = a change to the concrete columns (prohibited). With the basis 170 mm and corrected wind: K22 1.95, K6 1.12, K26 1.09, K9 1.02, K23 0.91, K27 0.88, K25 0.82. | Re-base all 27 bases on h_ef <= 170-200 mm (basis) and prove every base <= 1.0. Reduce the uplift at the source: e.g. F5/F6 rafters continuous to K1/K2 with the girder as a pinned prop on both ends is not enough - consider dropping the K22 prop reaction by making F5/F6 span K12-K1 / K13-K2 only with a cantilevered/propped girder sized for uplift, 6-8 anchor groups spread over the 800 x 800 solid zone, or an alternative base type. Supplier group verification (ETA) is mandatory, not "open". |
| 2 | MAJOR | Wind direction pairing (section 1) | See table above; K22 1.02 at h_ef 300, uplift +10-25 % everywhere, F5 sway h/163. | Swap `ROOF_CPE`, make S0 a theta = 0 (from N) case, use -2.3/-1.3 for S eaves beams / girder strip, -1.7/-1.2 for N; rerun and reissue all tables. |
| 3 | MAJOR | Zone size e | e = min(b, 2h) with h = building height above ground (the basis itself uses z_e = 10 m): 2h = 18-20 m, so e = 18-20 m, not 12 m. Strip e/10 = 1.8-2.0 m (not 1.2), corner F width 4.5-5 m (not 3). Along-ridge: F1/F7 lie in G/F (-1.8/-2.1), not -1.3. My rerun with e = 18 and -1.85 on F1/F7: K19 uplift 31 -> 46 kN (0.71 at h_ef 300, 1.12 at 170), K6 0.79 -> 0.94; edge purlin F1-F2 0.67 -> 0.92 (S eave, F -2.3), F2-F3 0.63 -> 0.73. | Correct the load basis (binding for both alternatives); recheck purlins, eaves beams, trimmers, gutter brackets, F1/F7 and the corner bases. |
| 4 | MAJOR | 3.0 m clear at the north eave | End plate 680 long extends 115 mm below the 450 mm haunch: bottom edge at 2.89 (K1/K2), 2.90 (K3/K4), 2.92 (K5), 2.93 m (K6/K7). Haunch soffit itself 3.01-3.04 m: zero margin. | Raise TOS at y 35.87 to 3.57 (all walls +120 mm, trivial) or use a flush/short plate and 1.2 h haunch at the 7 north knees (M <= 41 kNm there). State the clear height under the end plate in the report. |
| 5 | MAJOR | Gutter loads (drainage_loads.json) | Eaves beam uses 0.20 kN/m gravity (basis 0.25) and **no 0.50 kN/m uplift**; frames carry no gutter load; eccentricity 0.05 kNm/m and bracket/eave-rail fixings not checked. N eaves beam K5-K7: M_u 10.1 -> 12.4 kNm (with corrected G -1.2 and the gutter uplift), u 0.69 -> ~0.8. | Add 0.25 / -0.50 kN/m and the 0.05 kNm/m to the eaves beam, eave rail and rafter cantilevers; check the bracket fixings at 0.6 m (0.3 kN uplift each). |
| 6 | MAJOR | Shear toward the free slab edge | All N-S portal thrust at perimeter bases is resisted by concrete edge breakout at c1 = 100 mm in a hollow-block slab: V_Rd 34 kN (my 33.8), K1 24 kN -> 0.72, valid only if the edge is solid over >= 150 mm depth. Not verified. | Confirm a solid edge beam from the existing drawings/cores, otherwise shear key into the edge beam or an inboard steel column offset (which conflicts with "centred"). Must be closed before detailing, not left as an open item. |
| 7 | MAJOR | Temperature vs bracing layout | Both wings are E-W braced (K6-K5-K7 and K3-K1-K2 on the N line) and tied by the K7-K3 eaves beam and the mid roof panel: the 27.8 m length is fully restrained. +/-30 K gives ~5 mm between the braced zones and ~40 kN in the rods/eaves beams (wind gives 33 kN). The report's "slotted holes in the eaves beam" contradicts the eaves beams acting as 27.5 kN bracing struts. | Choose: (a) one expansion line at the stair bay (slot K7-K3 and the trimmers, drop the mid-panel diagonal, each wing braced independently) or (b) keep the tie and design rods, struts and the braced-bay bases for wind + temperature. |
| 8 | MINOR | F4 rafter over the elevator opening | F4 at x 81.85 lies 60-140 mm inside the client's opening range 77.89-81.99 (it sits on the 200 mm shaft wall). K21/K11 are at 81.78/81.79, K17/K3 at 81.89. | Client to confirm the opening edge = inside face of the shaft wall (81.79); if not, the east trimmer/upstand must be on the rafter flange at 81.93 and the panel stopped there. |
| 9 | MINOR | North roof edge of the west wing | Frames F1-F3 modelled to y 35.87 (0.6-0.7 m cantilevers); drainage puts the west north face at y 35.37 (gutter G-W). 0.5 m x 10 m strip inconsistency; loads negligible. | Coordinate the edge line; adjust F1-F3 cantilevers and the K7-K3 eaves beam jog. |
| 10 | MINOR | Knee joint | M_j,Rd 174 kNm confirmed; 10 mm column flange governs. Stiffness estimate S_j,ini ~ 50 000 kNm/rad vs rigid limit 25 E I_b / L_b = 33 000 for the 13.4 m rafter: rigid, but not by a wide margin. Panel shear 175/258 OK. | Full EN 1993-1-8 check incl. stiffness classification and weld sizes before fabrication; consider 12 mm flange doubler at K9 instead of relying on 0.81-0.90. |
| 11 | MINOR | Seismic mass | Steel taken as 0.20 kN/m2; actual 15.6 t / 446 m2 = 0.35. W ~380 kN (their 316), F_b,EW ~76 kN < wind 146 kN. Rooftop amplification (EN 1998-1 4.3.5) not mentioned. | Correct the mass; state that the appendage amplification is covered by the wind margin. |
| 12 | MINOR | Model idealisations | Haunch as a constant 450 mm stepped section (tapered in reality): slightly more moment to the knee, conservative. Prop spring from a 2-span girder (7 560 / 3 980 kN/m) with pin/spring envelope: realistic. alpha_cr 20.6 min, EHF included: OK. Sum of Nc,SLS 698 kN vs my 715 kN hand total: consistent. Reactions table complete for the slab check. | None; note the assumptions. |
| 13 | MINOR | Serviceability | F2 39.5 mm (L/339) while F1/F3 deflect ~1 mm: 38 mm differential across 4.1-5.7 m purlin spans; sway F5 h/163 after correction. | Precamber F2 by 20 mm; confirm the BoardX limit >= h/150. |
| 14 | MINOR | Weight / simplicity | 18.9 t vs 16.3 t scheme (+16 %): justified by one rafter, one column, one knee. Cost drivers are 36 haunch cuttings, 27 knees with 12 bolts and 2 stiffener pairs each, 27 x 4 drilled anchors. | Acceptable; show the client the 0.9 t + 0.9 t saving option (IPE 240 / HEA 160) as a priced alternative. |

Severity count: 1 BLOCKER, 6 MAJOR, 7 MINOR.

## 3. Checklist summary

1. Loads: dead/imposed/q_p/G_min/wall correct; zones (e) and direction wrong; gutter loads incomplete.
2. Analysis: geometry, pinned bases, single plane, haunches, prop compatibility (spring + pin envelope), alpha_cr (eigen 20.6, H/V 24.0), EHF, combinations: all verified and sound.
3. Members: rafter F2, K9, LTB (L 3.0 m, C1 1.13, chi 0.83), girder (0.75 -> 0.81), purlins (0.67 -> ~0.9 with e = 18), eaves strut (0.69 -> ~0.8 with gutter uplift), wind posts (0.64): all pass after correction.
4. Connections: knee 174 kNm verified (0.81-0.90), panel 0.68, prop pin 0.1, gussets not calculated (M20 rods 0.25, fine).
5. Bases: **fail** with basis anchors; 300 mm not feasible; edge shear unverified.
6. Stability: E-W path complete (roof X -> eaves struts -> 9 wall bays -> bases) but the two braced zones lock the length thermally; N-S by portal action OK; door-free bays to be confirmed by the client (N facade carries 4 downpipes and the kitchen/services doors).
7. SLS: OK; no ponding at 6 %; gutter edge deflection < 1 mm.
8. Constructability: 7 frame geometries but one detail set; erection of 13.4 m rafters over the occupied restaurant needs a crane plan; 108 drilled anchors with rebar scan.
9. Brief: openings, single plane, centred columns OK; 3.0 m clear violated by 70-110 mm; 300 mm anchors would modify the columns.
10. Reactions: complete and consistent (sum check OK), but to be reissued after items 2-3.

## 4. Verdict

**NOT ACCEPTABLE** in its present form. The steel superstructure is competently analysed and would pass after the wind corrections, but the scheme stands on anchors that do not exist (300 mm in a 250 mm slab) and fails at 6-7 bases with the binding basis values once the wind is corrected. The anchorage must be redesigned and proven before anything else is detailed; that redesign may change the scheme (uplift 80-110 kN at K9/K12/K13, 79 kN at the K22 post).

Five biggest risks: (1) uplift anchorage on the hollow-block slab (K22, K9, K12, corners); (2) portal thrust into the slab edge at perimeter columns with unknown edge construction; (3) wind basis errors (direction, e = 12 m) propagating to both alternatives; (4) thermal lock-up between the two braced wings on the 27.8 m length; (5) 3.0 m clear height at the north eave lost to the haunch/end plate.

Opinion on fitness for this client: rigid portal frames are the right answer for a clean site, but here they convert every wind case into 80-110 kN of uplift and 25-30 kN of thrust on drilled anchors in a 250 mm hollow-block slab over 200 x 400 columns that may not be touched - the weakest part of the whole system, and the part the client cannot see or fix later. The single-section decision is good for simplicity, and the report is transparent, but the client asked for simplicity first: a system that keeps base forces low (short spans, pinned beams, uplift resisted by gravity over the tributary area, few drilled anchors) fits the hollow-block slab and the occupied building better than this one. Alternative A should only be pursued if trial cores confirm solid column heads and an anchor layout with utilisation <= 1.0 at 170 mm can be shown for every base.

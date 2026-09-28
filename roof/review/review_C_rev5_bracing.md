# Alternative C - design Rev 5 (bracing rationalised): review

Scripts re-run: report, members, reactions and `bases_C.md` (Rev 7) regenerate byte-identical; `model.py` has the 8 bays, `bracing.py` the 5 strips (13 panels) and the strut checks. Units kN, m.

## 1. Load path, four directions and torsion

- **N-S.** Each rafter carries its band's inertia as a strut to the y 29.3 chord (8.2 kN, N_b,Rd 624 at L_y 9.2 / L_z 3.07 with the purlins and fly braces, 0.38 with gravity moment: fine). The two north strips carry it E-W to the three N-S lines: x 68 (R68 strut 3.0 m K8-K15 into B5), x 77.8 (R78 strut K10-K16-K20 into B7), x 95.5 (R95 into B6 + B9). The east strip's west reaction reaches x 77.8 through R82 (K11-K17), the jog panel (x 77.8-81.85, y 24.5-29.3, roofed) and R78. Complete; loads entering the y 29.3 chord between panel points (R70, R75) bend the IPE 330 about its weak axis by ~8 kNm against 42: fine.
- **E-W.** Purlin lines (3.4 kN, 0.41 with gravity bending, through the 2 M12 cleats) and the row-F / eave primaries collect the inertia to the west strip (R68 / R72 chords, B4-B2) and the east strip (R90 / R95, B3-B1); eave primaries as struts 72 kN (0.18). Complete.
- **Torsion.** With the south bands unbraced the roof is no rigid plate; the rigid / tributary envelope with 5 % eccentricity covers it (bay forces 32-71 kN, diagonals <= 0.44).
- **Jog panel.** V 66.8 through one active rod: T = 66.8 x 6.30 / 4.81 = 87.5 (0.43), chords 14 kN, 9.7 mm: adequate, and the X gives the reversed rod.
- **Chords.** Chord forces are axial (76 kN in R68 / R72, 0.36 with the strong-axis gravity moment); the weak-axis issue is the wall-column top load between panel points, which ST1 / ST2 carry - rightly kept.

## 2. NE corner cell

Both rod sets are needed, not double: the last panel of RT-N-E (N-S shear to B6 / B9) and the north end panel of RT-E (E-W shear to B1, rods over two rafter bays so that D = 5.65 - with the single 3.07 m cell the rod would be at 165 kN, 0.81) are end panels of two trusses in different directions. Cost: four rods and the R92 web clip cross in one cell, and the gussets at K2, K4, K13, K14 must take both rod forces under E_x + 0.3 E_y - to be drawn.

## 3. B8 and B10 removed

B5 alone: 49.2 kN, sway 3.0 mm; B7 alone: 66.8 kN, 3.7 mm (h/150 = 26-28). Net uplift without the pairing: K15 37.6, K19 23.3, K20 29.0, K27 42.4 kN (rebar <= 0.31); key pairs K15 / K19 0.36 (outward 24.6 + torque at c1 255), K20 / K27 0.48; K19-K25 line drift 3.0 mm. Removal is sound; the interior X in the hall is gone.

## 4. Deflection and drift

RT-W 15 mm is the ULS seismic truss deflection by virtual work over the rods; with the 3 mm bay sway the west wall mid-length moves 18 mm design. EN 1998-1 4.4.3.2 damage limitation is not stated: d_r = q x 18 = 27 mm, nu 0.5 -> 13.5 mm vs 0.005 h = 18 mm (brittle cladding): passes, add it.

## 5. Findings

**Z1 - MAJOR - Strut forces through the fin plates.** `bracing_rev5.md` credits every fin plate with 188 kN (2 M20 shear); the governing mode for an axial force is bearing on the 6.6 mm rafter web, 2 x 68.8 = 137 kN, and the through-web transfer at the primary. The R78 strut is also double-counted (133.6 = the full B7 force from RT-N-W plus the full B7 force again from the jog; the line carries 66.8). At 133.6 kN the fin plates at K10, K16, K20 would be at 0.97 in bearing; at the real 66.8 kN (+30 % orthogonal) about 0.5-0.6. Fix: state the R78 and R82 strut forces as the line forces, check those fin plates for axial + shear with web bearing and the primary web, and keep 2 M20 only if <= 0.6.

**Z2 - MINOR** - Corner gussets K2 / K4 / K13 / K14 for both rod sets concurrently; rod crossings and the R92 clip on S04.

**Z3 - MINOR** - Add the 4.4.3.2 drift check (13.5 vs 18 mm) and the seismic drift of the x 77.8 line (jog 9.7 mm + R78 strain + B7 3.7 mm).

**Z4 - MINOR** - Strip end shears set to the full bay force at both ends and R78 to their sum: conservative but inconsistent; state the actual split.

**Z5 - MINOR** - Erection: the south bands have no plan bracing until the panels are fixed - temporary plan bracing or guys in the S05 sequence.

**Z6 - MINOR** - Purlin strut check uses i_min 20 mm "assumed": supplier list.

Nothing else broke: the thermal path B2-RT-N-W-y 29.3-RT-N-E-B1 stands (15 / 37 kN), every braced-bay base keeps its Rev 5a keys, no bay shear points to a free edge, DCL / q 1.5 unchanged.

| ID | Severity | Item | Fix |
|---|---|---|---|
| Z1 | MAJOR | Fin plates credited with 188 kN; web bearing 137 kN; R78 force double-counted | Line forces; axial + shear check incl. web bearing at K10, K16, K20, K11, K17 |
| Z2 | MINOR | NE corner: both X sets needed; combined gussets | Design for both rods, E_x + 0.3 E_y; draw crossings |
| Z3 | MINOR | Seismic drift check absent | Add 4.4.3.2: 13.5 vs 18 mm |
| Z4 | MINOR | Strip end shears / R78 sum inconsistent | State the split |
| Z5 | MINOR | South bands unbraced during erection | Temporary plan bracing |
| Z6 | MINOR | Z200 i_min assumed | Supplier confirmation |

## 6. Verdict

**ACCEPTABLE WITH FIXES.** The rationalised layout is complete in all four directions and past both openings; Z1 is a statement error that the real force resolves but must be corrected before S04 is re-issued.

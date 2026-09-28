# Design C Rev 5 - bracing rationalised (brief Rev 6): before / after, analysis and reasons

Forces: design roof-level seismic 145 kN E-W / 146 kN N-S (two-mass, q 1.5) and wind 61.9-63.5 kN char. (x 1.5); every bay and strip is seismic-governed.

## 1. Before / after

| Item | Rev 4 | Rev 5 | Reason |
|---|---|---|---|
| Roof-plane braced panels (X of M24 rods) | 24 (every rafter cell of both bands, both wings, plus the edge strips and the jog) | **13** in five strips: north strip west (2), north strip east (3), jog (1), west strip (4), east strip (3) | south bands deleted: the rafters carry the south-half inertia as N-S struts to the y 29.3 chord; north-band rods now span two rafter cells with posts at the column lines |
| Rods / gussets | 48 rods, 96 gussets, 366 m | **26 rods, 52 gussets, 189 m** | |
| Wall bays (L70x7 X) | 10: B1-B10 | **8: B1, B2, B3, B4 (E-W), B5, B6, B7, B9 (N-S)** | B8 (K10-K16, the interior X in the hall) and B10 (K19-K25) removed: B7 alone carries the x 77.8 line (66.8 kN), B5 alone the x 68 line (49 kN); every remaining base passes with its Rev 5a keys and rebars |
| Truss posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) | 2 | **2, kept** | they carry the E-wall (K18) and W-wall (K15) column-top loads into the edge trusses; without them the R95 / R68 chords bend about their weak axis (32 / 24 kNm vs 26.7) |
| Bracing tonnage (rods + angles) | 1.30 + 0.96 = 2.26 t | **0.67 + 0.76 = 1.43 t** | -0.82 t (plus 44 gussets and 4 bracing base gussets) |
| Worst bay diagonal / roof rod / base | 0.44 / 0.39 / 0.90 | **0.44 / 0.43 / 0.90** | seismic-governed everywhere |

## 2. Diaphragm analysis (strips as horizontal trusses; end shear = the bay force of the line it delivers to, seismic envelope)

| Strip | Chords | Posts | Span m | Depth m | Delivers to | Shear V kN | Rod T kN (M24 203) | Chord kN | Post kN | Rod util. | Deflection mm (ULS) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RT-N-W | primaries y 29.3 / y 35.2 (IPE 330) | rafters R68, R72, R78 | 9.8 | 5.9 | B5 (x 68), B7 (x 77.8 via R78 strut) | 66.8 | 47.3 | 27.7 | 66.8 | 0.23 | 5.7 |
| RT-N-E | primaries y 29.3 / y 35.7 | rafters R82, R87, R92, R95 | 13.7 | 6.4 | B7 (via jog), B6 + B9 (x 95.5) | 66.8 | 57.5 | 35.8 | 66.8 | 0.28 | 7.9 |
| RT-JOG | primaries y 24.5 / y 29.3 | rafters R78, R82 | 4.1 | 4.8 | B7 through R78 | 66.8 | 87.5 | 14.1 | 66.8 | 0.43 | 9.7 |
| RT-W | rafters R68 / R72 (IPE 270) | primaries y 15.9, 21.8, 29.3, 35.2 + ST2 | 19.4 | 4.1 | B4 (y 15.9), B2 (y 35.2) | 64.4 | 78.5 | 76.1 | 64.4 | 0.39 | 15.0 |
| RT-E | rafters R90 / R95 | primaries y 20.1, 29.3, 35.7 + ST1 | 15.6 | 5.7 | B3 (y 20.1), B1 (y 35.7) | 70.9 | 64.6 | 49.1 | 70.9 | 0.32 | 10.4 |

Struts and chords (axial + bending): purlin lines as E-W struts 3.4 kN (Z200x2.0, N_b,Rd 55 kN) -> 0.41; rafter chords R68/R72/R90/R95 76.1 kN -> 0.36 (with the 7.5 m gravity moment); primaries y 29.3 as chords 35.8 kN -> 0.29; eave primaries as struts to B1-B4 72.3 kN -> 0.18; rafters as N-S struts (south-half inertia to the y 29.3 chord) 8.2 kN -> 0.38; R78 as the N-S strut from the north strips down to B7 133.6 kN -> 0.28. All fin plates (2 M20, 188 kN) carry the strut forces.

## 3. Wall bays: why each remaining bay is needed

| Bay | Columns | H_Ed kN (seismic / wind ULS) | Diagonal | Why it stays |
|---|---|---|---|---|
| B1 | K1-K2 | 41.9 / 20.0 | 0.26 | only E-W bay on the east north wall: the y 35.7 eave line cannot pass the stair-well jog to B2 |
| B2 | K5-K7 | 64.4 / 24.4 | 0.39 | only E-W bay on the west north wall; north support of the west strip RT-W and of the thermal path |
| B3 | K22-K23 | 70.9 / 32.5 | 0.44 | only E-W bay on the south (notch) wall; south support of the east strip RT-E |
| B4 | K25-K26 | 31.6 / 15.0 | 0.25 | only E-W bay on the west-wing south wall; south support of RT-W (the y 15.9 and y 20.1 eave lines are linked only through the weak axis of R78) |
| B5 | K15-K19 | 49.2 / 28.6 | 0.34 | the x 68 line now has one bay: takes the west strip reaction (49 kN); K15 / K19 keys and rebars pass (0.36) |
| B6 | K14-K18 | 35.5 / 21.7 | 0.24 | east wall line with B9: K14 has Key A only and its parallel-edge value (44 kN at c1 155) needs the line force shared |
| B7 | K20-K27 | 66.8 / 46.2 | 0.43 | the x 77.8 line now has one bay: takes the east reactions of both north strips through R78 (66.8 kN); K20 / K27 key pairs 0.48 / 0.52 |
| B9 | K18-K23 | 31.9 / 19.4 | 0.23 | shares the x 95.5 line with B6 (35.5 kN each) and keeps the net uplift at K18 near zero |

Removed: **B8 (K10-K16)** - the interior X in the hall; its role (west support of the jog panel) is taken by R78 as a strut down to B7. **B10 (K19-K25)** - added at Rev 2 only to keep the net uplift off K19 when the S-wind uplift was 73 kN; with the Rev 3 loads K19 sees 49 kN (rebar 0.36) and B5 alone carries the line.

## 4. Rules respected

- No bay shear towards a free slab edge without a key: every remaining braced-bay base keeps its Rev 5a key pair (K1, K2, K5, K7, K15, K18, K19, K20, K22, K23, K25, K27) or Key A + B (K14); no base type changed.
- Torsion of the L-shape with 5 % eccentricity: rigid-diaphragm and tributary distributions enveloped with the 8 bays (bay forces in the table).
- DCL, q 1.5, tension-only X, L70x7 unchanged; door-free bays for the client: B1 K1-K2, B2 K5-K7, B3 K22-K23, B4 K25-K26, B5 K15-K19, B6 K14-K18, B7 K20-K27, B9 K18-K23 (no interior bay any more).
- Both openings: the stair well is passed by the jog panel (y 24.5-29.3) and R78; the elevator opening lies south of the jog and below the west/east strips - no strip crosses it.
- Thermal path B2 - RT-N-W - y 29.3 - RT-N-E - B1: k_eff 3.1 kN/mm, 15 / 37 kN ULS (wind / erection) on B1, B2 - not governing.

- North-east corner: the last panel of the north strip east (x 92.5-95.5) and the first panel of the east strip (y 29.3-35.7) share the corner cell; both rod sets are kept (different chord/post pairs), gussets combined at K2, K4, K13, K14.

Figure: bracing_rev5.png (columns, primaries, rafters thin; braced strips and wall bays bold).

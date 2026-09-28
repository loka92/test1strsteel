# Design C Rev 5a - bracing rationalised (brief Rev 6, review Z1-Z6 closed): before / after, analysis and reasons

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

Struts and chords (axial + bending): purlin lines as E-W struts 3.4 kN (Z200x2.0, N_b,Rd 55 kN) -> 0.41; rafter chords R68/R72/R90/R95 76.1 kN -> 0.36 (with the 7.5 m gravity moment); primaries y 29.3 as chords 35.8 kN -> 0.29; eave primaries as struts to B1-B4 72.3 kN -> 0.18; rafters as N-S struts (south-half inertia to the y 29.3 chord) 8.2 kN -> 0.38; R78 as the N-S strut from the north strips down to B7 66.8 kN -> 0.20. The strut and chord forces pass through the rafter fin plates: checked in 2b (web bearing governs, not the 188 kN bolt shear).

### 2a. Actual strip end shears and line forces (Z4)

The rod design above takes V_end = the enveloped force of the line each strip delivers to (conservative, kept). The actual split, from the tributary N-S inertia of each block (roof grid) scaled per line so that the line totals equal the enveloped bay forces: RT-N-W 49.2 kN to x 68 (R68 -> B5) and 28.8 kN to x 77.8; jog panel 6.7 kN to x 77.8; RT-N-E 31.3 kN to x 77.8 (R82 -> jog -> R78) and 67.4 kN to x 95.5 (R95 -> B6 + B9). Line forces: **R68 49.2 kN, R78 66.8 kN (= B7, not the sum of the strip end shears), R82 31.3 kN, R95 67.4 kN**.

### 2b. Strut / chord forces through the rafter fin plates (Z1)

N = envelope of E_y + 0.3 E_x and E_x + 0.3 E_y (strut = N-S line force, chord = strip chord force at the splice); V = gravity end shear of the segment (G + Q, psi_2 = 0 in the seismic combination). Fin plate 10 mm S275, M20 8.8 in one row (pitch 70, e1 = e2 = 40; 3-bolt plate e1 35, 210 deep), bolt line 50 mm from the primary web. Bearing on the 6.6 mm IPE 270 web governs: 68.8 kN per bolt (60.2 with e1 35) in either direction, bolt shear 94 kN, plate net section, weld a 6 both sides; the force passes through the IPE 330 primary web plate-weld-web-weld-plate (web in through-thickness bearing, < 0.05).

| Member | Fin plates at | N strut kN | N chord kN | N design kN | V kN | Bolts | Web bearing | Bolt shear | Plate net | Weld | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R68 | K8, K15, K19, K25 (x 68 line) | 49.2 | 76.1 | 90.8 | 3.3 | 3 M20 | **0.46** | 0.33 | 0.18 | 0.15 | strut into B5 + RT-W chord |
| R72 | K9, ST2, K26 (RT-W chord) | 8.2 | 76.1 | 78.5 | 7.4 | 3 M20 | **0.42** | 0.31 | 0.18 | 0.13 | RT-W chord + rafter N-S strut |
| R78 | K10, K16, K20 (x 77.8 line) | 66.8 | 0.0 | 66.8 | 6.5 | 2 M20 | **0.55** | 0.41 | 0.22 | 0.17 | strut into B7: whole line force |
| R82 | K11, K17 (RT-N-E west post) | 31.3 | 0.0 | 31.3 | 6.3 | 2 M20 | **0.30** | 0.22 | 0.12 | 0.09 | RT-N-E west end shear (actual split) |
| R90 | K13, K22 (RT-E chord) | 8.2 | 49.1 | 51.6 | 9.8 | 3 M20 | **0.30** | 0.22 | 0.14 | 0.10 | RT-E chord + rafter N-S strut |
| R95 | K4, K14, K18, K23 (x 95.5 line) | 67.4 | 49.1 | 82.1 | 4.7 | 3 M20 | **0.42** | 0.31 | 0.17 | 0.14 | strut into B6 + B9 + RT-E chord |
| R70/R75/R85/R87/R92 | y 29.3 primary (N-S struts) | 8.2 | 0.0 | 8.2 | 10.3 | 2 M20 | **0.18** | 0.13 | 0.08 | 0.10 | south-band inertia to the y 29.3 chord |

With 2 M20 the chord rafters R68 / R95 would be at 0.69 / 0.62 in web bearing, so their splices (and R72 / R90, the other strip chords) get the 3 M20 plate; R78 stays at 2 M20 (0.55 <= 0.6). Purlin lines: 3.4 kN through the 2 M12 cleats (bearing on the 2.0 mm Z flange 2 x 16 kN, 0.11). Eave and row-F primaries: 72.3 kN through the 4 M20 of the cap plate (bolt shear + tension interaction 0.26). Bracing gussets at the NE corner (K2, K4, K13, K14): both rod sets concurrently, E_x + 0.3 E_y - rod forces 64.6 + 0.3 x 57.5 kN on a 10 mm gusset, 2 M20 per rod end (crossings and the R92 web clip to be drawn on S04 by detailing).

### 2c. Seismic drift, EN 1998-1 4.4.3.2 (Z3)

d_e = roof-truss deflection at the wall mid-length under the design (q 1.5) force + bay sway (+ strut strain); d_r = q d_e; nu = 0.5; limit 0.005 h for brittle cladding, h = TOS at the location.

| Line | d_e mm | nu d_r mm | 0.005 h mm | Ratio |
|---|---|---|---|---|
| west wall (RT-W + B4/B2) | 17.7 | 13.3 | 19.7 | 0.67 |
| east wall (RT-E + B3/B1) | 13.6 | 10.2 | 19.0 | 0.54 |
| x 77.8 line (jog + R78 + B7) | 14.4 | 10.8 | 20.1 | 0.54 |
| x 68 line (RT-N-W + R68 + B5) | 8.9 | 6.7 | 19.5 | 0.34 |

Passes everywhere; the west wall (13.3 vs 19.7 mm) governs.

### 2d. Erection (Z5) and purlin data (Z6)

- The south bands have no plan bracing until the sandwich panels are fixed: the erector shall place temporary plan bracing (crossed wire ropes or angles) in one rafter cell of each south band (west wing R70-R72 / y 15.9-21.8, east wing R85-R87 / y 20.1-29.3) or guy the wall columns, and keep it until the roof panels and the purlin bridging are complete - to be written into the S05 sequence by detailing. The permanent strips (north bands, jog, west / east edge) are erected and pinned with the first rafters of each block.
- Purlin strut check: Z200x2.0 S350GD, A 7.4 cm2, i_min 20 mm (principal minor axis; catalogue values 21-23 mm for Z200x65x2.0), buckling length 3.07 m between rafters - the supplier is to confirm A and i_min; with the sheeting fixed to the top flange the real length is the bridging spacing, so the 0.41 (mostly gravity bending) is an upper bound.

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

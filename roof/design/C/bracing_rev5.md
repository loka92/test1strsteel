# Design C Rev 5a bracing (rationalised, review Z1-Z6 closed) - figures re-run at Rev 6 with the IPE 300 / IPE 240 / HEA 140 sections

Forces: design roof-level seismic 137 kN E-W / 137 kN N-S (two-mass, q 1.5) and wind 61.9-63.5 kN char. (x 1.5); every bay and strip is seismic-governed.

## 1. Before / after

| Item | Rev 4 | Rev 5 | Reason |
|---|---|---|---|
| Roof-plane braced panels (X of M24 rods) | 24 (every rafter cell of both bands, both wings, plus the edge strips and the jog) | **13** in five strips: north strip west (2), north strip east (3), jog (1), west strip (4), east strip (3) | south bands deleted: the rafters carry the south-half inertia as N-S struts to the y 29.3 chord; north-band rods now span two rafter cells with posts at the column lines |
| Rods / gussets | 48 rods, 96 gussets, 366 m | **26 rods, 52 gussets, 189 m** | |
| Wall bays (L70x7 X) | 10: B1-B10 | **8: B1, B2, B3, B4 (E-W), B5, B6, B7, B9 (N-S)** | B8 (K10-K16, the interior X in the hall) and B10 (K19-K25) removed: B7 alone carries the x 77.8 line (66.8 kN), B5 alone the x 68 line (49 kN); every remaining base passes with its Rev 5a keys and rebars |
| Truss posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) | 2 | **2, kept** | they carry the E-wall (K18) and W-wall (K15) column-top loads into the edge trusses; without them the R95 / R68 chords bend about their weak axis (32 / 24 kNm vs 26.7) |
| Bracing tonnage (rods + angles) | 1.30 + 0.96 = 2.26 t | **0.67 + 0.77 = 1.44 t** | -0.82 t (plus 44 gussets and 4 bracing base gussets) |
| Worst bay diagonal / roof rod / base | 0.44 / 0.39 / 0.90 | **0.42 / 0.41 / 0.88** | seismic-governed everywhere |

## 2. Diaphragm analysis (strips as horizontal trusses; end shear = the bay force of the line it delivers to, seismic envelope)

| Strip | Chords | Posts | Span m | Depth m | Delivers to | Shear V kN | Rod T kN (M24 203) | Chord kN | Post kN | Rod util. | Deflection mm (ULS) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RT-N-W | primaries y 29.3 / y 35.2 (IPE 300) | rafters R68, R72, R78 | 9.8 | 5.9 | B5 (x 68), B7 (x 77.8 via R78 strut) | 63.1 | 44.6 | 26.2 | 63.1 | 0.22 | 5.4 |
| RT-N-E | primaries y 29.3 / y 35.7 | rafters R82, R87, R92, R95 | 13.7 | 6.4 | B7 (via jog), B6 + B9 (x 95.5) | 63.1 | 54.3 | 33.8 | 63.1 | 0.27 | 7.5 |
| RT-JOG | primaries y 24.5 / y 29.3 | rafters R78, R82 | 4.1 | 4.8 | B7 through R78 | 63.1 | 82.6 | 13.3 | 63.1 | 0.41 | 9.2 |
| RT-W | rafters R68 / R72 (IPE 240) | primaries y 15.9, 21.8, 29.3, 35.2 + ST2 | 19.4 | 4.1 | B4 (y 15.9), B2 (y 35.2) | 61.2 | 74.5 | 72.2 | 61.2 | 0.37 | 14.3 |
| RT-E | rafters R90 / R95 | primaries y 20.1, 29.3, 35.7 + ST1 | 15.6 | 5.7 | B3 (y 20.1), B1 (y 35.7) | 67.3 | 61.3 | 46.6 | 67.3 | 0.30 | 9.9 |

Struts and chords (axial + bending): purlin lines as E-W struts 3.2 kN (Z200x2.0, N_b,Rd 55 kN) -> 0.41; rafter chords R68/R72/R90/R95 72.2 kN -> 0.47 (with the 7.5 m gravity moment); primaries y 29.3 as chords 33.8 kN -> 0.37; eave primaries as struts to B1-B4 68.7 kN -> 0.23; rafters as N-S struts (south-half inertia to the y 29.3 chord) 7.8 kN -> 0.48; R78 as the N-S strut from the north strips down to B7 63.1 kN -> 0.25. The strut and chord forces pass through the rafter fin plates: checked in 2b (web bearing governs, not the 188 kN bolt shear).

### 2a. Actual strip end shears and line forces (Z4)

The rod design above takes V_end = the enveloped force of the line each strip delivers to (conservative, kept). The actual split, from the tributary N-S inertia of each block (roof grid) scaled per line so that the line totals equal the enveloped bay forces: RT-N-W 46.4 kN to x 68 (R68 -> B5) and 27.2 kN to x 77.8; jog panel 6.3 kN to x 77.8; RT-N-E 29.6 kN to x 77.8 (R82 -> jog -> R78) and 63.6 kN to x 95.5 (R95 -> B6 + B9). Line forces: **R68 46.4 kN, R78 63.1 kN (= B7, not the sum of the strip end shears), R82 29.6 kN, R95 63.6 kN**.

### 2b. Strut / chord forces through the rafter fin plates (Z1)

N = envelope of E_y + 0.3 E_x and E_x + 0.3 E_y (strut = N-S line force, chord = strip chord force at the splice); V = gravity end shear of the segment (G + Q, psi_2 = 0 in the seismic combination). Fin plate 10 mm S275, M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web; the strip-chord splices use two rows (2 x 2 M20, p2 60, plate 160 x 150) because the IPE 240 web (190 mm clear) takes no 3-bolt row. Bearing on the 6.2 mm IPE 240 web governs: 64.6 kN per bolt with one row, 54.8 kN with two rows (lesser of the two force directions), bolt shear 94 kN, plate net section, weld a 6 both sides; the force passes through the IPE 300 primary web plate-weld-web-weld-plate (web in through-thickness bearing, < 0.05).

| Member | Fin plates at | N strut kN | N chord kN | N design kN | V kN | Bolts | Web bearing | Bolt shear | Plate net | Weld | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R68 | K8, K15, K19, K25 (x 68 line) | 46.4 | 72.2 | 86.1 | 3.1 | 2x2 M20 | **0.41** | 0.24 | 0.25 | 0.21 | strut into B5 + RT-W chord |
| R72 | K9, ST2, K26 (RT-W chord) | 8.2 | 72.2 | 74.7 | 7.2 | 2x2 M20 | **0.39** | 0.23 | 0.25 | 0.20 | RT-W chord + rafter N-S strut |
| R78 | K10, K16, K20 (x 77.8 line) | 63.1 | 0.0 | 63.1 | 6.3 | 2 M20 | **0.56** | 0.38 | 0.21 | 0.16 | strut into B7: whole line force |
| R82 | K11, K17 (RT-N-E west post) | 29.6 | 0.0 | 29.6 | 6.2 | 2 M20 | **0.30** | 0.21 | 0.12 | 0.09 | RT-N-E west end shear (actual split) |
| R90 | K13, K22 (RT-E chord) | 8.2 | 46.6 | 49.1 | 9.5 | 2x2 M20 | **0.30** | 0.17 | 0.19 | 0.18 | RT-E chord + rafter N-S strut |
| R95 | K4, K14, K18, K23 (x 95.5 line) | 63.6 | 46.6 | 77.5 | 4.6 | 2x2 M20 | **0.38** | 0.22 | 0.24 | 0.19 | strut into B6 + B9 + RT-E chord |
| R70/R75/R85/R87/R92 | y 29.3 primary (N-S struts) | 8.2 | 0.0 | 8.2 | 10.1 | 2 M20 | **0.19** | 0.13 | 0.08 | 0.09 | south-band inertia to the y 29.3 chord |

With a single row of 2 M20 the chord rafters R68 / R95 would exceed 0.6 in web bearing, so their splices (and R72 / R90, the other strip chords) get the 2 x 2 M20 plate; R78 stays at 2 M20 (0.56 <= 0.6). Purlin lines: 3.4 kN through the 2 M12 cleats (bearing on the 2.0 mm Z flange 2 x 16 kN, 0.11). Eave and row-F primaries: 68.7 kN through the 4 M20 of the cap plate (bolt shear + tension interaction 0.25). Bracing gussets at the NE corner (K2, K4, K13, K14): both rod sets concurrently, E_x + 0.3 E_y - rod forces 61.3 + 0.3 x 54.3 kN on a 10 mm gusset, 2 M20 per rod end (crossings and the R92 web clip to be drawn on S04 by detailing).

### 2c. Seismic drift, EN 1998-1 4.4.3.2 (Z3)

d_e = roof-truss deflection at the wall mid-length under the design (q 1.5) force + bay sway (+ strut strain); d_r = q d_e; nu = 0.5; limit 0.005 h for brittle cladding, h = TOS at the location.

| Line | d_e mm | nu d_r mm | 0.005 h mm | Ratio |
|---|---|---|---|---|
| west wall (RT-W + B4/B2) | 17.0 | 12.7 | 19.7 | 0.65 |
| east wall (RT-E + B3/B1) | 13.1 | 9.8 | 19.0 | 0.52 |
| x 77.8 line (jog + R78 + B7) | 13.9 | 10.5 | 20.1 | 0.52 |
| x 68 line (RT-N-W + R68 + B5) | 8.7 | 6.5 | 19.5 | 0.33 |

Passes everywhere; the west wall (13.3 vs 19.7 mm) governs.

### 2d. Erection (Z5) and purlin data (Z6)

- The south bands have no plan bracing until the sandwich panels are fixed: the erector shall place temporary plan bracing (crossed wire ropes or angles) in one rafter cell of each south band (west wing R70-R72 / y 15.9-21.8, east wing R85-R87 / y 20.1-29.3) or guy the wall columns, and keep it until the roof panels and the purlin bridging are complete - to be written into the S05 sequence by detailing. The permanent strips (north bands, jog, west / east edge) are erected and pinned with the first rafters of each block.
- Purlin strut check: Z200x2.0 S350GD, A 7.4 cm2, i_min 20 mm (principal minor axis; catalogue values 21-23 mm for Z200x65x2.0), buckling length 3.07 m between rafters - the supplier is to confirm A and i_min; with the sheeting fixed to the top flange the real length is the bridging spacing, so the 0.41 (mostly gravity bending) is an upper bound.

## 3. Wall bays: why each remaining bay is needed

| Bay | Columns | H_Ed kN (seismic / wind ULS) | Diagonal | Why it stays |
|---|---|---|---|---|
| B1 | K1-K2 | 39.8 / 20.0 | 0.25 | only E-W bay on the east north wall: the y 35.7 eave line cannot pass the stair-well jog to B2 |
| B2 | K5-K7 | 61.2 / 24.4 | 0.37 | only E-W bay on the west north wall; north support of the west strip RT-W and of the thermal path |
| B3 | K22-K23 | 67.3 / 32.5 | 0.42 | only E-W bay on the south (notch) wall; south support of the east strip RT-E |
| B4 | K25-K26 | 29.8 / 14.9 | 0.23 | only E-W bay on the west-wing south wall; south support of RT-W (the y 15.9 and y 20.1 eave lines are linked only through the weak axis of R78) |
| B5 | K15-K19 | 46.4 / 28.5 | 0.32 | the x 68 line now has one bay: takes the west strip reaction (49 kN); K15 / K19 keys and rebars pass (0.36) |
| B6 | K14-K18 | 33.6 / 21.7 | 0.22 | east wall line with B9: K14 has Key A only and its parallel-edge value (44 kN at c1 155) needs the line force shared |
| B7 | K20-K27 | 63.1 / 46.2 | 0.41 | the x 77.8 line now has one bay: takes the east reactions of both north strips through R78 (66.8 kN); K20 / K27 key pairs 0.48 / 0.52 |
| B9 | K18-K23 | 30.0 / 19.4 | 0.22 | shares the x 95.5 line with B6 (35.5 kN each) and keeps the net uplift at K18 near zero |

Removed: **B8 (K10-K16)** - the interior X in the hall; its role (west support of the jog panel) is taken by R78 as a strut down to B7. **B10 (K19-K25)** - added at Rev 2 only to keep the net uplift off K19 when the S-wind uplift was 73 kN; with the Rev 3 loads K19 sees 49 kN (rebar 0.36) and B5 alone carries the line.

## 4. Rules respected

- No bay shear towards a free slab edge without a key: every remaining braced-bay base keeps its Rev 5a key pair (K1, K2, K5, K7, K15, K18, K19, K20, K22, K23, K25, K27) or Key A + B (K14); no base type changed.
- Torsion of the L-shape with 5 % eccentricity: rigid-diaphragm and tributary distributions enveloped with the 8 bays (bay forces in the table).
- DCL, q 1.5, tension-only X, L70x7 unchanged; door-free bays for the client: B1 K1-K2, B2 K5-K7, B3 K22-K23, B4 K25-K26, B5 K15-K19, B6 K14-K18, B7 K20-K27, B9 K18-K23 (no interior bay any more).
- Both openings: the stair well is passed by the jog panel (y 24.5-29.3) and R78; the elevator opening lies south of the jog and below the west/east strips - no strip crosses it.
- Thermal path B2 - RT-N-W - y 29.3 - RT-N-E - B1: k_eff 3.0 kN/mm, 15 / 37 kN ULS (wind / erection) on B1, B2 - not governing.

- North-east corner: the last panel of the north strip east (x 92.5-95.5) and the first panel of the east strip (y 29.3-35.7) share the corner cell; both rod sets are kept (different chord/post pairs), gussets combined at K2, K4, K13, K14.

Figure: bracing_rev5.png (columns, primaries, rafters thin; braced strips and wall bays bold).

# Alternative C - fabrication drawing package (detailing)

`C_detail_drawings.dxf` (DXF R2013, `$INSUNITS = 6` metres) generated with ezdxf from the Rev 2 calculation model (`design/C/calc/model.py`, `bracing.py`, `members_C.csv`) and `bases_C.md` Rev 4a. Audit: 0 errors. One model space; each sheet is a 42 x 30 m frame with a title strip (project, sheet title, sheet no., revision "Rev 2 superstructure / Rev 4a bases", date 2026-09-27, scale note). PNG renders `S00.png` ... `S06.png` (3360 x 2400 px) are for checking only.

## Sheets (model-space frame x range, y 8-38)

| Sheet | Title | Frame x | Content |
|---|---|---|---|
| S00 | Sheet index and general notes | 10-52 | index, layers, marks convention, design basis, status |
| S01 | Roof framing plan | 60-102 | **true coordinates** (plan at x 67.89-95.69, y 15.57-35.87): C1-C27 (K1-K27), P1-P19, R1-R11, T1/T2, ST1/ST2, WP1, purlin lines, B1-B10 with X symbols, RT-* rod panels, openings hatched, grids 1-11 / A-H with bubbles, bay and overall dimensions, north arrow, gutter, DP1-DP4, crickets, levels table, detail bubbles, section marks A-A / B-B |
| S02 | Column schedule and wall elevations | 110-152 | schedule (mark, K, section, x/y, L, cap top, base plate top, concrete orientation, HEA web, braced bays, face) + elevations W, E, N, S1 (y 15.57), S2 (y 19.97), notch face; girts, eave beams, bracing X, dimensions, clear heights |
| S03 | Typical sections A-A, B-B, C-C | 160-202 | A-A N-S at x 87.19 (rafter line 8), B-B E-W along row F (y 29.3) with the stair-well upstand, C-C braced line 5 (x 77.78, B7 + B8); true scale, levels in mm |
| S04 | Connection details D1-D10 | 210-252 | drawn **5x** (1 m model = 200 mm real), dimstyle S-MM (dimlfac 200) so DIMENSION text reads true mm; each detail in an 8.2 x 12.8 m frame with bubble and title |
| S05 | Base details and notes | 260-302 | B1 plan (300x400 and 350x400 with Key B) and section 1-1; B2 plan (800x550), section 2-2 across the wall (lever, tip strip, under-slab plate) and 3-3 along it; K21 pier base (P) and WP1; base schedule per column with coring zones; Rev 4a coring criterion; pre-installation checks; materials; erection sequence; tolerances / grout note |
| S06 | Bill of materials | 310-352 | all 116 member pieces (mark, section, L, n, kg, between) from members_C.csv + rod panels, cold-formed totals, plates, bolts and anchors, totals |

## Layers

S-COL (columns, blue), S-PRIM (primaries / eave beams / trimmers, red), S-RAFT (rafters, posts, green), S-PURL (purlins, girts, eave rail, cyan), S-BRACE (wall X bracing and roof rods, magenta dashed), S-OPEN (openings, hatched), S-GRID (grid lines, CENTER linetype), S-DIM (real DIMENSION entities; dimstyles S-M metres 2 dp text 0.25, S-MM details 5x -> mm, S-MM1 sections 1:1 -> mm), S-TEXT, S-TITLE, S-DETAIL, S-HATCH, S-DRAIN (gutter, downpipes, crickets), S-EXIST (existing slab and concrete columns, grey).

## Marks

- `Cn` steel column HEA 160 over existing concrete column `Kn` (n = 1-27); `WP1` wind post at (77.61, 20.25) (Rev 4: 280 mm inboard of the notch corner).
- `P1-P19` primaries / eave beams IPE 330 (level, on cap plates), in the order of `model.py` PRIMARIES; `T1` (y 35.44) / `T2` (y 24.09) trimmers IPE 270.
- `R1-R11` rafter lines IPE 270 west to east (R1 x 67.99 ... R11 x 95.55); pieces `Rn.1, Rn.2 ...` south to north in the BOM (one piece per span between primaries, fin plates D1).
- `ST1` (y 24.46, R9-R11) / `ST2` (y 26.37, R1-R3) roof-truss posts IPE 270.
- `B1-B10` wall X-bracing bays (2 x L70x7 tension-only); `RT-N-W, RT-N-E, RT-S-E, RT-S-W, RT-W, RT-E, RT-JOG` roof rod panels (M24 8.8), pieces `RT-x.i`.
- `D1-D10` connection details (S04); `B1`, `B2`, `P` base details (S05); sections `A`, `B`, `C` (S03).
- Grids: 1-11 on the rafter lines (+8a at x 88.88, K22), A-H on the primary rows (A 15.87, B 20.07, C 21.76, D 24.46, E 26.37, F 29.27, G 35.22, H 35.72).

## Levels

TOS(y) = 3.30 + 0.06 (35.87 - y); primary top = TOS + 0.05; cap-plate top = TOS - 0.28; column length = TOS - 0.34; base plate top +0.065 (40 grout + 25 plate). Clear height under the north eave beam 3.03 m.

## Bases (bases_C.md Rev 4a - final)

- Title strip: "Rev 2 superstructure / Rev 4a bases". Base type per column from `reactions_C.csv` (`base_type`) and `bases_C.md` section 3; the S05 schedule lists type, long axis, keys, bolts / anchors (mm from the column centre, x = E-W, y = N-S), plate, utilisation and the coring zone for every column.
- **B1** (15 bases): plate 300x400x25 at K5, K7, K9, K11, K12, K13, K16, K17, K24, K26; 350x400x25 with Key B dia 60 (180 inboard, c1 250) at K3 (+y), K4 (+x and +y, two keys), K6 (-x), K8 (-x), K14 (+x); 4 M20 8.8 resin anchors 80 x 280 h_ef 200 in the slab (280 along the concrete long axis), Key A SHS 90x90x8 stub 180 embedded in a 140 pocket under the column. Worst K7 0.86.
- **B2** (11 bases): standard plate 800 (along the wall) x 550 (100 out / 450 in) x 30 + two 120x10 stiffeners at K1, K2, K10, K15, K18, K19, K20, K22; K23 1000x550 skewed (bolts (-379, 250)/(-99, 250), keys (-699, 200)/(-99, 200)); K25 550x900 (bolts (250, 0)/(250, 280), keys (200, 0)/(200, 600)); K27 600x900 mirrored. 2 M24 8.8 through-bolts in one row 250 inboard, 280 apart, on a 400x200x25 under-slab plate (ceiling opening ~600x600), tip bearing strip 350x60 at b = 430 (lever 2.39 N_t; 2.59 at K25/K27, 2.93 at K23), SHS 90x90x8 key pair 200 inboard, +/-300 along (K1/K2/K10 y -200, K15/K19 x +200, K18/K20 x -200, K22 y +200). Worst K25 0.83.
- **P** (K21 pier): plate 300x400x25, 4 M16 resin anchors 70 x 280 h_ef 400 into the pier (lap with the pier bars, rebar scan) + saddle 2 x 400x150x15. **WP1**: (77.61, 20.25), plate 250x250x15, one centred dia 60 key (c1 250), 2 M12.
- Coring criterion Rev 4a (= the concrete the checks use): B1 edge heads solid to the face outboard, >= 340 inboard, +/- 400 along; interior B1 centred 400-650 per schedule; B2 the key breakout bodies plus the under-slab plate zone (standard +/- 700 along, to 600 from the face; K23 -1100..+250; K25/K27 to +1000), soffit accessible; K21 scan; 3 trial cores then every head. Slab forces T / C at the B2 bolt rows and tips are listed for the slab designer.
- Grout bed fixed at 40 mm on all drawings (column lengths per the schedule stay TOS - 0.34); bases_C.md checks are valid for 25-40 mm grout.
- BOM (S06): base plates 11 x 300x400x25, 5 x 350x400x25, 8 x 800x550x30 + 3 special (K23/K25/K27) with stiffeners, 11 under-slab plates 400x200x25, 37 SHS keys, 7 dia 60 keys, 60 M20 resin anchors, 22 M24 through-bolts, 4 M16 anchors, K21 saddle, 11 ceiling openings.

## Other open items carried on the drawings

- Gutter west run: drainage report at y 35.37, structure edge kept at y 35.87 (design report open item 6).
- Purlin/girt supplier capacities (uplift >= 9 kNm single span with one anti-sag row), BoardX product data.
- Door-free bays B1-B10 (client), R6 over the shaft east wall line.
- Purlin/girt lengths in the BOM come from the drawn layout (304 m purlins / 267 m girts) and are lower than the report's 372 / 359 m allowance.

## Regenerating

Scripts in `detailing/gen/` (`main.py` with `common.py`, `geom.py`, `s01.py` ... `s06.py`): `cd gen && python3 main.py` writes the DXF, audits it and renders the PNGs (`--norender` skips the renders).

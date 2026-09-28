# Alternative C - fabrication drawing package (detailing)

`C_detail_drawings.dxf` (DXF R2013, `$INSUNITS = 6` metres) generated with ezdxf from the design Rev 3 calculation model (`design/C/calc/model.py`, `bracing.py`, `members_C.csv` Rev 3) and `bases_C.md` Rev 4b, after the final critique C1-C15. Audit: 0 errors. One model space; each sheet is a 42 x 30 m frame with a title strip (project, sheet title, sheet no., revision "Rev 3 superstructure / Rev 4b bases", date 2026-09-28, scale note). PNG renders `S00.png` ... `S06.png` (3360 x 2400 px) are for checking only.

## Sheets (model-space frame x range, y 8-38)

| Sheet | Title | Frame x | Content |
|---|---|---|---|
| S00 | Sheet index and general notes | 10-52 | index, layers, marks convention, design basis, status, existing-structure note (slab-top survey = datum; as-builts and adequacy statement are client / structural open items) |
| S01 | Roof framing plan | 60-102 | **true coordinates**; north face jog (y 35.37 west of x 81.79, 35.87 east), C1-C27 (K1-K27), P1-P19, R1-R11 (R1-R5 end at 35.37), T2, ST1/ST2, WP1, purlin lines, B1-B10, RT-* rod panels, stair well open to the north face (wall header, no roof / eave beam), 0.5 m wall return at x 81.79, gutters G-W (y 35.37) / G-E (y 35.87) with stop ends, spouts, DP1-DP4, crickets, grids 1-11 / A-H, dimensions, levels table (TOS, primary top, column top, L B1 / L B2), detail bubbles, section marks |
| S02 | Column schedule and wall elevations | 110-152 | schedule (mark, K, section, x/y, base type, L col per type, column top, base plate top, concrete orientation, HEA web, braced bays, face) + elevations W, E, N1 (west, y 35.37, with the well header and return post), N2 (east, y 35.87), S1, S2, notch face |
| S03 | Typical sections A-A, B-B, C-C | 160-202 | A-A N-S at x 87.19; B-B E-W along row F with the open stair well beyond; C-C braced line 5 (R5 to y 35.37, B7 + B8); true scale, levels in mm; clear heights printed: 3.02 m under the cap-plate nuts (C1/C2), 3.06 m under the eave primary |
| S04 | Connection details D1-D11 | 210-252 | 5x details: D1 plain fin plate (no slots), D2 cap plate, D3 chord tie, D4 bracing gusset, D5 rod gusset shop-welded to the primary and bolted 2 M16 to the rafter (web hole at R2 / R10), D6 T2 / well upstand, D7 eave and gutter (two runs), D8 purlin cleat, D9 girt and panel, D10 WP1, **D11 wall sill / base rail**, general connection notes (no site welding, thermal +/-20 K) |
| S05 | Base details and notes | 260-302 | B1 plan (300x400 / 350x400 edge heads with Key B) and section 1-1; B2 plan (800 x 550 x 30, 100 outboard), section 2-2 across the wall (lever, tip strip, under-slab plate 400x200x25) and 3-3 along it; K21 pier base (anchor pattern fixed by scan) and WP1; base schedule per column with Rev 4b coring zones; coring criterion; pre-installation checks; materials; erection sequence; tolerances / grout note |
| S06 | Bill of materials | 310-352 | 115 member pieces from members_C.csv Rev 3 + rod panels, cold-formed (purlins, girts, eave rails, well header, sill rail, upstands), plates, bolts and anchors, totals |

## Layers

S-COL (columns, blue), S-PRIM (primaries / eave beams / trimmers, red), S-RAFT (rafters, posts, green), S-PURL (purlins, girts, eave rail, cyan), S-BRACE (wall X bracing and roof rods, magenta dashed), S-OPEN (openings, hatched), S-GRID (grid lines, CENTER linetype), S-DIM (real DIMENSION entities; dimstyles S-M metres 2 dp text 0.25, S-MM details 5x -> mm, S-MM1 sections 1:1 -> mm), S-TEXT, S-TITLE, S-DETAIL, S-HATCH, S-DRAIN (gutter, downpipes, crickets), S-EXIST (existing slab and concrete columns, grey).

## Marks

- `Cn` steel column HEA 160 over existing concrete column `Kn` (n = 1-27); `WP1` wind post at (77.61, 20.25) (Rev 4: 280 mm inboard of the notch corner).
- `P1-P19` primaries / eave beams IPE 330 (level, on cap plates), in the order of `model.py` PRIMARIES; `T2` (y 24.09) trimmer IPE 270 (T1 deleted in Rev 3: the stair well is open to the north face).
- `R1-R11` rafter lines IPE 270 west to east (R1 x 67.99 ... R11 x 95.55); pieces `Rn.1, Rn.2 ...` south to north in the BOM (one piece per span between primaries, fin plates D1).
- `ST1` (y 24.46, R9-R11) / `ST2` (y 26.37, R1-R3) roof-truss posts IPE 270.
- `B1-B10` wall X-bracing bays (2 x L70x7 tension-only); `RT-N-W, RT-N-E, RT-S-E, RT-S-W, RT-W, RT-E, RT-JOG` roof rod panels (M24 8.8), pieces `RT-x.i`.
- `D1-D11` connection details (S04); `B1`, `B2`, `P` base details (S05); sections `A`, `B`, `C` (S03).
- Grids: 1-11 on the rafter lines (+8a at x 88.88, K22), A-H on the primary rows (A 15.87, B 20.07, C 21.76, D 24.46, E 26.37, F 29.27, G 35.22, H 35.72).

## Levels (Rev 3)

TOS(y) = 3.33 + 0.06 (35.87 - y); primary top = TOS + 0.05; column top (cap-plate underside) = TOS - 0.30; column length = TOS - 0.35 (B1: 25 grout + 25 plate) / TOS - 0.355 (B2: 30 plate); base plate top +0.050 (B1) / +0.055 (B2). Clear height 3.02 m under the cap-plate nuts at C1/C2 and 3.06 m under the eave primary (the only clear-height figures printed). The slab-top level survey defines the datum for every column length.

## Bases (bases_C.md Rev 4b)

- Base type per column from `reactions_C.csv` (`base_type`) and `bases_C.md` section 3; the S05 schedule lists type, long axis, keys, bolts / anchors (mm from the column centre, x = E-W, y = N-S), plate, utilisation and coring zone for every column.
- **B1** (13: K3, K4, K6, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26): plate 300x400x25 (350x400x25 at the edge heads K3, K4, K6, K8, K11, K14), 4 M20 8.8 resin anchors 80 x 280 h_ef 200 in the slab, Key A SHS 90x90x8 stub under the column, Key B dia 60 at K3 (+y), K4 (+x, +y), K6 (-x, +y), K8 (-x), K14 (+x).
- **B2** (13: K1, K2, K5, K7, K10, K15, K18, K19, K20, K22, K23, K25, K27): standard plate 800 (along) x 550 (100 outboard / 450 inboard) x 30 + two 120x10 stiffeners; K7 500x1000 skewed, K23 1000x550 skewed, K25 550x900, K27 600x900; 2 M24 8.8 through-bolts in one row 250 inboard, 280 apart, on a 400x200x25 under-slab plate (13 ceiling openings ~600x600); tip bearing strip at b = 430 (lever 2.39 N_t; 2.59 at K25/K27, 2.93 at K7/K23); SHS 90x90x8 key pair 200 inboard, +/-300 along; bolt / key offsets per base in the schedule.
- **P** (K21 pier): plate 300x400x25, 4 M16 resin anchors 70 x 280 nominal h_ef 400 into the pier (lap with the pier bars), pattern fixed on site from the rebar scan, + saddle 2 x 400x150x15. **WP1**: (77.61, 20.25), plate 250x250x15, one centred dia 60 key, 2 M12.
- Coring criterion Rev 4b (= the concrete the checks use): B1 edge heads solid to the face outboard, >= 340 inboard, +/- 400 along; interior B1 centred 400-650 per schedule; B2 the key breakout bodies plus the under-slab plate zone (standard +/- 700 along, to 600 from the face; K7 / K23 -1100..+200; K25 / K27 to +1000), soffit accessible; K21 scan; GPR of all 27 heads plus 3-6 cores (critique), then every head against its own schedule line. Thermal (C4): +9 kN on the B1 / B2 bay shear with wind, 23 kN thermal-leading; no slotted holes anywhere.
- Grout 25 mm nominal (25-40 permitted); column lengths per the schedule.
- BOM (S06): base plates 8 x 300x400x25, 6 x 350x400x25, 9 x 800x550x30 + 4 special, 13 under-slab plates 400x200x25, 39 SHS keys, 8 dia 60 keys, 52 M20 resin anchors, 26 M24 through-bolts, 4 M16, K21 saddle, 13 ceiling openings.

## Open items carried on the drawings (final critique section 5)

- Slab investigation (GPR all heads, 3-6 cores, scans, pull-out tests, ETA group verification) before any anchor; soffit access at the 13 B2 bases.
- As-builts, existing-structure adequacy statement, roof / slab-top survey and datum (C5) - client / structural.
- q_p 1.30 confirmation; rainfall 100 / 150 mm/h; purlin / girt uplift capacities and panel fasteners; BoardX data; seismic floor amplification; slab local check at the B2 bolt rows; north facade at DP3 / DP4 and yard gullies; well outlets, waterproofing, hall-side well walls (blockwork, architect); gutter manufacturer data; notch edge beam at WP1; permit.
- Purlin / girt lengths in the BOM come from the drawn layout (290 / 278 m).

## Regenerating

Scripts in `detailing/gen/` (`main.py` with `common.py`, `geom.py`, `s01.py` ... `s06.py`): `cd gen && python3 main.py` writes the DXF, audits it and renders the PNGs (`--norender` skips the renders).

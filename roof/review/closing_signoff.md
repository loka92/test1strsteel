# Alternative C - closing sign-off (design Rev 3 / bases Rev 4b / sheets S00-S06)

Scripts re-run (`run_all.py`, `write_report.py`): report, members, reactions and `bases_C.md` regenerate byte-identical. Units kN, m, mm.

## 1. Final-critique items in the documents

| Item | Where | Status |
|---|---|---|
| C1 north jog | `model.py` north_edge (35.37 west of x 81.79), rafters R1-R5 end at 35.37, no T1, roofed area **439.3 m2** (my grid 439.3), S01 plan and gutters G-W / G-E with stop ends, S02 elevations N1 / N2, S06 well header | closed |
| C2 column length | column top = cap underside = TOS - 0.30, plate top +0.050 / +0.055, L = TOS - 0.35 / 0.355; S02 schedule K1 2.981, K5 3.011, K7 3.017, K25 4.175 = my values | closed (note X2) |
| C3 clear height | TOS(35.77) 3.336, cap underside 3.036, nuts 3.016 -> **3.02 m**; eave primary 3.056; S01 / S03 print 3036 / 3330 / 3630 only | closed |
| C4 thermal | D1 plain (no slots); k_eff 2.8 kN/mm (bays 23 / 23.6 kN/mm in series with the rod panels and the row-F chord) x 5.36 mm at +/-30 K = **15 kN**, 10 kN at 20 K; ULS +9 kN with wind, 23 kN thermal-leading (16 ULST rows in reactions_C.csv); K1, K2, K5, K7 all B2 | closed |
| C6 sign-off lines | this note; JSON rev4b_status added | closed |
| C7 plate extents | 100 outboard / 450 inboard, one standard 800 x 550; S05 schedule agrees | closed |
| C8 weight | report s.10 quotes **24.9 t**, S06 totals **25.4 t** | correction X1 |
| C10 cleats | 10.8 kN per cleat, plate 0.66; fasteners from the supplier | closed |
| C11 RT-JOG | 50.6 kN rod, 0.25, drawn on S01 | closed |
| C13 K21 | pattern by scan on S05; K7 B2 | closed |
| C14 labels | superseded figures gone from report and S03 | closed |

## 2. Bases Rev 4b sign-off

T1-T6 are closed: per-base B2 plates and coring zones (K7 500 x 1000, K23 1000 x 550, K25 550 x 900, K27 600 x 900, standard 800 x 550 with zone +/-700 along); criterion identical to the extents used (B1 edge heads face / >= 340 inboard / +/-400 along); one rigid-post key-moment model; 0.92 cone factor at K3, K16, K17; under-slab plate 25 mm, class-3 stiffeners, skewed levers and the T / C couple listed for the slab designer; bond with real extents. Spot checks: **K7 B2 0.76** (key pair bearing, ULS2E, V 52.5), **K5 B2 0.57** (key pair outward), K23 0.80, K25 0.83, worst B1 K11 0.72 (cone 50.4 kN, no key moment). The Rev 4 sign-off condition ("K7 and K14 wait for T3") is met: K7 is B2, K14 0.49. Bases Rev 4b: **ACCEPTABLE**.

## 3. Sheets against the model

- **S05 vs bases_C.md Rev 4b**: types (13 B1, 13 B2, P at K21), long axes, plates (300 / 350 x 400 x 25; 800 x 550 x 30 standard; K7, K23, K25, K27 specials), bolt and key offsets (K23 (-380, 250) / (-100, 250) and (-700, 200) / (-100, 200); K7 mirrored), utilisations and coring zones match line by line; criterion, pre-installation checks and erection sequence as the note. BOM plate counts (8 + 6 + 9 + 4, 13 under-slab) agree.
- **S01 / S02 vs the Rev 3 model**: jog at 81.79, levels table (TOS, primary top, column top, L B1 / L B2) equals `model.py`; schedule lengths and base types equal `reactions_C.csv`; WP1 at (77.61, 20.25); bay list B1-B10 and rod panels as `bracing.py`.

## 4. Findings

**X1 - MINOR - Weight.** S06 gives 25.4 t (hot-rolled 14.9, plates 3.6, bracing 0.96, rods 1.30, cold-formed 4.6); the report still quotes 24.9 t, the BOM before the Rev 4b base plates, sill rail (0.40 t) and well header (0.22 t). Quote 25.4 t in report s.10 and in the cost line (+~1,000 $).

**X2 - MINOR - Column length and grout range.** L = TOS - 0.35 assumes a 25 mm bed; the permitted 25-40 mm range lifts a cap by up to 15 mm against the +/-5 mm primary tolerance. State on S02 that column lengths are cut to the surveyed plate-top level (cap underside - survey) and the bed is 25 +/- 5 mm; 40 mm only with a re-cut column.

**X3 - MINOR - Thermal model.** The rod panels are summed in parallel and the chord taken as 4.07 m: an elastic upper bound on the force, as stated; acceptable, no change.

| ID | Severity | Item | Fix |
|---|---|---|---|
| X1 | MINOR | Report 24.9 t vs BOM 25.4 t | Quote 25.4 t; cost +1,000 $ |
| X2 | MINOR | Grout 25-40 vs fixed column length | Cut to survey; bed 25 +/- 5 on S02 |
| X3 | MINOR | Thermal upper bound | None |

## 5. Verdict

**ISSUE WITH CORRECTIONS** (X1, X2: text on the report and S02, no recalculation). The conditions precedent remain as carried on S00 / S05: GPR of all 27 heads plus 3-6 cores, rebar scans, pull-out tests and ETA verification before any anchor; soffit access at the 13 B2 bases; as-builts, existing-structure adequacy statement and slab-top survey (C5); q_p, purlin / girt uplift and BoardX data from the suppliers; seismic floor amplification (F9) still open.

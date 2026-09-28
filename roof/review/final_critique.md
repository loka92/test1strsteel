# Final critique - Alternative C package (superstructure Rev 2, bases Rev 4a, drainage, sheets S00-S06)

Earlier findings (F, R, S, T series) were not repeated; their closure was checked in code, note and drawings.

## 1. Verdict: DO NOT ISSUE (as it stands)

The calculations are sound, every earlier finding except F9 is closed, and the concept (three sections, two connection types, pinned columns centred on the concrete columns, ten X-bays, per-base anchorage with the real slab edges) is right for this client. The fabrication drawings cannot go out: they wall and roof a 0.5 x 13.9 m strip outside the building (the west block's north face is at y 35.37, not 35.87), draw one gutter across the open stair well, and cut all 27 columns 25 mm too long. With C1-C6 corrected (about a week) the package becomes ISSUE WITH CORRECTIONS.

## 2. Defects

| Id | Sev. | Docs | What is wrong | Required correction | Owner |
|---|---|---|---|---|---|
| C1 | BLOCKER | load_basis; report item 6; model.py (ENV y1 = 35.87, wall N at 35.87 for all x); S01, S02, S06 | geometry.json (interior_walls_y 35.17/35.37, K5-K7 faces at 35.37, rooms SERVICES/STAIR to 35.4): the north face jogs, 35.37 for x 67.89-81.79, 35.87 east of it. Drainage is right. The model walls and roofs to 35.87 everywhere: BoardX 0.5 m outside the slab, T1 and 4.07 m purlins over a strip north of the open well, 446 m2 not 439, one gutter drawn across the well. | Draw the jog: wall and eave at 35.37 west of x 81.79 (rafter cantilever 0.10-0.20 m past P1/P2), delete T1 and the stair-strip purlins, 0.5 m wall return beside K3, gutters with stop ends at 77.89/81.79; re-run the take-down; re-issue S01-S03, S06. | structural + detailing |
| C2 | MAJOR | report s.1; README; S01 levels; S02 schedule | Column length TOS - 0.34 ignores the 20 mm cap plate: column top 25 mm above the cap-plate underside (TOS - 0.30); all 27 columns too long. | L = TOS - 0.365 (25 mm plate) / TOS - 0.370 (B2); re-issue the schedule. | detailing |
| C3 | MAJOR | brief; report F11; S00 (3.03); S02/S03 (3.02); D2 | At y 35.77: primary bottom 3.026, cap-plate underside 3.006, M20 nuts under it 2.99 m at seven north-row columns; three figures printed. | Raise the plane 30 mm (TOS(35.87) = 3.33) or record the client's acceptance of 2.99 m under the cap nuts; print one figure. | structural + client |
| C4 | MAJOR | load_basis (temperature); report item 8; D1 slots on row F; D5 | E-W thermal restraint is B2 - RT-N-W - y 29.3 chord - RT-N-E - B1. Slotting the row-F fin plates does not release it, is bridged by the rod gussets welded to both webs, and removes the bottom-flange restraint used in the primary LTB check. Locked-in force ~8 kN/mm x 5-10 mm = 40-80 kN, like a bay shear. | Delete the slots; state the conditioned-hall range (say +/-15 K); check B1/B2 and bases K1, K2, K5, K7 for wind + thermal; K7 (0.85 on an 18.5 kN parallel-edge value) becomes B2 with inboard keys if it fails. | structural |
| C5 | MAJOR | whole package | Nothing on the existing structure (~440 kN added gravity, ~150 kN char roof-level wind into 27 pinned 20x40 columns and foundations); no as-builts; no roof survey (screed thickness = datum for the 3.0 m and base seating, parapet, plant, lift overrun). | As-builts from the client; one-page adequacy statement; roof survey before cores; slab-top datum on S00. | structural + client |
| C6 | MAJOR | rev4 sign-off; findings JSON; S05 | T1-T3 were to close "before base drawings issue"; S05 went out on Rev 4a with no sign-off and no Rev 4a column in the JSON. Spot check: T1-T6 closed (criterion 340/+-400, rigid-post model, K7 0.85 = reactions_C.csv) except C7. | Reviewer adds the Rev 4a line and a short sign-off. | reviewer |
| C7 | MINOR | bases_C.md s.1/s.3; README; S05 | B2 plate extents in the table give 50 mm outboard (HEA 160 flange tip at 76 overhangs); s.1 says 700 long vs 800; K10/K20/K22 600 across vs 550 on S05. | Table to -450..+100; one length; reconcile 550/600. | structural |
| C8 | MINOR | report s.10; S06 | 23.4 t vs 24.9 t: plates 1.53 t assumed vs 3.4 t counted; purlins/girts 731 vs 571 m. | Quote the BOM: 24.9 t. | structural |
| C9 | MINOR | D5; concept "no site welding" | Rod gussets welded to both webs of two site-bolted members = overhead site welding on galvanised steel at ~96 corners; rod hole in the R2/R10 web not shown. | Shop-weld to the primary only or bolt; show the web hole. | detailing |
| C10 | MINOR | D8; report s.4 | Purlin-cleat uplift (~11 kN per cleat on zone-F spans) and panel fastener count in F/G unstated. | Cleat check; fastener schedule from the supplier. | structural + supplier |
| C11 | MINOR | report s.8 | Text says the north-band shear passes "through the jog panel"; table: RT-JOG 0.0 kN. | Delete RT-JOG or fix the text. | structural |
| C12 | MINOR | D9; drainage item 4 | No wall sill at the slab edge (bottom girt at 0.50 m); parapet unknown; hall-side well walls have no structural owner. | Sill detail; well walls as blockwork on the existing well walls. | architect + detailing |
| C13 | MINOR | bases_C.md | K7 0.85 on a plain-concrete edge value beside an assumed slab opening (0.95 at +10 % wind); K21 anchors 9 mm from the pier bars. | See C4; K21 pattern set by the scan, say so on S05. | structural |
| C14 | MINOR | comparison; decision_summary; S03 | Superseded figures (8 bays, 20.5 t; "clear under P4 3020" vs 3026). | Mark superseded; fix labels. | structural |
| C15 | MINOR | bases_C.md; S05 | Six base variants. B2 everywhere would drop the cone checks and the coring criterion for 16 more ceiling openings. | Offer the client the choice. | client |

## 3. Load path, once

Panel screws - Z200 purlins at 1.5 m - 2 M12 cleats - IPE 270 rafters, fly braces under uplift - fin plates 2 M20 (reversible; they also carry the rafter's truss-post axial force, unstated but far inside 188 kN) - IPE 330 primaries - cap plates, 4 M20 in tension for 67 kN uplift - HEA 160 columns - B1 resin anchors (cone in the slab) / B2 through-bolts (lever, under-slab plate) / P pier anchors - column head. Shear never passes through anchors: grouted SHS keys, Key B bars, K21 saddle. Walls: BoardX - girts - column flanges - wL/2 to the keys, wL/2 through the cap bolts into the primaries - primaries as chords, rafters as posts, M24 rod panels as diaphragm, tie plates at K10/K11 - ten L70x7 X-bays - gussets - keys - slab. Gutter loads are in the take-down. Weak or missing links: C4, C5, C9, C10, C12.

## 4. Client constraints and buildability

Openings unroofed: yes (R6 at 81.85 sits on the shaft's east wall, client to confirm). One plane at 6 %: yes. 3.0 m clear: 3.026 under the eave primary, 2.99 under the cap nuts (C3). Concrete columns untouched except K21: yes, though 37 pockets and 22 holes enter the slab over the heads. Columns centred on columns: yes. Simplicity: three sections, one fin plate, one cap plate, ten details - good; six base variants and a four-stage site verification are the price of the slab (C15). Tripoli parameters agree across all documents.

The S05 erection sequence is sound (cores/scans/tests, pockets, columns on keys and grout with temporary guys, anchors drilled through the plates after cure, primaries before rafters). Eleven through-bolt bases need the soffit (kitchen, services, both side walls, terraces): a night each. The coring criterion equals the checks, but "solid over +-700 along the wall" at B2 heads presumes hidden beams along the wall lines (usual in Libyan hollow-block slabs, never stated): specify GPR of all 27 heads plus 3-6 cores, not "60 mm cores against the schedule". Tolerances (base +/-10, primary +/-5, grout 25-40) absorb the slab; C2 would eat the grout range. Galvanising with bolted site work is consistent except C9.

## 5. Consolidated open items (owner - consequence if not closed)

1. Slab investigation: GPR all heads, 3-6 cores, thickness >= 250, C25, solid extents per the S05 line; rebar scans; pull-out tests; ETA group verification - site/structural/supplier - base types change or head-drilling fallback; no anchor before.
2. Soffit access at 11 B2 bases - client - inaccessible head falls back to head drilling.
3. As-builts, existing-structure adequacy, roof survey and datum (C5) - client/structural - permit refused; headroom and base seating undefined.
4. q_p 1.30 confirmation (LNMC) - structural - K7 0.95 at +10 %.
5. Rainfall 100/150 mm/h - mechanical - gutter at 0.93 at 150.
6. Purlin/girt uplift >= 9 kNm with one anti-sag row; sleeved girts; panel fasteners - supplier - purlin order.
7. BoardX data: weight, span, fixings, drift limit - client/supplier - girt rows, sway limit.
8. Seismic floor amplification (two-mass) - structural - bracing has 2.5x reserve.
9. North edge jog - resolved here: 35.37 west of x 81.79 (C1) - drawings.
10. Door-free bays B1-B10, B8 visible in the hall, R6 over the shaft wall - client - bracing layout.
11. Thermal check (C4) - structural - K7 base.
12. Slab local check at the B2 bolt rows (K19 175/102 kN couple) - structural - B2 unproven.
13. North facade at DP3/DP4, height to grade, yard gullies 12.6 l/s - client/mechanical - downpipes discharge nowhere.
14. Well outlets, existing pipes, waterproofing, thresholds, hall-side well walls - architect - wells flood the hall.
15. Gutter manufacturer data - supplier. 16. Notch edge beam at WP1 - site.
17. Permit: change of use, fire, escape, lift, Libyan engineer's stamp - client.

## 6. Cost update (same indicative MENA rates as the 80,000 $ figure)

| Item | Earlier | Now | Why |
|---|---|---|---|
| Steel fabricated, erected | 20.5 t, 41,000 $ | 24.9 t (BOM), 49,800 + ~2,000 for the heavy base plates | two more bays, M24 rods, posts, 3.4 t plates |
| Roof panel | 18,000 | 18,000 | 439 m2 |
| Wall cladding 405 m2 | 14,100 | 14,100 | jog neutral |
| Bases | 6,800 | 17,000: 44 cored pockets 3,500; 22 through-holes + 11 ceiling openings, night work 4,500; anchors and bolts 2,700; GPR + cores + lab 4,000; pull-out tests 1,000; finishes cut/resealed 1,300 | anchorage on an unknown slab |
| Gutters, 4 RWPs, outlets, spouts | - | 3,000 | not in the earlier figure |
| Well upstands, flashings, cricket, outlets | - | 3,000 | not in the earlier figure |
| **Total** | **80,000** | **~107,000 $ (+34 %)** | |

Risk: all-B2 fallback +6,000 $; steel rate to include hot-dip galvanising (else +7,000 $).

## 7. Authority / independent checker

Would reject today: no existing-structure statement or as-builts (C5); drawings inconsistent with the site (C1, C2); anchorage conditional on tests not yet done (tolerable only because the S05 decision tree exists); wind unconfirmed locally. The permit for an enclosed second floor (fire, escape, lift) is outside this package. Eurocode with the Tripoli parameters passes with a licensed Libyan engineer's stamp.

## 8. Closing opinion

The client asked for a simple, repetitive, bolted roof on the existing slab, one plane at 6 %, 3.0 m clear, openings left open, columns on columns. The superstructure delivers that and has survived a hard review. What the client did not ask for, and now owns, is the anchorage: the hollow-block slab turns every base into a small investigation (GPR, cores, tests, two base families, eleven ceiling openings) and adds a third to the cost - the honest price of this slab, not a design fault. The drawings are not yet what was asked for: a wall over the yard and columns cut to the wrong length. Fix C1-C6, re-issue, build.

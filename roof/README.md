# Steel and sandwich-panel roof over the existing slab - Tripoli - design package

Alternative C: post-and-beam braced steel frame, all pinned, single 6 % plane falling north, PIR 50 mm roof, BoardX walls.
Status: design Rev 3 / bases Rev 4b / drawings Rev 3 - closing sign-off "ISSUE WITH CORRECTIONS", corrections X1-X2 applied (2026-09-28).

| Folder / file | Content |
|---|---|
| brief.md | Client brief Rev 0-3 (interview, revisions, decisions) |
| geometry.json, column_plan.png | 27 concrete columns, envelope, openings, slope |
| systems/ | Three system proposals (A portal, B truss, C post-and-beam), comparison.md (technical, cost, programme), three_systems.dxf |
| design/load_basis.md | Binding load and material basis Rev 2 (Eurocode, Tripoli wind/rain, anchorage) |
| design/A/ | Alternative A design (closed after review) |
| design/C/ | Alternative C design: design_report_C.md (Rev 3), bases_C.md (Rev 4b), members_C.csv, reactions_C.csv, framing_C.png, calc/ (re-runnable: python3 calc/run_all.py; python3 calc/write_report.py) |
| drainage/ | EN 12056-3 rainwater design: report, layout, gutter section, loads |
| review/ | Independent reviews (A, C), base re-reviews Rev 2-4, decision_summary.md, final_critique.md, closing_signoff.md, findings JSON |
| detailing/ | C_detail_drawings.dxf (sheets S00-S06), renders S00-S06.png, README.md, gen/ (generator) |

Conditions precedent before any site work (owners in review/final_critique.md section 5 and closing_signoff.md):
1. Client: as-built drawings of the slab, columns and foundations; adequacy statement for the added roof load; slab-top level survey (datum for the 3.0 m clear height and the column cut list).
2. Site: GPR scan of all 27 column heads, 3-6 cores, pull-out tests, ETA verification of the anchors; soffit (ceiling) access at the 13 through-bolt bases.
3. Supplier data: local q_p confirmation, purlin/girt uplift capacities, BoardX panel data and fastener schedule, rainfall intensity from the Libyan National Meteorological Centre.
4. Client confirmation: the 10 braced wall bays are door-free; base option (13 anchor + 13 through-bolt bases as designed, or through-bolts at all 27).

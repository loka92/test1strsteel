# Steel and sandwich-panel roof over the existing slab - Tripoli - design package

Alternative C: post-and-beam braced steel frame, all pinned, single 6 % plane falling north, PIR 50 mm roof, BoardX walls.
Status: design Rev 7 (reduced roofed area 316 m2, brief Rev 8, 2026-09-29) - no detailing; offer Rev A issued on it. Rev 6a (439 m2) with drawings S00-S06 and offer RTV-2026-01 remains the detailed reference set.

| Folder / file | Content |
|---|---|
| brief.md | Client brief Rev 0-8 (interview, revisions, decisions) |
| geometry.json, column_plan.png | 27 concrete columns, envelope, openings, slope |
| systems/ | Three system proposals (A portal, B truss, C post-and-beam), comparison.md (technical, cost, programme), three_systems.dxf |
| design/load_basis.md | Binding load and material basis Rev 2 (Eurocode, Tripoli wind/rain, anchorage) |
| design/A/ | Alternative A design (closed after review) |
| design/C/ | Alternative C design Rev 6a (full L-shape): design_report_C.md, bases_C.md (Rev 8), members_C.csv, reactions_C.csv, framing_C.png, calc/ (python3 calc/run_all.py; python3 calc/write_report.py) |
| design/C7/ | **Design Rev 7, reduced roofed area** (architect's plan A_103): design_report_C7.md, members_C7.csv, reactions_C7.csv, framing_C7.png, view3d_C7.png, calc/ (python3 calc/run_rev7.py; python3 calc/write_report_rev7.py; sensitivities with SENS=tag QP_SCALE=.. E_ZONE=.. G_WALL_SEIS=..) |
| drainage/ | EN 12056-3 rainwater design: report, layout, gutter section, loads |
| review/ | Independent reviews (A, C), base re-reviews Rev 2-4, decision_summary.md, final_critique.md, closing_signoff.md, findings JSON |
| offer/ | Offers RTV-2026-01 (Rev 6a, 404,000 LYD) and **Rev A (design Rev 7, 284,000 LYD)**, internal pricing, bilingual section tables (Rev 6a and Rev 7) |
| review/ | architect_set_A101-A103_review.md: review of the architect's facade set |
| detailing/ | C_detail_drawings.dxf (sheets S00-S06), renders S00-S06.png, README.md, gen/ (generator) |

Conditions precedent before any site work (owners in review/final_critique.md section 5 and closing_signoff.md):
1. Client: as-built drawings of the slab, columns and foundations; adequacy statement for the added roof load; slab-top level survey (datum for the 3.0 m clear height and the column cut list).
2. Site: GPR scan of all 27 column heads, 3-6 cores, pull-out tests, ETA verification of the anchors; soffit (ceiling) access at the 13 through-bolt bases.
3. Supplier data: local q_p confirmation, purlin/girt uplift capacities, BoardX panel data and fastener schedule, rainfall intensity from the Libyan National Meteorological Centre.
4. Client confirmation: the 10 braced wall bays are door-free; base option (13 anchor + 13 through-bolt bases as designed, or through-bolts at all 27).

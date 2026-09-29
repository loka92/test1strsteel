# Steel and sandwich-panel roof over the existing slab - Tripoli - design package

Alternative C: post-and-beam braced steel frame, all pinned, single 6 % plane falling north, PIR 50 mm roof, BoardX walls.
Status: design Rev 8a (reduced roofed area 316 m2, economic scheme on 23 existing columns, brief Rev 9, 2026-09-29) - no detailing; offer Rev D issued on it (Rev A-C superseded). Rev 6a (439 m2) with drawings S00-S06 and offer RTV-2026-01 remains the detailed reference set.

| Folder / file | Content |
|---|---|
| brief.md | Client brief Rev 0-8 (interview, revisions, decisions) |
| geometry.json, column_plan.png | 30 concrete columns (K28-K30 added 29 Sep 2026 from the re-issued Drawing 3), envelope, openings, slope |
| systems/ | Three system proposals (A portal, B truss, C post-and-beam), comparison.md (technical, cost, programme), three_systems.dxf |
| design/load_basis.md | Binding load and material basis Rev 2 (Eurocode, Tripoli wind/rain, anchorage) |
| design/A/ | Alternative A design (closed after review) |
| design/C/ | Alternative C design Rev 6a (full L-shape): design_report_C.md, bases_C.md (Rev 8), members_C.csv, reactions_C.csv, framing_C.png, calc/ (python3 calc/run_all.py; python3 calc/write_report.py) |
| design/C7/ | **Design Rev 8a (current): reduced roofed area, economic scheme, 23 columns** - design_report_C7_rev8a.md (Rev 8: design_report_C7_rev8.md), members_C7.csv, reactions_C7.csv, framing_C7.png, view3d_C7.png (all Rev 8); design_report_C7.md = Rev 7 (heavy set); calc/ (python3 calc/run_rev7.py; python3 calc/write_report_rev8a.py; Rev 7 / 7b by env vars, see model.py; sensitivities SENS=tag QP_SCALE=.. E_ZONE=.. G_WALL_SEIS=..) |
| drainage/ | EN 12056-3 rainwater design: report, layout, gutter section, loads |
| review/ | Independent reviews (A, C), base re-reviews Rev 2-4, decision_summary.md, final_critique.md, closing_signoff.md, findings JSON |
| offer/ | Offers RTV-2026-01 (Rev 6a), Rev A / Rev B (Rev 7, superseded), internal pricing, bilingual section tables (Rev 6a, Rev 7), **cost_sections_invoice*.md: section costs at the supplier's quotation (Rev 7 and Rev 8)** |
| review/ | architect_set_A101-A103_review.md: review of the architect's facade set |
| detailing/ | C_detail_drawings.dxf (sheets S00-S06), renders S00-S06.png, README.md, gen/ (generator) |

Conditions precedent before any site work (owners in review/final_critique.md section 5 and closing_signoff.md):
1. Client: as-built drawings of the slab, columns and foundations; adequacy statement for the added roof load; slab-top level survey (datum for the 3.0 m clear height and the column cut list).
2. Site: GPR scan of all 27 column heads, 3-6 cores, pull-out tests, ETA verification of the anchors; soffit (ceiling) access at the 13 through-bolt bases.
3. Supplier data: local q_p confirmation, purlin/girt uplift capacities, BoardX panel data and fastener schedule, rainfall intensity from the Libyan National Meteorological Centre.
4. Client confirmation: the 10 braced wall bays are door-free; base option (13 anchor + 13 through-bolt bases as designed, or through-bolts at all 27).

# Review of the architect's set A_101 - A_103 (ALWATD Architects, "S_NEW_FACADE.pdf", 29 Sep 2026)

Sheets: A_101 South facade 1:100 + curtain-wall schedule; A_102 3D view; A_103 "2ND LEVEL" plan 1:100 + gypsum-wall schedule. A2 landscape, Revit output.

## Reading of the set against the steel roof design (Rev 6a)
- Levels: street 0.00, yard 0.15, ground 0.75, 1st 4.45, 2nd 8.10, roof 11.40, tower cap 13.40. The "2ND LEVEL" plan is the rooftop hall on the existing slab (+8.10). Roof level 11.40 = 3.30 m above the slab = our north-eave TOS 3.33 m.
- The architect's roof is drawn FLAT at 11.40 with a 0.60 m fascia. Our roof is one plane at 6 % falling north: south edge TOS 4.55 m above the slab (about +12.65). The south elevation and the 3D do not show this; the fascia, the 2nd-level strip windows CW_01 and the tower junction all change.
- Roofed area: the architect's note says 300 m2 of sandwich roof; the plan encloses only the west block (x 67.9-77.9, y 20.0-35.4) and the east block north of y about 24.5-25.4. The SW terrace (railing, 45 l.m.) and the 14.05 x 5.35 m strip along the south of the east wing (with the pyramid skylight) stay open. Our brief Rev 1 roofs the whole L (439 m2 net). Difference about 140 m2, 7 of the 27 columns (K21-K27) outside the enclosed area.
- The "elevator shaft" opening of Drawing 3 (x 77.9-82.0, y 20.2-24.2) is a light well with a pyramid skylight on the flat roof of the 1st floor. Trimmer T2 and the opening detail are then not needed.
- Two new lifts in a 13.65 m tower (CW_03) east of the existing envelope (x > 95.7), landing at the east end of the 2nd-level corridor (y about 25.4-29.3). Our braced bay B6 (K14-K18, east wall, y 24.5-29.3) sits exactly on the lift lobby wall: clash. The tower also needs a movement joint and flashing against the roof edge, and its own structure and foundations.
- Walls: all 2nd-level walls, external and internal, are "20 cm GYPSUM" (881 m2 two-face, about 125 m of wall), not BoardX panels on girts. Wall girts (271 m Z200) fall away; wall heads need deflection heads under the rafters and a raked top under the slope; the wall weight (gypsum block 1.0-2.0 kN/m2 or drywall 0.5 kN/m2) sits on the existing slab and, tied at the head, adds roof-level seismic mass (up to +200-250 kN against 440 kN roof) - the two-mass check and the bracing must be re-run.
- Three 0.20 m posts at 4.0 m spacing on the south wall of the east block (x about 85.5, 89.7, 93.9, y about 25) are not on the structural column plan (Drawing 3 has K16, K17, K18 only on y 24.46): new mullion posts or a drafting inconsistency.
- Wind reference height: load basis uses z_e = 9-10 m (single-storey building assumed). The set shows a two-storey building with the hall at +8.10 and the roof top at about +12.7: z_e about 12.7 m, q_p from the north +8 % (1.25 -> 1.35 kN/m2). Purlins (0.41), rafters (0.69) and columns (0.80) have margin; re-check formally.
- No north elevation: gutter 150 x 100 and the four dia 100 downpipes on the north facade are not shown anywhere in the set.
- Strip windows CW_01 (module 2.00 x 2.20, 104 m2) along the 2nd level: window head is level while the eave rises, so the wall above the head varies 0-1.2 m unless the windows follow the slope.

## Drafting notes
- Title block placeholders unfilled: Client Name, Project Name, Project Number, Issue Date, Author, Checker, "Unnamed", and "Organization Name" sitting in the Total Area field. Floor Area empty. A_102 has no scale.
- Arabic address text is rendered with disconnected letters (font shaping); the Arabic notes are fine.
- View names left as Revit defaults: "{3D} Copy 1", "Wall Schedule 2 Copy 1", "South_Facade".
- "curtin grass" should read "curtain glass"; type mark "CW04" vs "CW_01/02/03"; "PRPT", "LEFT_CAP", "FENCE LEVEL" level names; Arabic note "300 m2 m" has a stray unit.
- A_101 wall schedule split: the "COBEST FACADE 2" group header is orphaned at the foot of the left table and continues in the right table.
- A red dashed section/callout marker runs through the middle of the facade with no matching section sheet.
- The plan has no grid lines, room names, level tag, section marks or door/window tags; the wall schedule lists 40 segments by area only.
- The plan's north arrow, scale bar and the 1:100 title are present; the elevation dimensions are readable at A2.

## What this changes for the roof package if the architect's layout stands
1. Roof boundary shrinks to the enclosed area (about 300-320 m2), stepped south edge (y 20.0 west, y 24.5 east), 20 columns instead of 27, no south-eave rows at y 15.9 and y 20.1, bays B3 and B4 disappear, B6 clashes with the lifts: bracing re-plan.
2. Steel about 25-30 % less (roughly 5-6 t, 40,000 LYD); roof panels 300 m2 (about 47,000 LYD); offer price falls accordingly.
3. Load basis: z_e 12.7 m, gypsum wall mass in the seismic appendage check, wall heads restrained by the roof steel.
4. Architect to show the 6 % slope (or a parapet hiding it), the gutter/downpipes on the north facade, and the tower/roof junction; confirm the wall system and the three extra posts.

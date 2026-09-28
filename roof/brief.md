# Design brief – steel and sandwich-panel roof over existing restaurant roof slab

Agreed with the client in interview on 2026-09-27.

## Site and codes
- Location: MENA region, city not given. Design to **Eurocode** (EN 1990/1991/1993/1998) with generic parameters.
- Assumed: basic wind velocity v_b = 30 m/s (10-min mean), terrain category II; no snow; seismic low-moderate a_g = 0.10 g; temperature -5 to +50 C.

## Existing structure (from Drawing 3.dxf, units metres)
- Single-storey restaurant, L-shaped, outer faces x 67.89-95.69 (27.8 m E-W) and y 15.57-35.87 (20.3 m N-S).
- 27 concrete columns C1 20x40 cm, 6 dia14, stirrups dia6/20 (coordinates in geometry.json).
- **There is a complete concrete roof slab on top of these columns. The slab is a hollow-block (ribbed) slab.** Thickness and concrete grade unknown: assume 250 mm ribbed slab with solid zones at column heads, C25.
- **No change to the existing concrete columns is permitted.**
- The new steel structure is built ON TOP of the slab. New steel columns are bolted to the slab directly above the concrete columns (27 positions). Anchors must land in the solid concrete over the column heads / drop beams; no new concrete columns.

## Architecture
- Cover the **whole footprint including the terraces** (full L-shape).
- Space under the new roof is an **enclosed rooftop hall**, air-conditioned.
- Roof: **mono-pitch falling to the NORTH** (kitchen/services side is north on the plan, terraces are south). Low eave on the north edge.
- Clear height under steel at the low (north) eave: **3.0 m** above the slab. Slope to be chosen by the structural agents (5-10 % typical for sandwich panels; state the value).
- Roof cladding: **PIR/PUR sandwich panel 50 mm** (about 0.12 kN/m2), on cold-formed Z purlins.
- Outer walls: **"BoardX" panels** (client's term; treated as lightweight board wall cladding on cold-formed girts, assume 0.30 kN/m2 of wall incl. framing; confirm product data). Walls span between steel columns on the perimeter.

## Loads (additional to self-weight)
- Services (lighting, fans, light services): 0.20 kN/m2.
- Imposed roof load (not accessible, maintenance only): 0.60 kN/m2 (EN 1991-1-1 category H, national annexes vary) - or 0.40 kN/m2 with note.
- No solar, no HVAC on roof, no signage.

## Drainage
- Gutter along the **north** low eave; **external downpipes on the north facade** to ground drains.
- Assumed rainfall intensity 100 mm/h (2-min, MENA thunderstorm); confirm locally.

## Materials and constraints
- Steel: European sections IPE/HEA/UPN, **S275**; cold-formed Z purlins/girts S350GD; bolts 8.8.
- **Simplicity is the priority**: repetitive members, bolted site connections, standard details, minimum number of different sections.
- Restaurant operation during works: not constrained by the client.

## Open assumptions to be confirmed by the client
1. Slab thickness, block type, solid-zone extent at column heads, concrete grade.
2. Wind speed / seismic zone for the actual city.
3. "BoardX" wall panel product data (weight, span, fixing).
4. Whether the stair and elevator penetrate the new roof (assumed: they stop at the existing slab; a roof access hatch/stair is not part of this scope).

## Revision 1 (client markup, 2026-09-27)
- **Roof openings**: the stair well (x 77.89-81.79, y 29.37-35.37) and the elevator shaft (x 77.89-81.99, y 20.17-24.16) are **not roofed**. They are openings in the sandwich roof: trimmer members around each opening, upstand and flashing on all sides, panels stop at the trimmers. The steel framing may pass beside them but not over them.
- **Single-stage slope**: the roof is ONE plane at ONE constant pitch, falling north from the south edge (y 15.57, high) to the north edge (y 35.87, low). No steps, no change of pitch, no separate slopes for the north block and the hall. Pitch 6 % -> total rise 1.22 m over 20.3 m; low eave 3.0 m clear at the north edge.
- Roof boundary confirmed as the outer faces of the L-shape (yellow line on the client's markup); notch remains outside.

## Revision 2 (client decisions after the independent review, 2026-09-27)
- **Alternative C (post-and-beam braced frame) is carried forward.** Alternative A is closed.
- **Anchorage: resin anchors drilled 300 mm into the column heads are permitted** (client waives "no changes to the concrete columns" for the anchor holes only). Anchors must sit inside the column core (clear of the 6 dia14 bars and inside the stirrups); a rebar scan at every column head before drilling is mandatory. Anchors are not to resist shear towards a free slab edge: a grouted shear key or through-bolt is used where the base shear points towards the slab edge.
- **Site: Tripoli, Libya.** Design parameters set in load_basis.md Rev 2: coastal site (Mediterranean 0.3-2 km to the north), basic wind velocity v_b = 27 m/s (10-min mean, 50-year), terrain category I for winds from the sea -> q_p = 1.25 kN/m2 at z_e = 10 m; design keeps the binding q_p = 1.30 kN/m2 (4 % margin). Rainfall for gutters: 100 mm/h (5-min, about 2-year return) design and 150 mm/h (about 10-year) overflow check, 380 mm/year, no snow. Seismic: Tripoli low seismicity, a_g = 0.05-0.10 g, keep 0.10 g check. Temperature -2 to +48 C (Ghibli), design range +/-30 K.
- Next steps: re-run C with load basis Rev 2 and the review fixes; re-review the bases only; then detailing and final critique.

## Revision 3 (after the final critique, 2026-09-28)
- North wall jog confirmed from Drawing 3: the west block's north face is at y 35.37 (x 67.89-81.79); the kitchen's at y 35.87 (x 81.79-95.69). The stair well reaches the north face. Roof and walls follow the jog; the 0.5 m strip north of the west block is outside the building.
- Roof plane raised 30 mm: TOS(y) = 3.33 + 0.06 (35.87 - y), so the clear height under the cap-plate nuts at the north eave is >= 3.00 m.
- Existing structure (client items, open): as-built drawings of the slab and columns (slab thickness, hidden beams on the wall lines, C25, foundations); a one-page adequacy statement for the added roof load (about 440 kN gravity, 150 kN roof-level wind) is to be produced once the as-builts arrive; a level survey of the slab top (screed thickness) fixes the 3.0 m datum and the base seating before any coring.
- Base option for the client: 15 drilled-anchor bases + 11 through-bolt bases (as designed) or through-bolts at all 27 bases, which removes the per-head coring criterion at the cost of 16 more ceiling openings.

## Revision 4 (client decisions, 2026-09-28)
- **No through-bolts at any column.** Every base is anchored from above into the slab / column head (post-installed anchors). Drilling into the column heads remains permitted (Rev 2).
- **The ribbed (hollow-block) slab is 300 mm thick** (not 250 mm as assumed). Solid zones at the column heads and on the wall lines still to be confirmed by scan and cores.
- 3D concept model requested for understanding of the column / beam / bracing system.
- Detailing will be reviewed again after the base redesign and the 3D model.

## Revision 5 (client, 2026-09-28)
- **Ignore the BoardX wall cladding and girt weight** (0.30 kN/m2 of wall) in the design: no wall self-weight on the perimeter columns. The walls still exist as wind-loaded surfaces (enclosed hall), so wall wind pressure and internal pressure remain.
- Client considers the load assumptions and combinations possibly overestimated: an independent load critic reviews load_basis.md Rev 2 before any further design work.

## Revision 6 (client, 2026-09-28)
- **Rationalise all bracing**: check every roof-plane rod panel and every wall braced bay; remove all that are unnecessary; keep only what the diaphragm and the lateral system need on load basis Rev 3 (seismic-governed). Design change only; detailing remains frozen.

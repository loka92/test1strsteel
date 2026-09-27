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

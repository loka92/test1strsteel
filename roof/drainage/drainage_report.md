# Rainwater drainage – steel and sandwich roof over the restaurant slab

Design to EN 12056-3, r = 100 mm/h (0.028 l/s·m²) per brief, runoff coefficient C = 1.0 (metal roof); sensitivity 150 mm/h. No snow, no ice load (brief). Figures: `drainage_layout.png` (plan), `gutter_section.png` (eave section); structural hand-over in `drainage_loads.json`.

## 1. Roof, gutter line and catchments

One plane at 6 % falling north. The north outer face jogs (geometry.json `interior_walls_y`): x 67.89–81.79 at y 35.37, x 81.79–95.69 at y 35.87. Two external eaves gutters follow the outer faces:

- **G-W**: x 67.89–77.89 (10.0 m) on the y 35.37 face; it stops at the stair well, which reaches the north edge (y 29.37–35.37).
- **G-E**: x 81.79–95.69 (13.9 m) on the y 35.87 face.

Footprint with the jog 479.1 m² (the load basis' 486 m² ignores the 0.5 m jog); openings 23.4 + 16.4 m²; roofed 439.3 m². The strip between the openings (x 77.89–81.79, y 24.16–29.37, 20.3 m²) plus the 0.2 m sliver south of the elevator (0.8 m²) has no gutter of its own: the stair cricket sends it 50/50 to the west and east gutters (10.6 m² each). Effective catchment for wind-driven rain, EN 12056-3 4.2: A = (L + H/2)·B = plan area × 1.03 at 6 %.

| Catchment | Plan m² | Effective m² | Q₁₀₀ l/s | Q₁₅₀ l/s |
|---|---|---|---|---|
| G-W (west wing 198.0 + 10.6 diverted) | 208.6 | 214.9 | 5.97 | 8.95 |
| G-E (east block 220.2 + 10.6 diverted) | 230.8 | 237.7 | 6.60 | 9.90 |
| Roof total | 439.4 | 452.6 | 12.6 | 18.9 |
| Stair well (onto existing slab) | 23.4 | – | 0.65 | 0.98 |
| Elevator well (onto existing slab) | 16.4 | – | 0.45 | 0.68 |

## 2. Outlets, downpipes and gutter reaches

Four outlets/downpipes on the north facade, clear of the stair well and beside existing concrete columns where possible; positions balance the flow to about 3 l/s each. Gutters fall 1:350 from a high point midway between the outlets (x 73.00 and x 88.65) to each outlet; capacity is checked as a level gutter (conservative).

| Reach (gutter length draining to one outlet) | L m | A_eff m² | Q₁₀₀ l/s | Q₁₅₀ l/s |
|---|---|---|---|---|
| G-W end 67.89 → DP1 | 0.81 | 16.5 | 0.46 | 0.69 |
| high pt 73.00 → DP1 | 4.30 | 87.7 | 2.44 | 3.65 |
| high pt 73.00 → DP2 | 4.30 | 87.7 | 2.44 | 3.65 |
| G-W end 77.89 → DP2 (incl. cricket W) | 0.59 | 22.9 | 0.64 | 0.95 |
| G-E end 81.79 → DP3 (incl. cricket E) | 3.51 | 67.5 | 1.88 | 2.81 |
| high pt 88.65 → DP3 | 3.35 | 54.9 | 1.52 | 2.29 |
| high pt 88.65 → DP4 | 3.35 | 54.9 | 1.52 | 2.29 |
| G-E end 95.69 → DP4 | 3.69 | 60.4 | 1.68 | 2.52 |

| Downpipe | x (m) | Face y | Fixed to | Q₁₀₀ l/s | Q₁₅₀ l/s | Head at 100 mm outlet |
|---|---|---|---|---|---|---|
| DP1 | 68.7 | 35.37 | wall beside K6 | 2.89 | 4.34 | 53 mm |
| DP2 | 77.3 | 35.37 | wall beside K7, 0.6 m west of the stair well | 3.07 | 4.61 | 55 mm |
| DP3 | 85.3 | 35.87 | kitchen north wall between K3 and K1 | 3.40 | 5.10 | 59 mm |
| DP4 | 92.0 | 35.87 | wall beside K2 | 3.20 | 4.80 | 57 mm |

If the wall at x 85.3 is glazed or a door, move DP3 to x 82.4 (beside K3); DP4 then takes 3.9 l/s at 65 mm head, still within the 100 mm gutter depth. Longest reach 4.3 m.

## 3. Gutter sizing (EN 12056-3 clause 5)

Q_N = 2.78·10⁻⁵·A_E^1.25 (A_E in mm²), design Q_L = 0.9·Q_N·F_d·F_s with F_d = 0.95 (box, W/T = 1.5), F_s = 1.0, F_L = 1.0 (L/W ≤ 50 for all reaches).

| Profile | A_E mm² | Q_L l/s | Utilisation, governing reach 2.44 / 3.66 l/s | Verdict |
|---|---|---|---|---|
| Half-round 125 | 6 136 | 1.36 | 1.79 / 2.69 | no |
| Half-round 150 | 8 836 | 2.14 | 1.14 / 1.71 | no |
| Half-round 200 | 15 708 | 4.40 | 0.55 / 0.83 | ok but bulky |
| **Box 150 wide × 100 deep** | 15 000 | **3.95** | **0.62 / 0.93** | **adopted** |

**Adopted: external box gutter 150 × 100 mm**, 0.7 mm galvanised + polyester-coated steel (or 1.0 mm aluminium), riveted and butyl-sealed joints. Water depth in the longest reach ≈ 60 mm at 100 mm/h (freeboard 40 mm), ≈ 83 mm at 150 mm/h. Outer lip 10 mm lower than the back edge so the whole length overflows outward, never under the panel. Fall 1:350 to the outlets (12 mm over 4.3 m) set by the bracket line; panel drip flashing laps 60 mm into the gutter.

**Outlets**: 100 mm conical outlets in the sole at DP1–DP4, wire-balloon strainer on each. Sharp-edged weir capacity per clause 7, Q_o = 7.5·10⁻⁵·D·h^1.5: 2.65 l/s at 50 mm head, 3.5 l/s at 60 mm. All outlets work at ≤ 59 mm head at 100 mm/h; at 150 mm/h the head reaches 76 mm and the gutter runs near full, acceptable for the sensitivity case with the outward overflow. The conical inlet adds margin.

**Overflow**: (i) the lower outer lip (10 m weir at 10 mm head passes >15 l/s, more than the whole roof); (ii) tell-tale spouts 100 × 30 mm, sole +70 mm, in each stop end at x 67.89, 77.89, 81.79 and 95.69, discharging outward with a drip so a blocked outlet is seen from the ground.

## 4. Rainwater pipes

100 mm dia (coated steel or aluminium, bottom 1.5 m in steel/cast iron), one per outlet, swan neck (2 × 45°) to the wall, centre 85 mm off the facade. Capacity, clause 6 (Wyly–Eaton, k_b 0.25 mm, filling 0.33): 10.7 l/s per pipe against 3.4 l/s maximum (5.1 at 150 mm/h): utilisation 0.32 / 0.48; 100 mm kept for sand and blockage tolerance. Pipes run down the BoardX wall and the existing facade, about 3.4 + 4.0 = 7.4 m to grade, clips into concrete at ≤ 2.0 m, rodding access 1.0 m above ground, shoe over an existing yard gully or a back-inlet gully. Any lateral to the surface drain: 110 mm uPVC at ≥ 1:100 (≈ 5.6 l/s). Total to the site drain 12.6 l/s (18.9 at 150 mm/h): existing capacity to be confirmed.

## 5. Openings: upstands, crickets, well drainage

- **Upstands ≥ 150 mm** above panel top on all sides of both wells, on the trimmers; flashing under the panel skin uphill, over it downhill and at the sides, soakers at panel seams.
- **Stair well cricket** on the south side at y 29.37: saddle, ridge at x 79.84 running 2.0 m up-slope to the apex, 120 mm above the roof plane at the upstand (cross-fall 6 % = main pitch), valleys at 4.3 % to the corners (77.89, 29.37) and (81.79, 29.37); upstand behind the ridge 270–300 mm. Light Z sub-purlins on the trimmers clad in 0.7 mm coated sheet, laps sealed. Extra load ≈ 0.05 kN/m² over 2 m on the y 29.37 trimmer and the side rafters.
- **Elevator well**: no room for a cricket (roof edge y 19.97 is 0.2 m south of the upstand). South upstand merges with the notch verge flashing; the 0.2 m strip is capped falling 5 % to each side (0.8 m²).
- **Wells** (open courtyards on the existing slab): stair 0.65 l/s, elevator 0.45 l/s. Each keeps or gets one 100 mm outlet in the existing slab (existing roof outlet if inside the well, else a new cored outlet into the existing rainwater pipe) plus an emergency overflow: 100 × 50 mm scupper through the north wall at slab level for the stair well, a second outlet for the elevator. Screed to fall ≥ 1:80, waterproofing 150 mm up the walls, 100 mm threshold at any door into the hall. Other existing slab outlets under the new roof become dry; cap but keep accessible.

## 6. Supports, movement, loads for the structural designers

- **Brackets**: galvanised flat 40 × 5 at **600 mm**, plus one within 150 mm of each stop end, outlet and expansion joint, screwed to a **continuous fascia rail** (C 200 × 60 × 2.5 S350GD or the eave Z200 purlin) fixed to every rafter end / eave beam (spans ≤ 5.7 m in A, ≤ 4.1 m in C: M ≈ 1.7 kNm, fine).
- **Line load along the north eave** (characteristic): gutter brim-full 0.15 + gutter, brackets, fascia trim 0.10 = **0.25 kN/m**, 0.20 m outside the fascia line (0.05 kNm/m). Wind uplift on the gutter (zone F, −3.3 kN/m² × 0.15 m) **−0.50 kN/m**. Maintenance point load **0.5 kN** at any bracket. Per bracket: 0.15 kN gravity + 0.5 kN point, 0.30 kN uplift. No snow, no ice.
- **Thermal movement** (±40 K): steel 4.8 / 6.7 mm, aluminium 9.6 / 13.3 mm on G-W / G-E. One EPDM expansion joint per run at the high point (x 73.00, x 88.65) where the water depth is nil; fixed brackets at the outlets, sliding elsewhere; sliding sockets at the swan necks.
- **Leaf/sand guards**: wire-balloon strainers on all outlets; no gutter mesh (sand crusts on it). Hail not a design case.

## 7. Maintenance

Clear gutters, strainers, spouts and well outlets twice a year and after every dust storm or thunderstorm; check sealed and expansion joints every two years, EPDM at 10 years; ladder access from the north yard (gutter at ≈ 7.4 m) with edge protection.

## 8. Open items

1. Rainfall intensity for the actual city (100 mm/h assumed, 150 checked).
2. Existing north facade: construction between columns at x 85.3 / 92.0, height to grade (4.0 m assumed), position and capacity of yard gullies (12.6 l/s).
3. Existing slab outlets inside the wells and the route of the existing rainwater pipes.
4. Hall-side walls of both wells to full height, well waterproofing and thresholds (architect).
5. F_d and outlet coefficients to be confirmed against the chosen manufacturer's tested data.

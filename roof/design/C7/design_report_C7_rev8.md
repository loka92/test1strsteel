# Design report - alternative C, design Rev 8: reduced roofed area, economic scheme (2026-09-29)

**Status: design complete, no detailing (brief Rev 8). Basis for the next offer revision.** Supersedes design Rev 7 / 7b: same reduced roof extent, loads (load basis Rev 3), base type and drainage; new economic scheme (section 1a). Re-run: `python3 calc/run_rev7.py; python3 calc/write_report_rev8.py` (Rev 7 heavy set: `SCHEME=nested ECON=0 SEC_PRIM="IPE 300" SEC_RAFT="IPE 240" PRIM_TOP_OFFSET=0.03 SPAN_SECTION=...`).

## 1. What changed and why

The architect's 2nd-level plan (ALWATD sheet A_103, 29 Sep 2026) encloses only the west block and the north part of the east block; the SW terrace, the south strip of the east wing with the pyramid skylight (our former "elevator" opening) and the stair well stay open. The client adopted this reduced area (brief Rev 8). The roof boundary is put on existing column lines so that no new gravity column is needed:

| | Rev 6a | Rev 7 |
|---|---|---|
| Roof boundary | whole L-shape x 67.89-95.69, y 15.57-35.87 less the notch and two wells | west block x 67.89-77.89 / y 21.66-35.37 (south face on the K19-K20 line); east block x 77.89-95.69 / y 24.36-35.87 (south face on the K16-K17-K18 line); stair well open |
| Roofed area | 439 m2 | **316 m2** (architect's note: 300 m2) |
| Steel columns | 27 (K1-K27) + WP1 | **20 (K1-K20)** + wind posts WP2, WP3 (13.7 m south eave of the east block) and WP4 (9.8 m south eave of the west block) |
| Wall braced bays | 8 (B1-B7, B9) | **6**: B1 K1-K2, B2 K5-K7, B3 K16-K17 (E-W); B5 K15-K19, B6 K4-K14, B7 K16-K20 (N-S) |
| Roof rod panels | 13 in 5 strips | **12 in 6 strips** (RT-N-W 2, RT-N-E 3, RT-JOG 1, RT-W 3, RT-SW 1, RT-E 2) |
| Longest primary | P13 K19-K20 9.8 m IPE 330 | P_K17K18 K17-K18 **13.7 m IPE 330** (south eave of the east block, no column between K17 and K18); P13 9.8 m IPE 330 |
| Roof edge heights above the slab | north 3.33, south 4.55 m | north 3.42, south-west edge (y 21.66) 4.27, south-east edge (y 24.36) 4.11 m |
| Steel for the offer | 22.2 t (incl. 1.6 t girts) | **11.6 t** without girts (13.3 t with girts); Rev 7 heavy set 14.7 t |

Design choices to note for the architect and the client:

- The west block's south wall sits on the K19-K20 column line (y 21.66 outer face), 1.7 m north of the existing terrace wall line (y 19.97) drawn by the architect. Putting the roof edge on the existing wall line would need three gravity posts on the slab (no concrete column there) or 1.8 m rafter cantilevers through the flush fin-plate framing; both were rejected for simplicity and for the no-new-columns rule. The 1.7 m strip stays open terrace (about 17 m2).
- The east block's south wall sits on the K16-K17-K18 line (y 24.36 outer face), 0.7-0.9 m south of the architect's corridor wall, which gains a wider corridor. The three 0.20 m posts the architect drew on this wall at 4 m spacing do not exist as concrete columns; the design uses two wind posts WP2/WP3 (HEA 140, shear only, anchored on the slab like WP1 was) and one 13.7 m IPE 330 eave beam between K17 and K18.
- Braced bay B6 moved from K14-K18 (now the lift lobby) to K4-K14 on the east wall north of the corridor; B3 sits in the blank wall above the skylight (K16-K17); B7 is the 2.7 m wide bay K16-K20 on the light-well face (steep X: 1.5 x H uplift, checked). The bays B1 K1-K2, B2 K5-K7, B3 K16-K17, B5 K15-K19, B6 K4-K14 and B7 K16-K20 must stay free of doors and windows; B4, B9 and the old B6 are gone.
- Openings: the stair well keeps its trimmers, upstand and flashing on P_K10K11, R78 and R82; the light well no longer needs T2 or an upstand (it is outside the roof). The south roof edges get a verge flashing and a fascia; there is no gutter on them (the roof still falls north).

## 1a. Economic scheme (Rev 8) and what it saves

The column grid gives rafter spans of 4.8-7.6 m instead of the 9.2 m of the full roof, so the Rev 6a section set was under-used (rafters 0.38, primaries 0.24). Rev 8 changes the framing scheme to exploit that:

- **Rafters continuous over the y 29.3 primaries and seated on top of the primaries** (bottom flange bolted to the primary top flange with 2 M16, no fin plates, no coped webs). Continuity halves the long-span deflection and moves the peak moment to the support: rafters **IPE 180** (west lines 13.7 m long, one bolted splice at the low-moment point; east lines 11.5 m from one bar).
- Primaries no longer have to be deeper than the rafters: **IPE 200** for the 4.1-5.7 m spans; the two long eave beams (13.7 m and 9.8 m) stay **IPE 330**, cut from two 12 m bars without offcut (12 + 1.7 and 9.8).
- Roof plane raised to TOS = 3.42 + 0.06 (35.87 - y) so the 3.00 m clear height under the cap-plate nuts at the north eave is kept (3.01 m); columns are shorter under the shallower primaries (K1 2.981 m, K19 3.692 m).
- Wall diagonals **L 60x6** with M16 bolts at the 35 mm gauge, roof rods **M20 rod 8.8**; purlins Z200x2.0 at 1.5 m and columns HEA 140 unchanged.
- Bases, drainage, wind posts and the six braced bays are unchanged from Rev 7.

| | Rev 7 (IPE 300 / 240) | Rev 7b (IPE 240 / 200) | **Rev 8 (continuous IPE 180 on IPE 200)** |
|---|---|---|---|
| Steel for the offer, girts excluded | 14.7 t | 13.0 t | **11.6 t** |
| Hot-rolled sections | 9.8 t | 8.1 t | **7.0 t** |
| Governing utilisation: beams / columns / bases / bays | 0.77 / 0.80 / 0.82 / 0.70 | 0.75 / 0.78 / 0.76 / 0.67 | **0.88 / 0.71 / 0.72 / 0.89** |
| Seismic weight and design force | 236.5 / 104.0 kN | 218.2 / 96.0 kN | **208.6 / 91.8 kN** |

## 2. Loads and combinations (load basis Rev 3, unchanged)

G roof 0.37 kN/m2 (panel 0.12, purlins 0.05, services 0.10) + steel; G_min 0.17; Q 0.40 (cat. H, psi_0 = 0); wind v_b 27 m/s, z_e = h = 9 m, q_p by direction N 1.25 / E, W 1.05 / S 0.75 kN/m2, flat-roof zones with e = 18 m, c_pi +0.2 / -0.3, wall D +0.75 / E -0.40 / A -1.2 / B -0.8 / C -0.5; no wall self-weight (brief Rev 5), wall mass 0.30 kN/m2 in the seismic mass; seismic a_g 0.10 g, S 1.2, q 1.5, two-mass appendage amplification (resonance bound 5.5 alpha S = 0.66 g). Combinations EN 1990 6.10: ULS1 1.35 G + 1.5 Q, ULS2 1.35 G + 1.5 W_down, ULS3 1.0 G_min + 1.5 W_uplift per direction, ULS4 G + E (amplified, E_x + 0.3 E_y), thermal +/-30 K on the north bay pair, SLS G + Q and G + W_down, L/200 beams, L/150 purlins.

Totals on the 20 columns (characteristic): G 163.1 kN, Q 126.6, wind uplift N/S/E/W -361.5 / -231.1 / -242.0 / -235.9, pressure 175.2 kN; roof-level wind force N 63.4, S 58.5, E 43.8, W 43.4 kN (char.); seismic weight 208.6 kN, amplified design force 91.8 kN in both directions (Rev 6a: 137.4 kN on 312.2 kN).

## 3. Members (EN 1993-1-1; full list in members_C7.csv, plan in framing_C7.png)

Sections: primaries and eave beams **IPE 200** (P_K17K18 and P13 **IPE 330**), rafters, T3 and ST2 **IPE 180**, columns and wind posts **HEA 140**, S275; purlins Z200x2.0 @ 1.5 m; wall diagonals L 60x6; roof rods M20 rod 8.8. Governing utilisations: beams 0.88, columns 0.71, bases 0.72, wall bays 0.89, roof rods 0.48, wind posts 0.47, diaphragm struts/chords 0.61, fin plates 0.54.

| Member | Span | Section | L m | M_Ed kNm | defl. mm / limit | util. | governs |
|---|---|---|---|---|---|---|---|
| P_K9K10 | K9-K10 | IPE 200 | 5.69 | 45.0 | 20.9 / 28.4 | 0.88 | LTBg |
| R92 | K13-K2 | IPE 180 | 6.50 | 12.2 | 10.5 / 32.5 | 0.71 | LTBu |
| P_K11K12 | K11-K12 | IPE 200 | 5.34 | 32.9 | 13.5 / 26.7 | 0.68 | LTBu |
| P_K12K13 | K12-K13 | IPE 200 | 5.29 | 32.6 | 13.1 / 26.5 | 0.66 | LTBu |
| R85 | P_K11K12-P_K3K1 | IPE 180 | 6.40 | 11.1 | 9.3 / 32.0 | 0.63 | LTBu |
| R87 | K12-K1 | IPE 180 | 6.50 | 11.7 | 10.1 / 32.5 | 0.62 | LTBu |
| R90 | P_K12K13-P_K1K2 | IPE 180 | 6.50 | 11.5 | 9.9 / 32.5 | 0.60 | LTBu |
| R75 | P_K9K10-P_K5K7 | IPE 180 | 5.93 | 6.8 | 2.7 / 29.7 | 0.58 | LTBg |
| R75 | P_K19K20-P_K9K10 | IPE 180 | 7.51 | 17.9 | 21.3 / 37.5 | 0.57 | defl |
| P_K17K18 | K17-K18 | IPE 330 | 13.70 | 66.7 | 37.2 / 68.5 | 0.54 | defl |

P_K17K18 (13.7 m eave, IPE 330): M_Ed 66.7 kNm, deflection 37.2 mm = L/367 under G + Q (L/200 = 68.5 mm); top flange held by the four rafter seats at 2.6-2.9 m, bottom flange by fly braces at the rafters for the uplift case; as the E-W eave strut it carries the RT-E south reaction (49.9 kN) to B3: N + M interaction 0.35. P13 K19-K20 (9.8 m, IPE 330): 0.33. T3 (IPE 180, 2.88 m) is the north chord of the RT-SW panel: 0.27. ST2 (IPE 180, K15-R72): 0.19. Rafters: continuous over the y 29.3 line, hogging moment over the support checked for LTB of the bottom flange between the support and the first fly brace; worst rafter R92 0.71 (LTBu), R85 0.63 (LTBu).

Columns HEA 140 (6.3.3 with wall wind, bay compression and the amplified seismic case): worst K20 0.71, K19 0.64, K18 0.58, K16 0.48; lengths L = cap-plate top - 0.065 (130 mm lower under the IPE 330 eaves): K19 3.692, K17 3.530, K6 3.017, K1 2.981 m. Clear height under the cap-plate nuts at the north eave 3.01 m.

Wind posts (HEA 140, base = centred 60 mm key 280 mm inboard of the face, shear only, slotted top connection so they carry no roof gravity): WP2 on face S2, trib 4.6 m, q 1.05 kN/m2, M_Ed 14.9 kNm, LTB 0.40, base shear 14.6 kN (0.35); WP3 on face S2, trib 4.6 m, q 1.05 kN/m2, M_Ed 14.9 kNm, LTB 0.40, base shear 14.6 kN (0.35); WP4 on face S1, trib 4.9 m, q 1.05 kN/m2, M_Ed 17.3 kNm, LTB 0.47, base shear 16.3 kN (0.39).

Purlins Z200x2.0 @ 1.5 m: worst gravity moment 3.00 kNm (limit 12.5 single / 16 sleeved) at x 77.8-81.8, y 28.1, worst uplift 6.45 kNm at x 77.8-81.8, y 25.1 (sleeved + anti-sag / fly braces as Rev 6a); longest span 4.07 m, deflection 4.4 mm (L/150 = 27.1). Rafter seat on the primary (web crippling): 0.15; cap plates: 0.23; strut / chord forces through the 2 M16 flange bolts: 0.54.

## 4. Lateral system (seismic governs every bay, as in Rev 6a)

| Bay | Columns | dir | w x h m | H_Ed kN (wind / seismic) | diagonal T kN | uplift N kN | L 60x6 util. (angle / bolts) | sway mm / lim |
|---|---|---|---|---|---|---|---|---|
| B1 | K1-K2 | E-W | 5.29 x 3.15 | 31.3 (15.6 / 31.3) | 36.4 | 18.6 | 0.26 / 0.39 | 2.6 / 21.0 |
| B2 | K5-K7 | E-W | 5.70 x 3.18 | 40.3 (17.3 / 40.3) | 46.2 | 22.5 | 0.33 / 0.49 | 2.7 / 21.2 |
| B3 | K16-K17 | E-W | 4.11 x 3.82 | 49.9 (27.2 / 49.9) | 68.1 | 46.4 | 0.49 / 0.73 | 3.3 / 25.5 |
| B5 | K15-K19 | N-S | 4.61 x 3.85 | 36.1 (32.8 / 36.1) | 47.1 | 30.2 | 0.34 / 0.50 | 3.5 / 25.7 |
| B6 | K4-K14 | N-S | 6.40 x 3.34 | 40.4 (39.0 / 40.4) | 45.6 | 21.1 | 0.32 / 0.49 | 3.6 / 22.3 |
| B7 | K16-K20 | N-S | 2.70 x 3.91 | 47.3 (47.3 / 42.7) | 83.2 | 68.4 | 0.59 / 0.89 | 5.2 / 26.0 |

| Roof strip | supports | end shear V kN | rod T kN | util. | deflection mm |
|---|---|---|---|---|---|
| RT-N-W | B5 - B7 | 47.3 | 33.5 | 0.24 | 5.9 |
| RT-N-E | B7 - B6 | 47.3 | 40.7 | 0.29 | 8.1 |
| RT-JOG | B7 (via R78) | 47.3 | 61.9 | 0.44 | 9.9 |
| RT-W | B3 (via P13, RT-SW) - B2 | 49.9 | 49.3 | 0.35 | 11.0 |
| RT-SW | B3 (T3 -> K16) | 49.9 | 68.4 | 0.48 | 7.2 |
| RT-E | B3 (via eave strut) - B1 | 49.9 | 37.5 | 0.27 | 7.6 |

Load paths: N-S inertia of the north strips to B5 (x 68), B7 (x 77.8, through R78 as a strut K10 -> K16) and B6 (x 95.5, straight into K4-K14); E-W inertia of the west block to B2 (north) and, through the west strip RT-W, the P13 eave strut and the RT-SW panel (T3 chord into K16), to B3; E-W inertia of the east block to B1 (north) and, through RT-E and the 13.7 m eave strut, to B3. Struts and chords: purlins 0.29, rafter chords 0.33, rafter N-S struts 0.16, R78 strut 0.25, y 29.3 primary chord 0.52. Drift (EN 1998-1 4.4.3.2, nu 0.5, 0.005 h): west wall (RT-W + B3/B2) 0.83, east wall (RT-E + B3/B1) 0.43, x 77.8 line (jog + R78 + B7) 0.57, x 68 line (RT-N-W + R68 + B5) 0.36. Thermal lock-in on the north pair B1-B2: 10.4 kN ULS with wind, 25.9 kN erection state (as Rev 6a).

## 5. Bases (bases Rev 9 = Rev 8 detail on 20 columns; reactions per case in reactions_C7.csv)

One base type at all 20 columns: plate 300 x 400 x 20 on a 25 mm grout bed, 4 post-installed dia 16 B500 rebars at 70 x 240 through the 300 mm slab (debonded) and 250-300 mm into the column head (EAD 330087 resin, rebar scan first), Key A SHS 90x90x8 in a cored, grouted pocket; inboard key pairs at K1, K2, K4, K5, K7, K10, K15, K18, K19, K20; Key B (dia 60 bar) where an outward shear meets a free edge. Wind posts: centred 60 mm key only.

| Column | bays | N_c max kN (case) | N_t max kN (case) | V max kN | util. | governing check |
|---|---|---|---|---|---|---|
| K1 | B1 | 37.7 (ULS2E) | 34.2 (ULS3N) | 31.6 | 0.33 | E key pair outward (c1 >= 255) |
| K2 | B1 | 33.1 (ULS2W) | 32.0 (ULS3E) | 31.6 | 0.34 | E key pair outward (c1 >= 255) |
| K3 | - | 12.9 (ULS2N) | 18.8 (ULS3N) | 14.0 | 0.37 | Key B outward +y (c1 250) |
| K4 | B6 | 26.6 (ULS2S) | 32.4 (ULS3N) | 45.9 | 0.66 | E key pair outward (c1 >= 255) |
| K5 | B2 | 32.5 (ULS2E) | 30.8 (ULS3W) | 40.6 | 0.42 | plate strip at key moment |
| K6 | - | 9.2 (ULS2N) | 14.6 (ULS3N) | 13.8 | 0.35 | Key A parallel to edge -x (c1 55) |
| K7 | B2 | 28.1 (ULS4+x) | 17.7 (ULS3E) | 40.6 | 0.57 | E key pair bearing |
| K8 | - | 21.3 (ULS2N) | 25.9 (ULS3W) | 13.9 | 0.37 | Key B outward -x (c1 250) |
| K9 | - | 56.4 (ULS2N) | 50.7 (ULS3N) | 0.0 | 0.37 | E rebar bond in the column head, embed 250 min (N_Rd 136) |
| K10 | - | 39.7 (ULS2N) | 33.7 (ULS3N) | 0.0 | 0.25 | E rebar bond in the column head, embed 250 min (N_Rd 136) |
| K11 | - | 38.0 (ULS2N) | 32.9 (ULS3N) | 0.0 | 0.24 | E rebar bond in the column head, embed 250 min (N_Rd 136) |
| K12 | - | 50.8 (ULS2N) | 51.8 (ULS3N) | 0.0 | 0.38 | E rebar bond in the column head, embed 250 min (N_Rd 136) |
| K13 | - | 40.2 (ULS2N) | 41.3 (ULS3N) | 0.0 | 0.30 | E rebar bond in the column head, embed 250 min (N_Rd 136) |
| K14 | B6 | 37.6 (ULS2N) | 30.7 (ULS3E) | 43.8 | 0.72 | Key A parallel to edge +x (c1 165) |
| K15 | B5 | 35.2 (ULS4+y) | 28.2 (ULS3N) | 39.0 | 0.40 | plate strip at key moment |
| K16 | B3, B7 | 80.3 (ULS2S) | 75.6 (ULS3N) | 51.7 | 0.62 | plate strip at key moment |
| K17 | B3 | 56.6 (ULS4+x) | 36.8 (ULS4-x) | 50.5 | 0.60 | Key A SHS bearing |
| K18 | - | 21.8 (ULS2N) | 14.5 (ULS3S) | 11.8 | 0.13 | E key pair outward (c1 >= 255) |
| K19 | B5 | 52.1 (ULS2N) | 42.2 (ULS3S) | 39.0 | 0.40 | plate strip at key moment |
| K20 | B7 | 88.9 (ULS2N) | 75.4 (ULS3S) | 48.8 | 0.56 | E rebar bond in the column head, embed 250 min (N_Rd 136) |

Highest: K14 0.72 (Key A parallel to the east edge, B6 shear; an inboard pair as at K4 would bring it to about 0.5), K16 0.62 (B3 + B7 corner, uplift 75.6 kN: rebar bond 0.56), K17 0.60, K4 0.66 (pair added in Rev 7). Rev 6a maximum was 0.88.

## 6. Sensitivities (not the binding basis; for the client's decisions)

- (Sensitivities below were run on the Rev 7 heavy set; the margins of Rev 8 are similar and the conclusions hold.)
- **Wind reference height 12.7 m** (the architect's levels put the hall at +8.10 and the roof top near +12.7 above the street; load basis Rev 3 assumed 9 m): q_p +8 % and e = 25.4 m. All checks pass: beams 0.75, columns 0.84, bases 0.82, bays 0.72, wind posts 0.67. Recommendation: adopt in the next load-basis revision; no member changes.
- **Gypsum walls 20 cm** (architect's wall schedule) instead of light panels: with 1.0 kN/m2 of wall (half of it acting at roof level because the wall heads are tied to the steel) the seismic weight rises from 208.6 to 354.9 kN and the design force to 156.2 kN: bases K14 1.23, K16 1.05, K17 1.02 and bay B7 1.05 **fail**. Either the walls are light (<= 0.3 kN/m2 effective, as the brief assumes), or their heads are tied to the roof only for out-of-plane restraint through slotted connections that do not transfer the wall mass laterally, or the three bases get key pairs / larger keys and B7 gets 3 M20 gussets. To be settled with the wall system (brief: "later").

## 7. Drainage (unchanged, north)

The roof still falls 6 % north to the two external box gutters 150 x 100 on the north faces (y 35.37 west of the jog, y 35.87 east of it) with the four dia 100 downpipes DP1-DP4 on the north facade as in drainage_report.md. The catchment drops from 439 to 316 m2 (west gutter about 137 m2, east gutter about 180 m2), so every reach, outlet and downpipe has more margin than before (worst outlet head about 45 mm at 100 mm/h); gutter section, falls, overflows and the stair-well outlet are kept. The south edges are verges with a drip flashing, no gutter. The light-well terrace keeps the existing slab drainage.

## 8. Quantities (calc take-off; connection steel scaled from the Rev 6a BOM)

| Item | Length m | kg |
|---|---|---|
| IPE 180 rafters (11 lines, continuous), T3, ST2 | 144.6 | 2718 |
| IPE 200 primaries and eave beams | 55.1 | 1235 |
| IPE 330 eave beams P_K17K18 and P13 | 23.5 | 1153 |
| HEA 140 columns K1-K20 | 66.2 | 1636 |
| HEA 140 wind posts WP2-WP4 | 12.4 | 306 |
| L 60x6 wall diagonals, 6 bays | 72.5 | 393 |
| M20 rod 8.8 roof rods, 12 panels | 167.8 | 414 |
| Z200x2.0 purlins @ 1.5 m (+3 % anti-sag / eave rails) | 217 | 1280 |
| Plates, cap/fin/gussets/cleats, keys, rebars, bolts (scaled allowance) | - | 2467 |
| **Steel in the offer** | | **11.6 t** |
| Z200 girts for panel walls (wall system open, not in the offer) | 286 | 1687 |

Hot-rolled sections 7.0 t (assembly rule base), roof panels 316 m2 net.

## 9. Open items carried into the offer conditions

1. Architect to redraw the 2nd level and the south elevation on the Rev 7 roof boundary (wall lines on the K19-K20 and K16-K17-K18 column lines), with the 6 % slope, the verge fascias and the north gutter/downpipes; confirm the six door-free braced bays.
2. Wall system (gypsum vs light panel) and its head connection, see section 6; girts are not in the offer.
3. Unchanged from Rev 6a: as-built slab data and level survey, column-head scans and cores, adequacy statement of the existing structure (now about 290 kN gravity and 92 kN roof-level seismic force), purlin supplier data, local wind/rain confirmation; the lift tower is a separate structure with a movement joint and flashing against the east roof edge.

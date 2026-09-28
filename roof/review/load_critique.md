# Independent load critique - load_basis.md Rev 2 as applied in design C (Rev 3 / bases Rev 5a)

Critic's brief: find every conservatism, flag every unconservative item. Every "mine" figure below comes from re-running the designer's own `calc/` (takedown, bracing, column cases) with the constants replaced (`scratchpad/recalc.py`); the baseline run reproduces the report exactly (K19 -73.2 kN, K19-K20 131.3 kNm, hall 148.5 kN, worst base K23 0.80). Units kN, m, kN/m2. Building height for wind h = 4.0 (existing) + 4.85 (new, high eave + 0.3 flashing) = 8.9 m, h/d = 0.44 (N-S), 0.32 (E-W).

## 1. Verdict: OVERESTIMATED

Gravity is over by about a quarter, wind on the hall and on the bracing by about a half, column uplift by a third to a half. The superstructure sections do not change much (the flat-roof pressure case and LTB keep IPE 330 at 0.69), but the quantities that drove the anchorage saga - base uplift, bay shears, key shears - drop by 30-60 %. Three unconservative items exist (section 5); none is critical, one (seismic now governing the E-W bays) must be closed before the wind conservatism is removed.

## 2. Item-by-item

| Item | Theirs (Rev 2 / code) | Code basis | Mine (recommended) | Effect (uplift / gravity / bracing) |
|---|---|---|---|---|
| Panel 50 mm PIR | 0.12 | EN 1991-1-1 2.1, product 9.5-10.5 kg/m2 + laps, screws | 0.12 keep | - |
| Purlins Z200x2.0 @ 1.5 + bridging | 0.05 | 5.9 kg/m / 1.5 = 0.04 | 0.05 keep | - |
| Services "lighting, fans, light services" | 0.20, permanent | EN 1991-1-1 2.1(1): fixed equipment = permanent; typical exposed-soffit hall 0.05-0.15 | **0.10 permanent** (0.20 only if a suspended ceiling or ducted AC is decided; then agree it as a separate line) | gravity -0.135 ULS (-8 %); uplift none (correctly excluded from G_min) |
| Wall BoardX 0.30 kN/m2 (Rev 5: delete) | still in `takedown.py` l.134 for **G and G_min** of every column, and in report s.2 | brief Rev 5 | **0.0 in G and in G_min**; keep the physical mass in the seismic mass | gravity on bases -116 kN total; **uplift +7 kN at K19 (-73 -> -80), +8 at K23 - the deletion was not implemented and its uplift side is unconservative (s.5)** |
| G_min | 0.17 + steel (+ gutter 0.25 incl. 0.15 water) | EN 1990 6.4.3.1(4), Table A1.2(B) gamma_G,inf 1.0 | 0.17 + steel; gutter **0.10** in G_min (water is not a reliable permanent) | -0.4 kN per rafter end, formal |
| Imposed roof Q, cat. H | 0.60, psi_0 0; Q_k 1.0 kN | EN 1991-1-1 Table 6.10: q_k 0.4 recommended (NA 0.0-1.0), Q_k 1.0; 3.3.2(1) not with wind. ECP 201 (Egypt) about 0.5 inaccessible; SBC 301 / ASCE 7 L_r 0.96 reducible to 0.58 at A_t > 56 m2 (LRFD 1.6 L_r) | **0.40 + 1.0 kN point** (0.50 if an Egyptian-code checker is expected); 0.60 was a policy match to the ASCE reduced value, not a requirement | gravity -0.30 ULS (-17 %); K19-K20 deflection 36 -> 27 mm (L/271 -> L/363); K19-K20 M_ULS1 131 -> 98 (but see pressure case) |
| v_b | 27 m/s (Libyan 22; gust maps 36-40 m/s) | EN 1991-1-4 4.2; 3-s gust / 10-min = 1.42-1.45 -> 25-28 m/s | **27 keep until LNMC data**; 25 m/s if confirmed (-14 % on every wind figure, shown as S3) | 0 / -14 % |
| Terrain | I for all directions | 4.3.2(2), Annex A.2 procedure 1: roughness per direction; smoother category counts only within 2 km (cat 0) / 1 km (I-III) upwind | **N (sea): I; E, W (along the coast, city): II; S (city 2-storey, > 1 km): III** - confirm on the map in +/-15 deg sectors | S-wind q_p 1.30 -> 0.75 (-42 %); E/W 1.30 -> 1.05 (-19 %); S-wind hall force -40 %, K19 S-case -50 % |
| z_e, q_p | z_e 10 m, q_p 1.30 (derived 1.25, +4 %) | 7.2.2(1) z_e = h = 8.9 m (h < b); 4.5 c_e(9 m, I) 2.71 | **z_e 9 m: q_p(N) 1.25, (E/W) 1.05, (S) 0.75** | -4 % N; the "4 % margin" is not needed |
| Roof c_pe, 3.43 deg | Table 7.3a 5 deg, theta = 180 set (F -2.3 / G -1.3 / H -0.8) for N and S wind, no I zone; theta = 90 set for E/W (F -2.1, G -1.8, H -0.6, I -0.5) | **7.2.3(1): -5 < alpha < 5 deg is a flat roof -> Table 7.2 sharp eaves: F -1.8, G -1.2, H -0.7 (e/10-e/2), I -0.2 / +0.2 beyond e/2**; 7.2.4 starts at 5 deg | Table 7.2 for all four directions; downward case I +0.2 with c_pi -0.3 = +0.5 q_p | K12 uplift -31 %, K19 -24 % (with terrain I); purlin zone F -3.25 -> -2.5 kN/m2; the symmetric envelope disappears (one set) |
| Zone size e | 20 m (h 10) | 7.2.3 Fig 7.6: e = min(b, 2h) = 17.8 m | **e = 18 m: F/G strip 1.8 m, F corners 4.5 m, H to 9 m** | slightly less edge area; I zone starts 1 m earlier (not used in my run: e = 20 kept, conservative) |
| c_pi | +0.2 / -0.3 | 7.2.9(6) Note 2, no dominant opening (doors closed at ULS, 7.2.9(4)) | keep; if the south terrace facade gets openable glazing > 2x all other openings, add the accidental case c_pi 0.75-0.9 c_pe (+0.6) | - |
| Walls D / E | +0.8 / -0.5 (h/d = 1 values) | Table 7.1 interpolated at h/d 0.44: D +0.73, E -0.35 (7.2.2(2) Note) | **D +0.75, E -0.40**; A/B/C keep | column D-face bending -7 %; hall force wall part -12 % |
| Lack of correlation | not used | 7.2.2(3): h/d <= 1 -> 0.85 on the D + E resultant | **0.85** | hall force wall part -15 % |
| Hall force build-up | 1.3 q_p x wall area (half to roof) + roof-suction horizontal component 38.6 kN; no friction | 5.3(3) vector sum of surface pressures: the roof component is **correct, not double counting**; 5.3(4) friction rightly omitted (parallel area 622 < 4 x 245); c_s c_d 1.0 OK (6.2(1)a) | (0.75 + 0.40) x 0.85 = **0.98 q_p** on the wall area + roof component with the new q_p and c_pe (15.7 kN) | S 148.5 -> 63.3 (-57 %), N 85.6 -> 61.9, E/W 103 -> 64 |
| Rigid / tributary envelope of bay forces | envelope, sum 1.2-1.4 x applied | EN 1990 5.1.1: one consistent model suffices; the rod diaphragm (7-8 kN/mm) is semi-rigid against 15-24 kN/mm bays | keep the envelope (L-shape, +20-30 % on bays at 0.2-0.4 utilisation is cheap robustness) - noted, not claimed | - |
| Bracing uplift at the middle column of a two-bay line (K19, K18, K20) | ULS3 takes -1.5 N_t of the windward bay and ignores +1.5 N_c of the other bay on the same line and wind (`members.py` brace()) | statics: same wind, same line -> the two act together | net = N_t(B5) - N_c(B10) | K19 S-case: theirs -73.2 -> -49.7 with their loads (-32 %); mine -29.4 -> -19.5 |
| Combinations | 6.10: 1.35 G + 1.5 Q; 1.35 G + 1.5 W; 1.0 G_min + 1.5 W; 1.0 G +/- 1.0 E | EN 1990 A1.3.1(1) Note 1: 6.10a/6.10b with xi 0.85 are an admissible choice absent a Libyan NA; gamma_Q 1.5 on wind is the EC value and stays (BS 1.4, ECP 1.3, ASCE 1.0 x 700-yr are other systems, not mixable); 1.0 G_min + 1.5 W with services excluded is right | 6.10a/b optional: **-9 % on ULS gravity** where Q governs; keep 1.5 W | K19-K20 M 124 -> 116 with 6.10b |
| SLS | G + Q characteristic, L/200 total | EN 1990 A1.4.2 / EN 1993-1-1 7.2.1 NA: cat. H has psi_1 = psi_2 = 0; many NAs check the variable part only | keep L/200 on G + Q (with Q 0.4 it is L/363 anyway) | - |
| Seismic | 1.0 G +/- 1.0 E, roof mass only, F_b 75.9, "check only, wind governs" | EN 1998-1 4.3.3.2; floor amplification open (report item 5) | **with realistic wind, seismic governs the four E-W bays (1.0 E: B3 37.2, B2 33.8, B1 22.0, B4 16.2 kN vs wind ULS 32.5 / 23.9 / 18.7 / 13.5)**; the two-mass check becomes the design case (s.5) | E-W bays and K1, K2, K5, K7, K22, K23, K25, K26 bases: seismic |
| Temperature | +/-20 K service, +/-30 K erection | EN 1991-1-5 5.3, Table 5.2: T_max 48 + solar (bright surface) - T_0 15 = +50 K on bare steel; AC off (power cuts) -> hall 45-50 C | **service +/-30 K, erection +45 / -25 K**; locked-in B1/B2 force 22.6 -> ~34 kN ULS (0.18 of the angle) - not governing | B1/B2 bases +4 kN |

## 3. Recommended Rev 3 load basis (values)

- Permanent: panel 0.12; purlins 0.05; services 0.10 (permanent; revisit only if a ceiling / ducting is decided); steel from sections; gutter 0.25 G (0.10 in G_min), -0.5 W; upstands 0.30 kN/m. **No wall self-weight in G or G_min; wall mass 0.30 kN/m2 stays in the seismic mass.** G_min = 0.17 + steel.
- Imposed cat. H: q_k 0.40 (psi_0 = psi_1 = psi_2 = 0), Q_k 1.0 kN (purlin, panel supplier check); never with wind.
- Wind: v_b 27 m/s (LNMC to confirm; 25 m/s if confirmed), z_e = h = 9 m, c_s c_d 1.0, e = 18 m. q_p by direction: N (sea, terrain I) 1.25; E, W (terrain II) 1.05; S (terrain III) 0.75. Roof: flat, Table 7.2 sharp eaves: F -1.8, G -1.2, H -0.7 (1.8-9 m), I -0.2 / +0.2 beyond 9 m. c_pi +0.2 / -0.3. Walls D +0.75, E -0.40, A -1.2, B -0.8, C -0.5. Global: 0.85 x (D - E) = 0.98 q_p on the projected wall area, half to the roof, plus the horizontal component of the net roof suction (15.7 kN char. for S wind); no friction.
- Seismic: a_g 0.10 g, S 1.2, q 1.5, roof + wall mass, 5 % eccentricity, two-mass amplification check now mandatory (E-W bays are seismic-governed).
- Temperature: +/-30 K service, +45 / -25 K erection.
- Combinations: 6.10 (or 6.10a/b, xi 0.85, at the designer's choice): 1.35 G + 1.5 Q; 1.35 G + 1.5 W (pressure, I zone +0.5 q_p, c_pi -0.3); 1.0 G_min + 1.5 W (c_pi +0.2, four directions, bracing net per line); 1.0 G +/- 1.0 E; SLS G + Q (L/200, purlins L/150), G + W (H/150).

## 4. Recalculation with the recommended basis (their code, my constants)

| Quantity | Theirs | Mine (v_b 27) | Change | v_b 25 |
|---|---|---|---|---|
| Char. G on the bases, total | 439 kN | 279 kN | -36 % (walls 116, services 44) | 279 |
| ULS gravity, roof only (G 0.67 -> 0.57 + Q) | 1.35 x 0.67 + 0.90 = **1.80** | 1.35 x 0.57 + 0.60 = **1.37** (6.10b: 1.25); N-wind pressure case on the south half (I zone, +0.625): 1.71 | -24 % (-30 %) / -5 % where the pressure case governs | same |
| K19-K20 primary IPE 330 (9.79 m) | M 131.3, delta 36.1 mm (L/271), util 0.74 (deflection) | M 123.7 (N-wind pressure case; 97.5 for 1.35 G + 1.5 Q; 116 with 6.10b), delta 27.0 (L/363), **util 0.69 (LTB gravity)** | -6 % M, -25 % deflection | same |
| 9.2 m rafter IPE 270 (R92) | 0.57 (LTB uplift 57 kNm) | 0.41 (Mu 41) | -28 % | 0.37 |
| Column K25 (corner) HEA 160 | 0.72 | 0.56 | -22 % | 0.48 |
| Column uplift K19 (west wall, B5/B10, trib 32 m2) | **-73.2** (ULS3S; -43.8 roof + -29.4 bracing) | **-46.7** (now ULS3W, west-edge F/G zone); S-case -29.4 (net-bracing -19.5) | **-36 %** (S-case -60 %) | -37.9 (-48 %) |
| Column uplift K12 (interior, trib 42 m2) | -67.8 (ULS3N) | -47.1 | -31 % | -38.1 (-44 %) |
| Braced-bay bases: K16 (B8) / K23 (B3, B9) / K10 (B8) / K20 (B7) / K22 (B3) | -58.7 / -62.3 / -60.5 / -64.4 / -56.3 | -22.0 / -45.1 / -45.7 / -28.2 / -28.1 | -63 / -28 / -24 / -56 / -50 % | -17.9 / -37.6 / -37.6 / -22.0 / -22.1 |
| Anchor (column-head rebar) utilisation K19 / K23 / worst base | 0.54 / 0.46 / 0.80 (K23 key bearing) | 0.34 / 0.33 / **0.53 (K7)** | -34 % | 0.28 / 0.28 / 0.47 |
| Cap-plate tension (worst column) | 67.8 | 47.1 | -31 % | 38.1 |
| Hall wind force at roof level, char. N / S / E / W | 85.6 / **148.5** / 102.7 / 103.9 | 61.9 / **63.3** / 63.9 / 64.3 | -28 / **-57** / -38 / -38 % | 53 / 54 / 55 / 55 |
| Roof-suction horizontal component (S wind) | 38.6 | 15.7 | -59 % | 13.4 |
| Bay shear ULS: B8 / B3 / B7 / B6 (wind) | 57.3 / 53.6 / 50.9 / 42.6 | 24.5 / 32.5 / 21.8 / 18.3 | -57 / -39 / -57 / -57 % | 21.0 / 27.9 / 18.7 / 15.7 |
| Diagonal tension B8 / B3 (L70x7 189) | 72.2 / 63.1 | 30.9 / 38.3 | -57 / -39 % | 26.5 / 34.6 |
| Seismic 1.0 E bay shear B3 / B2 / B8 | 37.2 / 33.8 / 18.4 | unchanged | **now > wind on B1-B4** | - |
| Purlin uplift M (3.07 m corner span) | 8.3 kNm | 6.3 | -24 % | 5.4 |
| Existing-structure statement inputs | 439 kN G, 148.5 kN wind | 279 kN G (+116 wall if real), 63 kN wind | | |

What could be saved in steel: IPE 300 primaries (LTB about 0.9), IPE 240 rafters (about 0.55, L/359), HEA 140 columns (about 0.82 at K25) - roughly 2.3 t of 25.4 t (about 4,700 $); not worth re-detailing on its own. The real relief is at the bases (all 27 column-head anchorages at <= 0.35, keys <= 0.53), in the bracing (B8 at 0.16) and in the adequacy statement for the existing columns.

## 5. Unconservative items (clearly stated)

1. **Rev 5 not implemented and its uplift side wrong-way**: `takedown.py` line 134 still adds 0.30 kN/m2 x wall height to G **and to G_min** of every perimeter column; report s.2 still lists "wall self-weight". Removing it as the client ordered raises the current uplift at K19 from 73.2 to 80.2 kN and K23 from 62.3 to 70.3 (rebar 0.46 -> 0.52). With my basis this is moot (46.7), but the code and report must be corrected either way.
2. **Seismic becomes governing for the E-W bays and their bases once the wind is realistic** (B3 37.2 vs 32.5 kN; K22/K23 keys were sized for 59-64 kN wind shear and are fine, but with the floor amplification of report item 5 (S_a up to 0.6 g / q) the E-W bay shears could reach 60-90 kN). The two-mass check is no longer "check only"; do it before the wind reductions are banked. The wall mass must stay in the seismic mass despite Rev 5.
3. **Flat-roof pressure case**: with Table 7.2 the downward wind in zone I is +0.2 (+0.5 q_p with c_pi -0.3 = 0.625 kN/m2 for N wind), not the 0.39 used; it governs the south-half gravity design over Q 0.4 (1.71 vs 1.37 kN/m2). With the present Q 0.6 it is covered within 4 %.
4. Minor: gutter water (0.15 kN/m) in G_min; the 0.05 kNm/m gutter eccentricity on the eave rail is not in any script (< 0.2 kNm per rafter end); the 1.0 kN maintenance point load is positioned nowhere - it does not govern the Z200 (2.3 vs 4.3 kNm) but a 50 mm PIR panel on 1.5 m needs the supplier's walkability statement or a "crawl boards only" note; erection temperature +45 K rather than +30 K (B1/B2 +4 kN, not governing); e = 18 m puts the I zone 1 m closer to the edge (used conservatively as 20 m here).
5. Out of scope but unchanged: the existing ribbed slab and 20 x 40 columns receive 279 kN (my G) and 63 kN wind at roof level; the adequacy statement (brief Rev 3) is still the item a permit authority will ask for first. No ponding: 6 % fall to an external gutter with a 150 mm/h overflow check.

## 6. Top 5 changes ranked by effect

1. Terrain by direction (S: III, E/W: II, N: I) - S-wind hall force -40 %, S-wind bay shears -40 %, K19 S-case uplift -50 %.
2. Flat-roof Table 7.2 with the I zone instead of the 5-deg mono-pitch envelope, z_e 9 m - column uplift -24 to -31 %, hall/bays -21 %, purlin zone F -23 %.
3. Net bracing uplift at the middle column of each two-bay line (K19, K18, K20) - K19 -32 % on the S case (calculation, not basis).
4. Services 0.10 and Q 0.40 (6.10b optional) - ULS gravity -24 % (-30 %), K19-K20 deflection -25 %; K19-K20 moment only -6 % because the flat-roof pressure case takes over.
5. Wall D/E interpolated at h/d 0.44 and the 0.85 lack-of-correlation factor - hall force wall part -25 %; v_b 25 m/s if the LNMC confirms it - a further -14 % on every wind figure.

Combined: K19 uplift 73 -> 47 kN (-36 %), S-wind hall force 148 -> 63 kN (-57 %), ULS gravity 1.80 -> 1.37 kN/m2 (-24 %), worst base 0.80 -> 0.53, worst bay 0.58 -> 0.31.

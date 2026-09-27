# Alternative C - post-and-beam braced frame: design report, Rev 2

System C: E-W IPE 330 primaries on the column rows, N-S IPE 270 rafters, pinned HEA 160 columns, vertical X bracing for all lateral load, roof-plane X bracing as the diaphragm. All numbers come from `calc/` (`python3 run_all.py; python3 write_report.py`); ULS design values unless stated. Companion note: `bases_C.md` (bases and anchors, self-contained).

## 0. Change log Rev 1 -> Rev 2 (basis Rev 2 and independent review, every finding addressed)

| Ref | Change |
|---|---|
| Basis: wind zones | e = 20 m: F/G strip 2.0 m deep, F corners 5.0 m along the eave; zone sets kept as the envelope (theta = 180 values for both N and S wind, F5). Roof uplift total W_S -669 kN incl. gutter (Rev 1 -614). |
| Basis / F4 | Horizontal component of the roof suction added: {roofc} kN char. northward for S wind (resultant at x {roofx}, y {roofy}), also as an N-S load under E/W wind; S-wind roof-level force 108.7 -> **{wS} kN** (+36 %); no friction term. Bracing, braced columns and bases re-run. |
| Basis: anchorage / F1, F2, F3 | New base for all 27 columns: 4 M20 through the slab into the column head (h_ef 300, 80 x 280 in the core), bond + cracked cone in the slab, **grouted shear key** for all shear (no anchor shear, so the cracked-edge question F2 disappears), plate 25 mm. Wall shear wL/2 is at the column base in every case (F1); base struts deleted, every base carries its full concurrent H + V_wall (F3). |
| Bracing layout | K17-K21 (Rev 1 B8) dropped - K21 is a 200 mm pier between the notch edge and the shaft opening. N-S bracing now on three lines with two bays in series each: B5 K15-K19 + **B10 K19-K25**, B7 K20-K27 + **B8 K10-K16**, B6 K14-K18 + **B9 K18-K23**; E-W B1-B4 unchanged. 10 bays; no braced-bay base has its bay shear towards a free edge < 0.25 m. |
| F6 | Gutter/fascia 0.25 kN/m (G) and -0.50 kN/m (W) on the north eave in the take-down (rafter cantilevers, eave beams, fin plates). West-block north edge kept at y 35.87 (wall line); drainage's gutter line y 35.37 to be coordinated (open item 6). |
| F7 | Column interaction with k_zy from Annex B Table B.2 (0.97-1.00): K25 {K25u}, K23 {K23u}, K22 {K22u}. HEA 160 confirmed. |
| F8 | Purlin uplift re-run with the 2.0 m / 5.0 m zones: corner spans (3.07 m, zone F) 8.3 kNm, stair strip 4.07 m 8.6 kNm; mid-span anti-sag row on all spans; supplier uplift capacity before order (open item 3). |
| F9 | Seismic: ULS-4 rows (1.0 G +/- 1.0 E, both directions, 5 % eccentricity) added to reactions_C.csv; floor amplification through the existing building stated as open item 5. |
| F10 | Roof diaphragm re-modelled with the rods in the drawn cells; east/west edge trusses now use diagonals over two rafter bays (depth 5.65 / 4.10 m) and posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) at the wall-column lines; M24 rods throughout; truss deflection by virtual work: east wall drift {driftE} mm, west {driftW} mm (SLS, incl. bay sway) vs h/150 = 26-28 mm. |
| F11 | TOS(35.87) = 3.30 m, primary top at TOS + 0.05: clear height 3.03 m, rafter/primary bottom-flange clearance 18 mm nominal, 13 mm at the down-slope flange tip. T1 at y 35.44 and T2 at y 24.09 (half a flange inside the opening edges). R82 at x 81.85 over the shaft east wall line: client to confirm (open item 7). |
| F12 | Cap-plate bolts at pitch 200 (plate 200 x 280 x 20); primaries bolted before the rafters are landed. |
| F13 | reactions_C.csv now one row per column and load case (594 rows: ULS-1, ULS-2/3 x 4 wind directions, ULS-4 x 4, SLS) with concurrent N, V_x, V_y, near-edge flags and the base utilisation; WP1 included; envelope in section 9. |
| F14 | Angle bearing with e2 = 30 mm (124 kN per bolt): B8 gusset 0.57. |
| F15 | Base struts and wall-rail anchorage deleted; the lateral system is 10 wall bays + {n_panels} rod panels + 2 posts. |

## 1. Basis and assumptions

- Loads, combinations and resistances exactly per `../load_basis.md` Rev 2; geometry per `../../geometry.json` (27 columns, L-shape less the notch, stair and elevator openings not roofed; roofed area {roof_area} m2 from the grid).
- One roof plane at 6 % falling north, TOS(y) = 3.30 + 0.06 (35.87 - y); level primaries with their top at TOS + 0.05; cap-plate top = TOS - 0.28; column length = TOS - 0.34 (25 mm plate + 40 mm grout), 2.97 m (north rows) to 4.16 m (south row).
- Statics: all beams are chains of simple spans (fin plates, cap plates), purlins simple spans between rafters, columns pinned-pinned; girts span horizontally between columns, so each column delivers wL/2 of its wall to the roof and wL/2 to its base. The take-down integrates the roof on a 0.1 m grid (exact tributary, openings excluded) -> rafters -> primaries -> columns. Section tables IPE 200-360 / HEA 140-200 in `calc/sections.py`.
- Wind post WP1 (HEA 160) at the notch corner (77.89, 19.97): wall wind only, slotted top connection, base 2 M16 in the notch edge beam (shear {wpV} kN, no uplift).
- Slab: 250 mm ribbed, solid zone >= 800 x 800 at every column head, C25 cracked, column cage 6 dia14 + dia6/200 - all to be confirmed by cores and a rebar scan before drilling (bases_C.md section 6).

## 2. Loads and combinations (kN, m)

| Action | Value | Used for |
|---|---|---|
| Panel + purlins + services G | 0.12 + 0.05 + 0.20 = 0.37 kN/m2 + member self-weight; gutter 0.25 kN/m on the north eave | gravity |
| G_min (uplift) | 0.17 kN/m2 + member self-weight | ULS-3 |
| Imposed cat. H Q | 0.60 kN/m2, psi_0 = 0 (never with wind) | ULS-1, SLS |
| Wind q_p | 1.30 kN/m2 (Tripoli, binding) | all wind cases |
| Roof net uplift, c_pi +0.2, e = 20 m | H -1.30, G -1.95, F -3.25 kN/m2 (N and S wind, F/G strip 2.0 m, F corners 5.0 m); along the ridge F -2.99, G -2.60, H -1.04, I -0.91; gutter -0.50 kN/m | ULS-3, purlins, fly braces |
| Roof pressure case, c_pi -0.3 | +0.39 kN/m2 (never governs over Q) | ULS-2 |
| Walls, net | D +1.1 (c_pi -0.3); A -1.4 / B -1.0 / C -0.7 / E -0.7 (c_pi +0.2); x 1.3 -> up to 1.82 kN/m2 char. | column bending and base shear |
| Global horizontal wind at roof level | 1.3 q_p on the projected wall area, half to the roof, plus the roof-suction component ({roofc} kN, S wind; 30 kN N-S under E/W wind): **N {wN}, S {wS}, E/W 72 (+30 N-S) kN** char. | bracing, diaphragm |
| Wall self-weight | 0.30 kN/m2 x wall height (3.60 m N ... 4.82 m S) x column trib | column axial |
| Seismic (EN 1998-1, a_g 0.10 g, S 1.2, q 1.5, S_d 0.20 g) | seismic weight {seisW} kN -> F_b = **{Fb} kN** (1.0 E) with 5 % eccentricity -> max bay force {H4max} kN (E-W) / {H4maxy} kN (N-S) vs wind 53 / 57 kN: wind governs; ULS-4 in the reaction table | ULS-4 |

Combinations (EN 1990 6.10): ULS-1 1.35 G + 1.5 Q; ULS-2 1.35 G + 1.5 W (pressure, wall D/E with c_pi -0.3, roof +0.39, bracing compression); ULS-3 1.0 G_min + 1.5 W (uplift, c_pi +0.2, four wind directions, bracing tension); ULS-4 1.0 G +/- 1.0 E; SLS G + Q (L/200, purlins L/150) and G + W (sway H/150).

## 3. Load take-down and bracing analysis results

**Take-down (`takedown.py`).** 11 N-S rafter lines (x = 68.0, 70.0, 72.1, 74.9, 77.8, 81.85, 84.5, 87.2, 89.9, 92.5, 95.5), rafter spans 2.7-9.2 m, purlin spans 2.05-3.1 m (4.07 m over the north strip of the stair well). Example column loads (characteristic, kN): K12 interior G {K12[G]:.1f}, Q {K12[Q]:.1f}, W_N {K12[W_N]:.1f}; K19 (braced, west wall) G {K19[G]:.1f}, Q {K19[Q]:.1f}, W_S {K19[W_S]:.1f}. Sum of column loads: G 443 (incl. gutter), Q 268 (= 0.60 x 446), W_S -669 kN.

**Bracing (`bracing.py`).** The roof force of each windward face (and the roof-suction component at its centroid) is distributed to the bays twice: (a) rigid diaphragm, 3 DOF, bay stiffness k = E A cos^2(alpha)/L_d of one L70x7 diagonal (15.6-24 kN/mm), centre of rigidity and torsion included; (b) flexible-diaphragm tributary to the bracing lines, then to the bays of a line by stiffness. **The envelope of (a) and (b) is used** (sum of bay forces 1.2-1.4 x the applied force). Wind from S, characteristic: rigid B5 23.4 / B10 22.0 / B7 23.1 / B8 26.1 / B6 28.3 / B9 25.4 kN, tributary 15.2 / 14.3 / 33.9 / 38.2 / 24.9 / 22.3 kN; wind from E: rigid B1 20.0 / B2 19.5 / B3 17.5 / B4 15.2, tributary 1.3 / 26.1 / 35.5 / 9.8 kN.

Bay forces at ULS (1.5 W), tension-only diagonal T = H L_d/w, column axial N = H h/w, base shear H at the tension-diagonal base (windward column) concurrent with that column's wall shear:

{bay_table}

## 4. Member checks (EN 1993-1-1)

Checks per span: bending 6.2.5 (M_pl,Rd IPE 270 = 133 kNm, IPE 330 = 221 kNm), shear 6.2.6 (V_pl,Rd 351 / 489 kN; V_Ed < 0.5 V_pl everywhere), LTB 6.3.2 with M_cr from I_w, I_t and C1 per restraint segment (C1 = 1.88 - 1.40 psi + 0.52 psi^2 for linear segments, 1.0 when the maximum lies inside the segment), curve b, deflection G + Q <= L/200 by numerical double integration.

Restraints: rafters - top flange held by purlins @ 1.5 m (gravity, chi_LT = 1.0); under uplift the free bottom flange is held by **fly braces to the purlins at mid-span for spans <= 6.6 m and at the third points for 7.5 and 9.2 m spans** (segments 2.2-3.25 m). Primaries - both flanges restrained at every rafter fin plate (plate over the full rafter web depth) and at the columns, segments <= 4.1 m; the K19-K20 LTB check is governed by its 2.8 m middle segment (C1 1.07).

{member_table}

Governing members: primary **K19-K20 (9.79 m)** at 0.74 (deflection 36 mm = L/271; M_Ed 131 kNm = 0.59 M_pl; LTB 0.73); 9.2 m rafters at 0.49-0.52 (deflection 22-24 mm = L/390-410, M 0.35, LTB uplift 0.51). Max beam utilisation {maxbeam}. Alternatives run with the same scripts: IPE 240 rafters pass strength (M 0.58, LTB uplift 0.71) but give L/265 on the 9.2 m spans with no reserve for a future ceiling, so IPE 270 is kept; IPE 300 primaries put K19-K20 at L/194 (1.03): IPE 330 confirmed.

Rafters as roof-truss posts: N_Ed = {postN} kN with N_b,Rd = {postNb} kN (L_y 9.2, L_z 3.07 m) -> 0.06; new posts ST1 (IPE 270, 5.65 m, N {st1} kN vs {st1b}) and ST2 (4.10 m, {st2} vs {st2b}); eave primaries as struts <= 57 kN vs N_b,Rd >= 800 kN. Purlins are not used as struts.

**Columns** (6.3.1 pinned-pinned, L_cr = L both axes, HEA 160 curve b/c; 6.3.3 Annex B method 2, Table B.2 for the LTB-susceptible member, C_m = C_mLT = 0.95 for the wall-wind UDL, web normal to the wall it supports, corners biaxial). N_b,Rd = 461 kN (L 4.16 m) to 667 kN (L 2.97 m).

{column_table}

Max column utilisation {maxcol} (K25, SW corner). Wind post WP1 HEA 160, L {wpL} m: M_y {wpMy}, M_z {wpMz} kNm -> {wpu}. HEA 140 reaches 1.06 at K25 with Table B.2: **HEA 160 confirmed**.

**Purlins Z200x2.0 @ 1.5 m** (basis: M_Rd 12.5 kNm single span, 16 sleeved; I = 3.9e6 mm4): worst gravity M_Ed = {Mg} kNm; worst uplift M_Ed = **{Mu} kNm** on the 4.07 m stair strip ({Mu_where}, zone G) and 8.3 kNm on the 3.07 m corner spans (zone F, w = -7.1 kN/m), i.e. 0.66-0.69 of the single-span gravity value. Because the free-flange uplift capacity of a Z200x2.0 is typically 55-70 % of the gravity value, **a mid-span anti-sag row is specified on every span and the supplier's uplift capacity (>= 9 kNm single span with one anti-sag row, or sleeved) is required before order** (open item 3). Deflection G + Q on {Lp} m: {dp} mm < L/150 = {dplim} mm. Girts (wall net 2.15 kN/m2, zone A 2.73 within 2.4 m of a corner): 1.5 m rows single-span for bays <= 5.3 m (<= 11.3 kNm); 1.2 m rows sleeved on K5-K7, K25-K19, K8-K6 (<= 14.2 kNm); 1.0 m rows sleeved on K21-K22, K22-K23, K14-K4 (<= 14.9 kNm, 0.93).

## 5. Connections (EN 1993-1-8)

- **Rafter to primary fin plate**, one type: 100 x 150 x 10 S275, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web, 2 x 6 mm fillets. Max rafter end reaction {Vfin} kN (envelope ULS-1 / reversed ULS-3 incl. the gutter): bolt shear incl. eccentricity {fin2_bs}, bearing on the 6.6 mm rafter web **{fin2}** (governs), plate bearing {fin2_bp}, plate shear {fin2_ps}, plate bending {fin2_pb}, weld {fin2_w}, web block tearing {fin2_bt}. 9.2 m rafters: 3 bolts, plate 220 ({fin3} at {Vfin_long} kN). No copes. T1/T2, ST1/ST2 and the notch eave beam use the same detail.
- **Primary to column cap plate** 200 x 280 x 20, a = 6 all round, 4 M20 through the primary bottom flange (gauge 90, **pitch 200** so the nuts clear the passing rafter flange; primaries bolted before the rafters). Tension = roof uplift {Nt_cap} kN (K12, ULS-3N; the bracing vertical component enters below the cap through the gusset): bolt tension {cap_bt}, shear + tension interaction with the chord/strut force {Vh_cap} kN {cap_bi}, IPE 330 flange T-stub {cap_ts}, cap plate 0.05, weld {cap_w}. Chord continuity across a column (<= 61 kN): 10 mm tie plate between the primary bottom flanges on the lines y 29.3 and y 20.1.
- **Bracing gussets**: 10 mm plates welded to the column web and base plate; each L70x7 with 2 M20 (e1 40, p1 110, e2 30): angle net section 189 kN, bolt shear 188 kN, gusset bearing 2 x 124 kN; max T_Ed {B8T} kN (B8) -> 0.38 angle, 0.57 bolts.
- **Roof bracing** M24 rods 8.8 (F_t,Rd 203 kN) with turnbuckles to 8 mm gussets on the rafter and primary webs at the bottom flange level; on the east and west edge trusses the rods span two rafter bays and pass the intermediate rafter (R92 / R70) through a slotted web clip; sag ties to the purlins at the crossing and at 3 m centres.
- Trimmers T1 (y 35.44) and T2 (y 24.09) IPE 270 between the rafters x 77.8 / 81.85 carry only the 150 mm upstand (0.3 kN/m, M_Ed 1.8 kNm); upstand framing 100 x 50 x 3 cold-formed C on the trimmers and along the rafters beside the openings, cricket on the south side of the stair well.

## 6. Bases and anchors (EN 1993-1-8 6.2.5, EN 1992-4 with the Rev 2 basis) - full note in `bases_C.md`

One detail for all 27 columns: plate **300 x 400 x 25** on 40 mm grout; **4 M20 resin anchors at 80 x 280 inside the column core, through the slab into the column head, h_ef 300**, in 26 mm clearance holes (tension only); **grouted shear key**: 60 mm round bar S355 x 330 welded under the plate (a = 8), in a 90 mm cored pocket 350 deep (250 slab + 100 column head).

- Tension: steel 4 x 140 kN; cone in the slab solid zone (h_ef 250, k 7.2 cracked, N0 = {N0c} kN, group 80 x 280 in the 800 x 800 zone: A_c,N/A0 = {ratio_c}, psi_s 0.91) **N_Rd,c = {NRd_c} kN**; bond (pi x 20 x 300 x 10 MPa = {N0p} kN, s_cr,Np 462, group ratio 1.88) N_Rd,p = {NRd_p} kN -> **group {NRd_g} kN (cone)**. Max uplift {Ntmax} kN at {Ntmax_col} (ULS-3S: roof + bracing) -> 0.75; interior K12 66.7 kN -> 0.68.
- Compression: A_eff {Aeff} cm2 at 10 MPa = 934 kN; max 91 kN (K22) -> 0.10. Plate T-stub under uplift (m = 55 mm from the flange tips, t 25): 934 kN per anchor row -> <= 0.04.
- Shear: all through the key - bearing sigma_max = 2V/(60 x 250) <= f_cd gives 125 kN, key bending at the plate (lever 133 mm, M_Rd 12.8 kNm) **V_Rd = {VRd_key} kN**, weld 352 kN. Max base shear {Vmax} kN at {Vmax_col} (ULS-2E: B3 bay shear + wall wL/2, along the column's long axis into the solid zone) -> 0.71. Shear **towards a free slab edge closer than 0.25 m** (perimeter wall shear <= 29 kN; worst K21, 29 kN towards the notch edge under W wind, zone A suction, and 23 kN towards the shaft opening under S wind) is carried by the column cage in front of the key, V_Rd,edge = {VRd_edge} kN (3 dia14 dowels at 50 % + one dia6 stirrup) -> <= 0.49 at K21; no braced-bay base has its bay shear towards a near edge (bracing layout, section 8).
- Anchors take no shear and the key no tension, so no N-V interaction. Worst base **{worst}: {wb_u} ({wb_gov}, {wb_case})**; all 27 bases <= 1.0 with 4 M20 (M24 and h_ef 400 not needed).

## 7. Deflections and sway

- Roof members SLS G + Q: worst primary K19-K20 36 mm = L/271 (limit 49 mm); 9.2 m rafters 22-24 mm = L/390; 7.5 m rafters L/700-820; purlins L/640.
- Braced-bay sway under SLS wind (diagonal elongation + 2 mm bolt-slip allowance): 2.8-3.9 mm vs h/150 = 20-28 mm. Column bending under wall wind (K22, 9.8 kN/m on 3.91 m) 8.5 mm = h/460.
- **Roof diaphragm drift** at the mid-length of the east / west walls (truss deflection by virtual work over the M24 rods, SLS, plus bay sway): **{driftE} / {driftW} mm** vs h/150 = 26-28 mm (0.40).

## 8. Bracing

Vertical bays (X, one L70x7 per diagonal, tension-only), **final list for the client - these bays must stay door-free**: E-W **B1 K1-K2** (north wall, 5.3 m), **B2 K5-K7** (north wall, 5.7 m), **B3 K22-K23** (notch south wall, 6.6 m), **B4 K25-K26** (south wall, 4.0 m); N-S **B5 K15-K19** and **B10 K19-K25** (west wall, 4.6 + 5.9 m), **B6 K14-K18** and **B9 K18-K23** (east wall, 4.8 + 4.4 m), **B7 K20-K27** (notch west wall / shaft west line, 5.9 m) and **B8 K10-K16** (core west line between the stair well and the shaft, inside the hall, 4.8 m). Max diagonal utilisation 0.38 (B8), gusset bolts 0.57. Reason for the layout: at every braced-bay base the bay shear enters the concrete along the column's long axis or towards the slab interior, never towards a free edge < 0.25 m; the middle columns K19, K18, K20 of the three N-S lines carry no net bracing uplift. Alternates if a bay is not door-free: B1 -> K3-K1, B3 -> K21-K22 (K21 base then needs a supplier-verified edge detail), B5/B10 -> single bay K15-K25 not possible (7.5 m), B8 -> none (K17-K21 and K11-K17 are excluded by the K21 / K11 edge condition).

Roof-plane bracing: M24 rods in {n_panels} rafter cells (full rafter depth, primaries as chords, rafters as posts), east/west edge trusses with rods over two bays and posts ST1/ST2 at the wall-column lines; the north-band shear passes the stair well through the jog panel x 77.8-81.85 / y 24.5-29.3 (y 29.3 primary as continuous chord, tie plates at K10, K11).

{truss_table}

## 9. Reactions at the column bases (kN, ULS envelope with concurrent values; reactions_C.csv gives every column and case: ULS-1, ULS-2/3 for N, S, E, W wind, ULS-4 +/-x, +/-y, SLS, with N, V_x, V_y, near-edge flags and base utilisation)

{reaction_table}

## 10. Weight and section list

{weight_table}

Sections: **IPE 330** (all E-W primaries and eave beams on the column rows, 92.5 m), **IPE 270** (rafters, edge beams, trimmers, truss posts ST1/ST2, 215 m), **HEA 160** (27 columns, WP1), plus L70x7 wall bracing, M24 rod roof bracing, Z200x2.0 purlins/girts. Three hot-rolled sections kept. Weight {Wtot} t against Rev 1 23.6 t (struts -1.3 t, two more bays and M24 rods +0.8 t, posts +0.4 t) and the scheme's 20.5 t.

## 11. Open items / risks

1. **Slab and column-head verification** (bases_C.md section 6): cores at 3 heads (thickness, solid zone >= 800 x 800, grade), rebar scan at all 27 heads (6 dia14 + dia6/200, cover) before setting out the 80 x 280 anchor pattern and the key pocket; pull-out tests on 3 anchors to 100 kN; supplier ETA group verification. The cage is relied upon for wall shear towards the slab edge (<= 29 kN vs 60 kN).
2. Wind: q_p 1.30 to be confirmed with the Libyan National Meteorological Centre; a 10 % increase raises the anchor cone utilisation at K19 to 0.84.
3. Purlin uplift capacity (>= 9 kNm single span with one anti-sag row) and the sleeved girt capacities to be confirmed with the supplier before order.
4. BoardX product data (0.30 kN/m2, girt rows per section 4) and its drift limit (h/150 assumed; diaphragm drift 10 mm, bay sway 4 mm).
5. Seismic: F_b 77 kN on the roof mass alone is below the wind bay forces; floor amplification through the existing building (S_a up to ~0.6 g / q) could bring the E-W seismic bay forces to the wind level - two-mass check once the building period is known; the bracing has 2.5 x reserve.
6. Drainage coordination: the drainage layout puts the west gutter at y 35.37; the structure roofs and walls the west block to y 35.87. Confirm the north edge; if 35.37, the north eave beam K6-K5-K7 and wall move 0.5 m south (no member change).
7. Client confirmations: door-free bays B1-B10 (section 8), B8 visible inside the hall along the core line, rafter R82 over the shaft east wall line (x 81.85 vs shaft face 81.99).
8. Temperature: slotted holes in the fin plates on the y 29.3 line (27.8 m).

Files: `design_report_C.md` (this), `bases_C.md`, `members_C.csv` (99 rows), `reactions_C.csv` (595 rows), `framing_C.png`, `calc/` (sections.py, model.py, loads.py, statics.py, takedown.py, bracing.py, members.py, connections.py, bases_note.py, run_all.py, write_report.py, report_text.md, summary_C.json).

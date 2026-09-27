# Alternative C - post-and-beam braced frame: design report (Rev 1 geometry)

System C: E-W primaries on the column rows, N-S rafters, pinned HEA columns, vertical X bracing for all lateral load, roof-plane X bracing as the diaphragm. All numbers come from the scripts in `calc/` (`python3 run_all.py; python3 write_report.py`); ULS design values unless stated.

## 1. Basis and assumptions

- Loads, combinations and resistances exactly per the binding `../load_basis.md`; geometry per `../../geometry.json` (27 columns, L-shape less the notch, stair and elevator openings not roofed; roofed area {roof_area} m2 from the grid).
- One roof plane at 6 % falling north, TOS(y) = 3.28 + 0.06 (35.87 - y). **Detail change vs the scheme:** the level primaries have their top at TOS + 0.04 (scheme: + 0.06), so the IPE 270 rafter bottom flange sits 20 mm above the IPE 330 bottom flange and clears it on the 3.4 deg cut without a cope; panel underside (TOS + 0.20) clears the primary top by 160 mm. Cap-plate top = TOS - 0.29, column length = TOS - 0.35 (plate + grout), 2.94 m (north) to 4.13 m (south); 3.01 m clear at the north eave.
- Statics: all beams are chains of simple spans, purlins simple spans between rafters, columns pinned-pinned. The take-down integrates the roof on a 0.1 m grid (exact tributary, openings excluded) -> rafters -> primaries -> columns. Section tables IPE 200-360 / HEA 140-200 in `calc/sections.py`.
- Wind zone note: the basis labels theta = 0 as wind from S; in EN 1991-1-4 Fig. 7.6 theta = 0 is the wind blowing onto the low (north) eave. To remove the ambiguity the larger set (F -2.3, G -1.3, H -0.8) is applied for **both** N and S wind with the F/G strip (e/10 = 1.2 m, F over e/4 = 3 m at the corners) on the windward edge; wind along the ridge uses F -2.1, G -1.8, H -0.6, I -0.5 with e = 12 m. c_pi = +0.2 (uplift) and -0.3 (pressure) both applied.
- Walls: BoardX on Z girts spanning between columns; girt reactions load the columns, half to the cap and half to the base. **The wall base rail is assumed anchored to the slab (M10 @ 600), so the lower half of the wall wind goes to the slab directly and the column bases see the bracing shear only**; the wall base shear is listed separately (V_wall) in the reaction table.
- Wind post WP1 (HEA 160) added at the notch corner (77.89, 19.97): wall wind only, slotted top connection, no uplift, base 2 M16 in a solid rib (5 kN shear).

## 2. Loads and combinations (kN, m)

| Action | Value | Used for |
|---|---|---|
| Panel + purlins + services G | 0.12 + 0.05 + 0.20 = 0.37 kN/m2 + member self-weight from the sections | gravity |
| G_min (uplift) | 0.17 kN/m2 + member self-weight | ULS-3 |
| Imposed cat. H Q | 0.60 kN/m2, psi_0 = 0 (never with wind) | ULS-1, SLS |
| Wind q_p | 1.30 kN/m2 at z_e = 10 m | all wind cases |
| Roof net uplift, c_pi +0.2 | H zone -(0.8+0.2) 1.3 = **-1.30**; G -1.95; F **-3.25** kN/m2 (N/S wind); along ridge G -2.6, F -2.99, H -1.04, I -0.91 | ULS-3, purlins, fly braces |
| Roof pressure case, c_pi -0.3 | (0.0 + 0.3) 1.3 = +0.39 kN/m2 (never governs over Q) | ULS-2 |
| Walls, net | D +1.1 (c_pi -0.3), A -1.4 / B -1.0 / C -0.7 / E -0.7 (c_pi +0.2), x 1.3 -> up to 1.82 kN/m2 char. | column bending, base V_wall |
| Global horizontal wind at roof level | 1.3 q_p on the projected wall area above the slab, half to the roof: **N {wN}, S {wS}, E {wE}, W {wW} kN** (char.) | bracing, diaphragm |
| Wall self-weight | 0.30 kN/m2 x wall height (3.58 m N ... 4.80 m S) x column trib | column axial |
| Seismic check (EN 1998-1, a_g 0.10 g, S 1.2, q 1.5, plateau S_d = 0.20 g) | seismic weight {seisW} kN (roof G + steel + half walls) -> F_b = **{Fb} kN** (1.0 E) versus 1.5 W = {wS_uls} kN (N-S) and {wE_uls} kN (E-W): **wind governs both directions**, no seismic design of the bracing needed | ULS-4 |

Combinations (EN 1990 6.10): ULS-1 1.35 G + 1.5 Q; ULS-2 1.35 G + 1.5 W (pressure case, wall D/E with c_pi -0.3, roof +0.39, bracing compression); ULS-3 1.0 G_min + 1.5 W (uplift, c_pi +0.2, four wind directions, bracing tension); ULS-4 1.0 G +/- 1.0 E check only; SLS G + Q (deflection L/200, purlins L/150) and G + W (sway H/150). Uniform ULS-1 roof load 1.35 x 0.37 + 1.5 x 0.60 = 1.40 kN/m2 plus steel.

## 3. Load take-down and bracing analysis results

**Take-down (scripts `takedown.py`).** 11 N-S rafter lines (x = 68.0, **70.0 (added)**, 72.1, 74.9, 77.8, 81.85, 84.5, 87.2, 89.9, 92.5, 95.5), rafter spans 2.7-9.2 m; purlin spans now 2.05-3.1 m (4.07 m only over the north strip of the stair well). Example column loads (characteristic, kN): K12 interior G {K12[G]:.1f} (incl. 0.20 services), Q {K12[Q]:.1f}, W_N {K12[W_N]:.1f}; K19 (braced, west wall) G {K19[G]:.1f}, Q {K19[Q]:.1f}, W_S {K19[W_S]:.1f}. Sum of column loads: G 428 kN, Q 268 kN (= 0.60 x 446 m2, check), W_N -610 kN (mean -1.37 kN/m2 with edge zones).

**Bracing (script `bracing.py`).** The roof force of each windward face is distributed to the braced bays twice: (a) rigid diaphragm, 3-DOF, bay stiffness k = E A cos^2(alpha)/L_d of one tension diagonal (k = 15.6-23.9 kN/mm), centre of rigidity and torsion included; (b) flexible-diaphragm tributary (each eave strip to the two adjacent bracing lines). **The envelope of (a) and (b) is used** (sum of bay forces 1.2-1.5 x the applied force, deliberately conservative). Characteristic bay shears for wind from S: rigid B5 26.4 / B6 30.5 / B7 25.6 / B8 26.3 kN, tributary 20.4 / 27.0 / 27.9 / 34.0 kN; for wind from E: rigid B1 18.4 / B2 18.1 / B3 18.7 / B4 16.7, tributary 1.3 / 25.9 / 35.4 / 9.6 kN. Bay B8 (K17-K21, x = 81.85, along the elevator shaft east wall) was **added** to the scheme's seven bays: without it B7 collected 54 kN char. (81 kN ULS) and 102 kN uplift at K20/K27, which the 4-anchor group cannot take.

Bay forces at ULS (1.5 W), tension-only diagonal T = H L_d/w, column axial N = H h/w, base shear H shared by the two bases through an HEA 160 base strut (see section 6):

{bay_table}

## 4. Member checks (EN 1993-1-1)

Checks per span: bending 6.2.5 (M_pl,Rd IPE 270 = 133 kNm, IPE 330 = 221 kNm), shear 6.2.6 (V_pl,Rd 351 / 489 kN; V_Ed < 0.5 V_pl everywhere so no M-V interaction), LTB 6.3.2 with M_cr from I_w, I_t and C1 per restraint segment (C1 = 1.88 - 1.40 psi + 0.52 psi^2 for linear segments, 1.0 when the maximum lies inside the segment), curve b, and deflection G + Q <= L/200 by numerical double integration.

Restraint assumptions: rafters - top flange held by purlins @ 1.5 m (gravity, chi_LT = 1.0); under uplift the free bottom flange is held by **fly braces to the purlins at mid-span for spans <= 6.6 m and at the third points for 7.5 and 9.2 m spans** (segment 2.2-3.25 m, M_b,Rd >= 98 kNm for IPE 270). Primaries - both flanges restrained at the rafter fin plates (plate over the full rafter web depth, bottoms 20 mm apart) and at the columns, segments <= 4.1 m (eave beams without rafters: full span).

{member_table}

Governing members: primary **K19-K20 (9.79 m)** at 0.74 (deflection 36 mm = L/271; M_Ed 131 kNm = 0.59 M_pl; LTB 0.73 with C1 = 1.86 on the 4.1 m end segment); 9.2 m rafters at 0.49-0.52 (deflection 22-24 mm = L/390-410, M 0.35, LTB uplift 0.51). Max beam utilisation {maxbeam}. Alternatives run with the same scripts: IPE 240 rafters pass strength (M 0.58, LTB uplift 0.71) but give L/265 on the 9.2 m spans with no reserve for a future ceiling, so IPE 270 is kept; IPE 300 primaries put K19-K20 at L/194 (1.03): IPE 330 confirmed.

Rafters as roof-truss posts: N_Ed = {postN} kN with N_b,Rd = {postNb} kN (L_y 9.2, L_z 3.07 m) -> 0.09; eave primaries as struts <= 53 kN vs N_b,Rd >= 800 kN. Purlins are not used as struts.

**Columns** (6.3.1 pinned-pinned, L_cr = L both axes, HEA 160 curve b/c; 6.3.3 Annex B method 2 with C_m = 0.95 for the wall-wind UDL, orientation web perpendicular to the wall it supports, corners biaxial). N_b,Rd = 465 kN (L 4.13 m) to 673 kN (L 2.94 m).

{column_table}

Max column utilisation {maxcol} (K25, SW corner: N 50 kN, M_y 14.8 + M_z 12.2 kNm). Wind post WP1 HEA 160, L {wpL} m: M_y {wpMy}, M_z {wpMz} kNm -> {wpu}. HEA 140 was run and reaches 1.00 at K25: **HEA 160 confirmed**.

**Purlins Z200x2.0 @ 1.5 m** (basis: M_Rd 12.5 kNm single span, 16 sleeved; I = 3.9e6 mm4; capacity assumed valid for uplift with the free flange braced by the anti-sag bar at mid-span - to be confirmed by the supplier): worst gravity M_Ed = {Mg} kNm, worst uplift M_Ed = **{Mu} kNm** (4.07 m span over the north strip of the stair well, {Mu_where}, G zone), i.e. 0.68 of the single-span value; elsewhere spans <= 3.1 m give <= 6.5 kNm (0.52). Deflection G + Q on {Lp} m: {dp} mm < L/150 = {dplim} mm. Single-span cleated purlins are sufficient everywhere (sleeves optional). Girts (same section, wall net pressure 1.5 x 1.1 x 1.3 = 2.15 kN/m2, zone A 2.73 kN/m2 within 2.4 m of a corner): bays <= 5.3 m take 1.5 m rows single-span (M_Ed <= 11.3 kNm); **K5-K7, K25-K19 and K8-K6 (5.7-5.9 m) need 1.2 m rows sleeved (<= 14.2 kNm); K21-K22, K22-K23 and K14-K4 (6.4-7.1 m) need 1.0 m rows sleeved (<= 14.9 kNm, 0.93)**. The girt length in section 10 follows this rule.

## 5. Connections (EN 1993-1-8)

- **Rafter to primary fin plate**, one type: 100 x 150 x 10 S275, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web, 2 x 6 mm fillets. Max rafter end reaction {Vfin} kN (envelope ULS-1 / reversed ULS-3): bolt shear incl. eccentricity {fin2_bs}, bearing on the 6.6 mm rafter web **{fin2}** (governs), plate bearing {fin2_bp}, plate shear {fin2_ps}, plate bending {fin2_pb}, weld {fin2_w}, web block tearing {fin2_bt}. 9.2 m rafters: 3 bolts, plate 220 ({fin3} at {Vfin_long} kN). No copes. T1/T2 and the notch eave beam use the same detail.
- **Primary to column cap plate** 200 x 240 x 20, a = 6 all round, 4 M20 through the primary bottom flange (gauge 90, pitch 140). Tension = roof uplift {Nt_cap} kN (K12, ULS-3N; the bracing vertical component enters below the cap through the gusset): bolt tension {cap_bt}, shear + tension interaction with the chord/strut force {Vh_cap} kN {cap_bi}, IPE 330 flange T-stub {cap_ts}, cap plate 0.06, weld {cap_w}. Chord continuity across a column (<= 46 kN): 10 mm tie plate between the primary bottom flanges on the lines y 29.3 and y 20.1.
- **Bracing gussets**: 10 mm plates welded to the column web and base plate; each L70x7 with 2 M20 (e1 40, p1 110): angle net section 0.7 A_net f_u/gamma_M2 = 189 kN, bolt shear 188 kN, gusset bearing 2 x 98 kN; max T_Ed 68 kN (B8) -> 0.36 / 0.36 / 0.35.
- **Roof bracing** M20 rods 8.8 with turnbuckles, F_t,Rd 141 kN, to 8 mm gussets on the rafter and primary webs at the bottom flange level; sag ties to the purlins at the crossing and at 3 m centres on the 9.6 m diagonals.
- Trimmers T1 (y 35.37) and T2 (y 24.16) IPE 270 between the rafters x 77.8 / 81.85 carry only the 150 mm upstand (0.3 kN/m, M_Ed 1.8 kNm); upstand framing 100 x 50 x 3 cold-formed C on the trimmers and along the rafters beside the openings, cricket on the south side of the stair well.

## 6. Bases and anchors (EN 1993-1-8 6.2.5, EN 1992-4 with the basis values)

Base plate 300 x 400 x 20 S275 on 40 mm non-shrink grout, 4 M20 resin anchors at 200 x 300, h_ef 170 mm, in the assumed 800 x 800 solid zone (>= 100 mm from its edge in the plate's short direction; **cores to prove the solid zone before drilling**). In each braced bay an **HEA 160 base strut** lies on the slab between the two base plates (bolted to a side gusset on each plate, under the wall base rail), so the bay shear H is shared by the two 4-anchor groups (H/2 each in the table of section 9).

- Bearing: effective area {Aeff} cm2 (c = 60 mm), 10 MPa -> 763 kN; max N_c 90 kN (K22) -> 0.12. Plate under uplift (T-stub cantilever m = 69 mm): {wb_pb}.
- Anchor tension group: cone A_c,N/A_c,N0 = {ratio_c} (i.e. 0.55 per anchor, edge to the solid zone 250 mm, psi_s 0.99) -> N_Rd,c = **{NRd_c} kN**; bond N_Rd,p = {NRd_p} kN; steel 4 x 140 kN. Worst uplift 74 kN at K20/K19 (ULS-3S, roof + bracing) -> cone {wb_cone}.
- Anchor shear group: steel 4 x 70 kN, pry-out {VRd_cp} kN, concrete edge failure towards the solid-zone boundary (treated as a free edge, k = 2.4 uncracked, A_c,V limited by the 250 mm slab) V_Rd,c = **{VRd_c} kN**; V = 26.6 kN at K22/K23 (B3) -> 0.55, 20.9 kN at {worst} -> {wb_edge}. N-V interaction (exponent 1.5): **{wb_int} at {worst}**; all bases <= 0.80 (table in section 9).
- Without the base strut the braced-bay bases would see 51-53 kN shear (1.1 of V_Rd,c) and fail the interaction; without the anchored wall rail a further 13-29 kN. Both details are therefore mandatory.

## 7. Deflections and sway

- Roof members SLS G + Q: worst primary K19-K20 36 mm = L/271 (limit L/200 = 49 mm); 9.2 m rafters 22-24 mm = L/390; 7.5 m rafters L/700-820, all other spans > L/1000. Purlins L/640.
- Sway of the braced bays under SLS wind (elastic diagonal elongation + 2 mm bolt-slip allowance): 2.8-3.9 mm against h/150 = 20.7-28.7 mm (utilisation <= 0.15). Column bending deflection under wall wind (SLS, K22: 9.8 kN/m on 3.88 m) 8.2 mm = h/470. 

## 8. Bracing

Vertical bays (X, single L70x7 per diagonal, tension-only, 8 bays): E-W B1 K1-K2, B2 K5-K7, B3 K22-K23, B4 K25-K26; N-S B5 K15-K19, B6 K14-K18, B7 K20-K27, **B8 K17-K21 (new)**. Max diagonal utilisation 0.36 (B8); L60x6 would also pass, L70x7 kept for stiffness. Bays must stay door-free (alternates: B1 -> K3-K1, B3 -> K21-K22, B5 -> K19-K25, B6 -> K18-K23, B8 -> K11-K17).

Roof-plane bracing: X of M20 rods in {n_panels} rafter bays (full rafter depth, primaries as chords, rafters as posts) forming the horizontal trusses below; the north band shear passes the stair well through the jog panel x 77.8-81.85 / y 24.5-29.3 with the y 29.3 primary as continuous chord (tie plates at K10, K11).

{truss_table}

## 9. Reactions at the column bases (kN; + compression, uplift listed positive in its own column; V from bracing shared by the base strut; V_wall = wall base shear taken by the anchored wall rail)

{reaction_table}

## 10. Weight and section list

{weight_table}

Sections: **IPE 330** (all E-W primaries and eave beams on the column rows, 92.5 m), **IPE 270** (rafters, edge beams, trimmers, 205 m), **HEA 160** (27 columns, WP1, base struts), plus L70x7 wall bracing, M20 rod roof bracing, Z200x2.0 purlins/girts. Three hot-rolled sections as in the scheme; the weight is {Wtot} t against the scheme's 20.5 t (added rafter line +0.7 t, base struts +1.3 t, 10 % plates instead of 1.5 t, full girt count).

## 11. Open items / risks

1. **Slab solid zones**: the anchor group results assume an 800 x 800 solid zone at every column head and treat its boundary as a free edge for shear (V_Rd,c 48 kN). Core 3-4 column heads before final design; a larger zone or a drop beam lowers the utilisations, a smaller one means supplier-verified anchors or a second bay on the same line for the braced-bay bases. EN 1992-4 group verification with the supplier software remains open (basis).
2. Wind coefficients: the roof zones were enveloped (theta = 180 values for both N and S); local wind speed and the city are unconfirmed - a 10 % higher q_p raises uplift utilisations proportionally (anchor cone at K20 -> 0.72).
3. Purlin uplift capacity with the free flange in compression (Z200x2.0, 8.6 kNm required on the 4.07 m strip, 6.5 kNm elsewhere) and the girt capacity on the 7.1 m bay (sleeved) to be confirmed with the purlin supplier's tables.
4. Wall base rail anchorage to the slab (M10 @ 600) and the BoardX product data (0.30 kN/m2, girt rows per section 4) to be confirmed; otherwise add V_wall to the column bases.
5. Door-free braced bays B1-B8 to be confirmed by the client; B8 lies along the elevator shaft east wall inside the hall (hidden by the shaft enclosure if the lift stops at the slab).
6. Temperature: slotted holes in the fin plates on the y 29.3 line (27.8 m) and at the base struts.
7. Ponding: the 6 % slope and L/271 deflection give no risk; the cricket on the south side of the stair well must keep the 6 % fall to the trimmer.

Files: `design_report_C.md` (this), `members_C.csv` (96 rows: spans, columns, bracing), `reactions_C.csv`, `framing_C.png`, `calc/` (sections.py, model.py, loads.py, statics.py, takedown.py, bracing.py, members.py, connections.py, run_all.py, write_report.py, summary_C.json).

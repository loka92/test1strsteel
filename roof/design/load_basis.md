# Common load and design basis (binding for both alternatives A and C) - Rev 2

Codes: EN 1990, EN 1991-1-1/-1-4, EN 1993-1-1/-1-8, EN 1992-4 (anchors), EN 1998-1 (check only). Units kN, m.

## Geometry
- Roof: ONE plane, 6 % (3.43 deg) falling NORTH; top of steel at north edge y=35.87 set by 3.0 m clear at the north eave; rise 1.22 m to y=15.57.
- Openings not roofed: stair x 77.89-81.79 / y 29.37-35.37 and elevator x 77.89-81.99 / y 20.17-24.16. Roofed area 446 m2, footprint 486 m2.
- Enclosed hall: BoardX wall panels on cold-formed girts on all perimeter bays. Perimeter 96.2 m.
- Reference height for wind: existing building ~4.0 m + new roof up to 6.0 m -> z_e = 10 m.

## Permanent actions (characteristic)
- PIR sandwich roof panel 50 mm: 0.12 kN/m2
- Purlins Z200x2.0 @ 1.5 m incl. bridging: 0.05 kN/m2
- Services, lighting, fans: 0.20 kN/m2 (treat as permanent)
- Primary steel self-weight: from the actual sections (or 0.15-0.25 kN/m2 in first pass)
- Wall: BoardX + girts 0.30 kN/m2 of wall, applied to perimeter columns
- For uplift combinations use only panel + purlins + steel self-weight (no services): G_min = 0.17 kN/m2 + steel

## Variable actions
- Imposed roof load, category H (not accessible): q_k = 0.60 kN/m2 (uniform) and Q_k = 1.0 kN point; psi_0 = 0, so NOT combined with wind.
- Wind (Rev 2, site Tripoli, Libya): v_b = 27 m/s (10-min mean, 50-year; Libyan standard value 22 m/s and regional 3-s gust maps of 36-40 m/s bracket it), coastal site -> terrain category I for winds from the sea, c_e(10 m) = 2.75 -> q_p = 0.5 x 1.25 x 27^2 x 2.75 /1000 = 1.25 kN/m2. BINDING DESIGN VALUE UNCHANGED: q_p = 1.30 kN/m2 (covers the uncertainty; to be confirmed with the Libyan National Meteorological Centre).
  - Mono-pitch roof, pitch 3.4 deg -> use EN 1991-1-4 Table 7.3a for 5 deg (interpolate with flat roof if wanted):
    theta = 0 = wind from the LOW eave side = from the NORTH here (roof falls north): zones F -1.7/+0.0, G -1.2/+0.0, H -0.6/+0.0 (cpe,10)
    theta = 180 = wind from the HIGH eave side = from the SOUTH: F -2.3, G -1.3, H -0.8
    (Rev 2 correction: the two directions were labelled the wrong way round in Rev 1 - reviewers' finding.)
    wind along the ridge (theta=90): F_up -2.1, F_low -2.1, G -1.8, H -0.6, I -0.5
  - Walls: D +0.8 (h/d<=1 -> +0.7 to +0.8), E -0.5 (use -0.5), A -1.2, B -0.8, C -0.5.
  - Internal pressure enclosed building: c_pi = +0.2 and -0.3 (both to be tried).
  - Net roof uplift general zone H approx. -(0.8+0.2) x 1.30 = -1.3 kN/m2; edge zones F approx. -3.3 kN/m2 (use for purlins, trimmers and edge members only).
  - Zone size (Rev 2 correction): e = min(b, 2h) with h = height above GROUND (z_e = 10 m) -> e = 20 m for both wind directions; F/G edge strip = e/10 = 2.0 m deep, corner zone F width e/4 = 5.0 m along the eave.
  - Global horizontal wind force on the hall (Rev 2 correction): walls (cpe,D - cpe,E) = 0.8 + 0.5 = 1.3 x q_p on the projected wall area above the slab (no friction term: the building is shorter than 4h, so none applies), PLUS the horizontal component of the roof suction on the 3.43 deg plane: for wind from the south the net roof suction (zones per direction) acts normal to the roof and its horizontal component (sin 3.43 deg = 0.06) adds to the wind force on the walls (about +37 kN characteristic for the full roof). Wall height N 3.6-4.8 m, S 4.8-6.0 m depending on system.
- Seismic (Rev 2): Tripoli low seismicity; keep a_g = 0.10 g, soil B, q = 1.5 (braced) as a check only; wind governs.
- Temperature: +/-30 K on members: provide slotted holes / expansion allowance on the 27.8 m length; no calculation required.

## Combinations (EN 1990 eq. 6.10)
- ULS-1: 1.35 G + 1.5 Q_roof
- ULS-2: 1.35 G + 1.5 W (pressure case, wind from N with cpi -0.3 on walls; for the roof use the downward zones if any)
- ULS-3: 1.0 G_min + 1.5 W (uplift, cpi +0.2)
- ULS-4: 1.0 G +/- 1.0 E (seismic) - check only
- SLS: G + Q for deflections; G + W for sway.
- Deflection limits: roof members L/200 (purlins L/150), cantilevers L/100, column sway H/150 (BoardX panels; state if the panel supplier needs less).

## Materials and resistances
- Steel S275: f_y = 275 MPa (t <= 16 mm), E = 210 GPa, gamma_M0 = 1.0, gamma_M1 = 1.0, gamma_M2 = 1.25.
- Bolts 8.8: f_ub = 800 MPa; M20 A_s = 245 mm2, F_t,Rd = 0.9 x 800 x 245/1.25 = 141 kN, F_v,Rd (threads in shear) = 0.6 x 800 x 245/1.25 = 94 kN.
- Purlins/girts: Z200x2.0 S350GD, use manufacturer capacity as M_Rd = 12.5 kNm (single span), 16 kNm sleeved continuous; I = 3.9e6 mm4; state the assumption.
- Anchors (Rev 2, client decision): M20 (or M24) resin anchors (EN 1992-4 / ETA) drilled THROUGH the slab solid zone INTO the column head: total embedment h_ef = 300 mm (250 mm slab + >= 50 mm into the column; use h_ef = 400 mm if the check needs it). Anchors inside the column core: pattern within 200 x 400 minus 30 mm cover and clear of the 6 dia14 bars, e.g. 4 anchors at 80 x 280 mm; rebar scan before drilling. Tension: bond N_Rk,p = pi x d x h_ef x tau_Rk (tau_Rk = 10 MPa for C25, cracked) and concrete cone in the slab solid zone (assume solid zone >= 800 x 800, to be confirmed by cores) with h_ef = 250 mm for the cone, k = 7.2 (cracked); group factors per EN 1992-4. Shear: anchors may not resist shear towards a free slab edge (c1 < 150 mm); provide a grouted shear key (plate or stub welded under the base plate into a cored pocket) bearing on the slab/column-head concrete, or a through-bolt, wherever the base shear has a component towards the slab edge. gamma_Mc = 1.5, gamma_Ms = 1.4, gamma_Mp = 1.5.
  Assumed characteristic: N_Rk,steel = 196 kN; N_Rk,c (single, concrete cone, uncracked C25, h_ef 170) = 7.2 x sqrt(25) x 170^1.5 /1000 = 80 kN; N_Rk,p (bond, d=20, tau=10 MPa) = 107 kN; V_Rk,s = 98 kN. gamma_Mc = 1.5, gamma_Ms = 1.4. Group factors per EN 1992-4 (s_cr,N = 3 h_ef = 510 mm, so a 4-anchor group in a 200x400 column is heavily overlapped: A_c,N/A_c,N0 approx. 0.5-0.6). Anchor-group verification with the supplier software is a stated open item.
- Existing hollow-block slab: assume 250 mm ribbed slab, solid zone 800x800 around each column head (cores at 3 heads before detailing); bearing under grout: f_cd = 25/1.5 = 16.7 MPa, use 0.6 f_cd for local bearing on the slab = 10 MPa.

## Column positions
See ../geometry.json (27 columns K1-K27, 0.2 x 0.4 m, orientation as listed). Steel columns sit centred on them.

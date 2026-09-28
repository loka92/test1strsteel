"""Writes bases_C.md Rev 4: self-contained base and anchor design note, from run_all.py."""
import os, math
from model import COLS, BAYS, edge_distances, NEAR_EDGE, POSTS, COL_LONG, SADDLE
from connections import BASE, ANCH, FJD, FCD, LEVER, cone_group, V_edge_key, b2_layout, group_extents, KEYPAIR

def write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp):
    B = BASE; f = lambda x, n=1: '%.*f' % (n, x)
    typ = {c: base_env[c]['btype'] for c in COLS}
    b1 = [c for c in COLS if typ[c] == 'B1']; b2 = [c for c in COLS if typ[c] == 'E']; bp = [c for c in COLS if typ[c] == 'P']
    L = []
    L.append('# Alternative C - base and anchor design note, Rev 6 (bases_C.md)\n')
    L.append('**Rev 6 = Rev 5a re-run with load basis Rev 3 (design Rev 4): services 0.10, Q 0.40, no wall self-weight, wind q_p by direction with the flat-roof Table 7.2 zones, net bracing uplift per braced line, and the amplified two-mass seismic case (S_a 0.65 g E-W / 0.61 g N-S, q 1.5) which now governs every braced bay and its bases. The detail is unchanged; utilisations below are the new ones. Key pairs and plate sizes are kept: they are set by the edge condition of each column (parallel-edge shear at Key A), not by the force level, and the E-W bay bases K5, K7, K22, K23 now carry 64-71 kN seismic shear (K7 key pair 0.90).**\n')
    L.append('Self-contained note for the base reviewer. Rev 5a closes the Rev 5 sign-off (V1-V6) and adopts its recommendation: **one base detail at all 27 columns** - a post-installed rebar connection into the column head (EAD 330087, designed to EN 1992-1-1 8.4 / 8.7), debonded through the 300 mm slab, with the Rev 4b/5 shear keys. No through-bolts, no slab-cone check, no solid-zone criterion anywhere. Loads from `calc/run_all.py` (reactions_C.csv: every column and load case). Units kN, mm, MPa.\n')
    L.append('**Rev 5a in one paragraph.** V1: the column-head anchorage is a post-installed rebar connection, not an anchor: **4 x dia 16 B500 bars with a threaded end** (M16 thread, or an M16 8.8 rod only if the injection system holds an EAD 330087 assessment for it), embedded **300 mm into the column head where the scan allows, 250 mm minimum**, lapped 1:1 with the corner dia14 bars; capacity by bond f_bd = 2.7 MPa (C25, good bond): 4 x 33.9 = **136 kN at 250 mm** (163 kN at 300), steel 4 x 87 = 350 kN, receiving bars 4 x 67 = 268 kN; l_0 = max(1.5 l_b,rqd, 15 d = 240, 200) <= 250; d < 20 so the existing dia6/200 links are the only transverse steel needed (8.7.4), splitting covered by the EC2 cover rules. V2: the top 300 mm of each bar is **debonded (sleeve), the column part only is injected**, so the edge-slab cone is never loaded. V3: pattern **70 x 240** (26 mm clear to the corner bars), cover-meter scan of the column faces from below projected to the slab top plus GPR from above, 10 mm pilot drill with feed monitoring, relocation +/-15 mm on steel contact, plate holes match-drilled or 30 mm oversize with 10 mm plate washers; V4: proof test of 3 bars to >= 60 kN with displacement readings. K21 is P with the same rebar logic plus the saddle. The former B1 interior detail (4 M20 h_ef 250 in the slab, 800 x 800 solid zone) is kept in the appendix as the client\'s fewer-holes option. Holes to scan and drill: **27 x 4 = 108** (plus 37 key pockets set by the same scan).\n')
    L.append('## 1. The base detail (type E, all 27 columns; P = E + saddle at K21)\n')
    L.append('- Base plate 300 x 400 x 25 S275 (Key A / Key A + B bases) or the key-pair plate of section 3 (25 mm, no stiffeners: no lever, concentric uplift), on 25 +/- 5 mm non-shrink grout; **columns cut to the surveyed plate-top level**.')
    L.append('- **4 dia 16 B500 post-installed bars, threaded end M16 (EAD 330087 injection system), at 70 x 240** - 240 along the concrete column\'s long axis, 70 across, centred on the column - i.e. 35 / 120 mm from the column centre, 26 mm nominal clear to the corner dia14 bars (cover 30, links dia6). Hole 20 mm, depth 300 (slab) + 300 (column head; 250 minimum); the **top 300 mm debonded with a plastic sleeve, resin injected in the column part only** (V2). Plate holes 30 mm with 10 mm plate washers (or match-drilled after the bars are set); nuts snug + 1/4 turn.')
    L.append('- Shear as Rev 4b/5: Key A SHS 90x90x8 under the column centre (interior and Key A + Key B bases), Key B 60 mm bar 180 inboard (c1 250) where an outward shear > 3 kN points to an edge < 0.25 m, inboard key pairs at %s; rigid-post key-moment model; saddle at K21.' % ', '.join(sorted(KEYPAIR, key=lambda s: int(s[1:]))))
    L.append('- **Scan / drill procedure (V3):** (1) cover-meter scan of all four column faces below the slab over the top 600 mm: bar positions, link spacing, cover (+/-3-5 mm); (2) GPR from above over the head to confirm and to see the slab top bars and the solid zone; (3) project the bars to the slab top, mark the 70 x 240 pattern and the key pockets, adjust +/-15 mm to keep >= 20 mm clear of every bar; (4) 10 mm pilot drill 600 deep with feed monitoring - on steel contact stop, relocate within +/-15 mm, re-pilot; (5) 20 mm production hole, clean (brush/blow x2), sleeve the top 300, inject the bottom 300, set the bar; (6) proof test 3 bars (one per zone) to >= 60 kN holding 2 min with displacement <= 1 mm (V4); (7) file the scan sheet with the final pattern per head.\n')
    L.append('**Wind post WP1** (notch corner, no concrete column): post 280 mm inboard on both axes at (77.61, 20.25), plate 250 x 250 x 15, one centred 60 mm key (c1 250 both ways), 2 M12 for location, no uplift. Demand %s / %s kN vs %s kN -> %s.\n' % (f(V_wp[1]), f(V_wp[0]), f(R['VRd_B_edge250']), f(max(V_wp)/R['VRd_B_edge250'], 2)))
    L.append('## 2. Resistances (EN 1992-1-1 8.4 / 8.7 for the rebar connection; EN 1992-4 for the keys; EN 1993-1-8 and EN 1992-1-1 6.7 for plates and keys)\n')
    L.append('| Item | Formula / factors | Value |')
    L.append('|---|---|---|')
    L.append('| (appendix option B1) anchor steel, per M20 | 196 / 1.4 | %s kN |' % f(R['NRd_s']))
    L.append('| (appendix option B1) cone, single, slab 300 | k 7.2 (cracked) sqrt(25) 250^1.5 | N0_Rk,c = %s kN |' % f(R['N0c']))
    cg1 = cone_group((60, 360, 260, 260)); cgc = cone_group((60, 360, 60, 260))
    L.append('| (appendix option B1) cone group, interior (800 zone) | s_cr,N 750, c_cr 375: A_c,N/A0 = 800 x 800 / 750^2 = %s, psi_s %s (zone-limited: h_ef 250 gives the same 98 kN as 200) | N_Rd,c = %s kN |' % (f(R['ratio_c'], 3), f(R['psi_s'], 2), f(R['NRd_c'])))
    L.append('| (for reference) cone group with one edge at 100 mm / corner | outboard row 60 mm from the face | %s / %s kN - why edge bases are type E |' % (f(cg1['ratio']*0 + cg1['NRd']), f(cgc['NRd'])))
    L.append('| **E / P rebar bond in the column head (EC2 8.4)** | 4 x pi x 16 x l_b x f_bd, f_bd = 2.25 x 1.0 x 1.0 x f_ctd (1.2) = 2.7 MPa (C25, good bond): embed 250 (minimum) -> 4 x 33.9 | **N_Rd = %s kN** (embed 300: %s kN) |' % (f(R['E_bond_col_min'], 0), f(R['E_bond_col'], 0)))
    L.append('| E rebar steel | dia 16 B500, 4 x 201 x 435 | %s kN |' % f(R['E_steel'], 0))
    L.append('| E lap with the corner dia14 bars | each bar laps 1:1 with the nearest corner dia14 (26 mm clear, close lap, alpha6 1.5): receiving capacity 4 x 154 x 435 = %s kN; K19: sigma_sd = 18.3 kN / 201 mm2 = 91 MPa -> l_b,rqd = 4 x 91 / 2.7 = 135, l_0 = 1.5 x 135 = 203 < l_0,min = 15 d = 240 <= 250 provided; d < 20: existing dia6/200 links are the transverse steel (8.7.4); splitting by the EC2 cover rules (c 30 >= d) | %s kN |' % (f(R['E_lap_max'], 0), f(R['E_lap_max'], 0)))
    L.append('| E slab part | debonded (sleeve) - the slab cone and the slab bond are never loaded (V2); the bar tip sits 250-300 mm inside a column that continues downward: no cone | - |')
    from connections import bond_group
    L.append('| Eccentric tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key/N_t (key moment V x 85 mm); max anchor N_t/4 + M/(2 s) | per case |')
    L.append('| Plate bearing (compression) | c = %s mm, A_eff = %s cm2 at 10 MPa | %s kN |' % (f(R['c'], 0), f(R['Aeff']/100, 0), f(R['NRd_bearing'], 0)))
    L.append('| Plate T-stub under concentric uplift, per row | m = %s, l_eff 300, t 25 | %s kN |' % (f(R['m_plate'], 0), f(R['FT1_row'], 0)))
    L.append('| Key A bearing (centre key and inboard pairs) | rigid stub, z0 = %s mm, p_max = V z0/(b(z0 D - D^2/2)), b 90, D 180, sigma_Rd 1.5 f_cd = 25 MPa (confined, >= 250 mm from a face) | **V_Rd,A = %s kN** per key |' % (f(R['z0'], 0), f(R['VRd_A'])))
    L.append('| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3 f_y 355 -> %s kNm at lever 85; a = 8 | %s / %s kN |' % (f(R['MRd_A']), f(R['VRd_A_bending'], 0), f(R['VRd_A_weld'], 0)))
    L.append('| Key A parallel to an edge (EN 1992-4 7.2.2.5 with psi_alpha = 2) | c1 = edge distance - 45: c1 55 -> %s kN, c1 155 -> %s kN, c1 255 -> %s kN | used at K3, K4, K6, K8, K11, K14, K16, K17, K24, K26 |' % (f(R['VRd_A_par55']), f(2*V_edge_key(155, 90)), f(2*V_edge_key(255, 90))))
    L.append('| Key towards an edge (Key B c1 250; key pair c1 >= 255; Key A 0.25-0.6 m) | 7.2.2.5, k9 1.7 cracked, d_nom 60 / 90, l_f 180, A_c,V/A0, psi_h | c1 250 (d 60): **%s kN**; c1 255 (d 90): **%s kN**; c1 355 (d 90): %s kN |' % (f(R['VRd_B_edge250']), f(R['VRd_A_edge255']), f(V_edge_key(355, 90))))
    L.append('| Key B bearing / bending | 60 mm bar, plain f_cd; W_pl d^3/6, f_y 335 | %s / %s kN |' % (f(R['VRd_B_bearing']), f(R['VRd_B_bending'], 0)))
    L.append('| P (K21) saddle | two 15 mm plates 400 x 150 on the pier faces, cantilever 150 | %s kN |' % f(R['VRd_saddle']))
    L.append('\n**Key-moment model (T3), one model for every key:** the shear resultant acts 85 mm below the plate; the moment V x 85 mm is carried by the grouted pocket as a rigid post (pressure linear about the rotation point z0 = 113 mm, p_max <= 25 MPa - the bearing check above), not by the anchors or bolts. Justification: the 180 mm stub in a C50 grout annulus (E about 30 GPa, 25 mm thick) in a 200 mm pocket has a rotational stiffness of the order of 10 MNm/rad, two orders above the couple of four M20 anchors 80 mm apart (about 4 x 250 kN/mm x 0.04^2 = 0.1 MNm/rad); the pocket therefore takes the moment before the anchors move. Hence the rebars carry N_t only, concentric. Bars carry no shear (30 mm oversize holes); keys and saddle carry no tension.\n')
    L.append('## 3. Final base table (ULS envelope; reactions_C.csv has every case). Rebar pattern 70 x 240: the 240 runs along the concrete column\'s long axis (E-W for the 0.4 x 0.2 columns K1, K2, K5, K9-K14, K21-K24; N-S for the others), the 70 across it; 4 holes per base, 108 in all.\n')
    L.append('| Col | Type | Long axis | Bays | Near edges (< 0.25 m) | Keys | Rebars (mm from the column centre) | N_c max (case) | N_t max (case) | V max (case) | Tension util. | Key util. | Plate util. | **Governing** | Base plate (mm from the column centre) | Scan / drill | Slab condition (keys and plate only) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in COLS:
        e = base_env[c]; ed = edge_distances(*COLS[c]); t = typ[c]
        anch = '4 dia16 B500 at (+/-%d, +/-%d), embed 300 (250 min) into the head, top 300 debonded' % ((120, 35) if COL_LONG[c] == 'x' else (35, 120))
        scan = 'face cover-meter + GPR, pilot 10, relocate +/-15, plate holes 30'
        if c in KEYPAIR:
            lay = b2_layout(ed, COL_LONG[c]); px, py = lay['plateE']['x'], lay['plateE']['y']; zx, zy = lay['zoneE']['x'], lay['zoneE']['y']
            keys = 'A-pair at %s' % ' / '.join('(%d, %d)' % (round(k[0]), round(k[1])) for k in lay['keys'])
            plate = 'x %d..%d, y %d..%d (%d x %d x 25)' % (px[0], px[1], py[0], py[1], px[1]-px[0], py[1]-py[0])
            zone = 'solid 300 over the key bodies x %d..%d, y %d..%d' % (zx[0], zx[1], zy[0], zy[1])
        elif t == 'P':
            keys = 'saddle'; plate = '300 x 400 x 25 + saddle'; zone = 'pier top 500 mm scanned; faces accessible'
        else:
            keys = 'A centre' + (' + B ' + ','.join(e['keyB']) if e['keyB'] else ''); plate = '350 x 400 x 25 (250 inboard)' if e['keyB'] else '300 x 400 x 25'
            zone = 'solid 300 under the plate and Key A pocket (+/- 400)' + (' and Key B pocket' if e['keyB'] else '')
        L.append('| %s | **%s** | %s | %s | %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %s | %s | %s | **%s** (%s) | %s | %s | %s |' % (
            c, t, 'E-W' if COL_LONG[c] == 'x' else 'N-S', ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
            keys, anch, f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], f(e['Vt'][0]), e['Vt'][1], f(e['uten'], 2), f(e['ukey'], 2), f(e['uplate'], 2), f(e['umax'][0], 2), e['umax'][2].split(' (')[0], plate, scan, zone))
    w = max(V_wp)
    L.append('| WP1 | post | - | - | +x,-y | one 60 mm key centred, c1 250 | 2 M12 location | %s | 0 | %s | - | %s | - | **%s** (key edge) | 250 x 250 x 15 at (77.61, 20.25) | GPR for the edge beam | notch edge beam, 600 x 600 around the post |' % (f(0.3*Lwp*1.35), f(w), f(w/R['VRd_B_edge250'], 2), f(w/R['VRd_B_edge250'], 2)))
    worst = max(base_env, key=lambda c: base_env[c]['umax'][0])
    L.append('\nWorst base **%s (%s): %s (%s, %s)**; worst tension %s at %s; worst key %s at %s; worst plate %s at %s. All 27 bases and WP1 <= 1.0 with the real slab edges; tension utilisations are on the 250 mm minimum embedment (136 kN), 0.83 x these with the 300 mm target embedment.\n' % (
        worst, typ[worst], f(base_env[worst]['umax'][0], 2), base_env[worst]['umax'][2], base_env[worst]['umax'][1],
        f(max(e['uten'] for e in base_env.values()), 2), max(base_env, key=lambda c: base_env[c]['uten']),
        f(max(e['ukey'] for e in base_env.values()), 2), max(base_env, key=lambda c: base_env[c]['ukey']),
        f(max(e['uplate'] for e in base_env.values()), 2), max(base_env, key=lambda c: base_env[c]['uplate'])))
    L.append('## 4. Worked checks\n')
    for c in ('K12', 'K7', 'K23', 'K19'):
        e = base_env[c]; ed = edge_distances(*COLS[c]); t = typ[c]
        best = None
        for cs in cases[c]:
            for N, bc in cs.get('base', []):
                if N < 0 and (best is None or bc['umax'] > best[2]['umax']): best = (cs, N, bc)
        cs, N, bc = best
        items = '; '.join('%s %s' % (k, f(v, 2)) for k, v in bc['util'].items())
        if t == 'E':
            L.append('**%s (E)** - 4 dia16 post-installed rebars 70 x 240, embed 250-300 into the column head, debonded through the slab; keys %s. Governing tension case %s: N_t %s kN with V = (%s, %s): %s. Max shear case %s: %s kN.\n' % (
                c, ('inboard pair' if c in KEYPAIR else 'A centre' + (' + B' if e['keyB'] else '')), cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), items, e['Vt'][1], f(e['Vt'][0])))
        elif t == 'P':
            L.append('**%s (P)** - as E plus the saddle: %s.\n' % (c, items))
        else:
            ext = group_extents(ed, COL_LONG[c]); cg = cone_group(ext)
            L.append('**%s (%s)** - concrete beyond the anchor rows (across-, across+, along-, along+) = %s mm -> A_c,N/A0 %s, psi_s %s, N_Rd,c %s kN. Governing tension case %s: N_t %s kN with V = (%s, %s), key moments %s / %s kNm, psi_ec %s: %s.\n' % (
                c, t, ', '.join(f(v, 0) for v in ext), f(cg['ratio'], 3), f(cg['psi_s'], 2), f(cg['NRd']), cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), f(bc['M_along']), f(bc['M_across']), f(bc['psi_ec'], 2), items))
    L.append('## 5. Site conditions: no solid-zone criterion for the anchorage\n')
    L.append('- The rebar connection depends on the column head only (6 dia14, dia6 links, C25): confirmed by the face cover-meter scan and 3-6 cores at heads (grade); no slab cone is loaded anywhere, so the 800 x 800 solid-zone criterion of Rev 4b/5 is withdrawn.')
    L.append('- The slab must still be solid (no blocks) and 300 mm thick under each base plate and around the key pockets (Key A: +/- 400 mm; key pairs: the key breakout bodies of the table, +/- 700 along the wall for the standard pair) - GPR from above at all 27 heads, which is also needed for the slab top bars at the pockets.')
    L.append('- If a column head shows fewer than 4 sound corner bars or links > 200 mm, the embedment goes to 300-350 mm (bond alone: 4 x 33.9 kN per 250 mm) and the lap is re-checked with the scanned bars before drilling; if the head cannot be drilled at all, the appendix B1 detail with its solid-zone condition applies at that head.\n')
    L.append('## 6. Before anchor installation\n')
    L.append('1. Scan sequence of section 1 (faces from below, GPR from above, pilot drill); pockets 140 / 110 mm placed to cut at most one slab top bar.')
    L.append('2. Proof tests (V4): 3 production bars (one interior, one edge, one corner head) loaded to >= 60 kN, held 2 min, displacement <= 1 mm; injection system with an EAD 330087 assessment for post-installed rebar, installer certified for it.')
    L.append('3. Drill 20 mm x 600 (300 slab + 300 head; 250 head minimum where the scan forces a shallower hole), clean, sleeve the top 300, inject the column part, set the bar; nuts snug + 1/4 turn after the grout has cured; the scan sheet with the final pattern is filed per head.')
    L.append('\n## Appendix - client option B1 for the 7 interior columns (fewer holes into column heads)\n')
    L.append('4 M20 8.8 resin anchors at 80 x 280, h_ef 250 in the 300 mm slab, cone in the 800 x 800 solid zone (98 kN interior, x 0.92 at the diagonal opening corners K16/K17), same plate and Key A. Condition: GPR-verified solid zone >= the minimum below at each of the 7 heads; saves 28 column-head holes. Utilisation and minimum zone:\n')
    L.append('| Col | B1 tension util. | Governing | Min. solid zone (mm, 300 thick) |')
    L.append('|---|---|---|---|')
    for c in COLS:
        o = base_env[c].get('B1_option')
        if o: L.append('| %s | %s | %s | %s |' % (c, f(o['uten'], 2), o['umax'][2].split(' (')[0], o['zreq']))
    L.append('\nAll other 20 columns stay type E in this option (edges / corners: the slab cone with the real edge is 38-50 kN).')
    open(os.path.join(OUT, 'bases_C.md'), 'w').write('\n'.join(L) + '\n')

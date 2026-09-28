"""Writes bases_C.md Rev 4: self-contained base and anchor design note, from run_all.py."""
import os, math
from model import COLS, BAYS, edge_distances, NEAR_EDGE, POSTS, COL_LONG, SADDLE
from connections import BASE, ANCH, FJD, FCD, LEVER, cone_group, V_edge_key, b2_layout, group_extents, KEYPAIR

def write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp):
    B = BASE; f = lambda x, n=1: '%.*f' % (n, x)
    typ = {c: base_env[c]['btype'] for c in COLS}
    b1 = [c for c in COLS if typ[c] == 'B1']; b2 = [c for c in COLS if typ[c] == 'E']; bp = [c for c in COLS if typ[c] == 'P']
    L = []
    L.append('# Alternative C - base and anchor design note, Rev 5 (bases_C.md)\n')
    L.append('Self-contained note for the base reviewer. Rev 5 follows brief Rev 4: **no through-bolts anywhere, every base anchored from above; ribbed slab 300 mm thick**; drilling into the column heads stays permitted with a mandatory rebar scan. Loads from `calc/run_all.py` (reactions_C.csv: every column and load case with concurrent N, V_x, V_y, base type and utilisation); anchorage basis `../load_basis.md` Rev 2. Units kN, mm, MPa.\n')
    L.append('**Rev 5 in one paragraph.** The 13 former through-bolt bases are replaced by anchors into the column head. Options were tried in the order asked: (a) an anchor group moved fully inboard with the uplift resolved as a lever (rows 150 / 430 mm inboard, tip bearing beyond the outer row - the same statics as the Rev 4b through-bolts, T = 2.4 N_t): the 4-anchor cone group in the 300 mm slab solid zone (h_ef 270, 800 x 800 zone, c 250 to the face) carries at most 107 kN against 100-182 kN at K1, K2, K5, K19, K20, K22, K23 - fails at 9 of 13 bases and is not used; (c) 6-8 M20 or 4 M24 inboard: the cone is limited by the 800 mm solid zone (<= 93-107 kN for any pattern) - no gain; **(b) concentric anchors through the 300 mm slab into the column head** carry N_t without any lever (T = N_t) and pass everywhere: **4 M16 8.8 resin anchors at 70 x 280 inside the column core, h_ef 550 (300 slab + 250 into the column)**, designed as a lap with the six dia14 column bars (bond in the column part with the EN 1992-4 narrow-member group factor, 257 kN per base; dia16 < 20 so EN 1992-1-1 8.7.4 needs no added transverse steel; the existing dia6/200 links remain). No bay had to be added or re-paired (d). Shear keys are unchanged from Rev 4b (inboard key pairs at the 13 former B2 bases, Key A + Key B at the other edge bases, Key A at interior bases, saddle at K21). Base variants: **B1 interior, E edge, E-corner (two Key B or the corner key pair), P = K21** (E anchors + saddle).\n')
    L.append('## 1. Base details\n')
    L.append('**B1 - interior (K9, K12, K13, K16, K17, K24, K26):** plate 300 x 400 x 25 S275 on 25 mm grout; **4 M20 8.8 resin anchors at 80 x 280 (280 along the concrete column\'s long axis), h_ef 250 in the 300 mm slab** (ETA h_min = h_ef + 2 d0 = 298 <= 300), 26 mm clearance holes (tension only); Key A SHS 90x90x8 stub, 180 embedded in a 140 mm cored pocket 200 deep under the column centre. Cone with the concrete of the 800 x 800 solid zone (K16, K17, K24, K26: opening/edge 0.3-0.4 m away, real extents).\n')
    L.append('**E - edge and corner (%d bases: %s):** plate 300 x 400 x 25 where the shear goes through Key A (+ Key B), or the Rev 4b key-pair plate (x/y extents per base in section 3, 25 mm, no stiffeners - no lever) where the inboard key pair stays; **4 M16 8.8 resin anchors at 70 x 280 concentric in the column core** (65 mm from each column face; the pattern is fixed on site from the rebar scan, +/-15 mm, clear of the corner and mid-face dia14 bars and the links), **h_ef 550: through the 300 mm slab and 250 mm into the column head**, 26 mm plate holes (tension only). Nothing depends on the slab cone at these bases: the uplift passes by bond into the column head and by lap into the six dia14 bars.\n' % (len([c for c in COLS if typ[c] == 'E']), ', '.join(c for c in COLS if typ[c] == 'E')))
    L.append('**P - K21 (200 mm pier):** as E (4 M16 h_ef 550 into the pier), plus the saddle of two 15 mm plates 400 x 150 on the pier faces for the N-S shear.\n')
    L.append('**Wind post WP1** (notch corner, no concrete column): post 280 mm inboard on both axes at (77.61, 20.25), plate 250 x 250 x 15, one centred 60 mm key (c1 250 both ways), 2 M12 for location, no uplift. Demand %s / %s kN vs %s kN -> %s.\n' % (f(V_wp[1]), f(V_wp[0]), f(R['VRd_B_edge250']), f(max(V_wp)/R['VRd_B_edge250'], 2)))
    L.append('## 2. Resistances (EN 1992-4 with the basis values; EN 1993-1-8 and EN 1992-1-1 6.7 for plates and keys)\n')
    L.append('| Item | Formula / factors | Value |')
    L.append('|---|---|---|')
    L.append('| B1 anchor steel, per M20 | 196 / 1.4 | %s kN |' % f(R['NRd_s']))
    L.append('| B1 cone, single, slab 300 | k 7.2 (cracked) sqrt(25) 250^1.5 | N0_Rk,c = %s kN |' % f(R['N0c']))
    cg1 = cone_group((60, 360, 260, 260)); cgc = cone_group((60, 360, 60, 260))
    L.append('| B1 cone group, interior (800 zone) | s_cr,N 750, c_cr 375: A_c,N/A0 = 800 x 800 / 750^2 = %s, psi_s %s (zone-limited: h_ef 250 gives the same 98 kN as 200) | N_Rd,c = %s kN |' % (f(R['ratio_c'], 3), f(R['psi_s'], 2), f(R['NRd_c'])))
    L.append('| (for reference) B1 cone group with one edge at 100 mm / corner | outboard row 60 mm from the face | %s / %s kN - why edge bases are type E |' % (f(cg1['ratio']*0 + cg1['NRd']), f(cgc['NRd'])))
    L.append('| B1 cone group, diagonal opening corner (K16, K17) | A_c,N x 0.92 (T4) | e.g. K16 %s kN |' % f(cone_group((160, 300, 300, 300), diag=True)['NRd']))
    L.append('| **E / P anchors: bond in the column head** | 4 x pi x 16 x 250 x tau_Rk 10 (cracked) = 503 kN x narrow-member group factor A_p,N/A0 = 200 x 650 / 369^2 = %s x psi_s = 0.7 + 0.3 x 65/185 = %s, / gamma_Mp 1.5 (slab part of the bond ignored) | **N_Rd = %s kN** |' % (f(R['E_ratio_col'], 2), f(R['E_psi_col'], 2), f(R['E_bond_col'], 0)))
    L.append('| E anchor steel | 4 x 0.9 x 800 x 157 / 1.4 | %s kN |' % f(R['E_steel'], 0))
    L.append('| E lap into the column bars | 6 dia14 at f_yd 435 receive the load; lap length needed at 73 kN: sigma_sd 79 MPa -> l_bd = 3.5 x 79/2.7 = 102, l_0 = 1.5 l_bd >= 200 -> 250 mm provided; dia16 < 20: no added transverse reinforcement (EN 1992-1-1 8.7.4.1), dia6/200 links present | %s kN |' % f(R['E_lap_max'], 0))
    L.append('| E concrete modes not applicable | the anchor tip sits 250 mm inside a column that continues downward: no free surface for a cone; the slab part (300 mm) only adds bond and is ignored | - |')
    from connections import bond_group
    L.append('| B1 bond group | pi 20 x 250 x 10 = %s kN single, s_cr,Np %s; interior A_p,N/A0 %s | N_Rd,p = %s kN, not governing |' % (f(R['N0p']), f(R['scrp'], 0), f(R['ratio_p'], 2), f(R['NRd_p'])))
    L.append('| Eccentric tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key/N_t (key moment V x 85 mm); max anchor N_t/4 + M/(2 s) | per case |')
    L.append('| Plate bearing (compression) | c = %s mm, A_eff = %s cm2 at 10 MPa | %s kN |' % (f(R['c'], 0), f(R['Aeff']/100, 0), f(R['NRd_bearing'], 0)))
    L.append('| B1 plate T-stub under uplift, per row | m = %s, l_eff 300, t 25 | %s kN |' % (f(R['m_plate'], 0), f(R['FT1_row'], 0)))
    L.append('| Key A bearing (centre key and inboard pairs) | rigid stub, z0 = %s mm, p_max = V z0/(b(z0 D - D^2/2)), b 90, D 180, sigma_Rd 1.5 f_cd = 25 MPa (confined, >= 250 mm from a face) | **V_Rd,A = %s kN** per key |' % (f(R['z0'], 0), f(R['VRd_A'])))
    L.append('| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3 f_y 355 -> %s kNm at lever 85; a = 8 | %s / %s kN |' % (f(R['MRd_A']), f(R['VRd_A_bending'], 0), f(R['VRd_A_weld'], 0)))
    L.append('| Key A parallel to an edge (B1, EN 1992-4 7.2.2.5 with psi_alpha = 2) | c1 = edge distance - 45: c1 55 -> %s kN, c1 155 -> %s kN, c1 255 -> %s kN | used at K3, K4, K6, K8, K11, K14, K16, K17, K24, K26 |' % (f(R['VRd_A_par55']), f(2*V_edge_key(155, 90)), f(2*V_edge_key(255, 90))))
    L.append('| Key towards an edge (Key B c1 250; key pair c1 >= 255; Key A 0.25-0.6 m) | 7.2.2.5, k9 1.7 cracked, d_nom 60 / 90, l_f 180, A_c,V/A0, psi_h | c1 250 (d 60): **%s kN**; c1 255 (d 90): **%s kN**; c1 355 (d 90): %s kN |' % (f(R['VRd_B_edge250']), f(R['VRd_A_edge255']), f(V_edge_key(355, 90))))
    L.append('| Key B bearing / bending | 60 mm bar, plain f_cd; W_pl d^3/6, f_y 335 | %s / %s kN |' % (f(R['VRd_B_bearing']), f(R['VRd_B_bending'], 0)))
    L.append('| P (K21) saddle | two 15 mm plates 400 x 150 on the pier faces, cantilever 150 | %s kN |' % f(R['VRd_saddle']))
    L.append('\n**Key-moment model (T3), one model for every key:** the shear resultant acts 85 mm below the plate; the moment V x 85 mm is carried by the grouted pocket as a rigid post (pressure linear about the rotation point z0 = 113 mm, p_max <= 25 MPa - the bearing check above), not by the anchors or bolts. Justification: the 180 mm stub in a C50 grout annulus (E about 30 GPa, 25 mm thick) in a 200 mm pocket has a rotational stiffness of the order of 10 MNm/rad, two orders above the couple of four M20 anchors 80 mm apart (about 4 x 250 kN/mm x 0.04^2 = 0.1 MNm/rad); the pocket therefore takes the moment before the anchors move. Hence psi_ec,N = 1.0 in the B1 cone and the B1 / E anchors carry N_t only, concentric. Anchors carry no shear (clearance holes); keys and saddle carry no tension.\n')
    L.append('## 3. Final base-type table (ULS envelope; reactions_C.csv has every case). Anchor pattern: the 280 spacing runs along the concrete column\'s long axis (E-W for the 0.4 x 0.2 columns K1, K2, K5, K9-K14, K21-K24; N-S for the others), the 80 (B1) / 70 (E) across it.\n')
    L.append('| Col | Type | Long axis | Bays | Near edges (< 0.25 m) | Keys | Bolts / anchors (mm from the column centre) | N_c max (case) | N_t max (case) | V max (case) | Tension util. | Key util. | Plate util. | **Governing** | Base plate (mm from the column centre) | Coring zone (solid concrete required) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in COLS:
        e = base_env[c]; ed = edge_distances(*COLS[c]); t = typ[c]
        if t == 'E' or t == 'P':
            anch = '4 M16 h_ef 550 (300 slab + 250 column), 70 x 280 (280 %s), scan-set' % ('E-W' if COL_LONG[c] == 'x' else 'N-S')
            if c in KEYPAIR:
                lay = b2_layout(ed, COL_LONG[c]); px, py = lay['plateE']['x'], lay['plateE']['y']; zx, zy = lay['zoneE']['x'], lay['zoneE']['y']
                keys = 'A-pair at %s' % ' / '.join('(%d, %d)' % (round(k[0]), round(k[1])) for k in lay['keys'])
                plate = 'x %d..%d, y %d..%d (%d x %d x 25)' % (px[0], px[1], py[0], py[1], px[1]-px[0], py[1]-py[0])
                zone = 'keys: x %d..%d, y %d..%d, slab 300 solid; column head scanned' % (zx[0], zx[1], zy[0], zy[1])
            elif t == 'P':
                keys = 'saddle'; plate = '300 x 400 x 25 + saddle'; zone = 'pier 200 x >= 800, top 500 mm scanned'
            else:
                keys = 'A centre' + (' + B ' + ','.join(e['keyB']) if e['keyB'] else ''); plate = '350 x 400 x 25 (250 inboard)' if e['keyB'] else '300 x 400 x 25'
                zone = 'to the face outboard, inboard >= 340, +/- 400 along (keys); column head scanned'
        else:
            keys = 'A centre' + (' + B ' + ','.join(e['keyB']) if e['keyB'] else ''); anch = '4 M20 h_ef 250, 80 x 280 (280 %s)' % ('E-W' if COL_LONG[c] == 'x' else 'N-S')
            plate = '300 x 400 x 25'
            ex = group_extents(ed, COL_LONG[c]); zr = e['zreq'] or 400
            zone = '>= %d x %d centred, 300 thick (cone extents %s)' % (zr, zr, ', '.join('%d' % v for v in ex))
        L.append('| %s | **%s** | %s | %s | %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %s | %s | %s | **%s** (%s) | %s | %s |' % (
            c, t, 'E-W' if COL_LONG[c] == 'x' else 'N-S', ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
            keys, anch, f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], f(e['Vt'][0]), e['Vt'][1], f(e['uten'], 2), f(e['ukey'], 2), f(e['uplate'], 2), f(e['umax'][0], 2), e['umax'][2].split(' (')[0], plate, zone))
    w = max(V_wp)
    L.append('| WP1 | post | - | - | +x,-y | one 60 mm key centred, c1 250 | 2 M12 location | %s | 0 | %s | - | %s | - | **%s** (key edge) | 250 x 250 x 15 at (77.61, 20.25) | notch edge beam, 600 x 600 around the post |' % (f(0.3*Lwp*1.35), f(w), f(w/R['VRd_B_edge250'], 2), f(w/R['VRd_B_edge250'], 2)))
    worst = max(base_env, key=lambda c: base_env[c]['umax'][0])
    L.append('\nWorst base **%s (%s): %s (%s, %s)**; worst tension %s at %s; worst key %s at %s; worst plate %s at %s. All 27 bases and WP1 <= 1.0 with the real slab edges.\n' % (
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
            L.append('**%s (E)** - 4 M16 h_ef 550 concentric; keys %s. Governing tension case %s: N_t %s kN with V = (%s, %s): %s. Max shear case %s: %s kN.\n' % (
                c, ('inboard pair' if c in KEYPAIR else 'A centre' + (' + B' if e['keyB'] else '')), cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), items, e['Vt'][1], f(e['Vt'][0])))
        else:
            ext = group_extents(ed, COL_LONG[c]); cg = cone_group(ext)
            L.append('**%s (%s)** - concrete beyond the anchor rows (across-, across+, along-, along+) = %s mm -> A_c,N/A0 %s, psi_s %s, N_Rd,c %s kN. Governing tension case %s: N_t %s kN with V = (%s, %s), key moments %s / %s kNm, psi_ec %s: %s.\n' % (
                c, t, ', '.join(f(v, 0) for v in ext), f(cg['ratio'], 3), f(cg['psi_s'], 2), f(cg['NRd']), cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), f(bc['M_along']), f(bc['M_across']), f(bc['psi_ec'], 2), items))
    L.append('## 5. Coring / scanning acceptance criterion (slab 300 mm) and what happens if it fails\n')
    L.append('- **All heads:** ribbed slab 300 mm thick with a solid (no blocks, no voids) zone over the column head, C25 by rebound + core; GPR/scan of all 27 heads plus 3-6 cores (one B1, one E, one E-corner at least).')
    L.append('- **B1 heads (interior):** solid zone >= the tabulated minimum (K12 700, K16 700, K9/K13 650, K26 550, K17/K24 <= 500), full 300 mm, i.e. the cone extents of the check (h_ef 250, c_cr 375). A B1 head that fails is built as E (anchors into the column head, no cone).')
    L.append('- **E / P heads:** the anchors do not depend on the slab; the slab must be solid over the key breakout bodies (table: +/- 700 along the wall for the standard key pair, K23 to -1100, K25/K27 to +1000; 340 inboard / +/- 400 along at Key A + Key B heads) and under the plate; the column head is scanned (6 dia14, dia6 links, cover) and the 70 x 280 pattern set on site clear of the bars (+/- 15 mm; the group factor changes < 3 %). No soffit access is needed anywhere.')
    L.append('- If a column head shows fewer than 6 dia14 or links > 200 mm, the E anchorage at that head is re-checked with the scanned bars (lap capacity 6 x 67 kN = 402 kN has a 5x margin at K19) before drilling.\n')
    L.append('## 6. Before anchor installation\n')
    L.append('1. Rebar scan of the slab top bars at every head; place the 140 / 110 mm pockets and the through-bolt holes to cut at most one top bar.')
    L.append('2. Pull-out tests: 3 sacrificial M20 (h_ef 250, slab) to 1.3 x 17 = 25 kN and 3 sacrificial M16 (h_ef 550, into a column head) to 1.3 x 18 = 25 kN, with the ETA verification by the supplier (basis open item).')
    L.append('3. E / P: drill 20 mm holes through the plate template after the pockets are grouted, depth 550 +/- 10, blow/brush clean, inject, set; nuts snug + 1/4 turn; the scan sheet with the final pattern is filed per head.')
    open(os.path.join(OUT, 'bases_C.md'), 'w').write('\n'.join(L) + '\n')

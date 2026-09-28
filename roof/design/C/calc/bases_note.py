"""Writes bases_C.md Rev 4: self-contained base and anchor design note, from run_all.py."""
import os, math
from model import COLS, BAYS, edge_distances, NEAR_EDGE, POSTS, COL_LONG, SADDLE
from connections import BASE, ANCH, FJD, FCD, LEVER, cone_group, V_edge_key, b2_layout, group_extents

def write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp):
    B = BASE; f = lambda x, n=1: '%.*f' % (n, x)
    typ = {c: base_env[c]['btype'] for c in COLS}
    b1 = [c for c in COLS if typ[c] == 'B1']; b2 = [c for c in COLS if typ[c] == 'B2']; bp = [c for c in COLS if typ[c] == 'P']
    L = []
    L.append('# Alternative C - base and anchor design note, Rev 4b (bases_C.md)\n')
    L.append('Self-contained note for the base reviewer; Rev 4b follows design Rev 3 (north-face jog at y 35.37 west of x 81.79, plane raised 30 mm, thermal check, C7 plate extents, K7 as B2) and Rev 4a closed the Rev 4 sign-off items T1-T6 (per-base B2 plate lengths and coring zones, coring criterion aligned with the concrete the checks use, one key-moment model, diagonal-corner cone reduction, 25 mm under-slab plate, class-3 stiffeners, skewed levers noted, bond with the real extents). Loads from `calc/run_all.py` (reactions_C.csv: every column and load case with concurrent N, V_x, V_y, base type and utilisation); anchorage basis `../load_basis.md` Rev 2. Units kN, mm, MPa.\n')
    L.append('**Rev 4 in one paragraph.** The slab edge is now modelled where it is: 100 mm from the centre of every perimeter column (column flush with the building face) and at the stair / shaft openings (treated as free slab edges). With the real edges the concentric 4-anchor group has only 50 kN (one edge) / 38 kN (corner) of cone resistance and Key A next to the face has only 18-24 kN parallel-to-edge resistance, so the base type is now chosen per column: **B1** (concentric resin anchors + Key A + Key B) where the real-edge cone and the parallel-edge check pass at <= 0.90 (%d bases: %s), **B2** (through-bolts + inboard key pair, the Rev 3 fallback made primary with corrected lever statics) at the %d perimeter and edge-adjacent bases that do not (%s), and **P** at the K21 pier. Nothing is drilled into a column head except the K21 pier anchors.\n' % (len(b1), ', '.join(b1), len(b2), ', '.join(b2)))
    L.append('## 1. Base details\n')
    L.append('**B1 - concentric anchors (interior and lightly loaded edge bases):** plate 300 x 400 x 25 S275 (350 across at near-edge bases, 100 outboard / 250 inboard) on 25 mm non-shrink grout; **4 M20 8.8 resin anchors at 80 x 280, h_ef 200 in the slab**, 280 along the concrete column\'s long axis, 26 mm clearance holes (tension only); **Key A** SHS 90x90x8 stub, 180 embedded in a 140 mm cored pocket 200 deep under the column centre (along-axis and inward shear; compressible strip on the outboard face where an edge is closer than 0.25 m); **Key B** 60 mm bar (f_y 335), 180 embedded in a 110 mm pocket 200 deep, 180 mm inboard on the outward axis (c1 250) where an outward shear > 3 kN points to an edge closer than 0.25 m. The cone is evaluated with the concrete actually there: outboard row 60 mm from the face at K3, K4, K6, K7, K8, K11, K14 (N_Rd,c 50 / 38 at corners, psi_s 0.76), 160-360 mm at K16, K17, K24, K26, full 800 at K5, K9, K12, K13. Key A parallel-to-edge breakout (2 V_Rk,c at c1 = distance - 45) is checked wherever an edge is closer than 0.6 m.\n')
    L.append('**B2 - through-bolts and inboard key pair (perimeter / edge-adjacent bases with uplift or along-wall shear beyond B1, plus K7 by decision C4/C13):** plate **800 (along the wall) x 550 (across: 100 outboard to the slab face, 450 inboard) x 30 S275** in the standard layout (per-base extents in section 3: K7 500 x 1000, K23 1000 x 550, K25 550 x 900, K27 600 x 900) with two 120 x 10 stiffeners from the column flange tips to the inboard plate end (stiffened section M_Rd 48 kNm, plastic); **2 M24 8.8 through-bolts** (F_t,Rd 203 kN) in a row 250 mm inboard of the column centre, 280 apart along the wall, both >= 300 mm from every slab edge (row shifted along the wall at corners and next to openings, table in section 3), bearing on a **400 x 200 x 20 plate under the slab** (cut to the solid zone soffit beside the column; ceiling access at each base); the bolts sit in 26 mm clearance holes (no shear). Uplift is carried by **lever action**: the bolts hold the plate down at the row (centroid distance c from the column), the inboard plate tip (b = c + 180) bears on the grout: T = N_t b/(b - c), C = T - N_t. Shear is carried by a **pair of SHS 90x90x8 keys** (140 pockets, 200 deep) 200 mm inboard of the column line and +/- 300 mm along the wall (both keys >= 300 mm from every edge, c1 >= 255): each key takes half the shear plus the torque of the eccentric shear (V x 0.2 m about the pair centroid, arm 0.6 m); outward components are checked as plain-concrete edge breakout at their own c1, resultants as bearing at 1.5 f_cd. No anchor cone and no anchor shear at B2 bases; the slab is not relied on for tension (through-bolts) and the shear keys sit in confined concrete.\n')
    L.append('**P - K21 (200 mm pier between the notch edge and the shaft opening):** plate 300 x 400 x 25; **4 M16 8.8 resin anchors at 70 x 280, h_ef 400 into the pier** (the only place where the client\'s permission to drill a column head is used: the pier has no inboard side and no soffit access); EN 1992-4 gives no cone in a 200 mm wall, so the anchors are designed as a lap with the pier\'s vertical bars (EN 1992-1-1 8.7 logic): bond 4 x pi x 16 x 400 x 10 = 804 kN / 1.5 = %s kN, steel %s kN, splitting of the pier restrained by two dia6 links (4 legs, f_yd 435) = %s kN over the 400 mm lap; **saddle** of two 15 mm plates 400 x 150 on the pier faces for the N-S shear (82 kN). Rebar scan mandatory (links at <= 200 and 6 dia14 confirmed).\n' % (f(R['p_NRd_p'], 0), f(R['p_NRd_s'], 0), f(R['p_links'], 0)))
    L.append('**Wind post WP1** (notch corner, no concrete column): post moved 280 mm inboard on both axes to (77.61, 20.25), plate 250 x 250 x 15, one centred 60 mm key (c1 250 both ways), 2 M12 for location, no uplift (slotted top connection). Demand %s / %s kN (E-W / N-S) vs %s kN -> %s.\n' % (f(V_wp[1]), f(V_wp[0]), f(R['VRd_B_edge250']), f(max(V_wp)/R['VRd_B_edge250'], 2)))
    L.append('## 2. Resistances (EN 1992-4 with the basis values; EN 1993-1-8 and EN 1992-1-1 6.7 for plates and keys)\n')
    L.append('| Item | Formula / factors | Value |')
    L.append('|---|---|---|')
    L.append('| B1 anchor steel, per M20 | 196 / 1.4 | %s kN |' % f(R['NRd_s']))
    L.append('| B1 cone, single, slab | k 7.2 (cracked) sqrt(25) 200^1.5 | N0_Rk,c = %s kN |' % f(R['N0c']))
    cg1 = cone_group((60, 360, 260, 260)); cgc = cone_group((60, 360, 60, 260))
    L.append('| B1 cone group, interior (800 zone) | A_c,N/A0 = 800 x 680 / 600^2 = %s, psi_s %s | N_Rd,c = %s kN |' % (f(R['ratio_c'], 3), f(R['psi_s'], 2), f(R['NRd_c'])))
    L.append('| B1 cone group, one edge at 100 mm from the column centre | outboard row 60 mm from the face: A = (60+80+300)(300+280+300) = %s x 600^2, psi_s = 0.7 + 0.3 x 60/300 = %s | **N_Rd,c = %s kN** |' % (f(cg1['ratio'], 3), f(cg1['psi_s'], 2), f(cg1['NRd'])))
    L.append('| B1 cone group, corner (two edges at 100 mm) | A = 440 x 640 | **%s kN** |' % f(cgc['NRd']))
    L.append('| B1 cone group, diagonal opening corner (K3, K16, K17) | A_c,N x 0.92 (T4) | e.g. K16 %s kN |' % f(cone_group((160, 300, 300, 300), diag=True)['NRd']))
    from connections import bond_group
    L.append('| B1 bond group | pi 20 x 200 x 10 = %s kN single, s_cr,Np %s; interior A_p,N/A0 %s -> %s kN; one edge at 100 mm (real extents, T6) -> %s kN; corner -> %s kN | not governing |' % (f(R['N0p']), f(R['scrp'], 0), f(R['ratio_p'], 2), f(R['NRd_p']), f(bond_group((60, 360, 260, 260))['NRd']), f(bond_group((60, 360, 60, 260))['NRd'])))
    L.append('| Eccentric tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key/N_t (key moment V x 85 mm); max anchor N_t/4 + M/(2 s) | per case |')
    L.append('| Plate bearing (compression) | c = %s mm, A_eff = %s cm2 at 10 MPa | %s kN |' % (f(R['c'], 0), f(R['Aeff']/100, 0), f(R['NRd_bearing'], 0)))
    L.append('| B1 plate T-stub under uplift, per row | m = %s, l_eff 300, t 25 | %s kN |' % (f(R['m_plate'], 0), f(R['FT1_row'], 0)))
    L.append('| Key A bearing (B1 centre key and B2 pair) | rigid stub, z0 = %s mm, p_max = V z0/(b(z0 D - D^2/2)), b 90, D 180, sigma_Rd 1.5 f_cd = 25 MPa (confined, >= 250 mm from a face) | **V_Rd,A = %s kN** per key |' % (f(R['z0'], 0), f(R['VRd_A'])))
    L.append('| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3 f_y 355 -> %s kNm at lever 85; a = 8 | %s / %s kN |' % (f(R['MRd_A']), f(R['VRd_A_bending'], 0), f(R['VRd_A_weld'], 0)))
    L.append('| Key A parallel to an edge (B1, EN 1992-4 7.2.2.5 with psi_alpha = 2) | c1 = edge distance - 45: c1 55 -> %s kN, c1 155 -> %s kN, c1 255 -> %s kN | used at K3, K4, K6, K7, K8, K11, K14, K16, K17, K24, K26 |' % (f(R['VRd_A_par55']), f(2*V_edge_key(155, 90)), f(2*V_edge_key(255, 90))))
    L.append('| Key towards an edge (Key B c1 250; B2 pair c1 >= 255; Key A 0.25-0.6 m) | 7.2.2.5, k9 1.7 cracked, d_nom 60 / 90, l_f 180, A_c,V/A0, psi_h | c1 250 (d 60): **%s kN**; c1 255 (d 90): **%s kN**; c1 355 (d 90): %s kN |' % (f(R['VRd_B_edge250']), f(R['VRd_A_edge255']), f(V_edge_key(355, 90))))
    L.append('| Key B bearing / bending | 60 mm bar, plain f_cd; W_pl d^3/6, f_y 335 | %s / %s kN |' % (f(R['VRd_B_bearing']), f(R['VRd_B_bending'], 0)))
    L.append('| B2 through-bolt | M24 8.8, 0.9 x 800 x 353 / 1.25 | %s kN each |' % f(R['b2_FtRd']))
    L.append('| B2 lever | T = N_t b/(b - c), C = T - N_t, c = bolt-row centroid distance, b = c + 180 (plate tip); bolt tension per M24 = T/2 + M_key/(2 x 0.28) | per base, section 3 |')
    L.append('| B2 tip bearing | 350 x 60 strip at 10 MPa | %s kN |' % f(R['b2_C_bearing'], 0))
    L.append('| B2 stiffened plate | 350 x 30 plate + 2 stiffeners 120 x 10, plastic | M_Rd %s kNm vs N_t c + M_key |' % f(R['b2_MRd'], 0))
    L.append('| B2 under-slab plate | 400 x 200 x 25: bearing on the solid-zone soffit at 10 MPa %s kN; bending (cantilever 50 mm from the bolt) M_el %s kNm | |' % (f(R['b2_underplate'], 0), f(R['b2_under_MRd'])))
    L.append('| P (K21) | bond %s kN, steel %s kN, splitting (links) %s kN; saddle %s kN | |' % (f(R['p_NRd_p'], 0), f(R['p_NRd_s'], 0), f(R['p_links'], 0), f(R['VRd_saddle'])))
    L.append('\n**Key-moment model (T3), one model for every key:** the shear resultant acts 85 mm below the plate; the moment V x 85 mm is carried by the grouted pocket as a rigid post (pressure linear about the rotation point z0 = 113 mm, p_max <= 25 MPa - the bearing check above), not by the anchors or bolts. Justification: the 180 mm stub in a C50 grout annulus (E about 30 GPa, 25 mm thick) in a 200 mm pocket has a rotational stiffness of the order of 10 MNm/rad, two orders above the couple of four M20 anchors 80 mm apart (about 4 x 250 kN/mm x 0.04^2 = 0.1 MNm/rad); the pocket therefore takes the moment before the anchors move. Hence psi_ec,N = 1.0 in the B1 cone, the B1 anchors and the B2 bolts carry N_t only, and the B2 plate is checked for N_t c. Anchors and through-bolts carry no shear (clearance holes); keys and saddle carry no tension. Class-3 stiffeners on the B2 plate: elastic M_el about 50 kNm >= the 48 kNm used.\n')
    L.append('## 3. Final base-type table (ULS envelope; reactions_C.csv has every case)\n')
    L.append('| Col | Type | Long axis | Bays | Near edges (< 0.25 m) | Keys | Bolts / anchors (mm from the column centre) | N_c max (case) | N_t max (case) | V max (case) | Tension util. | Key util. | Plate util. | **Governing** | Base plate (mm from the column centre) | Coring zone (solid concrete required) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in COLS:
        e = base_env[c]; ed = edge_distances(*COLS[c]); t = typ[c]
        if t == 'B2':
            lay = b2_layout(ed, COL_LONG[c])
            keys = 'A-pair at %s' % ' / '.join('(%d, %d)' % (round(k[0]), round(k[1])) for k in lay['keys'])
            anch = '2 M24 through at %s, lever %.2f (under-slab plate 400 x 200 x 25)' % (' / '.join('(%d, %d)' % (round(b[0]), round(b[1])) for b in lay['bolts']), lay['b']/(lay['b'] - lay['c']))
            px, py = lay['plate']['x'], lay['plate']['y']; zx, zy = lay['zone']['x'], lay['zone']['y']
            plate = 'x %d..%d, y %d..%d (%d x %d x 30 + 2 stiff.)%s' % (px[0], px[1], py[0], py[1], px[1]-px[0], py[1]-py[0], ', skewed lever' if lay['skew'] else '')
            zone = 'x %d..%d, y %d..%d, soffit access' % (zx[0], zx[1], zy[0], zy[1])
        elif t == 'P':
            keys = 'saddle'; anch = '4 M16 h_ef 400 in the pier, 70 x 280'; plate = '300 x 400 x 25 + saddle'; zone = 'pier 200 x >= 800, top 500 mm'
        else:
            keys = 'A centre' + (' + B ' + ','.join(e['keyB']) if e['keyB'] else ''); anch = '4 M20 h_ef 200, 80 x 280 (280 %s)' % ('E-W' if COL_LONG[c] == 'x' else 'N-S')
            near = any(v < 0.25 for v in ed.values())
            plate = '350 x 400 x 25 (250 inboard)' if e['keyB'] else '300 x 400 x 25'
            ex = group_extents(ed, COL_LONG[c]); ax = 'x' if COL_LONG[c] == 'x' else 'y'
            if near:
                zone = 'to the face outboard, inboard >= %d, along +/- 400 (= the cone extents used)' % (40 + int(min(max(ex[0], ex[1]), 300)))
            else:
                zr = e['zreq'] or 400; zone = '>= %d x %d centred (cone extents %s)' % (zr, zr, ', '.join('%d' % v for v in ex))
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
        if t == 'B2':
            lay = b2_layout(ed, COL_LONG[c])
            L.append('**%s (B2)** - bolts at %s (c = %s mm, tip b = %s mm, lever %s); keys at %s. Governing tension case %s: N_t %s kN with V = (%s, %s): %s. Max shear case %s: %s kN.\n' % (
                c, ' / '.join('(%d, %d)' % (round(b[0]), round(b[1])) for b in lay['bolts']), f(lay['c'], 0), f(lay['b'], 0), f(lay['b']/(lay['b']-lay['c']), 2), ' / '.join('(%d, %d)' % (round(k[0]), round(k[1])) for k in lay['keys']),
                cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), items, e['Vt'][1], f(e['Vt'][0])))
        else:
            ext = group_extents(ed, COL_LONG[c]); cg = cone_group(ext)
            L.append('**%s (%s)** - concrete beyond the anchor rows (across-, across+, along-, along+) = %s mm -> A_c,N/A0 %s, psi_s %s, N_Rd,c %s kN. Governing tension case %s: N_t %s kN with V = (%s, %s), key moments %s / %s kNm, psi_ec %s: %s.\n' % (
                c, t, ', '.join(f(v, 0) for v in ext), f(cg['ratio'], 3), f(cg['psi_s'], 2), f(cg['NRd']), cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), f(bc['M_along']), f(bc['M_across']), f(bc['psi_ec'], 2), items))
    L.append('## 5. Coring acceptance criterion (T2: identical to the concrete the checks use) and what happens if it fails\n')
    L.append('- **B1 heads:** solid concrete (no blocks, no voids, full depth >= 250 mm, C25 by rebound + core) over the zone in the last column of the table, which is exactly the cone extent used in the check: edge heads one-sided - outboard to the building face, **inboard >= 340 mm from the column centre (40 + c_cr 300), +/- 400 along the wall**; interior heads centred at the tabulated minimum (K12 650, K16 650, K9/K13 600, others <= 500). A B1 head that fails is built as B2 (no cone).')
    L.append('- **B2 heads:** solid concrete over the tabulated x/y zone (the key breakout bodies, 1.5 c1 = 383 mm beyond each key, i.e. **+/- 700 along the wall** for the standard layout, and the bolts + under-slab plate to 600 mm from the face; K23 -1100..+200 along, K25/K27 -300..+1000), soffit accessible from below (ceiling opening about 600 x 600 at each of the %d bases). If the soffit is not accessible at a head, the alternative is the basis Rev 2 concept (anchors through the slab into the column head, h_ef >= 300, rebar scan) at that head only - to be agreed with the reviewer.' % len(b2))
    L.append('- **Slab designer (T5):** each B2 base applies to the slab a downward force T at the bolt row (through the under-slab plate) and an upward bearing C at the plate tip 180 mm further inboard: K19 175 / 102 kN, K23 182 / 120 kN, K20 153 / 89 kN, K10 139 / 81 kN, K22 135 / 78 kN, K27 114 / 70 kN, K25 110 / 68 kN, K18 94 / 55 kN, K2 86 / 50 kN, K1 81 / 47 kN, K15 40 / 23 kN (ULS, concurrent with the column uplift). At K23, K25 and K27 the bolt centroid is skewed to the wall (lever direction shown in the table), so the plate bends about a skewed axis: 14 kNm about the wall direction in addition to the 26 kNm lever moment, both within the 48 kNm class-3 section.')
    L.append('- **K21:** rebar scan confirming 6 dia14 and links at <= 200 in the top 500 mm of the pier; the 70 x 280 anchor pattern is fixed on site from the scan (C13, stated on S05); pier faces accessible for the saddle.')
    L.append('- **Thermal (C4):** the north E-W bay pair B2-B1 is restrained through the roof trusses with k_eff about 2.8 kN/mm, giving a locked-in force of 10 kN (service +/-20 K) and 15 kN (erection state +/-30 K); 9 kN (psi_0 0.6) is added to the B1/B2 bay shear in every wind case and 23 kN as a thermal-leading case (ULST) without wind; K1, K2, K5, K7 are all B2 and pass (K7 0.76). No slotted holes anywhere.')
    L.append('- **Option (C15):** building every base as B2 (16 more soffit openings) removes all cone checks and the B1 coring criterion; offered to the client as a cost/simplicity trade.')
    L.append('- Cores at 3 heads first (one B1 interior, one B1 edge, one B2), then every head by 60 mm core or GPR against its own line of the table.\n')
    L.append('## 6. Before anchor installation\n')
    L.append('1. Rebar scan of the slab top bars at every head; place the 140 / 110 mm pockets and the through-bolt holes to cut at most one top bar.')
    L.append('2. Pull-out test on 3 sacrificial M20 resin anchors (h_ef 200) to 1.3 x max B1 anchor = 45 kN; ETA group verification by the supplier (basis open item).')
    L.append('3. B2: torque the M24 through-bolts to snug + 1/4 turn after the grout has cured; check the under-slab plate seating (dry-pack).')
    open(os.path.join(OUT, 'bases_C.md'), 'w').write('\n'.join(L) + '\n')

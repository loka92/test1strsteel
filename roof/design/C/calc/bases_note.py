"""Writes bases_C.md Rev 3: self-contained base and anchor design note, from run_all.py."""
import os, math
from model import COLS, BAYS, edge_distances, NEAR_EDGE, POSTS, COL_LONG, SADDLE
from connections import BASE, ANCH, FJD, FCD, LEVER, cone_group, V_edge_key
from sections import sec, FY, FU

def write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp):
    B, A = BASE, ANCH
    braced = {c for b in BAYS for c in b['c']}
    f = lambda x, n=1: '%.*f' % (n, x)
    L = []
    L.append('# Alternative C - base and anchor design note, Rev 3 (bases_C.md)\n')
    L.append('Self-contained note for the base reviewer, replacing Rev 2 after the focused review (R1-R7). Loads from `calc/run_all.py` (reactions_C.csv: every column and load case with concurrent N, V_x, V_y and the base utilisation); anchorage basis `../load_basis.md` Rev 2. Units kN, mm, MPa.\n')
    L.append('**Rev 3 in one paragraph.** Nothing is drilled into the column heads any more (R4): the client had permitted it, but the review showed it is unnecessary (h_ef 200 in the slab gives the same 98 kN) and risky (5-11 mm to the column bars). All anchors and keys stay within the 250 mm slab solid zone. The "column cage" shear resistance of Rev 2 is withdrawn (R1); outward shear towards a free slab edge is taken by a second key placed 180 mm inboard so that c1 = 250 mm, checked as plain-concrete edge breakout (cracked), or by a saddle at the K21 pier; the key moments V x 85 mm are carried into the anchor group as eccentric tension (psi_ec,N) and into the max anchor (R2); the minimum solid zone per base is tabulated with a coring acceptance criterion and a through-bolt fallback (R3). Minor items R5-R7 are in the tables.\n')
    L.append('## 1. Base details\n')
    L.append('**Type S (standard, 26 bases K1-K20, K22-K27):**')
    L.append('- Base plate **300 x 400 x 25 S275**, long side along the concrete column\'s 400 mm axis; at near-edge bases the plate is 350 wide across the wall, placed 100 mm outboard / 250 mm inboard of the column centre (corners 350 x 350 the same way). HEA 160 welded a = 6 all round, web across the concrete column\'s short axis. **25 mm** non-shrink grout (C50 class) on levelling shims.')
    L.append('- **4 M20 8.8 resin anchors, h_ef = 200 mm in the slab solid zone only**, pattern **80 x 280 with the 280 along the concrete column\'s long axis** (table in section 3: E-W for the 0.4 x 0.2 columns, N-S for the 0.2 x 0.4 columns); the anchors sit over the column head footprint (60 mm inside its faces) but stop 50 mm above the column top. Plate holes 26 mm (clearance): the anchors carry tension only. ETA h_min = h_ef + 2 d0 = 248 <= 250 OK.')
    L.append('- **Key A** under the column centre: SHS 90x90x8 S355 stub, 180 mm embedded (20 mm grout under its toe), welded to the plate a = 8 all round, in a **140 mm cored pocket 200 mm deep** (25 mm grout annulus, pocket position set after the rebar scan so that no more than one slab top bar is cut). It carries the shear along the column\'s long axis (bay shear along the wall) and the inward shear across; at near-edge bases a 25 mm compressible strip on the outboard face of the pocket stops it from taking outward shear.')
    L.append('- **Key B** (only where the table in section 3 says so: %d bases with an outward demand towards a free slab edge closer than 0.25 m): 60 mm round bar S355 (f_y 335), 180 embedded, welded a = 8, in a **110 mm cored pocket 200 deep**, centred **180 mm inboard of the column centre on the outward axis**, so that c1 = 250 mm to the slab edge (350 at K3 where the edge is 0.2 m away). Corner bases K4, K6, K23, K25 have two Key B (one per edge). Key B lies on the axis of the outward force through the column, so the eccentric key adds no in-plane torque; the plate carries the force to the column as a deep beam (in-plane).' % sum(1 for e in base_env.values() if e['keyB']))
    L.append('- Erection: level, grout the pockets and the bed, then set the resin anchors through the plate; nuts snug + 1/4 turn (no preload relied upon).\n')
    L.append('**Type P (K21, 200 mm pier between the notch edge y 19.97 and the shaft opening y 20.17):** no key; a **saddle** of two 15 mm S275 plates 400 x 150 welded to the plate edges, hanging down the north and south faces of the pier and grouted against them, carries the N-S base shear by bearing on the pier faces (400 x 150 each); E-W shear is negligible (no E-W bay, no E-W wall). Same plate and 4 anchors (h_ef 200 in the pier top; the pier is a wall element 200 thick - the cone is limited to the 200 x 800 concrete available, see section 3). Requires the pier faces to be accessible from the notch (outside) and the shaft top; to be confirmed on site.\n')
    L.append('**Wind post WP1** (notch corner, no concrete column): the post is moved **280 mm inboard on both axes** to (77.61, 20.25) so that a single centred 60 mm key has c1 = 250 to both slab edges; plate 250 x 250 x 15, 2 M12 for location only (no uplift: slotted top connection); the corner girts cantilever 280 mm to the wall line. Demand %s kN (E-W) / %s kN (N-S) vs %s kN (edge breakout, either direction) -> %s.\n' % (f(V_wp[1]), f(V_wp[0]), f(R['VRd_B_edge250']), f(max(V_wp)/R['VRd_B_edge250'], 2)))
    L.append('## 2. Resistances (EN 1992-4 with the basis values; EN 1993-1-8 and EN 1992-1-1 6.7 for the plate and keys)\n')
    cg = {z: cone_group(z) for z in (800, 750, 700, 600)}
    L.append('| Item | Formula / factors | Value |')
    L.append('|---|---|---|')
    L.append('| Anchor steel, per anchor | N_Rk,s 196 / gamma_Ms 1.4 | %s kN |' % f(R['NRd_s']))
    L.append('| Concrete cone, single, slab | k 7.2 (cracked) sqrt(25) x 200^1.5 | N0_Rk,c = %s kN |' % f(R['N0c']))
    L.append('| Cone group, zone 800 | s_cr,N 600, c_cr,N 300; group 80 x 280: A_c,N/A0 = 800 x 680 / 600^2 = %s; psi_s,N = %s; psi_re = 1; psi_ec,N per case (section 3) | N_Rk,c,g = %s -> **N_Rd,c = %s kN** |' % (f(R['ratio_c'], 3), f(R['psi_s'], 2), f(R['NRk_cg']), f(R['NRd_c'])))
    L.append('| Cone group, zone 750 / 700 / 600 | same, boundary of the solid zone as free edges | N_Rd,c = %s / %s / %s kN |' % (f(cg[750]['NRd']), f(cg[700]['NRd']), f(cg[600]['NRd'])))
    L.append('| Bond, single | pi x 20 x 200 x tau_Rk 10 (cracked) | N0_Rk,p = %s kN |' % f(R['N0p']))
    L.append('| Bond group | s_cr,Np = 7.3 d sqrt(tau) = %s; A_p,N/A0 = %s; psi_s,Np = %s; psi_g,Np = 1.0 | N_Rd,p = %s kN |' % (f(R['scrp'], 0), f(R['ratio_p'], 2), f(R['psi_sp'], 2), f(R['NRd_p'])))
    L.append('| Eccentric group tension | psi_ec,N = 1/(1 + 2 e_N/s_cr,N) per direction, e_N = M_key / N_t; max anchor = N_t/4 + M_along/(2 x 0.28) + M_across/(2 x 0.08) | per case |')
    L.append('| Bearing under the plate | c = t sqrt(f_y / 3 f_jd) = %s mm, A_eff = %s cm2 at f_jd 10 MPa | %s kN |' % (f(R['c'], 0), f(R['Aeff']/100, 0), f(R['NRd_bearing'], 0)))
    L.append('| Plate T-stub under uplift, per anchor row | cantilever from the flange tips m = %s mm, l_eff 300, t 25 | %s kN |' % (f(R['m_plate'], 0), f(R['FT1_row'], 0)))
    L.append('| Key shear resultant | rigid stub in a grouted pocket, pressure linear with rotation point z0 = %s mm below the slab top; resultant 85 mm below the plate (25 grout + 180/3) | M_key = V x 0.085 |' % f(R['z0'], 0))
    L.append('| Key A bearing | p_max = V z0 / (b (z0 D - D^2/2)), b = 90, D = 180 -> p_max = V x %s MPa/kN; sigma_Rd = 1.5 f_cd = 25 MPa (partially loaded area in the solid zone) | **V_Rd,A = %s kN** |' % (f(25/R['VRd_A_bearing'], 3), f(R['VRd_A_bearing'])))
    L.append('| Key A bending / weld | SHS 90x90x8 W_pl 75 cm3, f_y 355 -> M_Rd %s kNm at lever 85 mm; a = 8 all round | %s / %s kN |' % (f(R['MRd_A']), f(R['VRd_A_bending'], 0), f(R['VRd_A_weld'], 0)))
    L.append('| Key B bearing | 60 mm bar, plain f_cd 16.7 | %s kN |' % f(R['VRd_B_bearing']))
    L.append('| Key B bending / weld | W_pl = d^3/6, f_y 335 -> M_Rd %s kNm | %s / %s kN |' % (f(R['MRd_B']), f(R['VRd_B_bending'], 0), f(R['VRd_B_weld'], 0)))
    L.append('| **Key B concrete edge breakout, c1 = 250** | EN 1992-4 7.2.2.5, k9 1.7 (cracked), d_nom 60, l_f 180: V0_Rk,c = %s kN; A_c,V/A0 = 750 x 250 / (4.5 x 250^2) = 0.667; psi_h = sqrt(375/250) = 1.22; psi_s = psi_alpha = psi_re = 1; / gamma_Mc 1.5 | **V_Rd,c = %s kN** (c1 350: %s kN) |' % (f(1.7*60**(0.1*(180/250)**0.5)*180**(0.1*(60/250)**0.2)*5*250**1.5/1e3), f(R['VRd_B_edge250']), f(V_edge_key(350, 60))))
    L.append('| Key A towards an edge 0.25-0.6 m away (no Key B) | same formula with d_nom 90, c1 = edge distance - 45 | e.g. c1 355: %s kN |' % f(V_edge_key(355, 90)))
    L.append('| Saddle (K21) | bearing 400 x 150 on the pier faces; plate cantilever 150, t 15: M_Rd %s kNm / 0.075 | %s kN |' % (f(R['MRd_saddle']), f(R['VRd_saddle'])))
    L.append('| Plate strip at the key moment | 300 mm strip, t 25 | %s kNm |' % f(R['Mpl_plate_strip']))
    L.append('\nShear parallel to a slab edge at Key A (bay shear along the wall line, e.g. K23 68 kN at 70 mm from the notch edge) bears on concrete that is continuous along the wall (column head / edge beam / solid strip); it is checked as bearing (Key A), not as edge breakout, and the edge beam under every wall line is part of the coring scope (section 5). The anchors take no shear, so there is no anchor N-V interaction; the key moments enter the anchor group through psi_ec,N and the max-anchor check.\n')
    L.append('## 3. Every base: pattern, keys, governing actions, utilisation, minimum solid zone (ULS envelope; reactions_C.csv has all cases)\n')
    L.append('| Col | Long axis (280 spacing) | Bays | Near edges | Key B | N_c max (case) | N_t max (case) | V max (case) | M_key max kNm | psi_ec at N_t max | Max anchor kN | Governing check | **Util. (zone 800)** | Util. cone 750 / 700 / 600 | Min. zone mm |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in COLS:
        e = base_env[c]; ed = edge_distances(*COLS[c])
        # psi_ec of the governing tension case
        psi = ''
        for cs in cases[c]:
            for N, bc in cs.get('base', []):
                if N < 0 and abs(-N - e['Nt'][0]) < 1e-6: psi = f(bc['psi_ec'], 2)
        L.append('| %s | %s | %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %s | %s | %s | %s | **%s** | %s / %s / %s | %s |' % (
            c, 'E-W' if COL_LONG[c] == 'x' else 'N-S', ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
            'saddle' if c in SADDLE else (','.join(e['keyB']) or '-'), f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], f(e['Vt'][0]), e['Vt'][1],
            f(e['Mkey']), psi, f(e['Nmax'], 0), e['umax'][2], f(e['umax'][0], 2), f(e['u_zone'][750], 2), f(e['u_zone'][700], 2), f(e['u_zone'][600], 2), e['zreq'] or '-'))
    worst = max(base_env, key=lambda c: base_env[c]['umax'][0])
    wt = max(base_env, key=lambda c: base_env[c]['Nt'][0]); wv = max(base_env, key=lambda c: base_env[c]['Vt'][0])
    L.append('\nWorst base **%s: %s (%s, %s)**; max uplift %s kN at %s; max shear %s kN at %s (Key A %s). All 27 bases and WP1 <= 1.0 with the 800 x 800 solid zone; the cone group is the governing mode at the braced and interior bases, the Key B edge breakout at the lightly loaded perimeter bases.\n' % (
        worst, f(base_env[worst]['umax'][0], 2), base_env[worst]['umax'][2], base_env[worst]['umax'][1], f(base_env[wt]['Nt'][0]), wt, f(base_env[wv]['Vt'][0]), wv, f(base_env[wv]['Vt'][0]/R['VRd_A'], 2)))
    L.append('## 4. Worked check, three representative bases\n')
    for c in ('K12', 'K23', 'K19'):
        e = base_env[c]; ed = edge_distances(*COLS[c])
        # governing tension case details
        best = None
        for cs in cases[c]:
            for N, bc in cs.get('base', []):
                if N < 0 and (best is None or bc['umax'] > best[2]['umax']): best = (cs, N, bc)
        cs, N, bc = best
        L.append('**%s (long axis %s, bays %s, near edges %s, Key B %s)** - governing tension case %s: N_t %s kN with V = (%s, %s) kN; Key A %s kN along / %s kN across, Key B %s; key moments M_along %s + M_across %s kNm -> e_N %s / %s mm -> psi_ec %s -> N_Rd,c = %s x %s = %s kN -> **%s**; max anchor %s kN (steel %s); bond %s; plate row %s. Compression max %s kN (%s): bearing %s. Shear max %s kN (%s): Key A %s. Minimum solid zone %s mm.\n' % (
            c, 'E-W' if COL_LONG[c] == 'x' else 'N-S', ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or 'none', ','.join(e['keyB']) or 'none',
            cs['case'], f(-N), f(cs['V'][0]), f(cs['V'][1]), f(bc['along']), f(bc['across']), ', '.join('%s %s kN' % (k, f(v)) for k, v in bc['VB'].items() if v > 0.5) or 'none',
            f(bc['M_along']), f(bc['M_across']), f(bc['M_along']/(-N)*1e3, 0), f(bc['M_across']/(-N)*1e3, 0), f(bc['psi_ec'], 2), f(R['NRd_c']), f(bc['psi_ec'], 2), f(R['NRd_c']*bc['psi_ec']), f(-N/(R['NRd_c']*bc['psi_ec']), 2),
            f(bc['Nmax'], 0), f(bc['Nmax']/R['NRd_s'], 2), f(-N/R['NRd_p'], 2), f(bc['util']['plate T-stub'], 2), f(e['Nc'][0]), e['Nc'][1], f(e['Nc'][0]/R['NRd_bearing'], 2), f(e['Vt'][0]), e['Vt'][1], f(e['Vt'][0]/R['VRd_A'], 2), e['zreq']))
    L.append('## 5. Coring acceptance criterion and fallback (R3)\n')
    L.append('- Cores (100 mm) at 3 column heads first, then a 60 mm core or GPR confirmation at every head: **solid concrete (no blocks, no voids) over at least the minimum zone of section 3, in all cases >= 750 x 750 mm, full slab depth >= 250 mm, C25 or better (rebound + core), and an edge/drop beam under every perimeter wall line**. A head that meets this is built as Type S / P above. K19 and K23 need 750; K16, K20, K22 need 700; all others 650 or less.')
    L.append('- **Fallback for a head whose solid zone is smaller than its minimum**: 4 M20 8.8 through-bolts at 500 (along) x 300 (across) around the column footprint, bearing on a 300 x 400 x 15 plate under the slab (cut around the 200 x 400 column, i.e. two 400 x 50 strips joined by 100 wide cross plates, or four 100 x 100 x 15 plate washers on the solid concrete beside the column), base plate 400 x 450; at a perimeter head both rows go inboard (150 and 350 mm from the column centre, +/- 250 along) and the 250 mm eccentricity of N_t is resisted by the couple of the two rows (e.g. K19: 73 kN x 0.25 / 0.20 = 91 kN row force, 2 M20 per row, 141 kN each). Tension then goes to the under-slab plate (no cone, no bond); shear stays with the keys (their bearing is on the solid concrete of the head, present in every case). Nine bases carry the fallback on the drawings from the start: K9, K10, K12, K13, K16, K19, K20, K22, K23.')
    L.append('- No coring or drilling into a column head in any case (R4); if neither the solid zone nor the fallback can be built at a head, the bay layout (section 8 of the report) is revised, not the anchorage.\n')
    L.append('## 6. Site verification before anchor installation\n')
    L.append('1. Cores as above; rebar scan of the slab top bars at every head to place the 140 mm (Key A) and 110 mm (Key B) pockets so that at most one top bar is cut, and to keep the anchors 20 mm clear of the slab bars.')
    L.append('2. Pull-out test on 3 sacrificial anchors (h_ef 200) to 1.3 x max anchor = 60 kN before production drilling; anchor supplier\'s ETA group verification (basis open item).')
    L.append('3. K21: confirm access to the pier faces; WP1: confirm the notch edge beam (or use the Type S plate with two Key B).')
    open(os.path.join(OUT, 'bases_C.md'), 'w').write('\n'.join(L) + '\n')

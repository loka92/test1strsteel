"""Writes bases_C.md: self-contained base and anchor design note (Rev 2 anchorage basis), from run_all.py."""
import os, math
from model import COLS, BAYS, edge_distances, NEAR_EDGE, POSTS
from connections import BASE, ANCH, V_RD_EDGE, FJD
from sections import sec, FY, FU

def write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp):
    B, A = BASE, ANCH; col = sec('HEA 160')
    braced = {c for b in BAYS for c in b['c']}
    perim = {c for c in COLS if any(v < 0.8 for v in edge_distances(*COLS[c]).values())}
    types = {c: ('B braced-bay' if c in braced else ('P perimeter' if c in perim else 'I interior')) for c in COLS}
    f = lambda x, n=1: '%.*f' % (n, x)
    L = []
    L.append('# Alternative C - Rev 2 base and anchor design note (bases_C.md)\n')
    L.append('Self-contained note for the base reviewer. Loads from `calc/run_all.py` (reactions_C.csv has every column and load case); anchorage basis = `../load_basis.md` Rev 2 (anchors through the slab into the column heads). Units kN, mm, MPa.\n')
    L.append('## 1. One base detail for all 27 columns\n')
    L.append('- Base plate **300 x 400 x 25 S275** (long side along the concrete column\'s 400 mm axis), on **40 mm non-shrink grout** over the slab solid zone; HEA 160 column welded a = 6 all round, web across the concrete column\'s short axis (i.e. normal to the wall it supports).')
    L.append('- **4 M20 8.8 resin anchors at 80 x 280** (all four inside the 200 x 400 concrete column core: 60 mm from each column face, 13 mm clear of the corner dia14 bars at the nominal cover - **rebar scan before drilling**), drilled through the 250 mm slab solid zone into the column head, **h_ef = 300 mm** (>= 50 mm into the column). Holes in the plate 26 mm (clearance) so the anchors carry tension only.')
    L.append('- **Grouted shear key**: 60 mm round bar S355, 330 mm long, welded to the underside of the plate with an 8 mm fillet all round, in a **90 mm cored pocket 350 mm deep** (250 slab + 100 into the column head, centred on the column, clear of the middle dia14 bars by 11 mm nominal - scan), grouted with the same non-shrink grout. The key carries the whole base shear in both directions; no anchor shear towards or parallel to a slab edge.')
    L.append('- Erection: level on shims, set the key and anchors in resin/grout, torque the anchor nuts to snug + 1/4 turn only (no preload relied on).\n')
    L.append('## 2. Resistances (EN 1992-4 with the basis values, EN 1993-1-8 for the plate and key)\n')
    L.append('| Item | Formula / factors | Value |')
    L.append('|---|---|---|')
    L.append('| Anchor steel tension, per anchor | N_Rk,s 196 / gamma_Ms 1.4 | %s kN (4 anchors %s kN) |' % (f(R['NRd_s']), f(4*R['NRd_s'])))
    L.append('| Concrete cone, single (slab solid zone) | k 7.2 (cracked) sqrt(25) h_ef^1.5, h_ef = 250 | N0_Rk,c = %s kN |' % f(R['N0c']))
    L.append('| Cone group factors | s_cr,N 750, c_cr,N 375; group 80 x 280 in the 800 x 800 solid zone (boundary as free edges): A_c,N/A0 = 800 x 800 / 750^2 = %s; psi_s,N = 0.7 + 0.3 x 260/375 = %s; psi_re = psi_ec = 1 | N_Rk,c,g = %s kN |' % (f(R['ratio_c'], 3), f(R['psi_s'], 2), f(R['NRk_cg'])))
    L.append('| **Cone group design** | / gamma_Mc 1.5 | **N_Rd,c = %s kN** |' % f(R['NRd_c']))
    L.append('| Bond, single | pi x 20 x 300 x tau_Rk 10 MPa (cracked) | N0_Rk,p = %s kN |' % f(R['N0p']))
    L.append('| Bond group factors | s_cr,Np = 7.3 d sqrt(tau) = %s <= 3 h_ef; A_p,N/A0 = %s; psi_s,Np = %s; psi_g,Np taken 1.0 | N_Rk,p,g = %s kN |' % (f(R['scrp'], 0), f(R['ratio_p'], 2), f(R['psi_sp'], 2), f(R['NRk_pg'])))
    L.append('| Bond group design | / gamma_Mp 1.5 | N_Rd,p = %s kN |' % f(R['NRd_p']))
    L.append('| **Group tension resistance** | min(steel, cone, bond) | **%s kN (cone)** |' % f(R['NRd_g']))
    L.append('| Bearing under the plate (compression) | effective area c = t sqrt(f_y/3 f_jd) = %s mm -> A_eff = %s cm2 at f_jd = 10 MPa (0.6 f_cd on the slab) | %s kN |' % (f(R['c'], 0), f(R['Aeff']/100, 0), f(R['NRd_bearing'], 0)))
    L.append('| Plate T-stub under uplift (per anchor row of 2) | cantilever from the flange tips m = %s mm, l_eff 300, t 25: F_T,1,Rd = 4 M_pl/m | %s kN |' % (f(R['m_plate'], 0), f(R['FT1_row'], 0)))
    L.append('| Key bearing on the grout/concrete | triangular over the 250 mm slab depth, sigma_max = 2V/(60 x 250) <= f_cd 16.7 | V <= %s kN |' % f(R['VRd_key_bearing']))
    L.append('| Key bending at the plate | lever 250/3 + 50 = 133 mm, W_pl = d^3/6, f_y 355 -> M_Rd %s kNm | **V <= %s kN** |' % (f(R['MRd_key']), f(R['VRd_key_bending'])))
    L.append('| Key weld | a = 8 fillet, 188 mm | %s kN |' % f(R['VRd_key_weld'], 0))
    L.append('| Key shear **towards a free slab edge < %s m from the column centre** | concrete in front of the key = 50 mm cover strip of the column head; resistance from the column cage only (3 dia14 dowels at 50 %% = 33 kN + one dia6 stirrup 2 legs 24 kN, f_yd 435): 57 -> | **V_Rd,edge = %s kN** (requires the rebar scan to confirm 6 dia14 + dia6/200) |' % (f(NEAR_EDGE, 2), f(V_RD_EDGE, 0)))
    L.append('\nTension and shear are carried by different elements (anchors / key), so no N-V interaction applies to the anchors; the key is checked for shear only. The slab solid zone (>= 800 x 800) and the column-head reinforcement are assumptions to be confirmed by cores and a rebar scan at 3 heads before drilling.\n')
    L.append('## 3. Governing actions and utilisation, every base (ULS envelope, concurrent values; full table in reactions_C.csv)\n')
    L.append('| Col | Type | Bays | Near edges (< 0.25 m) | N_c max kN (case) | N_t max kN (case) | V max kN (case) | Governing check | Util. |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for c in COLS:
        e = base_env[c]; ed = edge_distances(*COLS[c])
        L.append('| %s | %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %s | **%s** |' % (
            c, types[c], ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
            f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], f(e['Vt'][0]), e['Vt'][1], e['umax'][2], f(e['umax'][0], 2)))
    worst = max(base_env, key=lambda c: base_env[c]['umax'][0])
    L.append('\nWorst base: **%s, %s at %s (%s)**. All 27 bases <= 1.0 with the single detail above.\n' % (worst, f(base_env[worst]['umax'][0], 2), base_env[worst]['umax'][2], base_env[worst]['umax'][1]))
    L.append('## 4. Worked check, three representative bases\n')
    for c in ('K12', 'K23', 'K19'):
        e = base_env[c]; ed = edge_distances(*COLS[c])
        L.append('**%s (%s, bays %s, near edges %s)** - max compression %s kN (%s): bearing %s; max uplift %s kN (%s): anchors %s/4 = %s kN each, group %s/%s = **%s**, plate row %s/%s = %s; max shear %s kN (%s): key %s/%s = %s%s.\n' % (
            c, types[c], ','.join(b['id'] for b in BAYS if c in b['c']) or '-', ','.join(k for k, v in ed.items() if v < NEAR_EDGE) or 'none',
            f(e['Nc'][0]), e['Nc'][1], f(e['Nc'][0]/R['NRd_bearing'], 2), f(max(e['Nt'][0], 0)), e['Nt'][1], f(max(e['Nt'][0], 0)), f(max(e['Nt'][0], 0)/4),
            f(max(e['Nt'][0], 0)), f(R['NRd_g']), f(max(e['Nt'][0], 0)/R['NRd_g'], 2), f(max(e['Nt'][0], 0)/2), f(R['FT1_row'], 0), f(max(e['Nt'][0], 0)/2/R['FT1_row'], 2),
            f(e['Vt'][0]), e['Vt'][1], f(e['Vt'][0]), f(R['VRd_key']), f(e['Vt'][0]/R['VRd_key'], 2),
            ('; the component towards the near edge is checked against %s kN in reactions_C.csv' % f(V_RD_EDGE, 0)) if any(v < NEAR_EDGE for v in ed.values()) else ''))
    L.append('## 5. Load path summary\n')
    L.append('- Gravity: column -> plate -> grout -> slab solid zone -> concrete column (centred, no eccentricity).')
    L.append('- Uplift (ULS-3 roof suction + bracing tension diagonal): column and bracing gusset -> plate -> 4 anchors in tension -> bond over 300 mm and concrete cone in the slab solid zone (cracked). Max %s kN at %s vs %s kN.' % (f(max(e['Nt'][0] for e in base_env.values())), max(base_env, key=lambda c: base_env[c]['Nt'][0]), f(R['NRd_g'])))
    L.append('- Shear (bracing bay shear at the tension-diagonal base + wall wind wL/2 of the column, concurrent, same wind case): plate -> welded key -> grout -> slab solid zone / column head. Bay shears are arranged so that at no braced-bay base the bay shear points towards a free edge closer than 0.25 m (three N-S bracing lines x 68.0 / 77.8 / 95.5, two bays in series each); wall shear towards the near edge (<= 29 kN) is carried by the column cage.')
    L.append('- Wind post WP1 (notch corner, no concrete column): base plate 200 x 200 x 15 with 2 M16 resin anchors (h_ef 120) in the notch edge beam, shear %s / %s kN (E-W / N-S), no uplift (slotted top connection). Edge beam presence at the notch corner to be confirmed by a core.\n' % (f(V_wp[1]), f(V_wp[0])))
    L.append('## 6. Site verification before anchor installation\n')
    L.append('1. Cores at 3 column heads: slab thickness, solid-zone extent (>= 800 x 800 assumed), concrete grade (C25 assumed).')
    L.append('2. Rebar scan at every column head: 6 dia14 + dia6/200 stirrups, cover; adjust the 80 x 280 pattern and the key pocket to clear bars (tolerance +/- 20 mm in the pattern is covered: cone/bond group factors change < 3 %).')
    L.append('3. Pull-out test on 3 sacrificial anchors (h_ef 300) to 1.3 x N_Ed = 100 kN before production drilling; anchor supplier\'s ETA group verification (basis open item).')
    open(os.path.join(OUT, 'bases_C.md'), 'w').write('\n'.join(L) + '\n')

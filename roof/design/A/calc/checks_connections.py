"""Connections and bases (Alternative A): haunched end-plate knee (EN 1993-1-8 component method, simplified),
column web panel, rafter-to-girder pin, base plates and resin anchors (EN 1992-4 with the load-basis values).
Reads results_frames.pkl, results_secondary.pkl. Writes results_connections.pkl.
"""
import os, pickle, math
import numpy as np
from sections import sec, haunch_props, FY
import loads as L
from frames_model import COMBOS, DESIGN
from checks_members import rafter_profile, column_forces, frame_keys, RES, ULS

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = pickle.load(open(os.path.join(HERE, 'results_secondary.pkl'), 'rb'))
BB = SEC['base_brace']

# ============================================================== 1. design forces at every knee
rs = sec('IPE300'); hp = haunch_props(rs); cs = sec('HEA200')
knee = {}
for fname in L.FRAMES:
    for key in frame_keys(fname):
        meta = RES[key]['_meta']
        for c in ULS:
            r = RES[key][c]
            y, M, V, N, hz, dz = rafter_profile(r)
            for k, yc in meta['cols']:
                d = knee.setdefault(k, dict(M_hog=0, M_sag=0, V=0, dM=0, N=0, combo_hog='', combo_sag=''))
                # moment at the column face (h_col/2 = 95 mm from the centreline) on both sides
                face = []
                for sgn in (-1, +1):
                    yf = yc + sgn * cs['h'] / 2000
                    if meta['y0'] - 1e-6 <= yf <= meta['y1'] + 1e-6:
                        face.append((np.interp(yf, y, M), np.interp(yf, y, V), np.interp(yf, y, N)))
                for Mf, Vf, Nf in face:
                    if -Mf > d['M_hog']: d['M_hog'] = -Mf; d['combo_hog'] = c
                    if Mf > d['M_sag']: d['M_sag'] = Mf; d['combo_sag'] = c
                    d['V'] = max(d['V'], abs(Vf)); d['N'] = max(d['N'], abs(Nf))
                if len(face) == 2:
                    d['dM'] = max(d['dM'], abs(face[0][0] - face[1][0]))
                else:
                    d['dM'] = max(d['dM'], abs(face[0][0]))
M_hog = max(v['M_hog'] for v in knee.values()); M_sag = max(v['M_sag'] for v in knee.values())
V_knee = max(v['V'] for v in knee.values()); dM = max(v['dM'] for v in knee.values())

# ============================================================== 2. end-plate connection, component method
# geometry (mm): end plate 200 x 680 x 20 S275 (symmetric, extended top and bottom), bolts M20 8.8, 2 lines, gauge w = 100
tp, w, bp = 20.0, 100.0, 200.0
a_w, a_f = 5.0, 8.0                       # fillet welds web / flange
H_h = hp['H']                             # 450 haunched depth at the column face
tf_b, tw_b = rs['tf'], rs['tw']
# bolt rows measured from the top of the rafter (positive downwards): extension row, then pitch 100, last row 55 above haunch flange
rows_y = [-45.0, 55.0, 155.0, 295.0, 395.0, 495.0]   # symmetric about the haunched depth 450
F_t = 141.0                               # kN per M20 8.8 (basis)
F_v = 94.0
tfc, twc, rc = cs['tf'], cs['tw'], cs['r']
m_c = w / 2 - twc / 2 - 0.8 * rc; e_c = (cs['b'] - w) / 2
m_p = w / 2 - tw_b / 2 - 0.8 * math.sqrt(2) * a_w; e_p = (bp - w) / 2


def Mpl_plate(leff, t):                   # kNm
    return 0.25 * leff * t**2 * FY / 1e6


def tstub(leff, m, e, t, Ft_sum, t_bp=0.0):
    """T-stub resistance (kN), modes 1-3. m, e in mm, Ft_sum = sum of bolt tension resistances of the row."""
    Mpl = Mpl_plate(leff, t); Mbp = Mpl_plate(leff, t_bp) if t_bp else 0.0
    n = min(e, 1.25 * m)
    F1 = (4 * Mpl + 2 * Mbp) / (m / 1e3)
    F2 = (2 * Mpl + n / 1e3 * Ft_sum) / ((m + n) / 1e3)
    return min(F1, F2, Ft_sum), (F1, F2, Ft_sum)


def row_resistance(kind, t_bp=0.0):
    """kind: 'ext' (extension row, end plate), 'adj' (row adjacent to a stiffened flange), 'inner'."""
    res = {}
    if kind == 'ext':
        mx = 45.0 - 0.8 * math.sqrt(2) * a_f; ex = 50.0
        leff = min(2 * math.pi * mx, math.pi * mx + w, math.pi * mx + 2 * e_p, 4 * mx + 1.25 * ex,
                   e_p + 2 * mx + 0.625 * ex, 0.5 * bp, 0.5 * w + 2 * mx + 0.625 * ex)
        res['plate'] = tstub(leff, mx, ex, tp, 2 * F_t)
        leff_c = 2 * math.pi * m_c                                    # column flange, row adjacent to stiffener (alpha m ~ 2 pi m)
        res['col'] = tstub(leff_c, m_c, e_c, tfc, 2 * F_t, t_bp)
    elif kind == 'adj':
        leff = min(2 * math.pi * m_p, 6.5 * m_p)                      # adjacent to beam flange (alpha ~ 6.5)
        res['plate'] = tstub(leff, m_p, e_p, tp, 2 * F_t)
        res['col'] = tstub(min(2 * math.pi * m_c, 6.5 * m_c), m_c, e_c, tfc, 2 * F_t, t_bp)
    else:
        leff = min(2 * math.pi * m_p, 4 * m_p + 1.25 * e_p)
        res['plate'] = tstub(leff, m_p, e_p, tp, 2 * F_t)
        res['col'] = tstub(min(2 * math.pi * m_c, 4 * m_c + 1.25 * e_c), m_c, e_c, tfc, 2 * F_t, t_bp)
    # column web in tension (stiffened where adjacent), beam web in tension
    leff_wt = min(2 * math.pi * m_c, 4 * m_c + 1.25 * e_c)
    res['col_web_t'] = (leff_wt * twc * FY / 1e3, ())
    res['beam_web_t'] = (min(2 * math.pi * m_p, 4 * m_p + 1.25 * e_p) * tw_b * FY / 1e3, ())
    F = min(v[0] for v in res.values())
    return F, res


def group_cap(nrows, t_bp=0.0):
    """Column-flange group T-stub of nrows adjacent inner rows at pitch 100 (mode 1 governs): sum limited."""
    p = 100.0
    leff_g = nrows * (2 * m_c + 0.625 * e_c + 0.5 * p) + (2 * m_c + 0.625 * e_c) * 0   # each inner row 2m+0.625e+p, end rows 0.5p... simplified
    leff_g = 2 * (2 * m_c + 0.625 * e_c + 0.5 * p) + (nrows - 2) * p if nrows >= 2 else leff_g
    return tstub(leff_g, m_c, e_c, tfc, 2 * nrows * F_t, t_bp)[0]


def Mj_Rd(sign, t_bp=0.0):
    """sign 'hog': tension rows at the top, compression centre at the haunch bottom flange.
       sign 'sag': tension rows at the bottom (haunch), compression centre at the rafter top flange."""
    if sign == 'hog':
        zc = H_h - tf_b / 2
        rows = [(-45.0, 'ext'), (55.0, 'adj'), (155.0, 'inner')]
        lever = [zc - yy for yy, _ in rows]
    else:
        zc = tf_b / 2
        rows = [(495.0, 'ext'), (395.0, 'adj'), (295.0, 'inner')]
        lever = [yy - zc for yy, _ in rows]
    Fr = []; detail = []
    for (yy, kind), z in zip(rows, lever):
        F, res = row_resistance(kind, t_bp)
        Fr.append(F); detail.append((yy, kind, F, {k: round(v[0], 0) for k, v in res.items()}))
    # group limitation on the column flange for the inner rows (adjacent + inner rows as a group)
    inner = [i for i, (yy, kind) in enumerate(rows) if kind in ('adj', 'inner')]
    cap = group_cap(len(inner), t_bp)
    if sum(Fr[i] for i in inner) > cap:
        # reduce from the row nearest the compression centre (smallest lever)
        excess = sum(Fr[i] for i in inner) - cap
        for i in reversed(inner):
            take = min(Fr[i], excess); Fr[i] -= take; excess -= take
            if excess <= 0: break
    # compression side: haunch flange + web (beam flange compression) and column web with stiffener
    F_c_beam = hp['Mel'] / ((H_h - tf_b) / 1e3)
    F_c_col = (2 * 95 * 10 + 200 * twc) * FY / 1e3                 # stiffener pair 95x10 + effective web
    F_c = min(F_c_beam, F_c_col)
    scale = min(1.0, F_c / sum(Fr))
    M = sum(F * z / 1e3 * scale for F, z in zip(Fr, lever))
    return M, list(zip([r[0] for r in rows], Fr, lever)), detail, dict(F_c_beam=F_c_beam, F_c_col=F_c_col, cap_group=cap)


M_Rd_hog, rows_hog, det_hog, comp_hog = Mj_Rd('hog')
M_Rd_sag, rows_sag, det_sag, comp_sag = Mj_Rd('sag')
# column web panel in shear (6.2.6.1): V_wp,Rd = 0.9 f_y A_vc / (sqrt(3) gamma_M0)
V_wp_Rd = 0.9 * FY * cs['Av'] / math.sqrt(3) / 1e3
z_panel = (H_h - tf_b) / 1e3
V_wp_Ed = dM / z_panel
# bolt shear: 4 bolts of the compression-side rows (not in tension) carry V; tension bolts checked combined
u_bolt_v = V_knee / (4 * F_v)
conn = dict(M_hog=M_hog, M_sag=M_sag, V=V_knee, dM=dM, M_Rd_hog=M_Rd_hog, M_Rd_sag=M_Rd_sag, rows_hog=rows_hog, rows_sag=rows_sag,
            det_hog=det_hog, det_sag=det_sag, comp_hog=comp_hog, V_wp_Rd=V_wp_Rd, V_wp_Ed=V_wp_Ed, z=z_panel,
            u_hog=M_hog / M_Rd_hog, u_sag=M_sag / M_Rd_sag, u_wp=V_wp_Ed / V_wp_Rd, u_bolt_v=u_bolt_v,
            plate='200 x 680 x 20 S275, 12 x M20 8.8, gauge 100, rows at -45/55/155/295/395/495 from rafter top (symmetric)',
            stiffeners='column: 2 pairs 95 x 10 at rafter top-flange and haunch bottom-flange levels', welds='flange 8 mm, web 5 mm double fillet',
            knee=knee)
# knee stiffness class (rough): S_j,ini ~ E z^2 / sum(1/k_i); rigid if S_j >= 8 E I_b / L_b for braced... noted only
# rafter-to-girder pin (F5/F6)
Rg = SEC['girder']
pin = dict(V_down=Rg['ULS_grav']['P5'], V_up=-Rg['ULS_uplift']['P5'], H=1.5 * (L.CPE_WALL_D - 0.3) * L.QP * 3.55 * L.wall_height(20.07) / 2)
pin['R'] = math.hypot(max(pin['V_down'], pin['V_up']), pin['H']); pin['u'] = pin['R'] / (4 * F_v)
pin['detail'] = 'rafter end plate 12 mm on a vertical T-stiffener (10 mm) welded to the girder top flange, 4 x M20 8.8, no slot (transfers wind to the roof plane)'

# ============================================================== 3. base plates and anchors
import sys
HEF = 300.0                                # anchor embedment (mm): 170 = load-basis assumption; 300 = deep anchor into the column head
if len(sys.argv) > 1: HEF = float(sys.argv[1])
gMc, gMs = 1.5, 1.4
f_jd = 10.0                                # MPa bearing on grout/slab (basis)
tbp = 20.0
c_eff = tbp * math.sqrt(FY / (3 * f_jd))    # EN 1993-1-8 6.2.5
A_eff = 2 * (cs['b'] + 2 * c_eff) * (cs['tf'] + 2 * c_eff) + (cs['hw'] - 2 * c_eff) * (cs['tw'] + 2 * c_eff)
N_Rd_bearing = A_eff * f_jd / 1e3


def anchor_values(h_ef):
    """Characteristic single-anchor values of the load basis, scaled with h_ef (cone ~ h_ef^1.5, bond ~ h_ef)."""
    return dict(N0_Rk_c=7.2 * math.sqrt(25) * h_ef**1.5 / 1e3, N_Rk_s=196.0, N_Rk_p=math.pi * 20 * h_ef * 10 / 1e3, V_Rk_s=98.0,
                c_cr=1.5 * h_ef, s_cr=3 * h_ef)


def cone_group(kind, h_ef, ecc=0.0):
    """EN 1992-4 concrete cone, 4-anchor group 300 x 150 (mm). kind: interior / edge (c1=100 on the 150 side) / corner."""
    av = anchor_values(h_ef); s_long, s_short = 300.0, 150.0
    if kind == 'interior':
        AcN = (s_long + 3 * h_ef) * (s_short + 3 * h_ef); psi_s = 1.0
    elif kind == 'edge':
        AcN = (s_long + 3 * h_ef) * (100.0 + s_short + 1.5 * h_ef); psi_s = 0.7 + 0.3 * 100.0 / av['c_cr']
    else:  # corner: c1 = 100 on the 150 side, c2 = 150 on the 300 side
        AcN = (150.0 + s_long + 1.5 * h_ef) * (100.0 + s_short + 1.5 * h_ef); psi_s = 0.7 + 0.3 * 100.0 / av['c_cr']
    AcN0 = (3 * h_ef)**2
    psi_ec = 1 / (1 + 2 * ecc / av['s_cr'])
    return av['N0_Rk_c'] * AcN / AcN0 * psi_s * psi_ec, AcN / AcN0, psi_s, psi_ec


def edge_shear(h_ef, parallel=False):
    """EN 1992-4 7.2.2.5 concrete edge breakout, near row of 2 anchors at c1 = 100 mm, s = 300, uncracked (k9 = 2.4)."""
    c1, d, lf = 100.0, 20.0, min(h_ef, 8 * 20)
    alpha = 0.1 * (lf / c1)**0.5; beta = 0.1 * (d / c1)**0.2
    V0 = 2.4 * d**alpha * lf**beta * math.sqrt(25) * c1**1.5 / 1e3
    AcV0 = 4.5 * c1**2; AcV = (1.5 * c1 + 300 + 1.5 * c1) * min(1.5 * c1, 250)
    psi_a = 2.0 if parallel else 1.0
    return V0 * AcV / AcV0 * psi_a


CORNER = {'K25', 'K6', 'K27', 'K4', 'K23'}
EDGE = {'K26', 'K24', 'K5', 'K7', 'K3', 'K1', 'K2', 'K21', 'K22', 'K19', 'K15', 'K8', 'K18', 'K14'}
GIRDER_R = SEC['girder']
EXTRA = {'K21': ('n1',), 'K22': ('n3',), 'K23': ('n5',)}     # girder reactions added to these bases; K24 from the eaves beam


def base_check(k, h_ef):
    av = anchor_values(h_ef)
    kind = 'corner' if k in CORNER else ('edge' if k in EDGE else 'interior')
    ecc = 0.0 if kind == 'interior' else 75.0
    side = L.WALL_SIDE.get(k); ew = L.WALL_TRIB.get(k, (0, 0))[1]
    NRk_c, ratioA, psi_s, psi_ec = cone_group(kind, h_ef, ecc)
    NRd_c = NRk_c / gMc
    n_eff = 4 if kind == 'interior' else 2                      # eccentric pattern: near row carries the tension
    NRd_t = min(NRd_c, av['N_Rk_s'] / gMs * n_eff, av['N_Rk_p'] / gMc * n_eff)
    VRd_s = av['V_Rk_s'] / gMs * 4
    VRd_edge = edge_shear(h_ef) / gMc; VRd_par = edge_shear(h_ef, True) / gMc; VRd_cp = 2 * NRk_c / gMc
    Vx_br = BB.get(k, {}).get('Vx', 0.0); Nv_br = BB.get(k, {}).get('Nv_abs', 0.0)
    rec = dict(kind=kind, NRd_c=NRd_c, NRd_t=NRd_t, ratioA=ratioA, psi_s=psi_s, psi_ec=psi_ec, VRd_edge=VRd_edge, VRd_par=VRd_par,
               Nc=0, Nt=0, Vy=0, Vx=0, Vout=0, Nc_s=0, Nt_s=0, Vy_s=0, Vx_s=0, u=0, u_t=0, u_v=0, combo='', comboC='', comboT='')
    # per-combo demands
    cases = []
    is_post = k in ('K22', 'K24')
    combos_here = []
    for fname in L.FRAMES:
        if k in L.FRAMES[fname]['cols']:
            for key in frame_keys(fname):
                for c in COMBOS:
                    R = RES[key][c]['reactions']['%s_0' % k]
                    combos_here.append((c, R[1], R[0]))
    if is_post:
        combos_here = [(c, 0.0, 0.0) for c in COMBOS]
    for c, Rz, Rx in combos_here:
        uls = c.startswith('ULS'); f = 1.0 if uls else 1 / 1.5
        Nt = -Rz; Nc = Rz
        Vy = abs(Rx)
        Vout = (-Rx if side == 'N' else (Rx if side == 'S' else 0.0))
        # girder / eaves-beam reactions (gravity in ULS1/2, uplift in ULS3 (R combos: half), SLS scaled)
        if k in EXTRA:
            n = EXTRA[k][0]
            if 'ULS1' in c or 'ULS2' in c or c in ('SLS_D', 'SLS_G'): Nc += GIRDER_R['ULS_grav']['R'][n] * f
            if 'ULS3' in c or c in ('SLS_WNp',): Nt += -GIRDER_R['ULS_uplift']['R'][n] * f * (0.5 if c.endswith('_R') else 1.0)
        if k == 'K24':
            Nc += 12.0 * f if ('ULS1' in c or 'ULS2' in c or c in ('SLS_D', 'SLS_G')) else 0.0
            Nt += 5.0 * f if 'ULS3' in c else 0.0
        if is_post:   # pinned wind post: wall wind shear at the base (half height), toward the edge under suction
            V_post = SEC['posts'][4 if k == 'K22' else 3]['V'] * f
            Vy = V_post; Vout = V_post * (0.5 + 0.2) / (0.8 + 0.3)
        isR = c.endswith('_R') or c == 'SLS_WR'
        Vpar = Vy if (not side and ew) else 0.0                   # E/W-wall columns: frame shear is parallel to their edge
        Vedge = Vout if side else 0.0
        if isR:
            cpi = 0.2 if 'ULS3' in c or c == 'SLS_WR' else -0.3
            Nt += Nv_br * f; Nc += Nv_br * f
            Vpar = max(Vpar, Vx_br * f)
            if ew:  # out-of-plane wall wind on E/W-wall columns: leeward suction pulls toward the edge
                Vedge = max(Vedge, 1.5 * f * (0.5 + cpi) * L.QP * ew * L.TOS(L.COLS[k][1]) / 2)
                Vpar_wind = 0.0
        Vx = max(Vx_br * f if isR else 0.0, (1.5 * f * (0.8 + 0.3) * L.QP * ew * L.TOS(L.COLS[k][1]) / 2) if (ew and isR) else 0.0)
        Vres = math.hypot(Vx, Vy)
        if uls:
            u_t = Nt / NRd_t if Nt > 0 else 0.0
            if kind == 'interior':
                u_v = Vres / min(VRd_s, VRd_cp)
            else:
                u_v = max(Vedge / VRd_edge, Vpar / VRd_par, Vres / VRd_s)
            u = (u_t**1.5 + u_v**1.5) if (u_t > 0 and u_v > 0) else max(u_t, u_v)
            if u > rec['u']: rec.update(u=u, u_t=u_t, u_v=u_v, combo=c)
            if Nc > rec['Nc']: rec['Nc'] = Nc; rec['comboC'] = c
            if Nt > rec['Nt']: rec['Nt'] = Nt; rec['comboT'] = c
            rec['Vy'] = max(rec['Vy'], Vy); rec['Vx'] = max(rec['Vx'], Vx); rec['Vout'] = max(rec['Vout'], Vedge)
        else:
            rec['Nc_s'] = max(rec['Nc_s'], Nc); rec['Nt_s'] = max(rec['Nt_s'], Nt); rec['Vy_s'] = max(rec['Vy_s'], Vy); rec['Vx_s'] = max(rec['Vx_s'], Vx)
    rec['u_bear'] = rec['Nc'] / N_Rd_bearing
    F_row = rec['Nt'] / n_eff * 2; M_pl_strip = 0.25 * 250 * tbp**2 * FY / 1e6   # 250 mm wide plate strip, lever 55 mm
    rec['u_plate'] = F_row * 0.055 / M_pl_strip
    rec['Nv_br'] = Nv_br
    return rec


bases = {k: base_check(k, HEF) for k in L.COLS}
bases_170 = {k: base_check(k, 170.0) for k in L.COLS}
base_common = dict(h_ef=HEF, plate='300 x 400 x 20 S275 on 30-50 mm non-shrink grout (eccentric 75 mm inboard at perimeter bases)',
                   anchors='4 x M20 8.8 resin anchors, h_ef %.0f mm, group 300 x 150 (perimeter: outer row 100 mm from the slab edge)' % HEF,
                   c_eff=c_eff, A_eff=A_eff, N_Rd_bearing=N_Rd_bearing,
                   interior=cone_group('interior', HEF)[0] / gMc, edge=cone_group('edge', HEF, 75)[0] / gMc, corner=cone_group('corner', HEF, 75)[0] / gMc,
                   interior170=cone_group('interior', 170)[0] / gMc, edge170=cone_group('edge', 170, 75)[0] / gMc, corner170=cone_group('corner', 170, 75)[0] / gMc,
                   VRd_edge=edge_shear(HEF) / gMc, VRd_par=edge_shear(HEF, True) / gMc, VRd_s=4 * 98 / gMs, av=anchor_values(HEF))

pickle.dump(dict(conn=conn, pin=pin, bases=bases, bases_170=bases_170, base_common=base_common), open(os.path.join(HERE, 'results_connections.pkl'), 'wb'))

if __name__ == '__main__':
    print('KNEE: M_hog %.1f (%s) M_sag %.1f  V %.1f  dM %.1f' % (M_hog, max(knee.items(), key=lambda kv: kv[1]['M_hog'])[0], M_sag, V_knee, dM))
    print('  M_Rd hog %.1f  rows %s' % (M_Rd_hog, [(y, round(F), round(z)) for y, F, z in rows_hog]))
    print('  detail hog', det_hog, comp_hog)
    print('  M_Rd sag %.1f  rows %s' % (M_Rd_sag, [(y, round(F), round(z)) for y, F, z in rows_sag]))
    print('  detail sag', det_sag)
    print('  V_wp,Ed %.0f  V_wp,Rd %.0f   u_hog %.2f u_sag %.2f u_wp %.2f u_bolt_v %.2f' % (V_wp_Ed, V_wp_Rd, conn['u_hog'], conn['u_sag'], conn['u_wp'], u_bolt_v))
    for k, v in knee.items():
        print('   %s hog %.0f (%s) sag %.0f (%s) V %.0f dM %.0f' % (k, v['M_hog'], v['combo_hog'], v['M_sag'], v['combo_sag'], v['V'], v['dM']))
    print('PIN', pin)
    print('BASE common', base_common)
    for k in L.COLS:
        b = bases[k]; b1 = bases_170[k]
        print('%-4s %-8s Nc %6.1f Nt %6.1f (br %4.1f) Vy %5.1f Vx %5.1f Vout %5.1f | NRd_t %5.1f u_t %.2f u_v %.2f u %.2f [%s] bear %.2f plate %.2f | h_ef170: NRd_t %5.1f u %.2f' %
              (k, b['kind'], b['Nc'], b['Nt'], b['Nv_br'], b['Vy'], b['Vx'], b['Vout'], b['NRd_t'], b['u_t'], b['u_v'], b['u'], b['combo'], b['u_bear'], b['u_plate'], b1['NRd_t'], b1['u']))

"""Connections (EN 1993-1-8) and bases/anchors (EN 1992-4 with the load-basis values). kN, mm."""
import math
from sections import sec, FY, FU, GM0, GM2

BOLT = dict(d=20, d0=22, As=245.0, FvRd=94.0, FtRd=141.0, fub=800.0)
def bearing(t, e1, p1, e2, d=20, d0=22, fu=FU):
    ab = min(e1/(3*d0), p1/(3*d0) - 0.25 if p1 else 9, BOLT['fub']/fu, 1.0)
    k1 = min(2.8*e2/d0 - 1.7, 2.5)
    return k1*ab*fu*d*t/GM2/1e3

def weld_res(a):     # kN/mm per fillet weld throat a (mm), S275: fu 430, beta_w 0.85
    return a*FU/(3**0.5*0.85*GM2)/1e3

def fin_plate(V_Ed, n, tw_beam, tp=10, e=50, p1=70, e1=40, e2=40, hp=None):
    """Fin plate with n bolts M20 in one vertical row, plate tp, bolt line at e from the weld.
    Bolt group under V and M = V*e (EN 1993-1-8 3.6/3.7). Returns dict of utilisations."""
    hp = hp or (2*e1 + (n-1)*p1)
    M = V_Ed*e/1e3                                  # kNm
    if n == 1: Fb = V_Ed
    else:
        r = [(i - (n-1)/2)*p1 for i in range(n)]; sr2 = sum(ri**2 for ri in r)
        Fh = M*1e3*max(abs(x) for x in r)/sr2       # kN horizontal on the extreme bolt
        Fb = ((V_Ed/n)**2 + Fh**2)**0.5
    u = {}
    u['bolt shear'] = Fb/BOLT['FvRd']
    u['bearing plate'] = Fb/bearing(tp, e1, p1, e2)
    u['bearing web'] = Fb/bearing(tw_beam, e1, p1, e2)
    Av_g = hp*tp; Av_n = (hp - n*22)*tp
    u['plate shear'] = V_Ed/min(Av_g*FY/3**0.5/GM0/1e3, Av_n*FU/3**0.5/GM2/1e3)
    u['plate bending'] = M/(tp*hp**2/6*FY/1e6)    # elastic, with M at the weld line
    # welds: 2 fillets a=6 both sides, resist V and M (elastic): sigma = M/(2 a hp^2/6), tau = V/(2 a hp)
    a = 6.0; fw = weld_res(a)
    sig = M*1e6/(2*a*hp**2/6); tau = V_Ed*1e3/(2*a*hp)
    u['weld'] = (sig**2 + tau**2)**0.5/(fw*1e3/a)
    # block tearing of the beam web (EN 1993-1-8 3.10.2), Veff,2 (eccentric)
    Ant = (e2 - 22/2)*tw_beam; Anv = (e1 + (n-1)*p1 - (n-0.5)*22)*tw_beam
    Veff2 = 0.5*FU*Ant/GM2/1e3 + FY*Anv/3**0.5/GM0/1e3
    u['web block tearing'] = V_Ed/Veff2
    return dict(util=u, umax=max(u.values()), gov=max(u, key=u.get), n=n, tp=tp, hp=hp, V_Ed=V_Ed)

def cap_plate(N_t, V_h, tp=20, gauge=90, pitch=200, tf_beam=11.5, tw_beam=7.5):
    """Column cap plate 200x280x20 welded to HEA 160 (a=6 all round); primary bolted with 4 M20 through its
    bottom flange at pitch 200 so the nuts clear the passing rafter flange (review F12). Tension from uplift N_t (kN) and horizontal chord/strut force V_h (kN)."""
    u = {}
    u['bolt tension'] = N_t/4/BOLT['FtRd']
    u['bolt shear'] = V_h/4/BOLT['FvRd']
    u['bolt interaction'] = V_h/4/BOLT['FvRd'] + N_t/4/(1.4*BOLT['FtRd'])
    # T-stub of the IPE 330 bottom flange (mode 1, both rows): m = gauge/2 - tw/2 - 0.8 r (r=18)
    m = gauge/2 - tw_beam/2 - 0.8*18; leff = min(2*math.pi*m, 4*m + 1.25*40, pitch)
    Mpl = 0.25*leff*tf_beam**2*FY/1e3      # kNmm
    FT1 = 2*4*Mpl/m                         # two rows
    u['beam flange T-stub'] = N_t/FT1
    m2 = m; Mpl2 = 0.25*leff*tp**2*FY/1e3; FT1p = 2*4*Mpl2/m2
    u['cap plate T-stub'] = N_t/FT1p
    # weld cap plate to column: perimeter of HEA 160 (2 x 160 flanges x 2 faces + web) ~ 2*(2*160)+2*134 = 908 mm, a=6
    Lw = 908; u['weld'] = ((N_t*1e3/(Lw*6))**2 + (V_h*1e3/(Lw*6))**2)**0.5/(weld_res(6)*1e3/6)
    return dict(util=u, umax=max(u.values()), gov=max(u, key=u.get))

# ---- base plate and anchors, Rev 4 (sign-off S1-S4) ---------------------------------------------------------------
# B1 (interior and lightly loaded edge bases): plate 300 x 400 x 25, 4 M20 resin anchors 80 x 280 (280 along the concrete
#    column's long axis), h_ef 200 in the slab; cone with the REAL slab edges (column flush with the face: the outboard
#    row is 60 mm from the edge); Key A SHS 90x90x8 under the column centre (along/inward shear; parallel-to-edge breakout
#    2 V_Rk,c where an edge is closer than 0.6 m); Key B 60 mm bar 180 mm inboard for outward shear (c1 250).
# B2 (perimeter / edge-adjacent bases that fail B1): plate 700 (along) x 550 (across: 100 outboard, 450 inboard) x 30
#    with two 120 x 10 stiffeners; 2 M24 8.8 through-bolts at (+-140 along, +250 inboard), 400 x 200 x 20 plate under
#    the slab; uplift by lever action about the inboard plate tip (T = 2.39 N_t, C = 1.39 N_t); shear by a PAIR of SHS
#    90x90x8 keys at (+-300 along, +200 inboard): c1 = 255 to the building face, torque V_along x 0.2 m resolved by the
#    pair (arm 0.6 m); nothing drilled into the column head.
# P  (K21, 200 mm pier between the notch edge and the shaft opening): 4 M16 resin anchors 70 x 280, h_ef 400 into the
#    pier (the only base where the client's permission to drill the column/pier head is used), saddle for N-S shear.
BASE = dict(bp=300, lp=400, tp=25, sx=80, sy=280, hef=200, fck=25, zone=800, slab=250, grout=25,
            keyA_b=90, keyA_Wpl=75.0e3, keyA_fy=355.0, keyA_core=140, keyB_d=60, keyB_fy=335.0, emb=180, pocket=200, keyB_off=180, saddle_t=15,
            b2_row=250, b2_tip=430, b2_keys_x=300, b2_keys_y=200, b2_bolt_FtRd=0.9*800*353/1.25/1e3, b2_plate_b=350, b2_plate_t=30,
            b2_MRd_plate=48.0, b2_plate_c=60, p_hef=400, p_d=16, p_sx=70)
ANCH = dict(NRk_s=196.0, gMc=1.5, gMs=1.4, gMp=1.5, tau=10.0, d=20, k_cr=7.2)
FJD = 10.0; FCD = 25/1.5
LEVER = BASE['grout'] + BASE['emb']/3      # 85 mm

def V_edge_key(c1, d_nom, lf=BASE['emb'], h=BASE['slab'], fck=BASE['fck'], side=None):
    """EN 1992-4 7.2.2.5 edge breakout (cracked k9 1.7) of a stiff element of width d_nom loaded towards an edge at c1."""
    if c1 <= 0: return 0.0
    al = 0.1*(lf/c1)**0.5; be = 0.1*(d_nom/c1)**0.2
    V0 = 1.7*d_nom**al*lf**be*math.sqrt(fck)*c1**1.5/1e3
    A0 = 4.5*c1**2; w = 3*c1 if side is None else min(3*c1, 1.5*c1 + side)
    Ac = w*min(1.5*c1, h); psi_h = math.sqrt(1.5*c1/h) if 1.5*c1 > h else 1.0
    psi_s = 1.0 if side is None else min(1.0, 0.7 + 0.3*side/(1.5*c1))
    return V0*Ac/A0*psi_h*psi_s/ANCH['gMc']

def cone_group(ext, hef=BASE['hef'], sx=BASE['sx'], sy=BASE['sy'], k=ANCH['k_cr']):
    """Cone of a 2 x 2 group (spacings sx across, sy along) with the available solid concrete beyond the outer anchors:
    ext = (out, in, side1, side2) mm, each capped at c_cr = 1.5 h_ef. Returns dict (design N_Rd for the group)."""
    N0 = k*math.sqrt(BASE['fck'])*hef**1.5/1e3; scr = 3*hef; ccr = 1.5*hef
    e = [min(v, ccr) for v in ext]
    Ac = (e[0] + sx + e[1])*(e[2] + sy + e[3]); ratio = Ac/scr**2
    psi_s = min(1.0, 0.7 + 0.3*min(e)/ccr)
    return dict(N0=N0, ratio=ratio, psi_s=psi_s, NRk=N0*ratio*psi_s, NRd=N0*ratio*psi_s/ANCH['gMc'], scr=scr, ext=e)

def anchor_resistances(zone=BASE['zone'], B=BASE, A=ANCH):
    r = {}
    r['NRd_s'] = A['NRk_s']/A['gMs']
    h = zone/2
    cg = cone_group((h - B['sx']/2, h - B['sx']/2, h - B['sy']/2, h - B['sy']/2)); r.update(N0c=cg['N0'], ratio_c=cg['ratio'], psi_s=cg['psi_s'], NRk_cg=cg['NRk'], NRd_c=cg['NRd'], scr=cg['scr'])
    N0p = math.pi*A['d']*B['hef']*A['tau']/1e3
    scrp = min(7.3*A['d']*math.sqrt(A['tau']), 3*B['hef']); ccrp = scrp/2
    cxp = min(h - B['sy']/2, ccrp); cyp = min(h - B['sx']/2, ccrp)
    Ap = (cxp + B['sy'] + cxp)*(cyp + B['sx'] + cyp); ratio_p = Ap/scrp**2; psi_sp = min(1.0, 0.7 + 0.3*min(cxp, cyp)/ccrp)
    r.update(N0p=N0p, scrp=scrp, ratio_p=ratio_p, psi_sp=psi_sp, NRk_pg=N0p*ratio_p*psi_sp, NRd_p=N0p*ratio_p*psi_sp/A['gMp'])
    r['NRd_g'] = min(4*r['NRd_s'], r['NRd_c'], r['NRd_p'])
    D, hg = B['emb'], B['grout']; z0 = D*(D/3 + hg/2)/(D/2 + hg); r['z0'] = z0
    kA = z0/(B['keyA_b']*(z0*D - D**2/2)); r['sigma_A'] = 1.5*FCD; r['VRd_A_bearing'] = r['sigma_A']/kA/1e3
    r['MRd_A'] = B['keyA_Wpl']*B['keyA_fy']/1e6; r['VRd_A_bending'] = r['MRd_A']/(LEVER/1e3); r['VRd_A_weld'] = weld_res(8)*4*B['keyA_b']
    r['VRd_A'] = min(r['VRd_A_bearing'], r['VRd_A_bending'], r['VRd_A_weld'])
    kB = z0/(B['keyB_d']*(z0*D - D**2/2)); r['VRd_B_bearing'] = FCD/kB/1e3
    WB = B['keyB_d']**3/6; r['MRd_B'] = WB*B['keyB_fy']/1e6; r['VRd_B_bending'] = r['MRd_B']/(LEVER/1e3); r['VRd_B_weld'] = weld_res(8)*math.pi*B['keyB_d']
    r['VRd_B_edge250'] = V_edge_key(250, B['keyB_d']); r['VRd_B'] = min(r['VRd_B_bearing'], r['VRd_B_bending'], r['VRd_B_weld'], r['VRd_B_edge250'])
    r['VRd_A_par55'] = 2*V_edge_key(55, B['keyA_b'])               # Key A parallel to an edge 100 mm from the column centre
    r['VRd_A_edge255'] = V_edge_key(255, B['keyA_b'])              # B2 key pair outward, c1 = 300 - 45
    col = sec('HEA 160'); cc = B['tp']*math.sqrt(FY/(3*FJD)); r['c'] = cc
    r['Aeff'] = min(B['bp'], col['h'] + 2*cc)*min(B['lp'], col['b'] + 2*cc) - max(0, col['h'] - 2*col['tf'] - 2*cc)*max(0, col['b'] - col['tw'] - 2*cc)
    r['NRd_bearing'] = r['Aeff']*FJD/1e3
    mm = B['sy']/2 - col['b']/2 - 0.8*6; leff = min(2*math.pi*mm, B['sx'] + 4*mm, B['bp'])
    Mpl = 0.25*leff*B['tp']**2*FY/1e3; r['FT1_row'] = 4*Mpl/mm; r['m_plate'] = mm
    r['Mpl_plate_strip'] = 300*B['tp']**2/4*FY/1e6
    r['VRd_saddle_bearing'] = 400*150*FCD/1e3; r['MRd_saddle'] = 400*B['saddle_t']**2/4*FY/1e6; r['VRd_saddle'] = min(r['VRd_saddle_bearing'], r['MRd_saddle']/0.075)
    # B2 lever: row at b2_row, tip bearing at b2_tip -> T = N * tip/(tip - row), C = T - N
    r['b2_k'] = B['b2_tip']/(B['b2_tip'] - B['b2_row']); r['b2_FtRd'] = B['b2_bolt_FtRd']
    r['b2_C_bearing'] = B['b2_plate_b']*B['b2_plate_c']*FJD/1e3          # tip bearing strip 350 x 60 at 10 MPa
    r['b2_MRd'] = B['b2_MRd_plate']                                        # stiffened plate section (2 x 120x10 + 350x30), plastic
    r['b2_underplate'] = 400*200*FJD/1e3
    # P (K21): 4 M16 h_ef 400 in the 200 mm pier: cone limited by the two pier faces at 65 mm, bond
    cgp = cone_group((65, 65, 400, 400), hef=B['p_hef'], sx=B['p_sx'], sy=B['sy']); r['p_NRd_c'] = cgp['NRd']; r['p_cone'] = cgp
    r['p_NRd_p'] = 4*math.pi*B['p_d']*B['p_hef']*A['tau']/1e3*min(1.0, (65 + B['p_sx'] + 65)*(300 + B['sy'] + 300)/ (min(7.3*B['p_d']*math.sqrt(A['tau']), 3*B['p_hef']))**2)/A['gMp']
    r['p_NRd_s'] = 4*0.9*800*157/1.4/1e3
    r['p_links'] = 4*28.3*435/1e3      # 2 dia6 links (4 legs) crossing the splitting plane over the 400 mm lap, f_yd 435
    return r

def required_zone(Nt, e_along, e_across, B=BASE):
    if Nt <= 0: return 0
    for z in range(400, 1001, 50):
        h = z/2; cg = cone_group((h - B['sx']/2, h - B['sx']/2, h - B['sy']/2, h - B['sy']/2))
        if cg['NRd']/(1 + 2*e_along/cg['scr'])/(1 + 2*e_across/cg['scr']) >= Nt: return z
    return 9999

def group_extents(edges, orient, zone=BASE['zone']):
    """Available solid concrete beyond the anchor rows (mm) from the real edges: (across-, across+, along-, along+)."""
    h = zone/2
    if orient == 'x': ac = ('-y', '+y'); al = ('-x', '+x')
    else: ac = ('-x', '+x'); al = ('-y', '+y')
    ex = []
    for k in ac: ex.append(min(h, edges[k]*1000) - BASE['sx']/2)
    for k in al: ex.append(min(h, edges[k]*1000) - BASE['sy']/2)
    return tuple(max(v, 0.0) for v in ex)

def b2_layout(edges, orient):
    """Rev 4 B2 geometry from the real edges (m). Bolts and keys >= 300 mm from every slab edge. Returns dict with
    bolts [(x,y)], keys [(x,y)] (mm from the column centre), lever c (bolt centroid distance), tip b, plate extents."""
    lim = {k: edges[k]*1000 for k in edges}
    lo_x, hi_x = -(lim['-x'] - 300), lim['+x'] - 300; lo_y, hi_y = -(lim['-y'] - 300), lim['+y'] - 300
    def place(lo, hi, want):        # two points 'want' = (p1, p2) shifted into [lo, hi]
        p1, p2 = want; s = p2 - p1
        if p1 < lo: p1, p2 = lo, lo + s
        if p2 > hi: p2, p1 = hi, hi - s
        return p1, p2
    # primary (across) edge = nearest edge; the bolt row and key line sit 250 / 200 inboard of the column across it
    near = min(edges, key=edges.get)
    if near[1] == 'y':
        sgn = -1 if near == '+y' else 1
        by = sgn*250; ky = sgn*200
        by = max(lo_y, min(hi_y, by)); ky = max(lo_y, min(hi_y, ky))
        bx = place(lo_x, hi_x, (-140, 140)); kx = place(lo_x, hi_x, (-300, 300))
        bolts = [(bx[0], by), (bx[1], by)]; keys = [(kx[0], ky), (kx[1], ky)]
    else:
        sgn = -1 if near == '+x' else 1
        bx = sgn*250; kx = sgn*200
        bx = max(lo_x, min(hi_x, bx)); kx = max(lo_x, min(hi_x, kx))
        by = place(lo_y, hi_y, (-140, 140)); ky = place(lo_y, hi_y, (-300, 300))
        bolts = [(bx, by[0]), (bx, by[1])]; keys = [(kx, ky[0]), (kx, ky[1])]
    cx = 0.5*(bolts[0][0] + bolts[1][0]); cy = 0.5*(bolts[0][1] + bolts[1][1]); cc = math.hypot(cx, cy)
    return dict(bolts=bolts, keys=keys, c=cc, b=cc + 180, dirn=(cx/cc, cy/cc) if cc > 1 else (0, 1), near=near)

def b2_check(N, Vx, Vy, edges, lay, R):
    """B2 base: key pair (rigid distribution incl. torque) and through-bolt lever. Returns (utils dict, Nmax, M_along, M_across)."""
    u = {}
    k1, k2 = lay['keys']; xc, yc = 0.5*(k1[0]+k2[0]), 0.5*(k1[1]+k2[1])
    T = yc*Vx - xc*Vy                              # torque of the load (at the column) about the pair centroid, kN mm
    rr = sum((k[0]-xc)**2 + (k[1]-yc)**2 for k in (k1, k2))
    worst_bear = worst_edge = 0.0
    for k in (k1, k2):
        Rx = Vx/2 + T*(-(k[1]-yc))/rr; Ry = Vy/2 + T*(k[0]-xc)/rr      # reaction the key applies to the concrete
        worst_bear = max(worst_bear, math.hypot(Rx, Ry)/R['VRd_A'])
        for d, comp, pos in (('+x', Rx, k[0]), ('-x', -Rx, -k[0]), ('+y', Ry, k[1]), ('-y', -Ry, -k[1])):
            dist = edges[d]*1000 - pos - BASE['keyA_b']/2
            if comp > 3.0 and dist < 555:
                worst_edge = max(worst_edge, comp/V_edge_key(dist, BASE['keyA_b']))
    u['B2 key pair bearing'] = worst_bear
    if worst_edge > 0: u['B2 key pair outward (c1 >= 255)'] = worst_edge
    Vk = math.hypot(Vx, Vy); Mk = Vk*LEVER/1e3
    Nmax = 0.0
    if N >= 0: u['bearing'] = N/R['NRd_bearing']
    else:
        Nt = -N; kk = lay['b']/(lay['b'] - lay['c']); Tt = kk*Nt; C = Tt - Nt
        Tb = Tt/2 + Mk/(2*0.28); Nmax = Tb
        u['B2 through-bolt tension (lever %.2f, %.0f kN each)' % (kk, Tb)] = Tb/R['b2_FtRd']
        u['B2 tip bearing (%.0f kN)' % C] = C/R['b2_C_bearing']
        u['B2 stiffened plate (M %.0f kNm)' % (Nt*lay['c']/1e3 + Mk)] = (Nt*lay['c']/1e3 + Mk)/R['b2_MRd']
        u['B2 under-slab plate bearing'] = Tt/R['b2_underplate']
    return u, Nmax, Mk

def base_check(N, V, Vcross, edges, R=None, orient='x', keyB=(), btype='B1', zone=None):
    """One base, one load case. btype 'B1' | 'B2' | 'P'. Returns utilisations and the key/anchor actions."""
    from model import NEAR_EDGE
    R = R or anchor_resistances()
    u = {}; Vx, Vy = V
    comps = {'+x': Vx + Vcross[0], '-x': -Vx + Vcross[0], '+y': Vy + Vcross[1], '-y': -Vy + Vcross[1]}
    Ax = abs(Vx) + Vcross[0]; Ay = abs(Vy) + Vcross[1]
    along = Ax if orient == 'x' else Ay; across = Ay if orient == 'x' else Ax
    outdirs = [k for k in ('+x', '-x', '+y', '-y') if edges[k] < NEAR_EDGE]
    Vt = math.hypot(Ax, Ay); VB = {}; Nmax = 0.0; psi = 1.0; zreq = 0; M_along = M_across = 0.0
    if btype == 'B2':
        lay = b2_layout(edges, orient)
        u, Nmax, Mk = b2_check(N, Vx + (Vcross[0] if Vx >= 0 else -Vcross[0]), Vy + (Vcross[1] if Vy >= 0 else -Vcross[1]), edges, lay, R)
        M_along = Mk; M_across = 0.0
    elif btype == 'P':
        u['saddle plates (N-S)'] = Ay/R['VRd_saddle']
        M_along = Ay*0.075; M_across = Ax*LEVER/1e3
        if N >= 0: u['bearing'] = N/R['NRd_bearing']
        else:
            Nt = -N; Nmax = Nt/4 + M_along/(2*0.28)
            u['P pier anchors: splitting of the 200 pier restrained by the dia6/200 links (49 kN)'] = (Nt + M_along/0.28)/R['p_links']
            u['P pier anchors bond (h_ef 400)'] = Nt/R['p_NRd_p']; u['P anchor steel M16'] = Nmax/(R['p_NRd_s']/4)
    else:   # B1
        VB = {k: max(comps[k], 0.0) for k in keyB}
        for k, v in VB.items():
            if k[1] == 'x': Ax = max(Ax - v, 0.0)
            else: Ay = max(Ay - v, 0.0)
        along = Ax if orient == 'x' else Ay; across = Ay if orient == 'x' else Ax
        u['Key A SHS bearing'] = math.hypot(along, across)/R['VRd_A']
        # parallel-to-edge breakout at Key A for the components running along an edge closer than 0.6 m
        for k in ('+x', '-x', '+y', '-y'):
            if edges[k] < 0.60:
                par = Ay if k[1] == 'x' else Ax
                if par > 3.0:
                    c1 = edges[k]*1000 - BASE['keyA_b']/2
                    u['Key A parallel to edge %s (c1 %.0f)' % (k, c1)] = par/(2*V_edge_key(c1, BASE['keyA_b']))
        M_along = along*LEVER/1e3; M_across = across*LEVER/1e3
        for k, v in VB.items():
            if v > 0.5:
                u['Key B outward %s (c1 250)' % k] = v/R['VRd_B']
                if k[1] == ('x' if orient == 'x' else 'y'): M_along += v*LEVER/1e3
                else: M_across += v*LEVER/1e3
        for k, v in comps.items():
            if k in keyB or v <= 3.0: continue
            if NEAR_EDGE <= edges[k] < 0.60:
                c1 = edges[k]*1000 - BASE['keyA_b']/2; u['Key A towards edge %s (c1 %.0f)' % (k, c1)] = v/V_edge_key(c1, BASE['keyA_b'])
            elif edges[k] < NEAR_EDGE: u['UNRESOLVED outward %s' % k] = 9.9
        if N >= 0: u['bearing'] = N/R['NRd_bearing']
        else:
            Nt = -N; cg = cone_group(group_extents(edges, orient, zone or BASE['zone']))
            e1 = M_along/Nt*1e3; e2 = M_across/Nt*1e3; psi = 1/(1 + 2*e1/cg['scr'])/(1 + 2*e2/cg['scr'])
            u['anchor group cone, real edges (N_Rd,c %.0f, psi_ec %.2f)' % (cg['NRd'], psi)] = Nt/(cg['NRd']*psi)
            u['anchor group bond'] = Nt/R['NRd_p']
            Nmax = Nt/4 + M_along/(2*BASE['sy']/1e3) + M_across/(2*BASE['sx']/1e3)
            u['anchor steel (max anchor %.0f kN)' % Nmax] = Nmax/R['NRd_s']
            u['plate T-stub'] = (Nt/2 + M_along/(BASE['sy']/1e3))/R['FT1_row']
            zreq = required_zone(Nt, e1, e2)
        u['plate strip at key moment'] = (M_along + M_across)/R['Mpl_plate_strip']
    return dict(util=u, umax=max(u.values()), gov=max(u, key=u.get), Vt=Vt, VB=VB, along=along, across=across,
                M_along=M_along, M_across=M_across, psi_ec=psi, Nmax=Nmax, zreq=zreq)

def gusset_bolts(T):
    """Bracing gusset: single L70x7 with 2 M20 in single shear on a 10 mm gusset, e2 = 30 (review F14)."""
    Fb_g = bearing(10, 40, 110, 30); Fb_a = bearing(7, 40, 110, 30)
    return dict(bolt_shear=T/(2*BOLT['FvRd']), bearing_gusset=T/(2*Fb_g), bearing_angle=T/(2*Fb_a))

if __name__ == '__main__':
    R = anchor_resistances(); print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in R.items() if k != 'p_cone'})
    print(group_extents({'+x': 9, '-x': 0.1, '+y': 9, '-y': 9}, 'y'), cone_group(group_extents({'+x': 9, '-x': 0.1, '+y': 9, '-y': 9}, 'y'))['NRd'])
    for e in ({'+x': 9, '-x': 0.1, '+y': 9, '-y': 9}, {'+x': 0.2, '-x': 9, '+y': 9, '-y': 0.1}, {'+x': 0.11, '-x': 9, '+y': 9, '-y': 0.3}):
        print(b2_layout(e, 'x'))
    print(base_check(-62, (-63.7, 0), (0, 0), {'+x': 0.2, '-x': 9, '+y': 9, '-y': 0.1}, R, 'x', (), 'B2'))

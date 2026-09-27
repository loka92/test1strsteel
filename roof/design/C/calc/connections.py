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

# ---- base plate and anchors, Rev 3 (base re-review R1-R7) --------------------------------------------------------
# Plate 300 x 400 x 25 S275 (extended inboard to 350 across at near-edge bases) on 25 mm non-shrink grout.
# 4 M20 8.8 resin anchors at 80 x 280 (280 along the concrete column's long axis), h_ef = 200 IN THE SLAB ONLY,
# 26 mm clearance holes (tension only). Tension: steel, bond (tau_Rk 10 cracked) and cone (h_ef 200, k 7.2 cracked) in the
# slab solid zone (size Z, 800 assumed, boundary = free edges), eccentricity psi_ec,N from the key moments.
# Shear: Key A = SHS 90x90x8 S355 stub, 180 embedded, under the column centre in a 140 mm cored pocket 200 deep
# (along-axis and inward shear; 25 mm compressible strip on the outboard face at near-edge bases so it takes no outward
# shear). Key B = 60 mm round bar S355 (f_y 335)
# 180 embedded in a 90 pocket 200 deep, 180 mm inboard of the column centre on the outward axis, c1 >= 250 to the edge,
# for the outward shear at near-edge bases. Nothing is drilled into the column head.
BASE = dict(bp=300, lp=400, tp=25, sx=80, sy=280, hef=200, fck=25, zone=800, slab=250, grout=25,
            keyA_b=90, keyA_Wpl=75.0e3, keyA_fy=355.0, keyA_core=140, keyB_d=60, keyB_fy=335.0, emb=180, pocket=200, keyB_off=180, saddle_t=15)
ANCH = dict(NRk_s=196.0, gMc=1.5, gMs=1.4, gMp=1.5, tau=10.0, d=20, k_cr=7.2)
FJD = 10.0          # MPa bearing under the grout (0.6 f_cd, basis)
FCD = 25/1.5
LEVER = BASE['grout'] + BASE['emb']/3      # 85 mm: key shear resultant below the plate (triangular bearing in the pocket)

def V_edge_key(c1, d_nom, lf=BASE['emb'], h=BASE['slab'], fck=BASE['fck'], side=None):
    """EN 1992-4 7.2.2.5 concrete edge breakout (cracked, k9 = 1.7) for a stiff element of width d_nom loaded
    towards a free edge at c1 (mm), design value (kN). side = distance to a side edge (solid-zone boundary) or None."""
    if c1 <= 0: return 0.0
    al = 0.1*(lf/c1)**0.5; be = 0.1*(d_nom/c1)**0.2
    V0 = 1.7*d_nom**al*lf**be*math.sqrt(fck)*c1**1.5/1e3
    A0 = 4.5*c1**2
    w = 3*c1 if side is None else min(3*c1, 1.5*c1 + side)
    Ac = w*min(1.5*c1, h)
    psi_h = math.sqrt(1.5*c1/h) if 1.5*c1 > h else 1.0
    psi_s = 1.0 if side is None else min(1.0, 0.7 + 0.3*side/(1.5*c1))
    return V0*Ac/A0*psi_h*psi_s/ANCH['gMc']

def cone_group(zone, B=BASE, A=ANCH):
    """Concrete cone of the 4-anchor group in a solid zone 'zone' x 'zone' (mm), h_ef 200, cracked. Returns dict."""
    hef = B['hef']; N0 = A['k_cr']*math.sqrt(B['fck'])*hef**1.5/1e3
    scr = 3*hef; ccr = 1.5*hef
    cx = min((zone - B['sy'])/2, ccr); cy = min((zone - B['sx'])/2, ccr)
    Ac = (cx + B['sy'] + cx)*(cy + B['sx'] + cy); ratio = Ac/scr**2
    psi_s = min(1.0, 0.7 + 0.3*min(cx, cy)/ccr)
    return dict(N0=N0, ratio=ratio, psi_s=psi_s, NRk=N0*ratio*psi_s, NRd=N0*ratio*psi_s/A['gMc'], scr=scr, cx=cx, cy=cy)

def anchor_resistances(zone=BASE['zone'], B=BASE, A=ANCH):
    r = {}
    r['NRd_s'] = A['NRk_s']/A['gMs']
    cg = cone_group(zone); r.update(N0c=cg['N0'], ratio_c=cg['ratio'], psi_s=cg['psi_s'], NRk_cg=cg['NRk'], NRd_c=cg['NRd'], scr=cg['scr'])
    N0p = math.pi*A['d']*B['hef']*A['tau']/1e3
    scrp = min(7.3*A['d']*math.sqrt(A['tau']), 3*B['hef']); ccrp = scrp/2
    cxp = min((zone - B['sy'])/2, ccrp); cyp = min((zone - B['sx'])/2, ccrp)
    Ap = (cxp + B['sy'] + cxp)*(cyp + B['sx'] + cyp); ratio_p = Ap/scrp**2
    psi_sp = min(1.0, 0.7 + 0.3*min(cxp, cyp)/ccrp)
    r.update(N0p=N0p, scrp=scrp, ratio_p=ratio_p, psi_sp=psi_sp, NRk_pg=N0p*ratio_p*psi_sp, NRd_p=N0p*ratio_p*psi_sp/A['gMp'])
    r['NRd_g'] = min(4*r['NRd_s'], r['NRd_c'], r['NRd_p'])
    # Key A lug: rigid-post bearing bound (pressure linear, rotation point z0) and plate-fixed bending bound, weld
    D, h = B['emb'], B['grout']; z0 = D*(D/3 + h/2)/(D/2 + h); r['z0'] = z0
    kA = z0/(B['keyA_b']*(z0*D - D**2/2))          # p_max = V * kA  (MPa per N), rigid-post pressure distribution
    r['sigma_A'] = 1.5*FCD                          # partially loaded area, EN 1992-1-1 6.7: sqrt(A_c1/A_c0) >= 1.5 in the solid zone
    r['VRd_A_bearing'] = r['sigma_A']/kA/1e3
    r['MRd_A'] = B['keyA_Wpl']*B['keyA_fy']/1e6
    r['VRd_A_bending'] = r['MRd_A']/(LEVER/1e3)
    r['VRd_A_weld'] = weld_res(8)*4*B['keyA_b']
    r['VRd_A'] = min(r['VRd_A_bearing'], r['VRd_A_bending'], r['VRd_A_weld'])
    # Key B bar
    kB = z0/(B['keyB_d']*(z0*D - D**2/2)); r['VRd_B_bearing'] = FCD/kB/1e3
    WB = B['keyB_d']**3/6; r['MRd_B'] = WB*B['keyB_fy']/1e6; r['VRd_B_bending'] = r['MRd_B']/(LEVER/1e3)
    r['VRd_B_weld'] = weld_res(8)*math.pi*B['keyB_d']
    r['VRd_B_edge250'] = V_edge_key(250, B['keyB_d'])
    r['VRd_B'] = min(r['VRd_B_bearing'], r['VRd_B_bending'], r['VRd_B_weld'], r['VRd_B_edge250'])
    # plate
    col = sec('HEA 160'); cc = B['tp']*math.sqrt(FY/(3*FJD)); r['c'] = cc
    r['Aeff'] = min(B['bp'], col['h'] + 2*cc)*min(B['lp'], col['b'] + 2*cc) - max(0, col['h'] - 2*col['tf'] - 2*cc)*max(0, col['b'] - col['tw'] - 2*cc)
    r['NRd_bearing'] = r['Aeff']*FJD/1e3
    m = B['sy']/2 - col['b']/2 - 0.8*6; leff = min(2*math.pi*m, B['sx'] + 4*m, B['bp'])
    Mpl = 0.25*leff*B['tp']**2*FY/1e3; r['FT1_row'] = 4*Mpl/m; r['m_plate'] = m
    r['Mpl_plate_strip'] = 300*B['tp']**2/4*FY/1e6          # kNm, 300 mm strip at Key B
    # saddle (K21): two 15 mm plates 400 x 150 on the pier faces, cantilever 150, grouted
    r['VRd_saddle_bearing'] = 400*150*FCD/1e3
    r['MRd_saddle'] = 400*B['saddle_t']**2/4*FY/1e6; r['VRd_saddle'] = min(r['VRd_saddle_bearing'], r['MRd_saddle']/0.075)
    r['VRd_edge_fallback'] = V_edge_key(250, B['keyB_d'])
    return r

def required_zone(Nt, e_along, e_across, B=BASE):
    """Smallest solid zone (mm, 50 mm steps) for which the eccentric cone group carries Nt (kN)."""
    if Nt <= 0: return 0
    for z in range(400, 1001, 50):
        cg = cone_group(z)
        psi = 1/(1 + 2*e_along/cg['scr'])/(1 + 2*e_across/cg['scr'])
        if cg['NRd']*psi >= Nt: return z
    return 9999

def base_check(N, V, Vcross, edges, R=None, orient='x', keyB=(), saddle=False, zone=None):
    """One base, one load case. N (+ compression, - tension) kN; V = (Vx, Vy) signed shear on the concrete; Vcross =
    (|Vx|, |Vy|) cross-bay share (worst sign); edges = distances to free slab edges; orient = column long axis ('x'/'y');
    keyB = directions ('+x','-x','+y','-y') with a Key B; saddle = K21 detail. Returns utilisations."""
    from model import NEAR_EDGE
    R = R or anchor_resistances(zone or BASE['zone'])
    if zone: cg = cone_group(zone); NRd_c = cg['NRd']; scr = cg['scr']
    else: NRd_c = R['NRd_c']; scr = R['scr']
    u = {}; Vx, Vy = V
    comps = {'+x': Vx + Vcross[0], '-x': -Vx + Vcross[0], '+y': Vy + Vcross[1], '-y': -Vy + Vcross[1]}
    # split the shear: outward components towards a Key B direction go to Key B; the rest to Key A (or the saddle)
    VB = {k: max(comps[k], 0.0) for k in keyB}
    # Key A takes everything except the outward components assigned to a Key B
    Ax = abs(Vx) + Vcross[0]; Ay = abs(Vy) + Vcross[1]
    for k, v in VB.items():
        if k[1] == 'x': Ax = max(Ax - v, 0.0)
        else: Ay = max(Ay - v, 0.0)
    along = Ax if orient == 'x' else Ay; across = Ay if orient == 'x' else Ax
    if saddle:
        u['saddle plates (N-S)'] = Ay/R['VRd_saddle']; u['Key A (E-W)'] = Ax/R['VRd_A']
        M_along = Ay*0.075; M_across = Ax*LEVER/1e3
    else:
        u['Key A SHS bearing'] = math.hypot(along, across)/R['VRd_A']
        M_along = along*LEVER/1e3; M_across = across*LEVER/1e3      # kNm, key shear resultant 85 mm below the plate
    for k, v in VB.items():
        if v > 0.5:
            u['Key B outward %s (c1 250)' % k] = v/R['VRd_B']
            if k[1] == ('x' if orient == 'x' else 'y'): M_along += v*LEVER/1e3
            else: M_across += v*LEVER/1e3
    # Key A outward towards an edge 0.25-0.60 m away (no Key B): plain breakout with c1 = distance - lug half thickness
    for k, v in comps.items():   # outward components <= 3 kN (cross-bay torsion shares) are neglected
        if k in keyB or v <= 3.0 or (saddle and k[1] == 'y'): continue
        if NEAR_EDGE <= edges[k] < 0.60:
            c1 = edges[k]*1000 - BASE['keyA_b']/2
            u['Key A towards edge %s (c1 %.0f)' % (k, c1)] = v/V_edge_key(c1, BASE['keyA_b'])
        elif edges[k] < NEAR_EDGE: u['UNRESOLVED outward %s' % k] = 9.9
    Vt = math.hypot(abs(Vx) + Vcross[0], abs(Vy) + Vcross[1])
    # anchors
    if N >= 0:
        u['bearing'] = N/R['NRd_bearing']; psi = 1.0; e1 = e2 = 0.0; Nmax = 0.0; zreq = 0
    else:
        Nt = -N
        e1 = M_along/Nt*1e3; e2 = M_across/Nt*1e3        # mm, eccentricity of the group tension
        psi = 1/(1 + 2*e1/scr)/(1 + 2*e2/scr)
        u['anchor group cone (psi_ec %.2f)' % psi] = Nt/(NRd_c*psi)
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
    R = anchor_resistances(); print({k: round(v, 1) for k, v in R.items()})
    for z in (800, 750, 700, 600): print(z, round(cone_group(z)['NRd'], 1))
    print(base_check(-73, (-20, 40), (0, 0), {'+x': 9, '-x': 0.1, '+y': 9, '-y': 9}, R, 'y', ('-x',)))
    print(V_edge_key(250, 60), V_edge_key(285, 150), V_edge_key(205, 60))

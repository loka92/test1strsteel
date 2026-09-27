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

# ---- base plate and anchors, Rev 2 anchorage basis ----------------------------------------------------------
# Plate 300 x 400 x 25 S275 on 40 mm grout. 4 M20 8.8 resin anchors at 80 x 280 inside the concrete column core,
# drilled through the slab solid zone into the column head, h_ef = 300 (250 slab + 50 column). Tension: steel, bond
# (tau_Rk 10 MPa cracked, s_cr,Np = 7.3 d sqrt(tau)) and concrete cone in the slab solid zone (h_ef 250, k = 7.2 cracked,
# 800 x 800 zone treated as free edges). Shear: ALL shear through a central grouted shear key (60 mm round bar S355 in a
# 90 mm cored pocket 350 deep: 250 slab + 100 column head); the anchors sit in 26 mm clearance holes and take no shear.
BASE = dict(bp=300, lp=400, tp=25, sx=80, sy=280, hef=300, hef_cone=250, fck=25, zone=800, slab=250,
            key_d=60, key_fy=355.0, pocket_d=90, pocket_depth=350, key_bearing_depth=250)
ANCH = dict(NRk_s=196.0, VRk_s=98.0, gMc=1.5, gMs=1.4, gMp=1.5, tau=10.0, d=20, k_cr=7.2)
V_RD_EDGE = 60.0   # kN: key shear towards a free edge closer than 0.25 m, carried by the column cage (3 dia14 dowels
                   # at 50 % + one dia6 stirrup, f_yd 435): 3 x 0.5 x 21.7 + 24 = 57 -> 60 kN with the rebar scan (bases_C.md)
FJD = 10.0         # MPa bearing under the grout (0.6 f_cd, basis)

def anchor_resistances(B=BASE, A=ANCH):
    """Design resistances of the 4-anchor group (kN) per EN 1992-4 with the basis values."""
    r = {}
    r['NRd_s'] = A['NRk_s']/A['gMs']
    # concrete cone in the slab solid zone
    hef = B['hef_cone']; N0c = A['k_cr']*math.sqrt(B['fck'])*hef**1.5/1e3
    scr = 3*hef; ccr = 1.5*hef
    cx = min((B['zone'] - B['sy'])/2, ccr); cy = min((B['zone'] - B['sx'])/2, ccr)
    AcN = (cx + B['sy'] + cx)*(cy + B['sx'] + cy); ratio_c = AcN/scr**2
    psi_s = min(1.0, 0.7 + 0.3*min(cx, cy)/ccr)
    r.update(N0c=N0c, ratio_c=ratio_c, psi_s=psi_s, NRk_cg=N0c*ratio_c*psi_s)
    r['NRd_c'] = r['NRk_cg']/A['gMc']
    # bond (pull-out) over the full embedment
    N0p = math.pi*A['d']*B['hef']*A['tau']/1e3
    scrp = min(7.3*A['d']*math.sqrt(A['tau']), 3*B['hef']); ccrp = scrp/2
    cxp = min((B['zone'] - B['sy'])/2, ccrp); cyp = min((B['zone'] - B['sx'])/2, ccrp)
    ApN = (cxp + B['sy'] + cxp)*(cyp + B['sx'] + cyp); ratio_p = ApN/scrp**2
    psi_sp = min(1.0, 0.7 + 0.3*min(cxp, cyp)/ccrp)
    r.update(N0p=N0p, scrp=scrp, ratio_p=ratio_p, psi_sp=psi_sp, NRk_pg=N0p*ratio_p*psi_sp)
    r['NRd_p'] = r['NRk_pg']/A['gMp']
    r['NRd_g'] = min(4*r['NRd_s'], r['NRd_c'], r['NRd_p'])
    # shear key: bearing (triangular over the slab depth), bending at the plate, weld
    d = B['key_d']; hb = B['key_bearing_depth']
    fcd = B['fck']/1.5
    r['VRd_key_bearing'] = fcd*d*hb/2/1e3                        # sigma_max = 2V/(d hb) <= f_cd
    lever = hb/3 + 40 + 10                                         # grout + plate half... to the weld at the plate
    Wpl = d**3/6; r['MRd_key'] = Wpl*B['key_fy']/1e6              # kNm
    r['VRd_key_bending'] = r['MRd_key']/(lever/1e3)
    r['VRd_key_weld'] = weld_res(8)*math.pi*d                    # a = 8 all round
    r['VRd_key'] = min(r['VRd_key_bearing'], r['VRd_key_bending'], r['VRd_key_weld'])
    r['VRd_edge'] = V_RD_EDGE
    # plate: effective bearing area under compression, T-stub under uplift
    col = sec('HEA 160'); cc = B['tp']*math.sqrt(FY/(3*FJD))
    r['c'] = cc
    r['Aeff'] = min(B['bp'], col['h'] + 2*cc)*min(B['lp'], col['b'] + 2*cc) - max(0, col['h'] - 2*col['tf'] - 2*cc)*max(0, col['b'] - col['tw'] - 2*cc)
    r['NRd_bearing'] = r['Aeff']*FJD/1e3
    m = B['sy']/2 - col['b']/2 - 0.8*6; leff = min(2*math.pi*m, B['sx'] + 4*m, B['bp'])
    Mpl = 0.25*leff*B['tp']**2*FY/1e3; r['FT1_row'] = 4*Mpl/m; r['m_plate'] = m
    return r

def base_check(N, V, Vcross, edges, R=None):
    """One base, one load case. N: axial (+ compression, - tension) kN; V: (Vx, Vy) signed shear on the concrete;
    Vcross: (|Vx|, |Vy|) unsigned shear from cross bays (applied with the worst sign); edges: {'+x','-x','+y','-y'}
    distances (m) from the column centre to a free slab edge. Returns utilisations."""
    from model import NEAR_EDGE
    R = R or anchor_resistances()
    u = {}
    if N >= 0: u['bearing'] = N/R['NRd_bearing']
    else:
        u['anchor tension (cone governs)'] = -N/R['NRd_g']; u['plate T-stub'] = (-N/2)/R['FT1_row']
    Vx, Vy = V; Vt = math.hypot(abs(Vx) + Vcross[0], abs(Vy) + Vcross[1])
    u['key shear'] = Vt/R['VRd_key']
    # components towards near edges
    worst = 0.0; which = ''
    for k, comp in (('+x', Vx + Vcross[0]), ('-x', -Vx + Vcross[0]), ('+y', Vy + Vcross[1]), ('-y', -Vy + Vcross[1])):
        if edges[k] < NEAR_EDGE and comp > 0:
            if comp/R['VRd_edge'] > worst: worst = comp/R['VRd_edge']; which = k
    if which: u['edge shear %s (cage)' % which] = worst
    return dict(util=u, umax=max(u.values()), gov=max(u, key=u.get), Vt=Vt)

def gusset_bolts(T):
    """Bracing gusset: single L70x7 with 2 M20 in single shear on a 10 mm gusset, e2 = 30 (review F14)."""
    Fb_g = bearing(10, 40, 110, 30); Fb_a = bearing(7, 40, 110, 30)
    return dict(bolt_shear=T/(2*BOLT['FvRd']), bearing_gusset=T/(2*Fb_g), bearing_angle=T/(2*Fb_a))

if __name__ == '__main__':
    R = anchor_resistances(); print({k: round(v, 1) for k, v in R.items()})
    print(base_check(-80, (0, 40), (3, 0), {'+x': 9, '-x': 0.1, '+y': 9, '-y': 9}))

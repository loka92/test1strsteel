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

def cap_plate(N_t, V_h, tp=20, gauge=90, pitch=140, tf_beam=11.5, tw_beam=7.5):
    """Column cap plate 200x240x20 welded to HEA 160 (a=6 all round); primary bolted with 4 M20 through its
    bottom flange. Tension from uplift N_t (kN) and horizontal chord/strut force V_h (kN)."""
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

# ---- base plate and anchors (EN 1992-4 with the basis values) ------------------------------------------------
BASE = dict(bp=300, lp=400, tp=20, sx=200, sy=300, hef=170, fck=25, zone=800, slab=250)
ANCH = dict(NRk_s=196.0, NRk_c0=80.0, NRk_p0=107.0, VRk_s=98.0, gMc=1.5, gMs=1.4, tau=10.0, d=20)

def base_plate(N_c, N_t, V, B=BASE):
    """Bearing on grout (0.6 f_cd = 10 MPa), plate bending under compression (effective-area method) and
    under uplift (T-stub cantilever from the column flange to the anchor row), 4 M20 resin anchors group."""
    u = {}
    col = sec('HEA 160')
    fjd = 10.0
    c = B['tp']*math.sqrt(FY/(3*fjd*1.0))                     # cantilever width (EN 1993-1-8 6.2.5)
    Aeff = min(B['bp'], col['b'] + 2*c)*min(B['lp'], col['h'] + 2*c) - max(0, (col['h'] - 2*col['tf'] - 2*c))*max(0, (col['b'] - col['tw'] - 2*c))
    u['bearing (grout/slab)'] = N_c/(Aeff*fjd/1e3)
    # uplift: anchors at +-sy/2 = 150 from centre, flange face at h/2 = 76 -> m = 150-76-0.8*6
    m = B['sy']/2 - col['h']/2 - 0.8*6; leff = min(2*math.pi*m, 4*m + 1.25*50, B['bp'])
    Mpl = 0.25*leff*B['tp']**2*FY/1e3; FT1 = 4*Mpl/m          # per anchor pair (mode 1)
    u['plate bending (uplift)'] = (N_t/2)/FT1
    # --- anchors: tension
    NEd_a = N_t/4
    NRd_s = ANCH['NRk_s']/ANCH['gMs']
    scr = 3*B['hef']; ccr = scr/2
    cedge = (B['zone'] - max(B['sx'], B['sy']))/2.0            # distance from the outer anchors to the solid-zone edge
    c1 = min(cedge, ccr)
    AcN = (c1 + B['sy'] + c1)*(min((B['zone']-B['sx'])/2, ccr) + B['sx'] + min((B['zone']-B['sx'])/2, ccr))
    ratio_c = AcN/scr**2; psi_s = min(1.0, 0.7 + 0.3*c1/ccr)
    NRk_cg = ANCH['NRk_c0']*ratio_c*psi_s
    NRd_c = NRk_cg/ANCH['gMc']
    scrp = min(20*ANCH['d']*math.sqrt(ANCH['tau']/7.5), scr); ccrp = scrp/2
    c1p = min(cedge, ccrp)
    ApN = (c1p + B['sy'] + c1p)*(min((B['zone']-B['sx'])/2, ccrp) + B['sx'] + min((B['zone']-B['sx'])/2, ccrp))
    NRd_p = ANCH['NRk_p0']*ApN/scrp**2*min(1.0, 0.7 + 0.3*c1p/ccrp)/ANCH['gMc']
    NRd_g = min(4*NRd_s, NRd_c, NRd_p)
    u['anchor tension steel'] = NEd_a/NRd_s
    u['anchor group cone'] = N_t/NRd_c
    u['anchor group bond'] = N_t/NRd_p
    # --- anchors: shear (4 anchors, holes 22 mm with washers welded after fit-up so all 4 act)
    VRd_s = ANCH['VRk_s']/ANCH['gMs']; u['anchor shear steel'] = V/4/VRd_s
    VRd_cp = 2*NRk_cg/ANCH['gMc']; u['anchor pry-out'] = V/VRd_cp
    # concrete edge failure towards the solid-zone edge (treated as a free edge - conservative, see open items)
    c1v = cedge; lf = B['hef']; d = ANCH['d']
    al = 0.1*(lf/c1v)**0.5; be = 0.1*(d/c1v)**0.2
    V0 = 2.4*d**al*lf**be*math.sqrt(B['fck'])*c1v**1.5/1e3       # kN, uncracked k9 = 2.4
    AcV0 = 4.5*c1v**2
    AcV = min(3*c1v + B['sx'], B['zone'])*min(1.5*c1v, B['slab'])
    psi_h = math.sqrt(1.5*c1v/B['slab'])
    VRd_c = V0*AcV/AcV0*psi_h/ANCH['gMc']
    u['anchor group edge'] = V/VRd_c
    uN = max(u['anchor tension steel'], u['anchor group cone'], u['anchor group bond'])
    uV = max(u['anchor shear steel'], u['anchor pry-out'], u['anchor group edge'])
    u['N-V interaction'] = uN**1.5 + uV**1.5
    return dict(util=u, umax=max(u.values()), gov=max(u, key=u.get), NRd_g=NRd_g, NRd_c=NRd_c, NRd_p=NRd_p, VRd_c=VRd_c,
                VRd_cp=VRd_cp, Aeff=Aeff, ratio_c=ratio_c, cedge=cedge)

def gusset_bolts(T):
    """Bracing gusset: single L70x7 with 2 M20 in single shear on a 10 mm gusset."""
    Fb_g = bearing(10, 40, 110, 35); Fb_a = bearing(7, 40, 110, 35)
    return dict(bolt_shear=T/(2*BOLT['FvRd']), bearing_gusset=T/(2*Fb_g), bearing_angle=T/(2*Fb_a))

if __name__ == '__main__':
    print(fin_plate(30, 2, 6.6)); print(fin_plate(45, 3, 6.6)); print(cap_plate(70, 55)); 
    b = base_plate(100, 75, 74); print(b)

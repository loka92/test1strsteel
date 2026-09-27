"""Hot-rolled section properties (standard European tables), S275.
Units: mm, cm2, cm4, cm3, cm6, kg/m.  Av = shear area (rolled, EN 1993-1-1 6.2.6)."""
FY = 275.0      # MPa (t <= 16 mm)
FU = 430.0      # MPa
E = 210000.0    # MPa
G = 81000.0     # MPa
GM0, GM1, GM2 = 1.0, 1.0, 1.25

# h, b, tw, tf, A, Iy, Wpl_y, iy, Iz, Wpl_z, iz, It, Iw(1e3 cm6), Av, g
_T = {
 'IPE 200': (200,100,5.6, 8.5, 28.5, 1943, 220.6, 8.26, 142.4, 44.6, 2.24, 6.98, 12.99, 14.0, 22.4),
 'IPE 220': (220,110,5.9, 9.2, 33.4, 2772, 285.4, 9.11, 204.9, 58.1, 2.48, 9.07, 22.67, 15.9, 26.2),
 'IPE 240': (240,120,6.2, 9.8, 39.1, 3892, 366.6, 9.97, 283.6, 73.9, 2.69, 12.88, 37.39, 19.1, 30.7),
 'IPE 270': (270,135,6.6,10.2, 45.9, 5790, 484.0,11.23, 419.9, 97.0, 3.02, 15.94, 70.58, 22.1, 36.1),
 'IPE 300': (300,150,7.1,10.7, 53.8, 8356, 628.4,12.46, 603.8,125.2, 3.35, 20.12,125.9 , 25.7, 42.2),
 'IPE 330': (330,160,7.5,11.5, 62.6,11770, 804.3,13.71, 788.1,153.7, 3.55, 28.15,199.1 , 30.8, 49.1),
 'IPE 360': (360,170,8.0,12.7, 72.7,16270,1019.0,14.95,1043.0,191.1, 3.79, 37.32,313.6 , 35.1, 57.1),
 'HEA 140': (133,140,5.5, 8.5, 31.4, 1033, 173.5, 5.73, 389.3, 84.9, 3.52,  8.13, 15.06, 10.1, 24.7),
 'HEA 160': (152,160,6.0, 9.0, 38.8, 1673, 245.1, 6.57, 615.6,117.6, 3.98, 12.19, 31.41, 13.2, 30.4),
 'HEA 180': (171,180,6.0, 9.5, 45.3, 2510, 324.9, 7.45, 924.6,156.5, 4.52, 14.80, 60.21, 14.5, 35.5),
 'HEA 200': (190,200,6.5,10.0, 53.8, 3692, 429.5, 8.28,1336.0,203.8, 4.98, 20.98,108.0 , 18.1, 42.3),
}
KEYS = ('h','b','tw','tf','A','Iy','Wpl_y','iy','Iz','Wpl_z','iz','It','Iw','Av','g')

def sec(name):
    d = dict(zip(KEYS, _T[name])); d['name'] = name
    d['Iw'] *= 1e3
    d['Mpl_y'] = d['Wpl_y']*FY/1e3/GM0     # kNm
    d['Mpl_z'] = d['Wpl_z']*FY/1e3/GM0
    d['Npl']   = d['A']*FY/10/GM0          # kN
    d['Vpl']   = d['Av']*FY/10/3**0.5/GM0  # kN
    d['w']     = d['g']*9.81/1000          # kN/m self weight
    return d

def chi(lam, curve):
    """EN 1993-1-1 6.3.1.2 reduction factor."""
    a = {'a0':0.13,'a':0.21,'b':0.34,'c':0.49,'d':0.76}[curve]
    phi = 0.5*(1+a*(lam-0.2)+lam**2)
    return min(1.0, 1/(phi+(phi**2-lam**2)**0.5))

def Mcr(s, L, C1=1.0):
    """Elastic critical moment, doubly symmetric I, fork ends, load at shear centre (kNm). L in m."""
    import math
    Lm = L*1000
    EIz = E*s['Iz']*1e4; GIt = G*s['It']*1e4; Iw = s['Iw']*1e6
    return C1*math.pi**2*EIz/Lm**2*math.sqrt(Iw/(s['Iz']*1e4) + Lm**2*GIt/(math.pi**2*EIz))/1e6

def Mb_Rd(s, L, C1=1.0):
    """LTB resistance for a rolled I (6.3.2.3), curve b if h/b<=2 else c. Returns (Mb_Rd, chi_LT, lam_LT)."""
    import math
    if L <= 0.01: return s['Mpl_y'], 1.0, 0.0
    mcr = Mcr(s, L, C1)
    lam = math.sqrt(s['Wpl_y']*FY/1e3/mcr)
    if lam <= 0.4: return s['Mpl_y'], 1.0, lam
    curve = 'b' if s['h']/s['b'] <= 2 else 'c'
    a = {'b':0.34,'c':0.49}[curve]
    phi = 0.5*(1+a*(lam-0.4)+0.75*lam**2)
    x = min(1.0, 1/lam**2, 1/(phi+math.sqrt(phi**2-0.75*lam**2)))
    return x*s['Mpl_y']/GM1, x, lam

def Nb_Rd(s, Ly, Lz):
    """Flexural buckling resistance (kN), curves per table 6.2 (rolled H/I, tf<=40): h/b>1.2 -> a/b, else b/c."""
    import math
    lam1 = math.pi*math.sqrt(E/FY)
    if s['h']/s['b'] > 1.2: cy, cz = 'a', 'b'
    else: cy, cz = 'b', 'c'
    ly = Ly*1000/(s['iy']*10)/lam1; lz = Lz*1000/(s['iz']*10)/lam1
    xy, xz = chi(ly, cy), chi(lz, cz)
    return min(xy, xz)*s['Npl']/GM1, xy, xz, ly, lz

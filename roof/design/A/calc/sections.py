"""Hot-rolled section tables (standard European tables) and EN 1993-1-1 helpers.
Units in the tables: mm, cm2, cm4, cm3, cm, cm6 (Iw in 1e3 cm6), kg/m.
"""
import math

FY = 275.0      # MPa (t <= 16 mm)
E = 210000.0    # MPa
G = 81000.0     # MPa
EPS = math.sqrt(235 / FY)

# name: h, b, tw, tf, r, A, Iy, Wel_y, Wpl_y, iy, Iz, Wel_z, Wpl_z, iz, It, Iw(1e3 cm6), mass
_T = {
 'IPE200': (200, 100, 5.6, 8.5, 12, 28.5, 1943, 194.3, 220.6, 8.26, 142.4, 28.5, 44.6, 2.24, 6.98, 12.99, 22.4),
 'IPE220': (220, 110, 5.9, 9.2, 12, 33.4, 2772, 252.0, 285.4, 9.11, 204.9, 37.3, 58.1, 2.48, 9.07, 22.67, 26.2),
 'IPE240': (240, 120, 6.2, 9.8, 15, 39.1, 3892, 324.3, 366.6, 9.97, 283.6, 47.3, 73.9, 2.69, 12.88, 37.39, 30.7),
 'IPE270': (270, 135, 6.6, 10.2, 15, 45.9, 5790, 428.9, 484.0, 11.23, 419.9, 62.2, 97.0, 3.02, 15.94, 70.58, 36.1),
 'IPE300': (300, 150, 7.1, 10.7, 15, 53.8, 8356, 557.1, 628.4, 12.46, 603.8, 80.5, 125.2, 3.35, 20.12, 125.9, 42.2),
 'IPE330': (330, 160, 7.5, 11.5, 18, 62.6, 11770, 713.1, 804.3, 13.71, 788.1, 98.5, 153.7, 3.55, 28.15, 199.1, 49.1),
 'IPE360': (360, 170, 8.0, 12.7, 18, 72.7, 16270, 903.6, 1019, 14.95, 1043, 122.8, 191.1, 3.79, 37.32, 313.6, 57.1),
 'HEA140': (133, 140, 5.5, 8.5, 12, 31.4, 1033, 155.4, 173.5, 5.73, 389.3, 55.6, 84.9, 3.52, 8.13, 15.06, 24.7),
 'HEA160': (152, 160, 6.0, 9.0, 15, 38.8, 1673, 220.1, 245.1, 6.57, 615.6, 76.9, 117.6, 3.98, 12.19, 31.41, 30.4),
 'HEA180': (171, 180, 6.0, 9.5, 15, 45.3, 2510, 293.6, 324.9, 7.45, 924.6, 102.7, 156.5, 4.52, 14.80, 60.21, 35.5),
 'HEA200': (190, 200, 6.5, 10.0, 18, 53.8, 3692, 388.6, 429.5, 8.28, 1336, 133.6, 203.8, 4.98, 20.98, 108.0, 42.3),
 'HEA220': (210, 220, 7.0, 11.0, 18, 64.3, 5410, 515.2, 568.5, 9.17, 1955, 177.7, 270.6, 5.51, 28.46, 193.3, 50.5),
 'HEA240': (230, 240, 7.5, 12.0, 21, 76.8, 7763, 675.1, 744.6, 10.05, 2769, 230.7, 351.7, 6.00, 41.55, 328.5, 60.3),
}
_K = ['h', 'b', 'tw', 'tf', 'r', 'A', 'Iy', 'Wel_y', 'Wpl_y', 'iy', 'Iz', 'Wel_z', 'Wpl_z', 'iz', 'It', 'Iw', 'mass']


class Section(dict):
    """Section with SI-derived values: A_m2, I_m4 for the solver, plus resistances in kN, kNm."""
    def __init__(self, name):
        super().__init__(zip(_K, _T[name])); self['name'] = name
        self['Iw'] *= 1e3                                    # cm6
        self['A_m2'] = self['A'] * 1e-4; self['I_m4'] = self['Iy'] * 1e-8; self['Iz_m4'] = self['Iz'] * 1e-8
        h, b, tw, tf, r = self['h'], self['b'], self['tw'], self['tf'], self['r']
        self['hw'] = h - 2 * tf
        self['Av'] = max(self['A'] * 100 - 2 * b * tf + (tw + 2 * r) * tf, 1.0 * self['hw'] * tw)  # mm2 (6.2.6)
        self['Npl'] = self['A'] * 100 * FY / 1e3                # kN
        self['Mpl_y'] = self['Wpl_y'] * 1e3 * FY / 1e6           # kNm
        self['Mel_y'] = self['Wel_y'] * 1e3 * FY / 1e6
        self['Mpl_z'] = self['Wpl_z'] * 1e3 * FY / 1e6
        self['Vpl'] = self['Av'] * FY / math.sqrt(3) / 1e3      # kN
        self['cf'] = (b - tw - 2 * r) / 2                        # flange outstand
        self['cw'] = h - 2 * tf - 2 * r                          # web clear depth
        self['class_bending'] = self._class(alpha=0.5, psi=-1)
        self['class_compression'] = self._class(alpha=1.0, psi=1)

    def _class(self, alpha, psi):
        """EN 1993-1-1 Table 5.2. alpha = compressed part of web (plastic), psi = stress ratio (elastic)."""
        cf = self['cf'] / self['tf']; cw = self['cw'] / self['tw']
        # flange (outstand in compression)
        if cf <= 9 * EPS: kf = 1
        elif cf <= 10 * EPS: kf = 2
        elif cf <= 14 * EPS: kf = 3
        else: kf = 4
        # web
        if alpha > 0.5:
            l1, l2 = 396 * EPS / (13 * alpha - 1), 456 * EPS / (13 * alpha - 1)
        else:
            l1, l2 = 36 * EPS / alpha, 41.5 * EPS / alpha
        if psi > -1: l3 = 42 * EPS / (0.67 + 0.33 * psi)
        else: l3 = 62 * EPS * (1 - psi) * math.sqrt(-psi) if psi < -1 else 124 * EPS
        if cw <= l1: kw = 1
        elif cw <= l2: kw = 2
        elif cw <= l3: kw = 3
        else: kw = 4
        return max(kf, kw)

    def web_class_MN(self, N_Ed):
        """Class of the web under bending + compression N_Ed (kN, compression positive)."""
        # plastic neutral axis shift: alpha = 0.5 + N/(2 hw tw fy)  (limited 0..1)
        alpha = min(1.0, max(0.0, 0.5 + N_Ed * 1e3 / (2 * self['hw'] * self['tw'] * FY)))
        sig = N_Ed * 1e3 / (self['A'] * 100)
        psi = max(-1.0, -(1 - 2 * sig / FY)) if sig < FY else 1
        return self._class(alpha, psi)


def sec(name):
    return Section(name)


def haunch_props(base, factor=1.5):
    """Stepped haunched section: rafter IPE + tee cut from the same section welded below,
    total depth = factor * h. Returns dict with A_m2, I_m4, Wel (cm3, bottom fibre) and depth (mm).
    Root fillets of the cutting neglected (conservative)."""
    h, b, tw, tf = base['h'], base['b'], base['tw'], base['tf']
    H = factor * h
    # parts: (area mm2, centroid from top mm, own I mm4)
    parts = [(base['A'] * 100, h / 2, base['Iy'] * 1e4),
             (tw * (H - h - tf), h + (H - h - tf) / 2, tw * (H - h - tf)**3 / 12),
             (b * tf, H - tf / 2, b * tf**3 / 12)]
    A = sum(p[0] for p in parts); zc = sum(p[0] * p[1] for p in parts) / A
    I = sum(p[2] + p[0] * (p[1] - zc)**2 for p in parts)
    Wel = I / max(zc, H - zc)
    return dict(A_m2=A * 1e-6, I_m4=I * 1e-12, Wel=Wel / 1e3, H=H, zc=zc, Mel=Wel * FY / 1e6,
                A=A / 100, mass=A * 1e-6 * 7850)


# --------------------------- EN 1993-1-1 checks ---------------------------
def chi(lam, curve):
    a = {'a0': 0.13, 'a': 0.21, 'b': 0.34, 'c': 0.49, 'd': 0.76}[curve]
    phi = 0.5 * (1 + a * (lam - 0.2) + lam**2)
    return min(1.0, 1 / (phi + math.sqrt(max(phi**2 - lam**2, 0))))


def chi_LT(lam, curve, rolled=True):
    """6.3.2.3 for rolled sections (lambda_LT0 = 0.4, beta = 0.75) else 6.3.2.2."""
    a = {'a': 0.21, 'b': 0.34, 'c': 0.49, 'd': 0.76}[curve]
    if rolled:
        phi = 0.5 * (1 + a * (lam - 0.4) + 0.75 * lam**2)
        return min(1.0, 1 / lam**2 if lam > 0 else 1.0, 1 / (phi + math.sqrt(max(phi**2 - 0.75 * lam**2, 0))))
    phi = 0.5 * (1 + a * (lam - 0.2) + lam**2)
    return min(1.0, 1 / (phi + math.sqrt(max(phi**2 - lam**2, 0))))


def Mcr(s, L_mm, C1=1.0, kz=1.0, kw=1.0):
    """Elastic critical moment, doubly symmetric section, load through shear centre (kNm)."""
    Iz = s['Iz'] * 1e4; It = s['It'] * 1e4; Iw = s['Iw'] * 1e6
    return C1 * math.pi**2 * E * Iz / (kz * L_mm)**2 * math.sqrt((kz / kw)**2 * Iw / Iz + (kz * L_mm)**2 * G * It / (math.pi**2 * E * Iz)) / 1e6


def C1_from_psi(psi):
    """C1 for a linear moment distribution between restraints, psi = M_min/M_max (-1..1)."""
    psi = max(-1.0, min(1.0, psi))
    return min(2.7, 1.88 - 1.40 * psi + 0.52 * psi**2)


def curve_y(s):  # flexural buckling about y-y, rolled I, tf <= 40 mm
    return 'a' if s['h'] / s['b'] > 1.2 else 'b'


def curve_z(s):
    return 'b' if s['h'] / s['b'] > 1.2 else 'c'


def curve_LT(s):  # 6.3.2.3 Table 6.5 rolled
    return 'b' if s['h'] / s['b'] <= 2.0 else 'c'


def MN_Rd(s, N_Ed):
    """6.2.9.1 reduced plastic moment for class 1/2 I-section about y-y (kNm). N_Ed in kN (abs)."""
    n = abs(N_Ed) / s['Npl']
    a = min(0.5, (s['A'] * 100 - 2 * s['b'] * s['tf']) / (s['A'] * 100))
    if abs(N_Ed) <= 0.25 * s['Npl'] and abs(N_Ed) <= 0.5 * s['hw'] * s['tw'] * FY / 1e3:
        return s['Mpl_y']
    return min(s['Mpl_y'], s['Mpl_y'] * (1 - n) / (1 - 0.5 * a))


def annexB_k(s, N_Ed, chi_y, chi_z, lam_y, lam_z, Cmy, Cmz, CmLT, is_I=True):
    """Interaction factors k_yy, k_yz, k_zy, k_zz for class 1/2 I-sections (Annex B, Tables B.1/B.2)."""
    NRk_y = chi_y * s['Npl']; NRk_z = chi_z * s['Npl']
    n_y = abs(N_Ed) / NRk_y; n_z = abs(N_Ed) / NRk_z
    kyy = min(Cmy * (1 + (lam_y - 0.2) * n_y), Cmy * (1 + 0.8 * n_y))
    kzz = min(Cmz * (1 + (2 * lam_z - 0.6) * n_z), Cmz * (1 + 1.4 * n_z))
    kyz = 0.6 * kzz
    # susceptible to torsional deformation (I section, LTB possible)
    if lam_z < 0.4:
        kzy = min(0.6 + lam_z, 1 - 0.1 * lam_z * n_z / (CmLT - 0.25))
    else:
        kzy = max(1 - 0.1 * lam_z * n_z / (CmLT - 0.25), 1 - 0.1 * n_z / (CmLT - 0.25))
    return kyy, kyz, kzy, kzz


if __name__ == '__main__':
    for n in _T:
        s = sec(n)
        print('%-7s class bend %d comp %d  Mpl %.0f kNm  Vpl %.0f kN  Npl %.0f kN  Av %.0f mm2' %
              (n, s['class_bending'], s['class_compression'], s['Mpl_y'], s['Vpl'], s['Npl'], s['Av']))
    hp = haunch_props(sec('IPE300'))
    print('IPE300 haunch: H=%.0f I=%.0f cm4 Wel=%.0f cm3 Mel=%.0f kNm' % (hp['H'], hp['I_m4'] * 1e8, hp['Wel'], hp['Mel']))
    print('IPE300 Mcr L=3m C1=1: %.1f kNm' % Mcr(sec('IPE300'), 3000))

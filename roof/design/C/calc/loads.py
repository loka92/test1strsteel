"""Loads per design/load_basis.md (binding). kN, m."""
import numpy as np
from model import ENV, NOTCH, roofed

G_ROOF  = 0.12 + 0.05 + 0.20     # panel + purlins + services (kN/m2), + steel self weight from sections
G_MIN   = 0.17                   # panel + purlins only (uplift), + steel self weight
Q_ROOF  = 0.60                   # cat. H, psi0 = 0
QP      = 1.30                   # peak velocity pressure kN/m2 (z_e = 10 m)
G_WALL  = 0.30                   # kN/m2 of wall (BoardX + girts)
CPI_UP, CPI_PR = +0.2, -0.3
E_ZONE  = 20.0                   # Rev 2: e = min(b, 2h) with h above ground = 20 m -> strips e/10 = 2.0, e/4 = 5.0, e/2 = 10.0
GUTTER_G, GUTTER_W = 0.25, -0.50  # kN/m gravity / uplift on the north eave (gutter, fascia), Rev 2 (review F6)
SLOPE_SIN = 0.0598               # sin(3.43 deg): horizontal (northward) component of the roof suction

# Roof cpe (mono-pitch 5 deg, EN 1991-1-4 Table 7.3a). Basis Rev 2: theta=0 = wind from N (-1.7/-1.2/-0.6),
# theta=180 = wind from S (-2.3/-1.3/-0.8). The larger theta=180 set is kept for BOTH N and S wind (envelope,
# as agreed) with the F/G strip at the windward edge.
CPE_NS   = dict(F=-2.3, G=-1.3, H=-0.8)
CPE_EW   = dict(F=-2.1, G=-1.8, H=-0.6, I=-0.5)
CPE_WALL = dict(D=+0.8, E=-0.5, A=-1.2, B=-0.8, C=-0.5)

def cpe_roof(x, y, d):
    """Roof external pressure coefficient at (x,y) for wind from d in 'N','S','E','W'."""
    e10, e4, e2 = E_ZONE/10, E_ZONE/4, E_ZONE/2
    if d in ('N', 'S'):
        # windward edge: N: y=35.87 ; S: y=15.57 (x<77.89) and y=19.97 (x>=77.89)
        if d == 'N': dist = ENV['y1'] - y; corners = [ENV['x0'], ENV['x1']]
        else:
            if x < NOTCH['x0']: dist = y - ENV['y0']; corners = [ENV['x0'], NOTCH['x0']]
            else:               dist = y - NOTCH['y1']; corners = [NOTCH['x0'], ENV['x1']]
        if dist <= e10:
            return CPE_NS['F'] if min(abs(x-c) for c in corners) <= e4 else CPE_NS['G']
        return CPE_NS['H']
    else:
        if d == 'W': dist = x - ENV['x0']; corners = [ENV['y0'], ENV['y1']]
        else:
            if y >= NOTCH['y1']: dist = ENV['x1'] - x; corners = [NOTCH['y1'], ENV['y1']]
            else:                dist = NOTCH['x0'] - x; corners = [ENV['y0'], NOTCH['y1']]
        if dist <= e10:
            return CPE_EW['F'] if min(abs(y-c) for c in corners) <= e4 else CPE_EW['G']
        if dist <= e2: return CPE_EW['H']
        return CPE_EW['I']

def w_net_uplift(x, y, d):
    """Net roof wind pressure (kN/m2, negative = uplift) with cpi = +0.2."""
    return (cpe_roof(x, y, d) - CPI_UP)*QP
W_DOWN = (0.0 + 0.3)*QP     # pressure case: cpe +0.0 (downward zones), cpi -0.3 -> +0.39 kN/m2

def wall_cp_net(face_normal, d, dist_from_windward_corner):
    """Net wall cp (pressure positive on the wall, i.e. towards inside) for wind from d.
    Returns the worst of the pressure case (cpi -0.3) and the suction case (cpi +0.2)."""
    opp = {'N':'y+', 'S':'y-', 'E':'x+', 'W':'x-'}[d]     # normal of the windward face
    lee = {'y+':'y-', 'y-':'y+', 'x+':'x-', 'x-':'x+'}[opp]
    if face_normal == opp: cpe = CPE_WALL['D']
    elif face_normal == lee: cpe = CPE_WALL['E']
    else:
        s = dist_from_windward_corner
        cpe = CPE_WALL['A'] if s <= E_ZONE/5 else (CPE_WALL['B'] if s <= E_ZONE else CPE_WALL['C'])
    return cpe - CPI_PR if cpe > 0 else cpe - CPI_UP    # +1.1 (D), -0.7 (E), -1.4/-1.0/-0.7 (A/B/C)

def roof_grid(dx=0.1):
    xs = np.arange(ENV['x0']+dx/2, ENV['x1'], dx); ys = np.arange(ENV['y0']+dx/2, ENV['y1'], dx)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    R = np.vectorize(roofed)(X, Y)
    return X, Y, R, dx

def wind_fields(X, Y, R):
    out = {}
    for d in 'NSEW':
        f = np.vectorize(lambda x, y: w_net_uplift(x, y, d))(X, Y)
        out[d] = np.where(R, f, 0.0)
    return out

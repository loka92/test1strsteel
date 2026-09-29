"""Loads per design/load_basis.md Rev 3 (binding, supersedes Rev 2). kN, m."""
import numpy as np, os
from model import ENV, NOTCH, roofed, north_edge, NORTH_JOG_X

G_ROOF  = 0.12 + 0.05 + 0.10     # panel + purlins + services 0.10 (Rev 3), + steel self weight from sections
G_MIN   = 0.17                   # panel + purlins only (uplift), + steel self weight
Q_ROOF  = 0.40                   # cat. H, psi0 = 0 (Rev 3); Q_k 1.0 kN point for the purlin / panel-supplier check
QP_DIR  = {k: v*float(os.environ.get('QP_SCALE', '1.0')) for k, v in dict(N=1.25, S=0.75, E=1.05, W=1.05).items()}   # Rev 3: v_b 27, z_e = h = 9 m, terrain I (N, sea) / II (E, W) / III (S)
QP      = max(QP_DIR.values())   # kept for callers that need a single scalar (purlin edge check uses the direction fields)
G_WALL  = 0.0                    # Rev 3 / brief Rev 5: NO wall self-weight in G or G_min
G_WALL_SEIS = float(os.environ.get('G_WALL_SEIS', '0.30'))              # wall mass kept in the seismic mass
CPI_UP, CPI_PR = +0.2, -0.3
E_ZONE  = float(os.environ.get('E_ZONE', '18.0'))                  # Rev 3: e = min(b, 2h) = 18 m -> F/G strip 1.8 m, F corners 4.5 m, H to 9 m, I beyond
GUTTER_G, GUTTER_GMIN, GUTTER_W = 0.25, 0.10, -0.50  # kN/m gravity / in G_min / uplift on the north eave (Rev 3)
SLOPE_SIN = 0.0598               # sin(3.43 deg): horizontal (northward) component of the roof suction

# Roof cpe: FLAT ROOF (EN 1991-1-4 7.2.3, -5 < alpha < 5 deg), Table 7.2 sharp eaves, all four directions (Rev 3):
# F -1.8, G -1.2 (windward strip e/10), H -0.7 (e/10 to e/2), I -0.2 / +0.2 beyond e/2.
CPE_FLAT = dict(F=-1.8, G=-1.2, H=-0.7, I=-0.2); CPE_I_DOWN = +0.2
CPE_WALL = dict(D=+0.75, E=-0.40, A=-1.2, B=-0.8, C=-0.5)   # Rev 3: D/E at h/d 0.44
LACK_CORR = 0.85                                             # 7.2.2(3) on the D + E resultant (global force only)

def roof_zone(x, y, d):
    """Flat-roof zone letter for wind from d at (x, y)."""
    e10, e4, e2 = E_ZONE/10, E_ZONE/4, E_ZONE/2
    if d in ('N', 'S'):
        if d == 'N': dist = north_edge(x) - y; corners = [ENV['x0'], NORTH_JOG_X, ENV['x1']]
        else:
            if x < NOTCH['x0']: dist = y - ENV['y0']; corners = [ENV['x0'], NOTCH['x0']]
            else:               dist = y - NOTCH['y1']; corners = [NOTCH['x0'], ENV['x1']]
        along = x
    else:
        if d == 'W': dist = x - ENV['x0']; corners = [ENV['y0'], north_edge(x)]
        else:
            if y >= NOTCH['y1']: dist = ENV['x1'] - x; corners = [NOTCH['y1'], ENV['y1']]
            else:                dist = NOTCH['x0'] - x; corners = [ENV['y0'], NOTCH['y1']]
        along = y
    if dist <= e10: return 'F' if min(abs(along - c) for c in corners) <= e4 else 'G'
    if dist <= e2: return 'H'
    return 'I'

def cpe_roof(x, y, d):
    return CPE_FLAT[roof_zone(x, y, d)]

def w_net_uplift(x, y, d):
    """Net roof wind pressure (kN/m2, negative = uplift) with cpi = +0.2 and the direction's q_p."""
    return (cpe_roof(x, y, d) - CPI_UP)*QP_DIR[d]

def w_down(x, y, d):
    """Pressure case (ULS-2): zone I +0.2 with c_pi -0.3 -> +0.5 q_p beyond e/2 from the windward edge, else 0."""
    return (CPE_I_DOWN - CPI_PR)*QP_DIR[d] if roof_zone(x, y, d) == 'I' else 0.0
W_DOWN = (CPE_I_DOWN - CPI_PR)*QP_DIR['N']   # 0.625 kN/m2, the largest (N wind); the field is the per-cell envelope over directions

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
    return cpe - CPI_PR if cpe > 0 else cpe - CPI_UP    # +1.05 (D), -0.6 (E), -1.4/-1.0/-0.7 (A/B/C)

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

def down_field(X, Y, R):
    """Per-cell envelope of the pressure case over the four directions (zone I +0.5 q_p)."""
    f = np.zeros_like(X)
    for d in 'NSEW':
        f = np.maximum(f, np.vectorize(lambda x, y: w_down(x, y, d))(X, Y))
    return np.where(R, f, 0.0)

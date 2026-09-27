"""Load basis (binding values from ../../load_basis.md) and frame geometry for Alternative A.
Units kN, m. Frame local axis x = global y (positive NORTH), z = up.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
GEOM = json.load(open(os.path.join(HERE, '..', '..', '..', 'geometry.json')))
COLS = {c['id']: (c['cx'], c['cy']) for c in GEOM['columns']}

# ---- characteristic surface loads (kN/m2) ----
G_PANEL, G_PURLIN, G_SERV = 0.12, 0.05, 0.20
G_ROOF = G_PANEL + G_PURLIN + G_SERV          # 0.37
G_ROOF_MIN = G_PANEL + G_PURLIN               # 0.17 (uplift combinations)
G_WALL = 0.30                                  # kN/m2 of wall (BoardX + girts)
Q_ROOF = 0.60
QP = 1.30                                      # peak velocity pressure
CPI = {'p': +0.2, 'm': -0.3}
CPE_WALL_D, CPE_WALL_E, CPE_WALL_SIDE = 0.8, -0.5, -0.8   # windward, leeward, side (zone B average)
# roof cpe (Table 7.3a, 5 deg): zones by distance from the windward edge (e/10 = 1.2 m -> F or G, then H)
E_ZONE = 12.0
ROOF_CPE = {'N': dict(F=-2.3, G=-1.3, H=-0.8), 'S': dict(F=-1.7, G=-1.2, H=-0.6)}
# along-ridge wind (theta = 90): governing zone per frame (see report 2.3). Gable frames: area-weighted
# over their 2.2 m strip (1.2 m of G -1.8 + 1.0 m of H -0.6 -> -1.3); F/G values are kept for purlins and eaves members.
ROOF_CPE_RIDGE = {'F1': -1.3, 'F2': -0.6, 'F3': -0.5, 'F4': -0.5, 'F5': -0.5, 'F6': -0.6, 'F7': -1.3}
# vertical X-braced wall bays (E-W stability), two bays in series per corner region: (col_a, col_b)
BRACED_BAYS = [('K6', 'K5'), ('K5', 'K7'), ('K25', 'K26'), ('K26', 'K24'), ('K24', 'K27'),
               ('K3', 'K1'), ('K1', 'K2'), ('K21', 'K22'), ('K22', 'K23')]
BRACED_COLS = sorted({c for b in BRACED_BAYS for c in b})
UPSTAND = 0.3                                  # kN/m along opening edges
ALLOW_PLATES = 0.10                            # +10 % of rafter/column self-weight for haunches, plates, bolts

GAMMA_G, GAMMA_Q = 1.35, 1.5

# ---- roof plane ----
def TOS(y):
    """Top of steel of the rafter (m above slab) - single plane 6 % falling north."""
    return 3.45 + 0.06 * (35.87 - y)


def wall_height(y):
    return TOS(y) + 0.20


# ---- frames: columns (id, y), rafter extent (south end y0, north end y1), gable flag ----
FRAMES = {
    'F1': dict(x=68.0, cols=['K25', 'K19', 'K15', 'K8', 'K6'], y0=15.57, y1=35.87, gable='W'),
    'F2': dict(x=72.1, cols=['K26', 'K9', 'K5'], y0=15.57, y1=35.87, gable=None),
    'F3': dict(x=77.8, cols=['K27', 'K20', 'K16', 'K10', 'K7'], y0=15.57, y1=35.87, gable=None),
    'F4': dict(x=81.85, cols=['K21', 'K17', 'K11', 'K3'], y0=19.97, y1=35.87, gable=None),
    'F5': dict(x=87.2, cols=['K12', 'K1'], y0=20.07, y1=35.87, gable=None, propped=True),
    'F6': dict(x=92.5, cols=['K13', 'K2'], y0=20.07, y1=35.87, gable=None, propped=True),
    'F7': dict(x=95.55, cols=['K23', 'K18', 'K14', 'K4'], y0=19.97, y1=35.87, gable='E'),
}
OPEN_STAIR = (29.37, 35.37)
OPEN_ELEV = (20.17, 24.16)


def trib_roof(frame, y):
    """Tributary roof width (m) of the frame rafter at position y (openings excluded)."""
    if frame == 'F1': return 2.16
    if frame == 'F2': return 4.90
    if frame == 'F5': return 5.325
    if frame == 'F6': return 4.175
    if frame == 'F7': return 1.665
    in_open = OPEN_STAIR[0] <= y <= OPEN_STAIR[1] or OPEN_ELEV[0] <= y <= OPEN_ELEV[1]
    mid = 0.0 if in_open else 2.025
    if frame == 'F3':
        return 2.85 + (mid if y >= 19.97 else 0.0)
    if frame == 'F4':
        return 2.675 + mid
    raise KeyError(frame)


def on_opening_edge(frame, y):
    """Upstand line load applies where the rafter bounds an opening."""
    if frame in ('F3', 'F4'):
        return OPEN_STAIR[0] <= y <= OPEN_STAIR[1] or OPEN_ELEV[0] <= y <= OPEN_ELEV[1]
    return False


# ---- perimeter wall tributary widths (m): NS = north/south wall (in-plane wind), EW = east/west wall ----
WALL_TRIB = {  # column: (NS-wall width, EW-wall width)
    'K25': (2.10, 3.25), 'K26': (3.45, 0), 'K24': (2.90, 0), 'K27': (1.55, 2.10),
    'K21': (4.65, 0), 'K22': (2.65, 0), 'K23': (1.70, 2.70),
    'K6': (2.15, 3.60), 'K5': (4.90, 0), 'K7': (4.90, 0), 'K3': (4.70, 0), 'K1': (5.30, 0), 'K2': (4.20, 0),
    'K4': (1.70, 3.40),
    'K19': (0, 5.25), 'K15': (0, 3.80), 'K8': (0, 4.40),
    'K18': (0, 4.60), 'K14': (0, 5.60),
}
# south-wall wind of the east wing reaching the propped rafter ends of F5/F6 via the wind posts (roof-level half)
POST_TRIB = {'F5': 3.55, 'F6': 3.30}
WALL_SIDE = {'K25': 'S', 'K26': 'S', 'K24': 'S', 'K27': 'S', 'K21': 'S', 'K22': 'S', 'K23': 'S',
             'K6': 'N', 'K5': 'N', 'K7': 'N', 'K3': 'N', 'K1': 'N', 'K2': 'N', 'K4': 'N'}


def roof_cpe(direction, d_from_windward, gable):
    """cpe,10 of the roof for wind from N or S at distance d from the windward eave."""
    z = ROOF_CPE[direction]
    if d_from_windward <= E_ZONE / 10:
        return z['F'] if gable else z['G']
    return z['H']


def wall_cp(direction, side, cpi):
    """Net wall pressure coefficient (positive = pressure on the wall) for a wall facing `side`."""
    if direction == 'R':
        return CPE_WALL_SIDE - cpi
    if direction == side:
        return CPE_WALL_D - cpi
    return CPE_WALL_E - cpi


def ehf_phi(h, m):
    """EN 1993-1-1 5.3.2 initial sway imperfection phi = phi0 * alpha_h * alpha_m."""
    ah = min(1.0, max(2 / 3, 2 / h**0.5))
    am = (0.5 * (1 + 1 / m))**0.5
    return ah * am / 200

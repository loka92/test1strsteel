"""Geometry model for alternative C (post-and-beam, all pinned). Units m, kN.
Rev 2. Roof plane: TOS(y) = 3.30 + 0.06 (35.87 - y) (raised 20 mm, review F11). Primary top = TOS + 0.05 (rafter bottom
flange 30 mm above the primary bottom flange -> no cope, 13 mm clearance at the down-slope flange tip).
Cap plate top = TOS - 0.28, column length = TOS - 0.34 (grout 40 + plate 25 -> 65 mm, rounded)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
GEO = json.load(open(os.path.join(HERE, '..', '..', '..', 'geometry.json')))
COLS = {c['id']: (c['cx'], c['cy']) for c in GEO['columns']}
COL_LONG = {c['id']: ('x' if c['bx'] > c['by'] else 'y') for c in GEO['columns']}   # concrete column long-axis direction
SADDLE = {'K21'}   # 200 mm pier between the notch edge and the shaft opening: saddle base (bases_C.md)
ENV = dict(x0=67.89, x1=95.69, y0=15.57, y1=35.87)
NOTCH = dict(x0=77.89, x1=95.69, y0=15.57, y1=19.97)
OPEN = {'STAIR': dict(x0=77.89, x1=81.79, y0=29.37, y1=35.37),
        'ELEV':  dict(x0=77.89, x1=81.99, y0=20.17, y1=24.16)}
PITCH = 0.06
NORTH_JOG_X = 81.79                      # Rev 3 (C1): the north face is at y 35.37 west of x 81.79 and 35.87 east of it
def north_edge(x): return 35.37 if x < NORTH_JOG_X else 35.87
def TOS(y): return 3.33 + PITCH*(35.87 - y)   # Rev 3 (C3): plane raised 30 mm -> 3.02 m clear under the cap-plate nuts at y 35.77
def cap_top(y): return TOS(y) - 0.28           # column top = cap-plate underside = TOS + 0.05 - 0.33 - 0.02 = TOS - 0.30
def L_col(y): return TOS(y) - 0.35             # B1: 25 grout + 25 plate (B2: 30 plate -> TOS - 0.355, used for the schedule only)
def wall_h(y): return TOS(y) + 0.30          # panel top + flashing, above slab
SEC_PRIM, SEC_RAFT, SEC_COL = 'IPE 330', 'IPE 270', 'HEA 160'   # scheme sections (checked / revised in run)

def roofed(x, y):
    if not (ENV['x0'] <= x <= ENV['x1'] and ENV['y0'] <= y <= north_edge(x)): return False
    if NOTCH['x0'] < x and y < NOTCH['y1']: return False
    for o in OPEN.values():
        if o['x0'] < x < o['x1'] and o['y0'] < y < o['y1']: return False
    return True

# ---- N-S beams (rafters / edge beams): id, x, y-extent, supports [(y, support_id)], section key
# support ids: column 'Kn' or primary 'P..' or beam 'R..'
RAFTERS = [
 dict(id='R68',  x=67.99, y0=15.57, y1=35.37, sup=[(15.87,'K25'),(21.76,'K19'),(26.37,'K15'),(29.37,'K8'),(35.17,'K6')]),
 dict(id='R70',  x=70.04, y0=15.57, y1=35.37, sup=[(15.87,'P_K25K26'),(21.76,'P_K19K20'),(29.32,'P_K8K9'),(35.22,'P_K6K5')]),
 dict(id='R72',  x=72.09, y0=15.57, y1=35.37, sup=[(15.87,'K26'),(21.76,'P_K19K20'),(29.27,'K9'),(35.27,'K5')]),
 dict(id='R75',  x=74.90, y0=15.57, y1=35.37, sup=[(15.97,'K24'),(21.76,'P_K19K20'),(29.27,'P_K9K10'),(35.20,'P_K5K7')]),
 dict(id='R78',  x=77.78, y0=15.57, y1=35.37, sup=[(15.87,'K27'),(21.76,'K20'),(24.46,'K16'),(29.27,'K10'),(35.17,'K7')]),
 dict(id='R82',  x=81.85, y0=19.97, y1=35.87, sup=[(20.07,'K21'),(24.46,'K17'),(29.27,'K11'),(35.67,'K3')]),
 dict(id='R85',  x=84.50, y0=19.97, y1=35.87, sup=[(20.07,'P_K21K22'),(29.27,'P_K11K12'),(35.67,'P_K3K1')]),
 dict(id='R87',  x=87.19, y0=19.97, y1=35.87, sup=[(20.07,'P_K21K22'),(29.27,'K12'),(35.77,'K1')]),
 dict(id='R90',  x=89.90, y0=19.97, y1=35.87, sup=[(20.07,'P_K22K23'),(29.27,'P_K12K13'),(35.77,'P_K1K2')]),
 dict(id='R92',  x=92.48, y0=19.97, y1=35.87, sup=[(20.07,'P_K22K23'),(29.27,'K13'),(35.77,'K2')]),
 dict(id='R95',  x=95.55, y0=19.97, y1=35.87, sup=[(20.07,'K23'),(24.46,'K18'),(29.27,'K14'),(35.67,'K4')]),
]
# ---- E-W primaries (level, on column cap plates) and trimmers/eave beams: id, y, x-extent, supports [(x, id)]
PRIMARIES = [
 dict(id='P_K6K5',   y=35.22, x0=67.99, x1=72.09, sup=[(67.99,'K6'),(72.09,'K5')],  kind='eave'),
 dict(id='P_K5K7',   y=35.22, x0=72.09, x1=77.78, sup=[(72.09,'K5'),(77.78,'K7')],  kind='prim'),
 dict(id='P_K3K1',   y=35.72, x0=81.85, x1=87.19, sup=[(81.85,'K3'),(87.19,'K1')],  kind='prim'),
 dict(id='P_K1K2',   y=35.77, x0=87.19, x1=92.48, sup=[(87.19,'K1'),(92.48,'K2')],  kind='prim'),
 dict(id='P_K2K4',   y=35.72, x0=92.48, x1=95.55, sup=[(92.48,'K2'),(95.55,'K4')],  kind='eave'),
 dict(id='P_K8K9',   y=29.32, x0=67.99, x1=72.09, sup=[(67.99,'K8'),(72.09,'K9')],  kind='prim'),
 dict(id='P_K9K10',  y=29.27, x0=72.09, x1=77.78, sup=[(72.09,'K9'),(77.78,'K10')], kind='prim'),
 dict(id='P_K10K11', y=29.27, x0=77.78, x1=81.85, sup=[(77.78,'K10'),(81.85,'K11')],kind='prim'),
 dict(id='P_K11K12', y=29.27, x0=81.85, x1=87.19, sup=[(81.85,'K11'),(87.19,'K12')],kind='prim'),
 dict(id='P_K12K13', y=29.27, x0=87.19, x1=92.48, sup=[(87.19,'K12'),(92.48,'K13')],kind='prim'),
 dict(id='P_K13K14', y=29.27, x0=92.48, x1=95.55, sup=[(92.48,'K13'),(95.55,'K14')],kind='prim'),
 dict(id='P_K16K17', y=24.46, x0=77.78, x1=81.85, sup=[(77.78,'K16'),(81.85,'K17')],kind='prim'),
 dict(id='T2',       y=24.09, x0=77.78, x1=81.85, sup=[(77.78,'R78'),(81.85,'R82')],kind='trim'),
 dict(id='P_K19K20', y=21.76, x0=67.99, x1=77.78, sup=[(67.99,'K19'),(77.78,'K20')],kind='prim'),
 dict(id='P_NOTCH',  y=20.07, x0=77.78, x1=81.85, sup=[(77.78,'R78'),(81.85,'K21')],kind='eave'),
 dict(id='P_K21K22', y=20.07, x0=81.85, x1=88.88, sup=[(81.85,'K21'),(88.88,'K22')],kind='prim'),
 dict(id='P_K22K23', y=20.07, x0=88.88, x1=95.55, sup=[(88.88,'K22'),(95.55,'K23')],kind='prim'),
 dict(id='P_K25K26', y=15.87, x0=67.99, x1=71.99, sup=[(67.99,'K25'),(71.99,'K26')],kind='eave'),
 dict(id='P_K26K24', y=15.92, x0=71.99, x1=74.89, sup=[(71.99,'K26'),(74.89,'K24')],kind='eave'),
 dict(id='P_K24K27', y=15.92, x0=74.89, x1=77.78, sup=[(74.89,'K24'),(77.78,'K27')],kind='eave'),
]
# upstand (150 mm, flashing, cricket) line load kN/m (G) on the members bounding the openings
UPSTAND = 0.30
UPSTAND_ON = {'P_K10K11': (77.89, 81.79), 'T2': (77.89, 81.99), 'P_NOTCH': (77.89, 81.99)}   # T1 deleted (C1): the well's north edge is the wall
UPSTAND_ON_R = {'R78': [(29.37, 35.37), (20.17, 24.16)], 'R82': [(29.37, 35.37), (20.17, 24.16)]}

# ---- perimeter wall faces: list of (name, normal, fixed coordinate, from, to, [columns/posts along the face in order])
# posts on faces: 'WP1' is a wind post at the notch corner (77.89, 19.97)
POSTS = dict(COLS); POSTS['WP1'] = (77.89, 19.97)
FACES = [
 dict(id='N1', normal='y+', c=35.37, a=67.89, b=81.79, posts=['K6','K5','K7','K3']),   # west block north face (C1)
 dict(id='N2', normal='y+', c=35.87, a=81.79, b=95.69, posts=['K3','K1','K2','K4']),
 dict(id='NR', normal='x-', c=81.79, a=35.37, b=35.87, posts=['K3']),                 # 0.5 m wall return at the jog
 dict(id='S1', normal='y-', c=15.57, a=67.89, b=77.89, posts=['K25','K26','K24','K27']),
 dict(id='S2', normal='y-', c=19.97, a=77.89, b=95.69, posts=['WP1','K21','K22','K23']),
 dict(id='E',  normal='x+', c=95.69, a=19.97, b=35.87, posts=['K23','K18','K14','K4']),
 dict(id='W',  normal='x-', c=67.89, a=15.57, b=35.87, posts=['K25','K19','K15','K8','K6']),
 dict(id='EN', normal='x+', c=77.89, a=15.57, b=19.97, posts=['K27','WP1']),   # notch face, faces east
]
def face_tribs():
    """Return {post: [(face_id, trib_length, y_or_x_position)]} - girts simple spans between posts."""
    out = {}
    for f in FACES:
        along = 0 if f['normal'][0]=='x' else 1   # coordinate along the face: y for E/W faces, x for N/S faces
        pos = [POSTS[p][1 if f['normal'][0]=='x' else 0] for p in f['posts']]
        for i, p in enumerate(f['posts']):
            lo = f['a'] if i == 0 else 0.5*(pos[i-1]+pos[i])
            hi = f['b'] if i == len(pos)-1 else 0.5*(pos[i]+pos[i+1])
            out.setdefault(p, []).append((f['id'], hi-lo, f['normal']))
    return out

# ---- vertical X-braced bays (tension-only diagonals), Rev 2: 10 bays. The N-S bracing sits on three lines
# (x = 68.0, 77.8, 95.5) with two bays in series per line so that no braced-bay base has a bay shear towards a free
# slab edge and the middle column of each line carries no net bracing uplift. K17-K21 (Rev 1 B8) is dropped: K21 is a
# 200 mm pier between the notch edge and the shaft opening and cannot take shear across it.
BAYS = [
 dict(id='B1', dir='x', c=('K1','K2')),   dict(id='B2', dir='x', c=('K5','K7')),
 dict(id='B3', dir='x', c=('K22','K23')), dict(id='B4', dir='x', c=('K25','K26')),
 dict(id='B5', dir='y', c=('K15','K19')), dict(id='B6', dir='y', c=('K14','K18')),
 dict(id='B7', dir='y', c=('K20','K27')), dict(id='B8', dir='y', c=('K10','K16')),
 dict(id='B9', dir='y', c=('K18','K23')), dict(id='B10', dir='y', c=('K19','K25')),
]
def bay_geom(b):
    (x1,y1),(x2,y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    w = abs(x2-x1) if b['dir']=='x' else abs(y2-y1)
    ym = 0.5*(y1+y2); h = L_col(ym) + 0.17     # base plate to primary centre line
    return w, h, (h**2+w**2)**0.5, 0.5*(x1+x2), ym

# ---- free slab edges near a column base (Rev 2 anchorage basis): distance from the column centre to the nearest
# free edge in each direction (+x, -x, +y, -y); envelope, notch and the two shaft openings (assumed to be slab openings)
def edge_distances(cx, cy):
    """Distance (m) from the column centre to the nearest free slab edge in each direction. An opening edge counts
    only when the column lies within the opening's extent in the other coordinate (Rev 4 refinement)."""
    d = {'+x': 99.0, '-x': 99.0, '+y': 99.0, '-y': 99.0}
    def upd(k, v):
        if v >= -0.05: d[k] = min(d[k], max(v, 0.0))
    upd('+x', ENV['x1'] - cx); upd('-x', cx - ENV['x0']); upd('+y', north_edge(cx) - cy); upd('-y', cy - ENV['y0'])
    if NOTCH['y0'] - 0.05 <= cy <= NOTCH['y1'] + 0.05 and cx <= NOTCH['x0'] + 0.05: upd('+x', NOTCH['x0'] - cx)
    if cx >= NOTCH['x0'] - 0.05 and cy >= NOTCH['y1'] - 0.05: upd('-y', cy - NOTCH['y1'])
    for o in OPEN.values():
        if o['y0'] - 0.05 <= cy <= o['y1'] + 0.05:
            if cx <= o['x0'] + 0.05: upd('+x', o['x0'] - cx)
            if cx >= o['x1'] - 0.05: upd('-x', cx - o['x1'])
        if o['x0'] - 0.05 <= cx <= o['x1'] + 0.05:
            if cy <= o['y0'] + 0.05: upd('+y', o['y0'] - cy)
            if cy >= o['y1'] - 0.05: upd('-y', cy - o['y1'])
    return d
NEAR_EDGE = 0.25    # m from the column centre: closer than this, base shear in that direction counts as "towards a free edge"

"""Geometry model, design Rev 7: the roofed area reduced to the architect's enclosed 2nd level (ALWATD sheet A_103,
29 Sep 2026): west block x 67.89-77.89 / y 21.66-35.37 (south face on the K19-K20 column line), east block
x 77.89-95.69 / y 24.36-35.87 (south face on the K16-K17-K18 column line); the SW terrace, the south strip with the
light well (pyramid skylight) and the shaft opening stay open. 20 steel columns K1-K20 on the concrete columns,
3 wind posts on the slab (WP2, WP3 on the 13.7 m south eave of the east block, WP4 on the K19-K20 eave). Roof plane,
levels are unchanged from Rev 6a: TOS(y) = 3.33 + 0.06 (35.87 - y). Rev 7b section set (shorter spans): IPE 240 primaries,
IPE 200 rafters nested 10 mm clear inside the primary flanges (primary top TOS + 0.02), the two long eave beams IPE 330, HEA 140
columns; column length L = TOS + 0.02 - h_primary - 0.065 (90 mm lower under an IPE 330). Units m, kN."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
GEO = json.load(open(os.path.join(HERE, '..', '..', '..', 'geometry.json')))
COLS_ALL = {c['id']: (c['cx'], c['cy']) for c in GEO['columns']}
USED = ['K%d' % i for i in range(1, 21)]                       # K21-K27 lie under the open terraces: no steel column
COLS = {c: COLS_ALL[c] for c in USED}
UNUSED = [c for c in COLS_ALL if c not in COLS]
COL_LONG = {c['id']: ('x' if c['bx'] > c['by'] else 'y') for c in GEO['columns']}
SADDLE = set()                                                 # K21 (saddle base) is no longer used
# roof envelope (Rev 7) and the slab it stands on (unchanged existing slab: edges for the anchorage checks)
ENV = dict(x0=67.89, x1=95.69, y0=21.66, y1=35.87)
NOTCH = dict(x0=77.89, x1=95.69, y0=21.66, y1=24.36)          # SE area outside the roof (light-well terrace)
OPEN = {'STAIR': dict(x0=77.89, x1=81.79, y0=29.37, y1=35.37)}
SLAB_ENV = dict(x0=67.89, x1=95.69, y0=15.57, y1=35.87)
SLAB_NOTCH = dict(x0=77.89, x1=95.69, y0=15.57, y1=19.97)
SLAB_OPEN = dict(OPEN, ELEV=dict(x0=77.89, x1=81.99, y0=20.17, y1=24.16))   # light well: slab opening south of the roof
PITCH = 0.06
NORTH_JOG_X = 81.79
def north_edge(x): return 35.37 if x < NORTH_JOG_X else 35.87
def TOS(y): return 3.33 + PITCH*(35.87 - y)
SEC_PRIM = os.environ.get('SEC_PRIM', 'IPE 240'); SEC_RAFT = os.environ.get('SEC_RAFT', 'IPE 200'); SEC_COL = os.environ.get('SEC_COL', 'HEA 140')
# Rev 7b: lighter set on the shorter spans (heavy Rev 7 set: SEC_PRIM='IPE 300' SEC_RAFT='IPE 240' PRIM_TOP_OFFSET=0.03 SPAN_SECTION='{"P_K17K18": "IPE 330"}')
SPAN_SECTION = json.loads(os.environ.get('SPAN_SECTION', '{"P_K17K18": "IPE 330", "P_K19K20": "IPE 330"}'))   # the two long eave beams (13.7 m and 9.8 m) stay IPE 330: deflection
_H = {'IPE 200': 0.200, 'IPE 220': 0.220, 'IPE 240': 0.240, 'IPE 270': 0.270, 'IPE 300': 0.300, 'IPE 330': 0.330, 'IPE 360': 0.360}
H_PRIM = _H[SEC_PRIM]
PRIM_TOP_OFFSET = float(os.environ.get('PRIM_TOP_OFFSET', '0.02'))   # primary top above TOS: the rafter nests between the primary flanges
COL_DROP = {}
for _p, _s in SPAN_SECTION.items():
    for _c in _p[2:].replace('K', ' K').split():
        COL_DROP[_c] = _H[_s] - H_PRIM          # column top lower under a deeper primary
def cap_top(y, cid=None): return TOS(y) + PRIM_TOP_OFFSET - H_PRIM - COL_DROP.get(cid, 0.0)
def L_col(y, cid=None): return TOS(y) + PRIM_TOP_OFFSET - H_PRIM - 0.02 - 0.045 - COL_DROP.get(cid, 0.0)   # cap 20, grout 25 + plate 20
def wall_h(y): return TOS(y) + 0.30

def roofed(x, y):
    if not (ENV['x0'] <= x <= ENV['x1'] and ENV['y0'] <= y <= north_edge(x)): return False
    if NOTCH['x0'] < x and y < NOTCH['y1']: return False
    for o in OPEN.values():
        if o['x0'] < x < o['x1'] and o['y0'] < y < o['y1']: return False
    return True

RAFTERS = [
 dict(id='R68',  x=67.99, y0=21.66, y1=35.37, sup=[(21.76,'K19'),(26.37,'K15'),(29.37,'K8'),(35.17,'K6')]),
 dict(id='R70',  x=70.04, y0=21.66, y1=35.37, sup=[(21.76,'P_K19K20'),(29.32,'P_K8K9'),(35.22,'P_K6K5')]),
 dict(id='R72',  x=72.09, y0=21.66, y1=35.37, sup=[(21.76,'P_K19K20'),(29.27,'K9'),(35.27,'K5')]),
 dict(id='R75',  x=74.90, y0=21.66, y1=35.37, sup=[(21.76,'P_K19K20'),(29.27,'P_K9K10'),(35.20,'P_K5K7')]),
 dict(id='R78',  x=77.78, y0=21.66, y1=35.37, sup=[(21.76,'K20'),(24.46,'K16'),(29.27,'K10'),(35.17,'K7')]),
 dict(id='R82',  x=81.85, y0=24.36, y1=35.87, sup=[(24.46,'K17'),(29.27,'K11'),(35.67,'K3')]),
 dict(id='R85',  x=84.50, y0=24.36, y1=35.87, sup=[(24.46,'P_K17K18'),(29.27,'P_K11K12'),(35.67,'P_K3K1')]),
 dict(id='R87',  x=87.19, y0=24.36, y1=35.87, sup=[(24.46,'P_K17K18'),(29.27,'K12'),(35.77,'K1')]),
 dict(id='R90',  x=89.90, y0=24.36, y1=35.87, sup=[(24.46,'P_K17K18'),(29.27,'P_K12K13'),(35.77,'P_K1K2')]),
 dict(id='R92',  x=92.48, y0=24.36, y1=35.87, sup=[(24.46,'P_K17K18'),(29.27,'K13'),(35.77,'K2')]),
 dict(id='R95',  x=95.55, y0=24.36, y1=35.87, sup=[(24.46,'K18'),(29.27,'K14'),(35.67,'K4')]),
]
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
 dict(id='P_K16K17', y=24.46, x0=77.78, x1=81.85, sup=[(77.78,'K16'),(81.85,'K17')],kind='eave'),
 dict(id='P_K17K18', y=24.46, x0=81.85, x1=95.55, sup=[(81.85,'K17'),(95.55,'K18')],kind='eave'),   # 13.7 m, IPE 330
 dict(id='T3',       y=24.46, x0=74.90, x1=77.78, sup=[(74.90,'R75'),(77.78,'K16')],kind='trim'),   # chord of the RT-SW panel (IPE 240)
 dict(id='P_K19K20', y=21.76, x0=67.99, x1=77.78, sup=[(67.99,'K19'),(77.78,'K20')],kind='eave'),   # 9.8 m south eave of the west block
]
UPSTAND = 0.30
UPSTAND_ON = {'P_K10K11': (77.89, 81.79)}
UPSTAND_ON_R = {'R78': [(29.37, 35.37)], 'R82': [(29.37, 35.37)]}

POSTS = dict(COLS); POSTS['WP2'] = (86.46, 24.36); POSTS['WP3'] = (91.03, 24.36); POSTS['WP4'] = (72.89, 21.66)
WIND_POSTS = {'WP2': 'S2', 'WP3': 'S2', 'WP4': 'S1'}
FACES = [
 dict(id='N1', normal='y+', c=35.37, a=67.89, b=81.79, posts=['K6','K5','K7','K3']),
 dict(id='N2', normal='y+', c=35.87, a=81.79, b=95.69, posts=['K3','K1','K2','K4']),
 dict(id='NR', normal='x-', c=81.79, a=35.37, b=35.87, posts=['K3']),
 dict(id='S1', normal='y-', c=21.66, a=67.89, b=77.89, posts=['K19','WP4','K20']),
 dict(id='S2', normal='y-', c=24.36, a=77.89, b=95.69, posts=['K16','K17','WP2','WP3','K18']),
 dict(id='E',  normal='x+', c=95.69, a=24.36, b=35.87, posts=['K18','K14','K4']),
 dict(id='W',  normal='x-', c=67.89, a=21.66, b=35.37, posts=['K19','K15','K8','K6']),
 dict(id='EN', normal='x+', c=77.89, a=21.66, b=24.36, posts=['K20','K16']),     # east face of the west block, faces the light-well terrace
]
def face_tribs():
    out = {}
    for f in FACES:
        pos = [POSTS[p][1 if f['normal'][0]=='x' else 0] for p in f['posts']]
        for i, p in enumerate(f['posts']):
            lo = f['a'] if i == 0 else 0.5*(pos[i-1]+pos[i])
            hi = f['b'] if i == len(pos)-1 else 0.5*(pos[i]+pos[i+1])
            out.setdefault(p, []).append((f['id'], hi-lo, f['normal']))
    return out

# vertical X-braced bays, Rev 7: E-W on the two north faces (B1, B2) and at the jog (B3, K16-K17, the blank wall above the
# skylight); N-S on the west face (B5), the east face north of the lift lobby (B6, K4-K14) and the light-well face (B7, K16-K20).
BAYS = [
 dict(id='B1', dir='x', c=('K1','K2')),   dict(id='B2', dir='x', c=('K5','K7')),   dict(id='B3', dir='x', c=('K16','K17')),
 dict(id='B5', dir='y', c=('K15','K19')), dict(id='B6', dir='y', c=('K4','K14')),  dict(id='B7', dir='y', c=('K16','K20')),
]
def bay_geom(b):
    (x1,y1),(x2,y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    w = abs(x2-x1) if b['dir']=='x' else abs(y2-y1)
    ym = 0.5*(y1+y2); h = L_col(ym) + 0.22
    return w, h, (h**2+w**2)**0.5, 0.5*(x1+x2), ym

def edge_distances(cx, cy):
    """Distance (m) from the column centre to the nearest free SLAB edge (existing slab, notch, wells) in each direction."""
    d = {'+x': 99.0, '-x': 99.0, '+y': 99.0, '-y': 99.0}
    def upd(k, v):
        if v >= -0.05: d[k] = min(d[k], max(v, 0.0))
    E, N = SLAB_ENV, SLAB_NOTCH
    upd('+x', E['x1'] - cx); upd('-x', cx - E['x0']); upd('+y', north_edge(cx) - cy); upd('-y', cy - E['y0'])
    if N['y0'] - 0.05 <= cy <= N['y1'] + 0.05 and cx <= N['x0'] + 0.05: upd('+x', N['x0'] - cx)
    if cx >= N['x0'] - 0.05 and cy >= N['y1'] - 0.05: upd('-y', cy - N['y1'])
    for o in SLAB_OPEN.values():
        if o['y0'] - 0.05 <= cy <= o['y1'] + 0.05:
            if cx <= o['x0'] + 0.05: upd('+x', o['x0'] - cx)
            if cx >= o['x1'] - 0.05: upd('-x', cx - o['x1'])
        if o['x0'] - 0.05 <= cx <= o['x1'] + 0.05:
            if cy <= o['y0'] + 0.05: upd('+y', o['y0'] - cy)
            if cy >= o['y1'] - 0.05: upd('-y', cy - o['y1'])
    return d
NEAR_EDGE = 0.25

"""Rev 2 geometry for alternative C (from design/C/calc/model.py + bracing.py), units m."""
import json, csv, math
ROOT = '/home/user/test1strsteel/roof'
GEO = json.load(open(ROOT + '/geometry.json'))
COLS = {c['id']: c for c in GEO['columns']}          # K1..K27 -> dict(cx, cy, bx, by, orientation)
KXY = {k: (c['cx'], c['cy']) for k, c in COLS.items()}
ENV = dict(x0=67.89, x1=95.69, y0=15.57, y1=35.87)
NOTCH = dict(x0=77.89, x1=95.69, y0=15.57, y1=19.97)
OPEN = {'STAIR': dict(x0=77.89, x1=81.79, y0=29.37, y1=35.37), 'ELEV': dict(x0=77.89, x1=81.99, y0=20.17, y1=24.16)}
PITCH = 0.06
def TOS(y): return 3.30 + PITCH*(35.87 - y)
def prim_top(y): return TOS(y) + 0.05
def cap_top(y): return TOS(y) - 0.28
def L_col(y): return TOS(y) - 0.34
BASE_TOP = 0.065        # top of base plate (40 grout + 25 plate)
SEC = {'IPE 270': dict(h=0.270, b=0.135, tw=0.0066, tf=0.0102, kg=36.1),
       'IPE 330': dict(h=0.330, b=0.160, tw=0.0075, tf=0.0115, kg=49.1),
       'HEA 160': dict(h=0.152, b=0.160, tw=0.006, tf=0.009, kg=30.4),
       'L 70x7': dict(kg=7.38), 'M24 rod 8.8': dict(kg=3.55), 'Z200x2.0': dict(kg=5.9), 'C200x60x2.5': dict(kg=6.9)}
# N-S rafter lines (11), mark R1..R11 west to east
RAFTERS = [
 dict(id='R68', mark='R1',  x=67.99, y0=15.57, y1=35.87, sup=[(15.87,'K25'),(21.76,'K19'),(26.37,'K15'),(29.37,'K8'),(35.17,'K6')]),
 dict(id='R70', mark='R2',  x=70.04, y0=15.57, y1=35.87, sup=[(15.87,'P17'),(21.76,'P13'),(29.32,'P6'),(35.22,'P1')]),
 dict(id='R72', mark='R3',  x=72.09, y0=15.57, y1=35.87, sup=[(15.87,'K26'),(21.76,'P13'),(29.27,'K9'),(35.27,'K5')]),
 dict(id='R75', mark='R4',  x=74.90, y0=15.57, y1=35.87, sup=[(15.97,'K24'),(21.76,'P13'),(29.27,'P7'),(35.20,'P2')]),
 dict(id='R78', mark='R5',  x=77.78, y0=15.57, y1=35.87, sup=[(15.87,'K27'),(21.76,'K20'),(24.46,'K16'),(29.27,'K10'),(35.17,'K7')]),
 dict(id='R82', mark='R6',  x=81.85, y0=19.97, y1=35.87, sup=[(20.07,'K21'),(24.46,'K17'),(29.27,'K11'),(35.67,'K3')]),
 dict(id='R85', mark='R7',  x=84.50, y0=19.97, y1=35.87, sup=[(20.07,'P15'),(29.27,'P9'),(35.67,'P3')]),
 dict(id='R87', mark='R8',  x=87.19, y0=19.97, y1=35.87, sup=[(20.07,'P15'),(29.27,'K12'),(35.77,'K1')]),
 dict(id='R90', mark='R9',  x=89.90, y0=19.97, y1=35.87, sup=[(20.07,'P16'),(29.27,'P10'),(35.77,'P4')]),
 dict(id='R92', mark='R10', x=92.48, y0=19.97, y1=35.87, sup=[(20.07,'P16'),(29.27,'K13'),(35.77,'K2')]),
 dict(id='R95', mark='R11', x=95.55, y0=19.97, y1=35.87, sup=[(20.07,'K23'),(24.46,'K18'),(29.27,'K14'),(35.67,'K4')]),
]
RMARK = {r['id']: r['mark'] for r in RAFTERS}
# E-W primaries / eave beams (level, on cap plates) and trimmers, mark P1..P19, T1, T2
PRIMARIES = [
 dict(id='P_K6K5',   mark='P1',  y=35.22, x0=67.99, x1=72.09, sup=('K6','K5'),  kind='eave'),
 dict(id='P_K5K7',   mark='P2',  y=35.22, x0=72.09, x1=77.78, sup=('K5','K7'),  kind='prim'),
 dict(id='P_K3K1',   mark='P3',  y=35.72, x0=81.85, x1=87.19, sup=('K3','K1'),  kind='prim'),
 dict(id='P_K1K2',   mark='P4',  y=35.77, x0=87.19, x1=92.48, sup=('K1','K2'),  kind='prim'),
 dict(id='P_K2K4',   mark='P5',  y=35.72, x0=92.48, x1=95.55, sup=('K2','K4'),  kind='eave'),
 dict(id='P_K8K9',   mark='P6',  y=29.32, x0=67.99, x1=72.09, sup=('K8','K9'),  kind='prim'),
 dict(id='P_K9K10',  mark='P7',  y=29.27, x0=72.09, x1=77.78, sup=('K9','K10'), kind='prim'),
 dict(id='P_K10K11', mark='P8',  y=29.27, x0=77.78, x1=81.85, sup=('K10','K11'),kind='prim'),
 dict(id='P_K11K12', mark='P9',  y=29.27, x0=81.85, x1=87.19, sup=('K11','K12'),kind='prim'),
 dict(id='P_K12K13', mark='P10', y=29.27, x0=87.19, x1=92.48, sup=('K12','K13'),kind='prim'),
 dict(id='P_K13K14', mark='P11', y=29.27, x0=92.48, x1=95.55, sup=('K13','K14'),kind='prim'),
 dict(id='P_K16K17', mark='P12', y=24.46, x0=77.78, x1=81.85, sup=('K16','K17'),kind='prim'),
 dict(id='P_K19K20', mark='P13', y=21.76, x0=67.99, x1=77.78, sup=('K19','K20'),kind='prim'),
 dict(id='P_NOTCH',  mark='P14', y=20.07, x0=77.78, x1=81.85, sup=('R5','K21'), kind='eave'),
 dict(id='P_K21K22', mark='P15', y=20.07, x0=81.85, x1=88.88, sup=('K21','K22'),kind='prim'),
 dict(id='P_K22K23', mark='P16', y=20.07, x0=88.88, x1=95.55, sup=('K22','K23'),kind='prim'),
 dict(id='P_K25K26', mark='P17', y=15.87, x0=67.99, x1=71.99, sup=('K25','K26'),kind='eave'),
 dict(id='P_K26K24', mark='P18', y=15.92, x0=71.99, x1=74.89, sup=('K26','K24'),kind='eave'),
 dict(id='P_K24K27', mark='P19', y=15.92, x0=74.89, x1=77.78, sup=('K24','K27'),kind='eave'),
 dict(id='T1',       mark='T1',  y=35.44, x0=77.78, x1=81.85, sup=('R5','R6'),  kind='trim'),
 dict(id='T2',       mark='T2',  y=24.09, x0=77.78, x1=81.85, sup=('R5','R6'),  kind='trim'),
]
PMARK = {p['id']: p['mark'] for p in PRIMARIES}
POSTS = [dict(id='ST1', y=24.46, x0=89.90, x1=95.55), dict(id='ST2', y=26.37, x0=67.99, x1=72.09)]   # IPE 270 roof-truss posts
WP1 = (77.61, 20.25)   # Rev 3: post moved 280 mm inboard on both axes from the notch corner (77.89, 19.97)
BAYS = [('B1','x',('K1','K2')), ('B2','x',('K5','K7')), ('B3','x',('K22','K23')), ('B4','x',('K25','K26')),
        ('B5','y',('K15','K19')), ('B6','y',('K14','K18')), ('B7','y',('K20','K27')), ('B8','y',('K10','K16')),
        ('B9','y',('K18','K23')), ('B10','y',('K19','K25'))]
BAY_OF = {}
for b, d, (a, c) in BAYS:
    BAY_OF.setdefault(a, []).append(b); BAY_OF.setdefault(c, []).append(b)
ROOF_TRUSSES = [
 ('RT-N-W', [(67.99,70.04,29.32,35.22),(70.04,72.09,29.32,35.22),(72.09,74.90,29.27,35.22),(74.90,77.78,29.27,35.17)]),
 ('RT-N-E', [(81.85,84.50,29.27,35.67),(84.50,87.19,29.27,35.72),(87.19,89.90,29.27,35.77),(89.90,92.48,29.27,35.77),(92.48,95.55,29.27,35.67)]),
 ('RT-S-E', [(81.85,84.50,20.07,29.27),(84.50,87.19,20.07,29.27),(87.19,89.90,20.07,29.27),(89.90,92.48,20.07,29.27),(92.48,95.55,20.07,29.27)]),
 ('RT-S-W', [(67.99,70.04,15.87,21.76),(70.04,72.09,15.87,21.76),(72.09,74.90,15.92,21.76),(74.90,77.78,15.92,21.76)]),
 ('RT-W',   [(67.99,72.09,15.87,21.76),(67.99,72.09,21.76,29.32),(67.99,72.09,29.32,35.22)]),
 ('RT-E',   [(89.90,95.55,20.07,29.27),(89.90,95.55,29.27,35.72)]),
 ('RT-JOG', [(77.78,81.85,24.46,29.27)]),
]
# grids: numbered X grids on the rafter lines (+8a at K22), lettered Y grids on the primary rows
XGRID = [('1',67.99),('2',70.04),('3',72.09),('4',74.90),('5',77.78),('6',81.85),('7',84.50),('8',87.19),('8a',88.88),('9',89.90),('10',92.48),('11',95.55)]
YGRID = [('A',15.87),('B',20.07),('C',21.76),('D',24.46),('E',26.37),('F',29.27),('G',35.22),('H',35.72)]
# wall faces: (id, normal, fixed coord, from, to, posts in order)
FACES = [
 dict(id='N',  normal='y+', c=35.87, a=67.89, b=95.69, posts=['K6','K5','K7','K3','K1','K2','K4'], title='NORTH ELEVATION (low eave, gutter side)'),
 dict(id='S1', normal='y-', c=15.57, a=67.89, b=77.89, posts=['K25','K26','K24','K27'], title='SOUTH ELEVATION - WEST WING (y 15.57)'),
 dict(id='S2', normal='y-', c=19.97, a=77.89, b=95.69, posts=['WP1','K21','K22','K23'], title='SOUTH ELEVATION - EAST BLOCK (y 19.97)'),
 dict(id='E',  normal='x+', c=95.69, a=19.97, b=35.87, posts=['K23','K18','K14','K4'], title='EAST ELEVATION (x 95.69)'),
 dict(id='W',  normal='x-', c=67.89, a=15.57, b=35.87, posts=['K25','K19','K15','K8','K6'], title='WEST ELEVATION (x 67.89)'),
 dict(id='EN', normal='x+', c=77.89, a=15.57, b=19.97, posts=['K27','WP1'], title='NOTCH FACE (x 77.89, faces east)'),
]
POSTXY = dict(KXY); POSTXY['WP1'] = WP1
# girt row spacing per bay (report section 4): 1.5 m default, 1.2 sleeved, 1.0 sleeved
GIRT_S = {('K5','K7'):1.2, ('K25','K19'):1.2, ('K8','K6'):1.2, ('K21','K22'):1.0, ('K22','K23'):1.0, ('K14','K4'):1.0}
def girt_spacing(a, b):
    return GIRT_S.get((a, b), GIRT_S.get((b, a), 1.5))
# drainage
GUTTER = dict(y=35.87, x0=67.89, x1=95.69, w=0.15, d=0.10)
DOWNPIPES = [('DP1',68.7),('DP2',77.3),('DP3',85.3),('DP4',92.0)]
HIGH_PTS = [73.0, 88.65]
# purlins: E-W lines @ 1.5 m from the north eave, first line 0.30 m inside the edge
PURLIN_Y = [round(35.57 - 1.5*k, 2) for k in range(14)]   # 35.57 ... 16.07
def roofed(x, y):
    if not (ENV['x0'] <= x <= ENV['x1'] and ENV['y0'] <= y <= ENV['y1']): return False
    if NOTCH['x0'] < x and y < NOTCH['y1']: return False
    for o in OPEN.values():
        if o['x0'] < x < o['x1'] and o['y0'] < y < o['y1']: return False
    return True
def purlin_segments():
    """(y, x0, x1) purlin pieces between adjacent rafter lines, omitting cells that are not roofed."""
    xs = [r['x'] for r in RAFTERS]; segs = []
    for y in PURLIN_Y:
        for a, b in zip(xs[:-1], xs[1:]):
            xm = 0.5*(a+b)
            if roofed(xm, y): segs.append((y, a, b))
    return segs
def members_csv():
    return list(csv.DictReader(open(ROOT + '/design/C/members_C.csv')))

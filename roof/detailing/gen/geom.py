"""Design C Rev 6 geometry (calc/model.py Rev 6, calc/bracing.py Rev 5a, bases_C.md Rev 8), units m."""
import json, csv, math, re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # .../roof, wherever the repo is checked out
GEO = json.load(open(ROOT + '/geometry.json'))
COLS = {c['id']: c for c in GEO['columns'] if int(c['id'][1:]) <= 27}   # Rev 6a stands on K1-K27 (K28-K30 were added to geometry.json for Rev 8a)
KXY = {k: (c['cx'], c['cy']) for k, c in COLS.items()}
ENV = dict(x0=67.89, x1=95.69, y0=15.57, y1=35.87)
NOTCH = dict(x0=77.89, x1=95.69, y0=15.57, y1=19.97)
OPEN = {'STAIR': dict(x0=77.89, x1=81.79, y0=29.37, y1=35.37), 'ELEV': dict(x0=77.89, x1=81.99, y0=20.17, y1=24.16)}
PITCH = 0.06; NORTH_JOG_X = 81.79
def north_edge(x): return 35.37 if x < NORTH_JOG_X else 35.87
def TOS(y): return 3.33 + PITCH*(35.87 - y)
def prim_top(y): return TOS(y) + 0.03           # Rev 6a: + 0.03 (IPE 240 bottom flange clear of the IPE 300 bottom flange)
def cap_top(y): return TOS(y) - 0.27            # cap-plate top = primary underside (IPE 300: 0.03 + 0.30)
def col_top(y): return TOS(y) - 0.29            # cap-plate underside
def L_col(y): return TOS(y) - 0.335             # 25 grout + 20 plate
BASE_TOP, GROUT, PLATE_T = 0.045, 0.025, 0.020
CLEAR_NUTS, CLEAR_EAVE = 3.03, 3.07
SEC_PRIM, SEC_RAFT, SEC_COL = 'IPE 300', 'IPE 240', 'HEA 140'
SEC = {'IPE 240': dict(h=0.240, b=0.120, tw=0.0062, tf=0.0098, kg=30.7), 'IPE 330': dict(h=0.330, b=0.160, tw=0.0075, tf=0.0115, kg=49.1),
       'IPE 300': dict(h=0.300, b=0.150, tw=0.0071, tf=0.0107, kg=42.2),
       'HEA 140': dict(h=0.133, b=0.140, tw=0.0055, tf=0.0085, kg=24.7),
       'L 70x7': dict(kg=7.38), 'M24 rod 8.8': dict(kg=3.55), 'Z200x2.0': dict(kg=5.9), 'C200x60x2.5': dict(kg=6.9), 'C100x50x3': dict(kg=4.0)}
RAFTERS = [
 dict(id='R68', mark='R1',  x=67.99, y0=15.57, y1=35.37, sup=[(15.87,'K25'),(21.76,'K19'),(26.37,'K15'),(29.37,'K8'),(35.17,'K6')]),
 dict(id='R70', mark='R2',  x=70.04, y0=15.57, y1=35.37, sup=[(15.87,'P17'),(21.76,'P13'),(29.32,'P6'),(35.22,'P1')]),
 dict(id='R72', mark='R3',  x=72.09, y0=15.57, y1=35.37, sup=[(15.87,'K26'),(21.76,'P13'),(29.27,'K9'),(35.27,'K5')]),
 dict(id='R75', mark='R4',  x=74.90, y0=15.57, y1=35.37, sup=[(15.97,'K24'),(21.76,'P13'),(29.27,'P7'),(35.20,'P2')]),
 dict(id='R78', mark='R5',  x=77.78, y0=15.57, y1=35.37, sup=[(15.87,'K27'),(21.76,'K20'),(24.46,'K16'),(29.27,'K10'),(35.17,'K7')]),
 dict(id='R82', mark='R6',  x=81.85, y0=19.97, y1=35.87, sup=[(20.07,'K21'),(24.46,'K17'),(29.27,'K11'),(35.67,'K3')]),
 dict(id='R85', mark='R7',  x=84.50, y0=19.97, y1=35.87, sup=[(20.07,'P15'),(29.27,'P9'),(35.67,'P3')]),
 dict(id='R87', mark='R8',  x=87.19, y0=19.97, y1=35.87, sup=[(20.07,'P15'),(29.27,'K12'),(35.77,'K1')]),
 dict(id='R90', mark='R9',  x=89.90, y0=19.97, y1=35.87, sup=[(20.07,'P16'),(29.27,'P10'),(35.77,'P4')]),
 dict(id='R92', mark='R10', x=92.48, y0=19.97, y1=35.87, sup=[(20.07,'P16'),(29.27,'K13'),(35.77,'K2')]),
 dict(id='R95', mark='R11', x=95.55, y0=19.97, y1=35.87, sup=[(20.07,'K23'),(24.46,'K18'),(29.27,'K14'),(35.67,'K4')]),
]
RMARK = {r['id']: r['mark'] for r in RAFTERS}; RX = {r['mark']: r['x'] for r in RAFTERS}
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
 dict(id='P_K19K20', mark='P13', y=21.76, x0=67.99, x1=77.78, sup=('K19','K20'),kind='prim', sec='IPE 330'),
 dict(id='P_NOTCH',  mark='P14', y=20.07, x0=77.78, x1=81.85, sup=('R5','K21'), kind='eave'),
 dict(id='P_K21K22', mark='P15', y=20.07, x0=81.85, x1=88.88, sup=('K21','K22'),kind='prim'),
 dict(id='P_K22K23', mark='P16', y=20.07, x0=88.88, x1=95.55, sup=('K22','K23'),kind='prim'),
 dict(id='P_K25K26', mark='P17', y=15.87, x0=67.99, x1=71.99, sup=('K25','K26'),kind='eave'),
 dict(id='P_K26K24', mark='P18', y=15.92, x0=71.99, x1=74.89, sup=('K26','K24'),kind='eave'),
 dict(id='P_K24K27', mark='P19', y=15.92, x0=74.89, x1=77.78, sup=('K24','K27'),kind='eave'),
 dict(id='T2',       mark='T2',  y=24.09, x0=77.78, x1=81.85, sup=('R5','R6'),  kind='trim'),
]
PMARK = {p['id']: p['mark'] for p in PRIMARIES}
def prim_sec(p): return p.get('sec', 'IPE 240' if p['kind'] == 'trim' else 'IPE 300')
POSTS = [dict(id='ST1', y=24.46, x0=89.90, x1=95.55), dict(id='ST2', y=26.37, x0=67.99, x1=72.09)]
WP1 = (77.61, 20.25)
BAYS = [('B1','x',('K1','K2')), ('B2','x',('K5','K7')), ('B3','x',('K22','K23')), ('B4','x',('K25','K26')),
        ('B5','y',('K15','K19')), ('B6','y',('K14','K18')), ('B7','y',('K20','K27')), ('B9','y',('K18','K23'))]
BAY_OF = {}
for b, d, (a, c) in BAYS:
    BAY_OF.setdefault(a, []).append(b); BAY_OF.setdefault(c, []).append(b)
ROOF_TRUSSES = [   # Rev 5a: 13 panels in 5 strips (calc/bracing.py ROOF_TRUSSES)
 ('RT-N-W', [(67.99,72.09,29.32,35.22),(72.09,77.78,29.27,35.20)]),
 ('RT-N-E', [(81.85,87.19,29.27,35.72),(87.19,92.48,29.27,35.77),(92.48,95.55,29.27,35.67)]),
 ('RT-JOG', [(77.78,81.85,24.46,29.27)]),
 ('RT-W',   [(67.99,72.09,15.87,21.76),(67.99,72.09,21.76,26.37),(67.99,72.09,26.37,29.32),(67.99,72.09,29.32,35.22)]),
 ('RT-E',   [(89.90,95.55,20.07,24.46),(89.90,95.55,24.46,29.27),(89.90,95.55,29.27,35.72)]),
]
def rod_gusset_nodes():
    """Corner nodes that carry rod gussets (union of panel corners); NE corner cell K2/K4/K13/K14 gets combined gussets."""
    nodes = set()
    for tid, panels in ROOF_TRUSSES:
        for (x0, x1, y0, y1) in panels:
            for x in (x0, x1):
                for y in (y0, y1): nodes.add((round(x, 2), round(y, 2)))
    return sorted(nodes)
COMBINED_GUSSETS = ['K2', 'K4', 'K13', 'K14']
FIN2 = {'R1': 'FP2', 'R3': 'FP2', 'R9': 'FP2', 'R11': 'FP2'}     # 2 x 2 M20 chord-splice fin plates 160 x 150 x 10 (R68/R72/R90/R95)
XGRID = [('1',67.99),('2',70.04),('3',72.09),('4',74.90),('5',77.78),('6',81.85),('7',84.50),('8',87.19),('8a',88.88),('9',89.90),('10',92.48),('11',95.55)]
YGRID = [('A',15.87),('B',20.07),('C',21.76),('D',24.46),('E',26.37),('F',29.27),('G',35.22),('H',35.72)]
FACES = [
 dict(id='N1', normal='y+', c=35.37, a=67.89, b=81.79, posts=['K6','K5','K7','RET'], title='NORTH ELEVATION N1 - WEST BLOCK (y 35.37, gutter G-W)'),
 dict(id='N2', normal='y+', c=35.87, a=81.79, b=95.69, posts=['K3','K1','K2','K4'], title='NORTH ELEVATION N2 - EAST BLOCK (y 35.87, gutter G-E)'),
 dict(id='S1', normal='y-', c=15.57, a=67.89, b=77.89, posts=['K25','K26','K24','K27'], title='SOUTH ELEVATION S1 - WEST WING (y 15.57)'),
 dict(id='S2', normal='y-', c=19.97, a=77.89, b=95.69, posts=['WP1','K21','K22','K23'], title='SOUTH ELEVATION S2 - EAST BLOCK (y 19.97)'),
 dict(id='E',  normal='x+', c=95.69, a=19.97, b=35.87, posts=['K23','K18','K14','K4'], title='EAST ELEVATION (x 95.69)'),
 dict(id='W',  normal='x-', c=67.89, a=15.57, b=35.87, posts=['K25','K19','K15','K8','K6'], title='WEST ELEVATION (x 67.89)'),
 dict(id='EN', normal='x+', c=77.89, a=15.57, b=19.97, posts=['K27','WP1'], title='NOTCH FACE (x 77.89, faces east)'),
]
POSTXY = dict(KXY); POSTXY['WP1'] = WP1; POSTXY['RET'] = (81.79, 35.37)
GIRT_S = {('K5','K7'):1.2, ('K25','K19'):1.2, ('K8','K6'):1.2, ('K21','K22'):1.0, ('K22','K23'):1.0, ('K14','K4'):1.0}
def girt_spacing(a, b): return GIRT_S.get((a, b), GIRT_S.get((b, a), 1.5))
GUTTERS = [dict(id='G-W', y=35.37, x0=67.89, x1=77.89, hp=73.0), dict(id='G-E', y=35.87, x0=81.79, x1=95.69, hp=88.65)]
SPOUTS = [67.89, 77.89, 81.79, 95.69]
DOWNPIPES = [('DP1',68.7),('DP2',77.3),('DP3',85.3),('DP4',92.0)]
PURLIN_Y = [round(35.57 - 1.5*k, 2) for k in range(14)]
def roofed(x, y):
    if not (ENV['x0'] <= x <= ENV['x1'] and ENV['y0'] <= y <= north_edge(x)): return False
    if NOTCH['x0'] < x and y < NOTCH['y1']: return False
    for o in OPEN.values():
        if o['x0'] < x < o['x1'] and o['y0'] < y < o['y1']: return False
    return True
def purlin_segments():
    xs = [r['x'] for r in RAFTERS]; segs = []
    for y in PURLIN_Y:
        for a, b in zip(xs[:-1], xs[1:]):
            if roofed(0.5*(a+b), y): segs.append((y, a, b))
    return segs
def members_csv(): return list(csv.DictReader(open(ROOT + '/design/C/members_C.csv')))
# ---- bases Rev 8: all type E (P at K21); key layouts per bases_C.md section 3
EW_COLS = {'K1','K2','K5','K9','K10','K11','K12','K13','K14','K21','K22','K23'}     # 240 rebar spacing along E-W
KEYB = {'K3':'+y','K4':'+x,+y','K6':'-x,+y','K8':'-x','K14':'+x'}
KEYPAIR = {'K1':'(-300,-200)/(300,-200)','K2':'(-300,-200)/(300,-200)','K5':'(-300,-200)/(300,-200)','K7':'(-200,-700)/(-200,-100)','K10':'(-300,-200)/(300,-200)',
           'K15':'(200,-300)/(200,300)','K18':'(-200,-300)/(-200,300)','K19':'(200,-300)/(200,300)','K20':'(-200,-300)/(-200,300)','K22':'(-300,200)/(300,200)',
           'K23':'(-700,200)/(-100,200)','K25':'(200,0)/(200,600)','K27':'(-200,0)/(-200,600)'}
PLATE = {'K1':'800x400x20 (x -400..400, y -300..100)','K2':'800x400x20 (x -400..400, y -300..100)','K5':'800x400x20 (x -400..400, y -300..100)','K7':'400x950x20 (x -300..100, y -800..150)',
         'K10':'800x400x20 (x -400..400, y -300..100)','K15':'400x800x20 (x -100..300, y -400..400)','K18':'400x800x20 (x -300..100, y -400..400)','K19':'400x800x20 (x -100..300, y -400..400)',
         'K20':'400x800x20 (x -300..100, y -400..400)','K22':'800x400x20 (x -400..400, y -100..300)','K23':'1000x400x20 (x -800..200, y -100..300)','K25':'400x850x20 (x -100..300, y -150..700)','K27':'400x850x20 (x -300..100, y -150..700)'}
def base_util():
    u = {}
    for ln in open(ROOT + '/design/C/bases_C.md'):
        m = re.match(r'\| (K\d+|WP1) \|', ln); g = re.search(r'\*\*(\d\.\d\d)\*\* \(([^)]*)\)', ln)
        if m and g and m.group(1) not in u: u[m.group(1)] = (float(g.group(1)), g.group(2))
    return u
def base_type(k): return 'P' if k == 'K21' else 'E'

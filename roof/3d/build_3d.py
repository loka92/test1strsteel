"""3D concept model of alternative C (design Rev 3, bases Rev 4b): C_concept_3d.dxf + rendered views.
Geometry is imported from design/C/calc/model.py (+ bracing.py for the roof rod panels) and, for the drawn extras
(purlin rows, ST1/ST2 posts, WP1 Rev 4b position, base types, girt rows), from detailing/gen/geom.py, which is
cross-checked against model.py here. No members are invented. Units m.  Run: python3 build_3d.py"""
import sys, os, math, json
ROOT = '/home/user/test1strsteel/roof'
OUT = ROOT + '/3d'
sys.path.insert(0, ROOT + '/design/C/calc'); sys.path.insert(0, ROOT + '/detailing/gen')
import model as M                       # Rev 3 geometry (nodes, rafters, primaries, columns, bays, TOS)
import bracing as BR                    # ROOF_TRUSSES (24 rod panels)
import geom as G                        # detailing extras: PURLIN_Y, POSTS (ST1/ST2), WP1 (Rev 4b), base types, girts
import ezdxf
from ezdxf.math import Vec3, Matrix44, OCS
from ezdxf.render import forms, MeshBuilder, MeshVertexMerger
from ezdxf.math.triangulation import mapbox_earcut_2d
from ezdxf.enums import TextEntityAlignment

TOS = M.TOS
GEO = M.GEO
# ---------------------------------------------------------------- cross-checks model.py <-> detailing geom.py
MISMATCH = []
for a, b in zip(M.RAFTERS, G.RAFTERS):
    if (a['x'], a['y0'], a['y1'], [s[0] for s in a['sup']]) != (b['x'], b['y0'], b['y1'], [s[0] for s in b['sup']]):
        MISMATCH.append('rafter %s differs between model.py and geom.py' % a['id'])
for a in M.PRIMARIES:
    b = next(p for p in G.PRIMARIES if p['id'] == a['id'])
    if (a['y'], a['x0'], a['x1'], a['kind']) != (b['y'], b['x0'], b['x1'], b['kind']):
        MISMATCH.append('primary %s differs between model.py and geom.py' % a['id'])
for a, (bid, d, c) in zip(M.BAYS, G.BAYS):
    if (a['id'], a['dir'], tuple(a['c'])) != (bid, d, tuple(c)): MISMATCH.append('bay %s differs' % a['id'])
for t, (tid, panels) in zip(BR.ROOF_TRUSSES, G.ROOF_TRUSSES):
    if t['id'] != tid or t['panels'] != panels: MISMATCH.append('roof truss %s differs' % t['id'])
if M.POSTS['WP1'] != G.WP1:
    MISMATCH.append('WP1: model.py (%.2f, %.2f) = notch corner (wall-load model) vs drawings %s (Rev 4b, 280 mm inboard) - drawn position used' % (M.POSTS['WP1'][0], M.POSTS['WP1'][1], G.WP1))
# rafter line vs column centre eccentricities (columns at true positions)
for r in M.RAFTERS:
    for y, sid in r['sup']:
        if sid in M.COLS and abs(M.COLS[sid][0] - r['x']) > 0.03:
            MISMATCH.append('rafter %s at x %.2f is %.0f mm off column %s (x %.2f)' % (r['id'], r['x'], 1000*(r['x']-M.COLS[sid][0]), sid, M.COLS[sid][0]))

# ---------------------------------------------------------------- sections and layers
SEC = {'IPE 330': (0.160, 0.330), 'IPE 270': (0.135, 0.270), 'HEA 160': (0.160, 0.152), 'Z200': (0.070, 0.200), 'C200': (0.060, 0.200)}
LAYERS = {   # name: (ACI colour, transparency 0-1, description)
 '3D-EXIST-SLAB': (253, 0.0, 'existing slab 300 mm, L-shape with the notch and the two well openings'),
 '3D-EXIST-COL':  (253, 0.0, 'existing concrete columns 0.2 x 0.4 x 3.5 m below the slab (27)'),
 '3D-COL':        (5, 0.0, 'HEA 160 steel columns C1-C27 + WP1 wind post, cap plates 200x280x20'),
 '3D-PRIM':       (1, 0.0, 'IPE 330 primaries / eave beams, level, top at TOS + 0.05'),
 '3D-RAFT':       (3, 0.0, 'IPE 270 rafters (sloping 6 %), trimmer T2, roof-truss posts ST1/ST2'),
 '3D-PURL':       (8, 0.0, 'Z200 purlins @ 1.5 m on the roofed area, C200 eave rails'),
 '3D-BRACE-WALL': (6, 0.0, 'L70x7 wall X-bracing, bays B1-B10 (tension-only diagonals)'),
 '3D-BRACE-ROOF': (2, 0.0, 'M24 roof rods, 24 panels (RT-N-W, RT-N-E, RT-S-E, RT-S-W, RT-W, RT-E, RT-JOG)'),
 '3D-BASE':       (30, 0.0, 'base plates B1 / B2 / P / WP1 on the slab'),
 '3D-PANEL':      (9, 0.6, 'PIR sandwich panel 50 mm on the purlins (semi-transparent, switch off to see the framing)'),
 '3D-WALL':       (251, 0.0, 'wall panel outline (perimeter faces), girt rows, wall header at the stair well'),
 '3D-TEXT':       (7, 0.0, 'marks C1-C27, B1-B10, WP1, T2, ST1, ST2 (3D-placed TEXT)'),
}
ITEMS = []      # (layer, MeshBuilder)
LINES = []      # (layer, [Vec3 ...], closed)
TEXTS = []      # (layer, string, wcs point, height, extrusion)

def add(layer, mesh): ITEMS.append((layer, mesh))
def box(layer, x0, x1, y0, y1, z0, z1):
    m = forms.cube(center=True).scale(x1-x0, y1-y0, z1-z0).translate(0.5*(x0+x1), 0.5*(y0+y1), 0.5*(z0+z1))
    add(layer, m); return m
def prism(layer, p0, p1, profile, up=None):
    """Prism between centreline points p0-p1; profile (s, t): s across (horizontal), t along 'up' (perpendicular to the
    axis in the vertical plane, i.e. the roof-plane normal for sloping members)."""
    p0, p1 = Vec3(p0), Vec3(p1); u = (p1 - p0).normalize()
    if up is None:
        z = Vec3(0, 0, 1); v = z - u*z.dot(u)
        v = v.normalize() if v.magnitude > 1e-6 else Vec3(0, 1, 0)
    else: v = Vec3(up).normalize()
    w = u.cross(v).normalize(); n = len(profile)
    m = MeshBuilder()
    m.vertices = [p0 + w*s + v*t for s, t in profile] + [p1 + w*s + v*t for s, t in profile]
    m.faces = [tuple(range(n))[::-1], tuple(range(n, 2*n))] + [(i, (i+1) % n, n+(i+1) % n, n+i) for i in range(n)]
    add(layer, m); return m
def rect(w, h, t_off=0.0): return [(-w/2, -h/2+t_off), (w/2, -h/2+t_off), (w/2, h/2+t_off), (-w/2, h/2+t_off)]
def circ(r, n=8): return [(r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n)) for i in range(n)]
ROOF_N = Vec3(0, M.PITCH, 1).normalize()      # roof-plane normal (plane rises to the south)
def plate_mesh(layer, ext, holes, zb, zt):
    """Closed mesh of a polygon with holes between the surfaces z = zb(x, y) and z = zt(x, y)."""
    tris = mapbox_earcut_2d(ext, holes); m = MeshVertexMerger()
    for t in tris:
        m.add_face([Vec3(p.x, p.y, zt(p.x, p.y)) for p in t]); m.add_face([Vec3(p.x, p.y, zb(p.x, p.y)) for p in t][::-1])
    for ring in [ext] + list(holes or []):
        for a, b in zip(ring, ring[1:] + ring[:1]):
            m.add_face([Vec3(a[0], a[1], zb(*a)), Vec3(b[0], b[1], zb(*b)), Vec3(b[0], b[1], zt(*b)), Vec3(a[0], a[1], zt(*a))])
    add(layer, m); return m

# ---------------------------------------------------------------- existing structure
# slab outline (S01): L-shape less the notch; north face jog at x 81.79; stair well open to the north face; elevator well a hole
SLAB_EXT = [(67.89, 15.57), (77.89, 15.57), (77.89, 19.97), (95.69, 19.97), (95.69, 35.87), (81.79, 35.87), (81.79, 29.37), (77.89, 29.37), (77.89, 35.37), (67.89, 35.37)]
ELEV = M.OPEN['ELEV']; STAIR = M.OPEN['STAIR']
ELEV_RING = [(ELEV['x0'], ELEV['y0']), (ELEV['x1'], ELEV['y0']), (ELEV['x1'], ELEV['y1']), (ELEV['x0'], ELEV['y1'])]
plate_mesh('3D-EXIST-SLAB', SLAB_EXT, [ELEV_RING], lambda x, y: -0.30, lambda x, y: 0.0)
for c in GEO['columns']:
    box('3D-EXIST-COL', c['cx']-c['bx']/2, c['cx']+c['bx']/2, c['cy']-c['by']/2, c['cy']+c['by']/2, -3.80, -0.30)

# ---------------------------------------------------------------- steel columns, cap plates, base plates
COUNT = {}
def cnt(k, n=1): COUNT[k] = COUNT.get(k, 0) + n
for c in GEO['columns']:
    k, x, y = c['id'], c['cx'], c['cy']; ew = c['bx'] > c['by']    # concrete long axis E-W -> HEA web N-S (flanges parallel to x)
    b, h = SEC['HEA 160']; sx, sy = (b, h) if ew else (h, b)
    bt = G.base_type(k); z0 = G.base_top(k); z1 = TOS(y) - 0.30
    box('3D-COL', x-sx/2, x+sx/2, y-sy/2, y+sy/2, z0, z1); cnt('columns')
    cx_, cy_ = (0.20, 0.28) if ew else (0.28, 0.20)                # cap plate 200 x 280 x 20, long side along the web
    box('3D-COL', x-cx_/2, x+cx_/2, y-cy_/2, y+cy_/2, z1, z1+0.02); cnt('cap plates')
    if bt == 'B2': (px, py), t = ((0.80, 0.55) if ew else (0.55, 0.80)), 0.030      # B2 800 (along the long axis) x 550 x 30 (centred here; real plates 100 outboard / 450 inboard, S05)
    else: (px, py), t = ((0.40, 0.30) if ew else (0.30, 0.40)), 0.025          # B1 / P 300 x 400 x 25, long side along the concrete long axis
    box('3D-BASE', x-px/2, x+px/2, y-py/2, y+py/2, z0-t, z0); cnt('base plates')
    TEXTS.append(('3D-TEXT', 'C%d' % int(k[1:]), (x, y, TOS(y) + 0.75), 0.35, (0, -1, 0)))
# wind post WP1 (HEA 160, web N-S), Rev 4b position, base 250 x 250 x 15, top at TOS(19.97) - 0.30 (slotted, wall wind only)
wx, wy = G.WP1
box('3D-COL', wx-0.08, wx+0.08, wy-0.076, wy+0.076, 0.040, TOS(19.97) - 0.30); cnt('wind post WP1')
box('3D-BASE', wx-0.125, wx+0.125, wy-0.125, wy+0.125, 0.025, 0.040); cnt('base plates')
TEXTS.append(('3D-TEXT', 'WP1', (wx, wy, TOS(19.97) + 0.75), 0.30, (0, -1, 0)))

# ---------------------------------------------------------------- primaries / eave beams (level, IPE 330) and trimmer T2
def prim_at(x, y):
    """primary / eave beam crossing rafter line x at row y (for rafter splices)."""
    for p in M.PRIMARIES:
        if p['kind'] != 'trim' and abs(p['y'] - y) < 0.12 and p['x0'] - 0.05 <= x <= p['x1'] + 0.05: return p
    return None
for p in M.PRIMARIES:
    if p['kind'] == 'trim':                                                   # T2 IPE 270 between the rafters R78 / R82, top at TOS
        b, h = SEC['IPE 270']; x0 = p['x0'] + b/2 + 0.01; x1 = p['x1'] - b/2 - 0.01; z = TOS(p['y']) - h/2
        prism('3D-RAFT', (x0, p['y'], z), (x1, p['y'], z), rect(b, h), up=ROOF_N); cnt('trimmer T2')
        TEXTS.append(('3D-TEXT', 'T2', (0.5*(x0+x1), p['y'], TOS(p['y']) + 0.6), 0.25, (0, -1, 0)))
        continue
    b, h = SEC['IPE 330']; x0, x1 = p['x0'], p['x1']
    if p['sup'][0][1].startswith('R'): x0 += SEC['IPE 270'][0]/2 + 0.01     # P_NOTCH: fin plate on rafter R78
    z = TOS(p['y']) + 0.05 - h/2
    prism('3D-PRIM', (x0, p['y'], z), (x1, p['y'], z), rect(b, h)); cnt('primaries / eave beams')

# ---------------------------------------------------------------- rafters (IPE 270 on the plane, spliced at every primary)
RX = [r['x'] for r in M.RAFTERS]
for r in M.RAFTERS:
    b, h = SEC['IPE 270']; x = r['x']
    cuts = sorted({prim_at(x, y)['y'] for y, sid in r['sup'] if prim_at(x, y) is not None})
    gap = SEC['IPE 330'][0]/2 + 0.01
    ys = [r['y0']] + [v for y in cuts for v in (y-gap, y+gap)] + [r['y1']]
    for ya, yb in zip(ys[0::2], ys[1::2]):
        prism('3D-RAFT', (x, ya, TOS(ya) - h/2), (x, yb, TOS(yb) - h/2), rect(b, h)); cnt('rafter pieces')
# roof-truss posts ST1 / ST2 (IPE 270 between rafters, split at the intermediate rafter)
for s in G.POSTS:
    b, h = SEC['IPE 270']; xs = [s['x0']] + [x for x in RX if s['x0'] < x < s['x1']] + [s['x1']]
    for xa, xb in zip(xs[:-1], xs[1:]):
        prism('3D-RAFT', (xa + b/2 + 0.01, s['y'], TOS(s['y']) - h/2), (xb - b/2 - 0.01, s['y'], TOS(s['y']) - h/2), rect(b, h), up=ROOF_N); cnt('post pieces ST1/ST2')
    TEXTS.append(('3D-TEXT', s['id'], (0.5*(s['x0']+s['x1']), s['y'], TOS(s['y']) + 0.6), 0.25, (0, -1, 0)))

# ---------------------------------------------------------------- purlins Z200 @ 1.5 m (roofed cells only) + eave rails C200
for y, a, b_ in G.purlin_segments():
    w, h = SEC['Z200']
    prism('3D-PURL', (a, y, TOS(y) + h/2), (b_, y, TOS(y) + h/2), rect(w, h), up=ROOF_N); cnt('purlin pieces')
for y, a, b_ in ((35.32, 67.89, 77.89), (35.82, 81.79, 95.69)):     # eave rails C200x60 on the rafter ends (S01)
    w, h = SEC['C200']
    prism('3D-PURL', (a, y, TOS(y) + h/2), (b_, y, TOS(y) + h/2), rect(w, h), up=ROOF_N); cnt('eave rails')

# ---------------------------------------------------------------- wall bracing L70x7 (X, bays B1-B10)
BAY_NORMAL = {'B1': (0, 1, 0), 'B2': (0, 1, 0), 'B3': (0, -1, 0), 'B4': (0, -1, 0), 'B5': (-1, 0, 0), 'B10': (-1, 0, 0),
              'B6': (1, 0, 0), 'B9': (1, 0, 0), 'B7': (1, 0, 0), 'B8': (1, 0, 0)}
for b in M.BAYS:
    (xa, ya), (xc, yc) = M.COLS[b['c'][0]], M.COLS[b['c'][1]]
    za, zc = TOS(ya) - 0.12, TOS(yc) - 0.12          # top gusset at the primary / rafter centre line; bottom gusset 0.15 above the slab
    prism('3D-BRACE-WALL', (xa, ya, 0.15), (xc, yc, zc), rect(0.07, 0.07)); prism('3D-BRACE-WALL', (xa, ya, za), (xc, yc, 0.15), rect(0.07, 0.07)); cnt('wall diagonals', 2)
    n = Vec3(BAY_NORMAL[b['id']])
    TEXTS.append(('3D-TEXT', b['id'], (Vec3(0.5*(xa+xc), 0.5*(ya+yc), 1.4) + n*0.6), 0.40, tuple(n)))

# ---------------------------------------------------------------- roof rods M24 (24 panels, on the rafter mid-depth)
ROD_R = 0.020      # M24 drawn at r = 20 mm (exaggerated for visibility; nominal 12 mm)
for t in BR.ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        zf = lambda y: TOS(y) - SEC['IPE 270'][1]/2
        prism('3D-BRACE-ROOF', (x0, y0, zf(y0)), (x1, y1, zf(y1)), circ(ROD_R)); prism('3D-BRACE-ROOF', (x0, y1, zf(y1)), (x1, y0, zf(y0)), circ(ROD_R)); cnt('roof rods', 2)
        cnt('roof panels')

# ---------------------------------------------------------------- sandwich panel (50 mm on the purlins), split around the wells
plate_mesh('3D-PANEL', SLAB_EXT, [ELEV_RING], lambda x, y: TOS(y) + 0.20, lambda x, y: TOS(y) + 0.25)

# ---------------------------------------------------------------- walls: perimeter outline, girt rows, wall header, return
def face_pts(f, u, z):
    return Vec3(u, f['c'], z) if f['normal'][0] == 'y' else Vec3(f['c'], u, z)
for f in G.FACES:
    a, b_ = f['a'], f['b']; horiz = f['normal'][0] == 'y'
    zt = (lambda u: TOS(f['c']) + 0.30) if horiz else (lambda u: TOS(u) + 0.30)
    LINES.append(('3D-WALL', [face_pts(f, a, 0), face_pts(f, a, zt(a)), face_pts(f, b_, zt(b_)), face_pts(f, b_, 0)], True))
    posts = f['posts']
    for p, q in zip(posts[:-1], posts[1:]):
        (x1, y1), (x2, y2) = G.POSTXY[p], G.POSTXY[q]; u1, u2 = (x1, x2) if horiz else (y1, y2); s = G.girt_spacing(p, q)
        zmax = (TOS(f['c']) + 0.05 - 0.33 if horiz else TOS(max(u1, u2)) - 0.27) - 0.15
        z = 0.5
        while z < zmax:
            LINES.append(('3D-WALL', [face_pts(f, u1, z), face_pts(f, u2, z)], False)); z += s; cnt('girt rows')
# 0.5 m wall return at the jog (x 81.79, y 35.37-35.87) and the wall header 2 x C200 boxed over the stair well (no roof, no eave beam)
LINES.append(('3D-WALL', [Vec3(81.79, 35.37, 0), Vec3(81.79, 35.37, TOS(35.37)+0.30), Vec3(81.79, 35.87, TOS(35.87)+0.30), Vec3(81.79, 35.87, 0)], True))
box('3D-WALL', 77.89, 81.79, 35.37-0.12, 35.37, TOS(35.37)+0.05-0.20, TOS(35.37)+0.05); cnt('wall header')
# slab-edge lines of the stair well and the elevator well (upstand lines) for orientation
for o in (STAIR, ELEV):
    LINES.append(('3D-WALL', [Vec3(o['x0'], o['y0'], 0.0), Vec3(o['x1'], o['y0'], 0.0), Vec3(o['x1'], o['y1'], 0.0), Vec3(o['x0'], o['y1'], 0.0)], True))

# ================================================================ DXF
doc = ezdxf.new('R2013', setup=True)
doc.header['$INSUNITS'] = 6; doc.header['$MEASUREMENT'] = 1
for name, (col, tr, desc) in LAYERS.items():
    ly = doc.layers.add(name, color=col); ly.description = desc
    if tr: ly.transparency = tr
msp = doc.modelspace()
for layer, m in ITEMS:
    e = m.render_mesh(msp, dxfattribs={'layer': layer})
    if layer == '3D-PANEL': e.transparency = LAYERS[layer][1]
for layer, pts, closed in LINES:
    msp.add_polyline3d(pts, close=closed, dxfattribs={'layer': layer})
for layer, s, p, hgt, ext in TEXTS:
    ocs = OCS(ext); t = msp.add_text(s, height=hgt, dxfattribs={'layer': layer, 'extrusion': ext, 'style': 'OpenSans'})
    t.set_placement(ocs.from_wcs(Vec3(p)), align=TextEntityAlignment.MIDDLE_CENTER)
# model-space view: SW isometric, shaded
CENTRE = (81.79, 25.72, 1.5)
doc.set_modelspace_vport(height=34, center=(0, 0))
vp = doc.viewports.get('*Active')[0]
vp.dxf.direction = (-1, -1, 1); vp.dxf.target = CENTRE; vp.dxf.center = (0, 0); vp.dxf.height = 34; vp.dxf.aspect_ratio = 1.6
vp.dxf.render_mode = 5          # flat shaded with wireframe edges
for name, d in (('SW-ISO', (-1, -1, 1)), ('SE-ISO', (1, -1, 1)), ('NE-ISO', (1, 1, 1)), ('NW-ISO', (-1, 1, 1))):
    doc.views.add(name, dxfattribs={'direction': d, 'target': CENTRE, 'center': (0, 0), 'height': 34, 'width': 54, 'render_mode': 5})
auditor = doc.audit()
print('audit errors', len(auditor.errors), 'fixes', len(auditor.fixes))
doc.saveas(OUT + '/C_concept_3d.dxf')
n_by_layer = {}
for e in msp: n_by_layer[e.dxf.layer] = n_by_layer.get(e.dxf.layer, 0) + 1
print('entities per layer', n_by_layer)
print('member counts', COUNT)
json.dump(dict(entities=n_by_layer, counts=COUNT, mismatch=MISMATCH), open(OUT + '/model_stats.json', 'w'), indent=1)
print('MISMATCH:'); [print(' -', m) for m in MISMATCH]

# ================================================================ renders (matplotlib, Poly3DCollection of the same meshes)
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.patches import Patch
RGB = {'3D-EXIST-SLAB': '#c9c9c9', '3D-EXIST-COL': '#b5b5b5', '3D-COL': '#1f4fd8', '3D-PRIM': '#d81f1f', '3D-RAFT': '#1f9e3a',
       '3D-PURL': '#8a8a8a', '3D-BRACE-WALL': '#d81fd8', '3D-BRACE-ROOF': '#d9a800', '3D-BASE': '#e07b1f', '3D-PANEL': '#9fb7d1', '3D-WALL': '#6b6b6b', '3D-TEXT': '#000000'}
LEGEND = [('3D-COL', 'Columns HEA 160 (C1-C27, WP1)'), ('3D-PRIM', 'Primaries / eave beams IPE 330 (level)'), ('3D-RAFT', 'Rafters IPE 270, T2, ST1/ST2 (6 % slope)'),
          ('3D-PURL', 'Purlins Z200 @ 1.5 m, eave rails'), ('3D-BRACE-WALL', 'Wall X-bracing L70x7, B1-B10'), ('3D-BRACE-ROOF', 'Roof rods M24 (24 panels)'),
          ('3D-BASE', 'Base plates'), ('3D-PANEL', 'Sandwich panel 50 mm'), ('3D-WALL', 'Wall outline, girts, header'), ('3D-EXIST-SLAB', 'Existing slab and concrete columns')]
def hexrgb(h): return np.array([int(h[i:i+2], 16)/255 for i in (1, 3, 5)])
def render(fname, title, cam, hide=(), xray=False, ortho=False, elev=28, figsize=(24, 15), ax=None, legend=True, labels=False):
    own = ax is None
    if own:
        fig = plt.figure(figsize=figsize, dpi=100); ax = fig.add_subplot(111, projection='3d')
    if ortho: ax.set_proj_type('ortho')
    else: ax.set_proj_type('persp', focal_length=1.2)
    cam = np.array(cam, float); cam /= np.linalg.norm(cam); light = cam + np.array([0, 0, 0.8]); light /= np.linalg.norm(light)
    polys, cols = [], []
    for layer, m in ITEMS:
        if layer in hide: continue
        base = hexrgb(RGB[layer]); alpha = 0.35 if layer == '3D-PANEL' else 1.0
        if xray and layer not in ('3D-BRACE-WALL', '3D-BRACE-ROOF', '3D-COL'): alpha = 0.12
        for face in m.faces_as_vertices():
            pts = np.array([(v.x, v.y, v.z) for v in face])
            if len(pts) < 3: continue
            n = np.cross(pts[1]-pts[0], pts[2]-pts[0]); nn = np.linalg.norm(n)
            if nn < 1e-12: continue
            n /= nn
            if np.dot(n, cam) < 0: n = -n                 # two-sided
            shade = 0.55 + 0.45*max(0.0, float(np.dot(n, light)))
            polys.append(pts); cols.append((*np.clip(base*shade, 0, 1), alpha))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors=[(0, 0, 0, 0.15 if not xray else 0.05)]*len(polys), linewidths=0.2, zsort='average')
    pc.set_clip_on(False); ax.add_collection3d(pc)
    if '3D-WALL' not in hide:
        segs = []
        for layer, pts, closed in LINES:
            p = [(v.x, v.y, v.z) for v in pts] + ([(pts[0].x, pts[0].y, pts[0].z)] if closed else [])
            segs += [(p[i], p[i+1]) for i in range(len(p)-1)]
        lc = Line3DCollection(segs, colors=RGB['3D-WALL'], linewidths=0.6, alpha=0.5 if not xray else 0.25); lc.set_clip_on(False); ax.add_collection3d(lc)
    if labels:
        for layer, s, p, hgt, ext in TEXTS:
            if s.startswith('B') or s == 'WP1': ax.text(p[0], p[1], p[2] + 0.3, s, fontsize=13, clip_on=False, color='#7a007a' if s.startswith('B') else '#1f4fd8', ha='center', weight='bold')
    ax.set_xlim(66.5, 97); ax.set_ylim(14.5, 37); ax.set_zlim(-3.9, 5.2); ax.set_box_aspect((30.5, 22.5, 9.1), zoom=(2.0 if ortho else 1.38) if own else 1.25)
    az = math.degrees(math.atan2(cam[1], cam[0])); ax.view_init(elev=elev, azim=az)
    ax.set_axis_off(); ax.set_facecolor('white')
    ax.set_title(title, fontsize=22 if own else 15, pad=4, y=0.97 if own else 0.92)
    if legend:
        ax.legend(handles=[Patch(facecolor=RGB[l], edgecolor='k', label=t) for l, t in LEGEND if l not in hide and not (l == '3D-PURL' and '3D-PURL' in hide)],
                  loc='lower left', fontsize=13 if own else 9, frameon=True)
    if own:
        fig.patch.set_facecolor('white'); fig.subplots_adjust(left=0, right=1, bottom=0, top=0.95)
        fig.savefig(OUT + '/' + fname, dpi=100, facecolor='white'); plt.close(fig); print('wrote', fname)
SUB = 'Alternative C - post-and-beam braced steel roof over the existing slab (design Rev 3)'
render('iso_SW.png', 'SW isometric - ' + SUB, (-1, -1, 0.9))
render('iso_SE.png', 'SE isometric - ' + SUB, (1, -1, 0.9))
render('iso_NE_no_panel.png', 'NE isometric, roof panel hidden: purlins, rafters and roof rods - Alternative C, Rev 3', (1, 1, 0.9), hide=('3D-PANEL',))
render('elev_N.png', 'North elevation (from the north, orthographic) - ' + SUB, (0, 1, 0.0001), ortho=True, elev=0)
render('elev_S.png', 'South elevation (from the south, orthographic) - ' + SUB, (0, -1, 0.0001), ortho=True, elev=0)
render('section_xray.png', 'X-ray: panel and purlins hidden, bracing highlighted (wall bays B1-B10, roof rod panels) - Alternative C, Rev 3', (-1, -1, 0.9), hide=('3D-PANEL', '3D-PURL'), xray=True, labels=True)
fig = plt.figure(figsize=(24, 18), dpi=100)
for i, (t, cam, hide, xr) in enumerate((('SW isometric', (-1, -1, 0.9), (), False), ('SE isometric', (1, -1, 0.9), (), False),
                                        ('NE isometric, panel hidden', (1, 1, 0.9), ('3D-PANEL',), False), ('X-ray: bracing system', (-1, -1, 0.9), ('3D-PANEL', '3D-PURL'), True))):
    ax = fig.add_subplot(2, 2, i+1, projection='3d')
    render('', t, cam, hide=hide, xray=xr, ax=ax, legend=(i == 0), labels=xr)
fig.suptitle('Overview - ' + SUB, fontsize=22); fig.patch.set_facecolor('white'); fig.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0, hspace=0.02)
fig.savefig(OUT + '/overview.png', dpi=100, facecolor='white'); plt.close(fig); print('wrote overview.png')

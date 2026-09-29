import sys, os, importlib, collections
import matplotlib; matplotlib.use('Agg')
from common import *
import geom
OUT = '/home/user/test1strsteel/roof/detailing'
SHEETS = [('S01', 'Roof framing plan', 60.0), ('S02', 'Column schedule and wall elevations', 110.0), ('S03', 'Typical sections A-A, B-B, C-C', 160.0),
          ('S04', 'Connection details D1-D11', 210.0), ('S05', 'Base details B1 / B2 / P / WP1 and notes', 260.0), ('S06', 'Bill of materials', 310.0)]
def index_sheet(msp):
    sh = Sheet(msp, 10.0, 8.0, 'S00', 'SHEET INDEX AND GENERAL NOTES', 'Not to scale')
    rows = [[no, t, 'x %.0f-%.0f' % (ox, ox+42)] for no, t, ox in SHEETS]
    sh.table(1.0, 28.5, [('Sheet', 1.5), ('Title', 12.0), ('Model-space frame', 4.0)], [['S00', 'Sheet index and general notes', 'x 10-52']] + rows, 0.5, TH, title='SHEET INDEX - all sheets are 42 x 30 m frames side by side in model space, y 8-38')
    sh.note_block(1.0, 23.5, 'LAYERS', ['S-COL columns, S-PRIM primaries / eave beams / trimmers, S-RAFT rafters and posts, S-PURL purlins / girts / eave rail,',
        'S-BRACE wall X bracing and roof rods, S-OPEN openings (hatched), S-GRID grid lines, S-DIM dimensions (dimstyles S-M metres 2 dp,',
        'S-MM details 5x with true-mm text, S-MM1 sections mm text), S-TEXT, S-TITLE, S-DETAIL, S-HATCH, S-DRAIN gutter / downpipes / crickets, S-EXIST existing slab and columns (grey).'], TH_SMALL, 0.32)
    sh.note_block(1.0, 21.5, 'MARKS', ['Cn steel column HEA 160 over existing concrete column Kn (n = 1-27); WP1 wind post. Pn primaries / eave beams IPE 330 (P1-P19), T2 trimmer IPE 270 (elevator well north edge).',
        'Rn rafter lines IPE 270 west to east (R1 x 67.99 ... R11 x 95.55); pieces Rn.1, Rn.2 ... south to north in the BOM. ST1/ST2 roof-truss posts IPE 270.',
        'B1-B10 wall X-bracing bays (2 x L70x7); RT-* roof rod panels (M24). D1-D11 connection details on S04 (D11 wall sill); base details B1 (concentric anchors + keys), B2 (through-bolts + key pair), P (K21), WP1 on S05.',
        'Grids: 1-11 numbered on the rafter lines (+8a at K22), A-H lettered on the primary rows. Section A-A / B-B / C-C on S03.'], TH_SMALL, 0.32)
    sh.note_block(1.0, 18.5, 'DESIGN BASIS (see design_report_C.md Rev 3, load_basis.md Rev 2)', ['EN 1990/1991/1993/1998, EN 1992-4 anchors. Site Tripoli, q_p 1.30 kN/m2 (binding), no snow, a_g 0.10 g check only.',
        'Roof: one plane at 6 % falling north; TOS(y) = 3.33 + 0.06 (35.87 - y); clear height 3.02 m under the cap-plate nuts at C1/C2, 3.06 m under the eave primary. North face jogs: y 35.37 west of x 81.79, 35.87 east. Stair well open to the north face (no roof, no eave beam); elevator well not roofed.',
        'Steel S275 J0; bolts 8.8 (M20 fin/cap/gussets, M12 cleats, M24 rods); purlins / girts Z200x2.0 S350GD; PIR panel 50 mm; BoardX walls 0.30 kN/m2 (to be confirmed).',
        'BASES (bases_C.md Rev 4b, S05): B1 at 13 bases (K3, K4, K6, K8, K9, K11, K12, K13, K14, K16, K17, K24, K26) - plate 300x400x25 / 350x400x25 at edge heads, Key B dia 60 at K3, K4, K6, K8, K14, 4 M20 resin anchors 80 x 280 h_ef 200 in the slab, Key A SHS 90x90x8 centred;',
        'B2 at 13 bases (K1, K2, K5, K7, K10, K15, K18, K19, K20, K22, K23, K25, K27) - plate 800x550x30 + 2 stiffeners (K7 500x1000, K23 1000x550, K25 550x900, K27 600x900), 2 M24 through-bolts 250 inboard @ 280 on a 400x200x25 under-slab plate, SHS 90 key pair; P at K21 (4 M16 h_ef 400, pattern by scan, + saddle); WP1 280 inboard, one key. Grout 25 (25-40 permitted).'], TH_SMALL, 0.32, 175)
    sh.note_block(1.0, 14.5, 'STATUS AND EXISTING STRUCTURE', ['Superstructure: Rev 3 (final critique C1-C15 closed on the drawings); bases Rev 4b. No anchor / bolt installation before the slab investigation: GPR of all 27 heads, 3-6 cores, rebar scans, pull-out tests (S05).',
        'EXISTING STRUCTURE: the slab-top level survey defines the datum (0.000) for every column length, base seating and the 3.02 m clear height (survey before fabrication and before coring). Column lengths on S02 are nominal: cut to the surveyed plate-top level, grout bed 25 +/- 5 mm (X2).',
        'STEEL WEIGHT: 25.4 t per the bill of materials S06 (hot-rolled 14.9 t + plates 3.6 t + bracing 2.3 t + cold-formed 4.6 t); the design report Rev 3 is aligned to this figure (X1).',
        'As-built drawings of the existing building and the adequacy statement for the added ~440 kN gravity and ~150 kN roof-level wind into the 27 concrete columns and foundations are client / structural open items (critique C5) - to be closed before the permit.',
        'Date ' + DATE + '. Generated with ezdxf from the Rev 3 calculation model (calc/model.py, members_C.csv Rev 3, bases_C.md Rev 4b).'], TH_SMALL, 0.32, 150)
    return sh
def main():
    doc = new_doc(); msp = doc.modelspace()
    index_sheet(msp)
    for mod in ('s01', 's02', 's03', 's04', 's05', 's06'):
        importlib.import_module(mod).draw(msp)
    os.makedirs(OUT, exist_ok=True)
    path = OUT + '/C_detail_drawings.dxf'
    doc.saveas(path)
    from ezdxf import recover
    doc2, auditor = recover.readfile(path)
    print('audit errors', len(auditor.errors), 'fixes', len(auditor.fixes))
    for e in auditor.errors[:10]: print('  ERR', e)
    c = collections.Counter(e.dxftype() for e in doc2.modelspace()); print('entities', sum(c.values()), dict(c))
    cl = collections.Counter(e.dxf.layer for e in doc2.modelspace()); print('by layer', dict(cl))
    return doc2
def ent_x(e):
    d = e.dxf; t = e.dxftype()
    if t == 'LINE': return d.start.x
    if t == 'LWPOLYLINE': return e[0][0]
    if t in ('TEXT', 'MTEXT'): return d.insert.x
    if t == 'CIRCLE': return d.center.x
    if t == 'DIMENSION': return d.defpoint.x
    if t == 'HATCH':
        p = e.paths[0]; return p.vertices[0][0] if hasattr(p, 'vertices') else p.edges[0].start[0]
    return None
def render(doc):
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
    import matplotlib.pyplot as plt
    msp = doc.modelspace()
    for no, t, ox in [('S00', '', 10.0)] + SHEETS:
        ents = [e for e in msp if (ent_x(e) is not None and ox - 1 <= ent_x(e) <= ox + 43)]
        fig = plt.figure(figsize=(16.8, 12.0)); ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc); ctx.set_current_layout(msp); ctx.current_layout_properties.set_colors('#ffffff')
        be = MatplotlibBackend(ax); fe = Frontend(ctx, be, config=Configuration(background_policy=BackgroundPolicy.WHITE))
        fe.draw_entities(ents); be.finalize(); fig.set_size_inches(16.8, 12.0)
        ax.set_xlim(ox - 0.3, ox + 42.3); ax.set_ylim(7.85, 38.15)
        fig.savefig(OUT + '/%s.png' % no, dpi=200, facecolor='white'); plt.close(fig); print('rendered', no, len(ents))
if __name__ == '__main__':
    doc = main()
    if '--norender' not in sys.argv: render(doc)

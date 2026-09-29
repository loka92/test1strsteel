"""Build the whole package: sheets S00-S06 + S01a, audit, overlap check, PNG renders, README report."""
import sys, os, importlib, collections, json
import matplotlib; matplotlib.use('Agg')
from common import *
OUT = '/home/user/test1strsteel/roof/detailing'
MODS = ['s00', 's01', 's01a', 's02', 's03', 's04', 's04a', 's05', 's06']
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
def build():
    doc = new_doc(); msp = doc.modelspace(); sheets = []
    for m in MODS:
        M = importlib.import_module(m); sh = M.draw(msp); sh.finish(); sheets.append((sh, M.OX, M.OY))
    os.makedirs(OUT, exist_ok=True); path = OUT + '/C_detail_drawings.dxf'; doc.saveas(path)
    from ezdxf import recover
    doc2, auditor = recover.readfile(path)
    c = collections.Counter(e.dxftype() for e in doc2.modelspace())
    report = {'audit_errors': len(auditor.errors), 'audit_fixes': len(auditor.fixes), 'entities': sum(c.values()), 'by_type': dict(c), 'sheets': {}}
    print('audit errors', len(auditor.errors), 'fixes', len(auditor.fixes), 'entities', sum(c.values()), dict(c))
    for sh, ox, oy in sheets:
        tt, tl, ltt, ltl = check_sheet(doc, sh, ox, oy)
        report['sheets'][sh.no] = {'text_text': tt, 'text_line': tl, 'unplaced': getattr(sh, 'unplaced', 0), 'texts': len(sh.texts), 'tt': ltt[:20], 'tl': [x[:3] for x in ltl[:30]]}
        print(sh.no, 'texts', len(sh.texts), 'text-text', tt, 'text-line', tl, 'unplaced', getattr(sh, 'unplaced', 0), getattr(sh, 'unplaced_list', [])[:8])
        for a in ltt[:8]: print('   TT', a)
        for a in ltl[:12]: print('   TL', a)
    json.dump(report, open(OUT + '/overlap_report.json', 'w'), indent=1)
    return doc, sheets, report
def render(doc, sheets):
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
    import matplotlib.pyplot as plt
    msp = doc.modelspace()
    for sh, ox, oy in sheets:
        ents = [e for e in msp if (ent_x(e) is not None and ox - 1 <= ent_x(e) <= ox + 43)]
        fig = plt.figure(figsize=(16.8, 12.0)); ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc); ctx.set_current_layout(msp); ctx.current_layout_properties.set_colors('#ffffff')
        be = MatplotlibBackend(ax); fe = Frontend(ctx, be, config=Configuration(background_policy=BackgroundPolicy.WHITE)); fe.draw_entities(ents); be.finalize(); fig.set_size_inches(16.8, 12.0)
        ax.set_xlim(ox - 0.3, ox + 42.3); ax.set_ylim(oy - 0.15, oy + 30.15); fig.savefig(OUT + '/%s.png' % sh.no, dpi=200, facecolor='white'); plt.close(fig); print('rendered', sh.no)
if __name__ == '__main__':
    doc, sheets, report = build()
    if '--norender' not in sys.argv: render(doc, sheets)

import sys, importlib, collections, matplotlib; matplotlib.use('Agg')
from common import *
import common
mods = sys.argv[1].split(',')
doc = new_doc(); msp = doc.modelspace(); sheets = []
for m in mods:
    M = importlib.import_module(m); sh = M.draw(msp); sh.finish(); sheets.append((sh, M.OX, M.OY))
doc.saveas('/tmp/test_sheets.dxf')
for sh, ox, oy in sheets:
    tt, tl, ltt, ltl = check_sheet(doc, sh, ox, oy)
    print(sh.no, 'text-text', tt, 'text-line', tl, 'unplaced', getattr(sh, 'unplaced', 0), getattr(sh, 'unplaced_list', [])[:12])
    for a in ltt[:12]: print('   TT', a)
    import collections as _c
    for (s, o), n in _c.Counter((a[0], a[1]) for a in ltl).items(): print('   TL', n, repr(s), o, [a[2] for a in ltl if a[0] == s][0])
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
import matplotlib.pyplot as plt
from main import ent_x
for sh, ox, oy in sheets:
    ents = [e for e in msp if (ent_x(e) is not None and ox - 1 <= ent_x(e) <= ox + 43)]
    fig = plt.figure(figsize=(16.8, 12.0)); ax = fig.add_axes([0, 0, 1, 1]); ctx = RenderContext(doc); ctx.set_current_layout(msp); ctx.current_layout_properties.set_colors('#ffffff')
    be = MatplotlibBackend(ax); fe = Frontend(ctx, be, config=Configuration(background_policy=BackgroundPolicy.WHITE)); fe.draw_entities(ents); be.finalize(); fig.set_size_inches(16.8, 12.0)
    ax.set_xlim(ox - 0.3, ox + 42.3); ax.set_ylim(oy - 0.15, oy + 30.15); fig.savefig('/tmp/%s.png' % sh.no, dpi=200, facecolor='white'); plt.close(fig); print('rendered', sh.no)

"""Render every sheet of C_detail_drawings.dxf to a vector PDF page (A2 landscape) and merge into one file."""
import sys, os, importlib
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
from pypdf import PdfWriter, PdfReader
from common import SHEET_W, SHEET_H

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # .../roof/detailing, wherever the repo is checked out
MODS = ['s00', 's01', 's01a', 's02', 's03', 's04', 's04a', 's05', 's06']
A2 = (23.39, 16.54)   # inches, landscape

def main(paper=A2, tag='A2'):
    from ezdxf.addons import Importer
    from ezdxf import bbox as _bbox
    src = ezdxf.readfile(OUT + '/C_detail_drawings.dxf'); smsp = src.modelspace()
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR)
    pages = []
    os.makedirs(OUT + '/pdf', exist_ok=True)
    # assign every entity to a sheet by its bounding-box centre
    frames = []
    for m in MODS:
        M = importlib.import_module(m); frames.append((m, M.OX, M.OY))
    buckets = {m: [] for m, _, _ in frames}
    for e in smsp:
        try: b = _bbox.extents([e], fast=True)
        except Exception: continue
        if not b.has_data: continue
        cx = 0.5 * (b.extmin.x + b.extmax.x)
        for m, ox, oy in frames:
            if ox - 1 <= cx <= ox + SHEET_W + 1: buckets[m].append(e); break
    for m, ox, oy in frames:
        doc = ezdxf.new('R2013'); imp = Importer(src, doc); imp.import_entities(buckets[m]); imp.finalize()
        msp = doc.modelspace(); ctx = RenderContext(doc); ctx.set_current_layout(msp)
        print(m, 'entities', len(buckets[m]))
        fig = plt.figure(figsize=paper); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
        be = MatplotlibBackend(ax)
        Frontend(ctx, be, config=cfg).draw_layout(msp, finalize=True)
        # sheet frame 42 x 30 m -> paper 1.4 aspect; A2 is 1.414 -> tiny side margins
        cx, cy = ox + SHEET_W / 2, oy + SHEET_H / 2
        w = SHEET_W + 0.6; h = w / (paper[0] / paper[1])
        if h < SHEET_H + 0.4: h = SHEET_H + 0.4; w = h * (paper[0] / paper[1])
        ax.set_xlim(cx - w / 2, cx + w / 2); ax.set_ylim(cy - h / 2, cy + h / 2); ax.set_aspect('equal')
        fig.set_size_inches(paper[0], paper[1], forward=True)
        no = M.draw.__globals__.get('NO', None)
        name = m.upper().replace('S0', 'S0')
        path = '%s/pdf/%s_%s.pdf' % (OUT, name, tag)
        fig.savefig(path, format='pdf', facecolor='white'); plt.close(fig); pages.append(path); print('pdf', path)
    w = PdfWriter()
    for p in pages: w.append(PdfReader(p))
    merged = '%s/C_detail_drawings_%s.pdf' % (OUT, tag)
    with open(merged, 'wb') as f: w.write(f)
    print('merged', merged, len(pages), 'pages')
    return merged

if __name__ == '__main__':
    main()

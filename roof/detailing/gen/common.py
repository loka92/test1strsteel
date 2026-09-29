"""Drawing framework v2: layers with lineweights, sheet frame with title block / revision table / legend, label placer
with collision avoidance and leaders, registered dimensions and tables, and the overlap checker."""
import math, textwrap, ezdxf
from ezdxf import bbox as _bbox
from ezdxf.enums import TextEntityAlignment as TA
PROJECT = 'Steel roof - Administration Building, Regatta Tourist Village, Tripoli'
SUBTITLE = 'ALTERNATIVE C - POST-AND-BEAM BRACED STEEL ROOF, SANDWICH PANELS'
REV = 'Rev 6a superstructure / Rev 8 bases / bracing Rev 5a'
DATE = '2026-09-29'
REVISIONS = [('1', '2026-09-27', 'First issue: design Rev 2, bases Rev 3'), ('2', '2026-09-28', 'Design Rev 3 / bases Rev 4b (critique C1-C15)'), ('3', DATE, 'Rev 6a (IPE 300/240, HEA 140), bases Rev 8, bracing Rev 5a')]
SHEET_W, SHEET_H, STRIP = 42.0, 30.0, 3.0
TH_MARK, TH_DIM, TH_NOTE, TH_TITLE = 0.25, 0.2, 0.25, 0.5
LAYERS = [('S-COL',5,'CONTINUOUS',35),('S-PRIM',1,'CONTINUOUS',50),('S-RAFT',3,'CONTINUOUS',35),('S-PURL',4,'CONTINUOUS',15),
          ('S-BRACE',6,'DASHED',35),('S-OPEN',8,'CONTINUOUS',25),('S-GRID',9,'CENTER',13),('S-DIM',2,'CONTINUOUS',13),
          ('S-TEXT-MEMBER',7,'CONTINUOUS',18),('S-TEXT-DIM',7,'CONTINUOUS',18),('S-TEXT-NOTE',7,'CONTINUOUS',18),
          ('S-TITLE',7,'CONTINUOUS',35),('S-DETAIL',7,'CONTINUOUS',25),('S-HATCH',8,'CONTINUOUS',9),
          ('S-DRAIN',4,'DASHDOT',18),('S-EXIST',8,'CONTINUOUS',15),('S-LEADER',7,'CONTINUOUS',13)]
def new_doc():
    doc = ezdxf.new('R2013', setup=True)
    doc.header['$INSUNITS'] = 6; doc.header['$LTSCALE'] = 0.5; doc.header['$LWDISPLAY'] = 1
    for n, c, lt, lw in LAYERS: doc.layers.add(n, color=c, linetype=lt, lineweight=lw)
    common = dict(dimtxt=TH_DIM, dimasz=0.18, dimexo=0.08, dimexe=0.12, dimgap=0.05, dimtad=1, dimtih=0, dimtoh=0, dimclrt=7, dimclrd=2, dimclre=2, dimtxsty='Standard', dimlwd=-3)
    doc.dimstyles.new('S-M', dxfattribs=dict(common, dimdec=2, dimlfac=1.0, dimzin=0))
    doc.dimstyles.new('S-MM', dxfattribs=dict(common, dimdec=0, dimlfac=250.0, dimzin=8))     # details at 4x
    doc.dimstyles.new('S-MM5', dxfattribs=dict(common, dimdec=0, dimlfac=200.0, dimzin=8))    # details at 5x
    doc.dimstyles.new('S-MM1', dxfattribs=dict(common, dimdec=0, dimlfac=1000.0, dimzin=8))
    doc.dimstyles.new('S-MM2', dxfattribs=dict(common, dimdec=0, dimlfac=500.0, dimzin=8))     # partial plans at 2x
    return doc
# ---------------------------------------------------------------- geometry helpers
def seg_box(seg, box):
    """Segment (x1,y1,x2,y2) intersects axis-aligned box (x0,y0,x1,y1)? Liang-Barsky."""
    x1, y1, x2, y2 = seg; bx0, by0, bx1, by1 = box
    if max(x1, x2) < bx0 or min(x1, x2) > bx1 or max(y1, y2) < by0 or min(y1, y2) > by1: return False
    dx, dy = x2 - x1, y2 - y1; t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0: return False
        else:
            t = q / p
            if p < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
            if t0 > t1: return False
    return True
def box_box(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
def grow(b, m): return (b[0]-m, b[1]-m, b[2]+m, b[3]+m)
class Registry:
    """Per-sheet index of linework segments and text boxes with owner ids (entity handles or logical ids)."""
    def __init__(self, cell=2.0):
        self.cell = cell; self.segs = {}; self.boxes = {}; self.tboxes = {}; self.allowed = {}; self.text_owner = {}
    def _cells(self, b):
        c = self.cell
        for i in range(int(math.floor(b[0]/c)), int(math.floor(b[2]/c)) + 1):
            for j in range(int(math.floor(b[1]/c)), int(math.floor(b[3]/c)) + 1): yield (i, j)
    def add_seg(self, seg, owner):
        b = (min(seg[0], seg[2]), min(seg[1], seg[3]), max(seg[0], seg[2]), max(seg[1], seg[3]))
        for cl in self._cells(b): self.segs.setdefault(cl, []).append((seg, owner))
    def add_box(self, box, owner, kind='text'):
        """kind 'text': a text box (labels keep clear of it and leaders must not cross it); 'fill': a hatched area or a
        member outline interior (labels keep clear of it, leaders may cross it)."""
        for cl in self._cells(box): self.boxes.setdefault(cl, []).append((box, owner))
        if kind == 'text':
            for cl in self._cells(box): self.tboxes.setdefault(cl, []).append((box, owner))
    def hits(self, box, allowed=(), margin=0.03):
        gb = grow(box, margin); out = []; seen = set()
        for cl in self._cells(gb):
            for seg, o in self.segs.get(cl, []):
                if o in allowed or (seg, o) in seen: continue
                if seg_box(seg, gb): out.append(('seg', o)); seen.add((seg, o))
            for bx, o in self.boxes.get(cl, []):
                if o in allowed or (bx, o) in seen: continue
                if box_box(gb, bx): out.append(('box', o)); seen.add((bx, o))
        return out
import os
FILL_LAYERS = ('S-COL', 'S-PRIM', 'S-RAFT', 'S-PURL', 'S-DETAIL', 'S-EXIST', 'S-BRACE', 'S-DRAIN')   # closed outlines whose interior is kept free of text
FILL_MAX_AREA = 5.0   # m2 on the sheet: member sections and plates, not slab outlines or reference boxes
DEBUG_LABELS = set(filter(None, os.environ.get('DEBUG_LABELS', '').split('|')))
class Sheet:
    def __init__(self, msp, ox, oy, no, title, scale_note, legend=None):
        self.msp, self.ox, self.oy, self.no, self.title = msp, ox, oy, no, title
        self.reg = Registry(); self.texts = []; self._nid = 0; self.queue = []; self.late = []; self.defer = True
        self.frame(scale_note)
        if legend: self.legend_block(legend)
    def nid(self, tag='g'):
        self._nid += 1; return '%s%d' % (tag, self._nid)
    def P(self, x, y): return (self.ox + x, self.oy + y)
    # ---- primitives: every linework call registers its segments under an owner id
    def line(self, x0, y0, x1, y1, layer='S-DETAIL', owner=None, **kw):
        e = self.msp.add_line(self.P(x0, y0), self.P(x1, y1), dxfattribs=dict(layer=layer, **kw)); o = owner or e.dxf.handle
        self.reg.add_seg((self.ox+x0, self.oy+y0, self.ox+x1, self.oy+y1), o); self.reg.text_owner[e.dxf.handle] = o; return e
    def pline(self, pts, layer='S-DETAIL', close=False, owner=None, **kw):
        e = self.msp.add_lwpolyline([self.P(*p) for p in pts], close=close, dxfattribs=dict(layer=layer, **kw))
        o = owner or e.dxf.handle; P = [self.P(*p) for p in pts]; self.reg.text_owner[e.dxf.handle] = o
        if close and layer in FILL_LAYERS:
            xs = [p[0] for p in P]; ys = [p[1] for p in P]
            if (max(xs) - min(xs))*(max(ys) - min(ys)) <= FILL_MAX_AREA: self.reg.add_box((min(xs), min(ys), max(xs), max(ys)), o, 'fill')
        if close: P = P + [P[0]]
        for a, b in zip(P[:-1], P[1:]): self.reg.add_seg((a[0], a[1], b[0], b[1]), o)
        return e
    def rect(self, x0, y0, x1, y1, layer='S-DETAIL', owner=None, **kw): return self.pline([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], layer, True, owner, **kw)
    def circle(self, x, y, r, layer='S-DETAIL', owner=None, **kw):
        e = self.msp.add_circle(self.P(x, y), r, dxfattribs=dict(layer=layer, **kw)); o = owner or e.dxf.handle; self.reg.text_owner[e.dxf.handle] = o
        cx, cy = self.P(x, y); pts = [(cx + r*math.cos(2*math.pi*i/12), cy + r*math.sin(2*math.pi*i/12)) for i in range(13)]
        for a, b in zip(pts[:-1], pts[1:]): self.reg.add_seg((a[0], a[1], b[0], b[1]), o)
        return e
    def hatch(self, pts, layer='S-HATCH', pattern='ANSI31', scale=0.15, color=8, angle=0, owner=None):
        """Hatched area: its boundary AND its interior (bbox) are registered so no text lands on the hatching."""
        h = self.msp.add_hatch(color=color, dxfattribs={'layer': layer})
        if pattern == 'SOLID': h.set_solid_fill(color=color)
        else: h.set_pattern_fill(pattern, scale=scale, angle=angle)
        P = [self.P(*p) for p in pts]; h.paths.add_polyline_path(P, is_closed=True); o = owner or h.dxf.handle; self.reg.text_owner[h.dxf.handle] = o
        xs = [p[0] for p in P]; ys = [p[1] for p in P]; self.reg.add_box((min(xs), min(ys), max(xs), max(ys)), o, 'fill'); return h
    # ---- text
    def raw_text(self, x, y, s, h, layer, align='LEFT', rot=0):
        a = {'LEFT': TA.LEFT, 'CENTER': TA.CENTER, 'RIGHT': TA.RIGHT, 'MIDDLE_CENTER': TA.MIDDLE_CENTER, 'MIDDLE_LEFT': TA.MIDDLE_LEFT, 'MIDDLE_RIGHT': TA.MIDDLE_RIGHT}[align]
        return self.msp.add_text(s, height=h, dxfattribs={'layer': layer, 'style': 'Standard', 'rotation': rot}).set_placement(self.P(x, y), align=a)
    def tbox(self, e):
        b = _bbox.extents([e]); return (b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y)
    def text(self, x, y, s, h=TH_NOTE, layer='S-TEXT-NOTE', align='LEFT', rot=0, allowed=(), owner=None):
        """Fixed-position text (notes, tables, titles); registered with its allowed owners."""
        e = self.raw_text(x, y, s, h, layer, align, rot); b = self.tbox(e); o = owner or e.dxf.handle
        self.reg.add_box(b, o); self.reg.allowed[e.dxf.handle] = set(allowed) | {o}; self.texts.append(e); return e
    def finish(self):
        """Place the deferred labels (after every line of the sheet exists), then run the late callables (detail bubbles)."""
        self.defer = False
        for args, kw in self.queue: self.label(*args, **kw)
        self.queue = []
        for fn in self.late: fn()
        self.late = []
    def label(self, s, ax, ay, h=TH_MARK, layer='S-TEXT-MEMBER', rot=0, cands=None, allowed=(), leader=True, margin=0.05, align=None, bounds=None, side=None):
        """Place a label near anchor (ax, ay) at the first collision-free candidate; draw a leader if it had to move away.
        cands: list of (dx, dy, align) in sheet units; default ring around the anchor. Deferred until finish() by default."""
        if self.defer:
            self.queue.append(((s, ax, ay), dict(h=h, layer=layer, rot=rot, cands=cands, allowed=allowed, leader=leader, margin=margin, align=align, bounds=bounds, side=side))); return None
        if bounds is None: bounds = (0.3, STRIP + 0.2, SHEET_W - 0.3, SHEET_H - 0.3)
        if cands is None:
            cands = [(0.15, 0.12, 'LEFT'), (-0.15, 0.12, 'RIGHT'), (0.15, -0.37, 'LEFT'), (-0.15, -0.37, 'RIGHT'), (0.0, 0.25, 'CENTER'), (0.0, -0.5, 'CENTER'), (0.35, 0.3, 'LEFT'), (-0.35, 0.3, 'RIGHT'), (0.35, -0.55, 'LEFT'), (-0.35, -0.55, 'RIGHT'),
                     (0.6, 0.3, 'LEFT'), (-0.6, 0.3, 'RIGHT'), (0.6, -0.55, 'LEFT'), (-0.6, -0.55, 'RIGHT'), (1.2, 0.5, 'LEFT'), (-1.2, 0.5, 'RIGHT'), (1.2, -0.8, 'LEFT'), (-1.2, -0.8, 'RIGHT'),
                     (0.0, 0.9, 'CENTER'), (0.0, -1.15, 'CENTER'), (1.8, 0.9, 'LEFT'), (-1.8, 0.9, 'RIGHT'), (1.8, -1.2, 'LEFT'), (-1.8, -1.2, 'RIGHT'), (2.4, 1.4, 'LEFT'), (-2.4, 1.4, 'RIGHT'), (0.0, 1.6, 'CENTER'), (0.0, -1.85, 'CENTER')]
        e = self.raw_text(ax, ay, s, h, layer, 'LEFT', rot); own = e.dxf.handle; allowed = set(allowed) | {own}
        best = None
        # spiral ring: the text extends AWAY from the anchor (left-aligned on the right side, right-aligned on the left)
        if side in ('R', 'L'):   # detail labels: text extends away from the anchor; preferred side first (other side costs 1.5 m of radius)
            spiral = [(r*math.cos(a), r*math.sin(a), 'LEFT' if math.cos(a) > 0.3 else ('RIGHT' if math.cos(a) < -0.3 else 'CENTER')) for r in (0.5, 0.8, 1.1, 1.5, 2.0, 2.6, 3.3, 4.1, 5.0) for a in [k*math.pi/12 for k in range(24)]]
            spiral.sort(key=lambda c: math.hypot(c[0], c[1]) + (0.0 if (c[0] > 0.1 if side == 'R' else c[0] < -0.1) else 1.5))
        else: spiral = [(r*math.cos(a), r*math.sin(a), 'CENTER') for r in (0.5, 0.8, 1.1, 1.5, 2.0, 2.6, 3.3, 4.1, 5.2, 6.5) for a in [k*math.pi/12 for k in range(24)]]
        for i, (dx, dy, al) in enumerate(list(cands) + spiral):
            al = align or al
            a = {'LEFT': TA.LEFT, 'CENTER': TA.CENTER, 'RIGHT': TA.RIGHT}[al]
            e.set_placement(self.P(ax + dx, ay + dy), align=a); b = self.tbox(e)
            dbg = s in DEBUG_LABELS
            if bounds and not (b[0] >= self.ox + bounds[0] and b[2] <= self.ox + bounds[2] and b[1] >= self.oy + bounds[1] and b[3] <= self.oy + bounds[3]):
                if dbg: print('  DBG', s, i, (dx, dy, al), 'out of bounds', [round(v,2) for v in b], bounds)
                continue
            hh = self.reg.hits(b, allowed, margin)
            if hh:
                if dbg: print('  DBG', s, i, (dx, dy, al), 'hits', hh[:4])
                continue
            far = math.hypot(dx, dy) > 0.7
            if far and leader:
                cx, cy = self.ox + ax, self.oy + ay; tx = min(max(cx, b[0]), b[2]); ty = min(max(cy, b[1]), b[3])
                seg = (cx, cy, tx, ty)
                # leader must not cross other text boxes
                bad = any(seg_box(seg, bx) for cl in self.reg._cells((min(cx,tx), min(cy,ty), max(cx,tx), max(cy,ty))) for bx, o in self.reg.tboxes.get(cl, []))
                if bad:
                    if dbg: print('  DBG', s, i, 'leader crosses text')
                    continue
                best = (b, seg); break
            best = (b, None); break
        if best is None:      # give up: last candidate, flagged
            dx, dy, al = cands[-1]; e.set_placement(self.P(ax + dx, ay + dy), align=TA.CENTER); b = self.tbox(e); best = (b, None); self.unplaced = getattr(self, 'unplaced', 0) + 1
            self.unplaced_list = getattr(self, 'unplaced_list', []) + [s]
        b, seg = best
        self.reg.add_box(b, own); self.reg.allowed[own] = allowed; self.texts.append(e)
        if seg:
            l = self.msp.add_line((seg[0], seg[1]), (seg[2], seg[3]), dxfattribs={'layer': 'S-LEADER'})
            self.reg.add_seg(seg, l.dxf.handle); self.reg.allowed[own].add(l.dxf.handle); self.reg.text_owner[l.dxf.handle] = own
        return e
    # ---- dimensions: rendered, then registered (lines as segments, text as a box allowed over its own lines)
    def dim(self, x0, y0, x1, y1, off, style='S-M', angle=0, text=None, loc=None):
        p1, p2 = self.P(x0, y0), self.P(x1, y1)
        base = (p1[0], p1[1] + off) if angle == 0 else (p1[0] + off, p1[1])
        kw = dict(base=base, p1=p1, p2=p2, angle=angle, dimstyle=style, override={'dimtxt': TH_DIM}, dxfattribs={'layer': 'S-DIM'}, text=text or '<>')
        if loc is not None: kw['location'] = self.P(*loc)
        d = self.msp.add_linear_dim(**kw); d.render(); o = 'dim' + d.dimension.dxf.handle
        for v in d.dimension.virtual_entities():
            t = v.dxftype()
            if t == 'LINE': self.reg.add_seg((v.dxf.start.x, v.dxf.start.y, v.dxf.end.x, v.dxf.end.y), o)
            elif t == 'TEXT' or t == 'MTEXT':
                b = self.tbox(v); self.reg.add_box(b, o); self.reg.allowed[o + 'T'] = {o}
        return d
    # point order chosen so that the dimension text always sits on the OUTER side of the dimension line (away from the object)
    def dimh(self, x0, x1, y, off, style='S-M', text=None, loc=None, outer=False):
        if outer and (x1 > x0) == (off < 0): x0, x1 = x1, x0
        return self.dim(x0, y, x1, y, off, style, 0, text, loc)
    def dimv(self, y0, y1, x, off, style='S-M', text=None, loc=None, outer=False):
        if outer and (y1 > y0) == (off > 0): y0, y1 = y1, y0
        return self.dim(x, y0, x, y1, off, style, 90, text, loc)
    # ---- symbols
    def bubble(self, x, y, top, bottom='', r=0.5, layer='S-TEXT-DIM'):
        o = self.nid('bub'); self.circle(x, y, r, 'S-DIM', owner=o)
        if bottom:
            self.line(x-r, y, x+r, y, 'S-DIM', owner=o)
            self.text(x, y+0.07, top, TH_DIM, layer, 'CENTER', allowed=(o,), owner=o); self.text(x, y-r*0.5-0.1, bottom, 0.16, layer, 'CENTER', allowed=(o,), owner=o)
        else: self.text(x, y, top, TH_DIM, layer, 'MIDDLE_CENTER', allowed=(o,), owner=o)
        return o
    def north_arrow(self, x, y, s=1.4):
        o = self.nid('na'); self.pline([(x, y), (x-0.25*s, y-0.35*s), (x, y+s), (x+0.25*s, y-0.35*s)], 'S-TITLE', True, owner=o)
        self.hatch([(x, y), (x, y+s), (x+0.25*s, y-0.35*s)], pattern='SOLID', color=7, owner=o); self.text(x, y+s+0.15, 'N', TH_TITLE, 'S-TEXT-NOTE', 'CENTER', allowed=(o,), owner=o)
    def scale_bar(self, x, y, unit=1.0, n=5, label='m'):
        o = self.nid('sb')
        for i in range(n):
            self.rect(x+i*unit, y, x+(i+1)*unit, y+0.25, 'S-TITLE', owner=o)
            if i % 2 == 0: self.hatch([(x+i*unit, y), (x+(i+1)*unit, y), (x+(i+1)*unit, y+0.25), (x+i*unit, y+0.25)], pattern='SOLID', color=7, owner=o)
            self.text(x+i*unit, y-0.32, '%g' % (i*unit), TH_DIM, 'S-TEXT-DIM', 'CENTER', allowed=(o,), owner=o)
        self.text(x+n*unit, y-0.32, '%g %s' % (n*unit, label), TH_DIM, 'S-TEXT-DIM', 'CENTER', allowed=(o,), owner=o)
    def frame(self, scale_note):
        o = 'frame'; W, H, S = SHEET_W, SHEET_H, STRIP
        self.pline([(0,0), (W,0), (W,H), (0,H)], 'S-TITLE', True, owner=o, lineweight=70)
        self.line(0, S, W, S, 'S-TITLE', owner=o)
        for x in (12, 24, 34, 38): self.line(x, 0, x, S, 'S-TITLE', owner=o)
        T = lambda x, y, s, h=TH_DIM, al='LEFT': self.text(x, y, s, h, 'S-TEXT-NOTE', al, allowed=(o,), owner=o)
        T(0.3, 2.45, 'PROJECT', 0.16); T(0.3, 1.75, PROJECT, 0.22); T(0.3, 1.1, SUBTITLE, 0.16); T(0.3, 0.6, 'Client: Regatta Tourist Village, Tripoli   Issued by: Eng. MALEK ABOZRAIG (malek.abozraig@gmail.com)   Units: m', 0.14)
        T(12.3, 2.45, 'SHEET TITLE', 0.16); T(12.3, 1.75, self.title, 0.3); T(12.3, 1.1, scale_note, 0.16); T(12.3, 0.6, 'Status: ISSUED FOR CONSTRUCTION subject to the site verification of S00 section 9', 0.14)
        # revision table
        T(24.3, 2.45, 'REVISIONS', 0.16); ys = 2.2
        self.line(24, 2.25, 34, 2.25, 'S-TITLE', owner=o)
        for r, dte, desc in REVISIONS[::-1]:
            T(24.3, ys-0.32, r, 0.14); T(24.9, ys-0.32, dte, 0.14); T(26.6, ys-0.32, desc, 0.14); ys -= 0.42
            self.line(24, ys, 34, ys, 'S-TITLE', owner=o)
        T(34.3, 2.45, 'CURRENT REVISION', 0.16); T(34.3, 2.05, 'Rev 6a superstructure', 0.14); T(34.3, 1.75, 'Rev 8 bases / bracing Rev 5a', 0.14); T(34.3, 1.35, 'DATE ' + DATE, 0.16); T(34.3, 0.85, 'Drawn: ............   Designed: ............', 0.14); T(34.3, 0.45, 'Checked: ............   Approved: ............', 0.14)
        T(38.3, 2.45, 'DRAWING No.', 0.16); T(38.3, 2.05, 'RTV-ST-' + self.no, 0.2); T(38.3, 0.7, self.no, 1.0)
    def legend_block(self, items, x=None, y=None, w=9.0):
        """items: list of (layer, sample kind, text). Fixed at the bottom-right above the title strip unless given."""
        x = SHEET_W - w - 0.4 if x is None else x; y = STRIP + 0.4 if y is None else y
        n = len(items); h = 0.4*n + 0.6; o = self.nid('leg')
        self.rect(x, y, x+w, y+h, 'S-TITLE', owner=o); self.text(x+0.2, y+h-0.45, 'LEGEND', TH_NOTE, 'S-TEXT-NOTE', allowed=(o,), owner=o)
        yy = y + h - 0.9
        for layer, kind, txt in items:
            if kind == 'line': self.line(x+0.2, yy+0.1, x+1.6, yy+0.1, layer, owner=o)
            elif kind == 'dash': self.line(x+0.2, yy+0.1, x+1.6, yy+0.1, layer, owner=o, linetype='DASHED')
            elif kind == 'box': self.rect(x+0.4, yy-0.05, x+1.4, yy+0.25, layer, owner=o)
            elif kind == 'x': self.line(x+0.4, yy-0.05, x+1.4, yy+0.25, layer, owner=o); self.line(x+0.4, yy+0.25, x+1.4, yy-0.05, layer, owner=o)
            elif kind == 'hatch': self.rect(x+0.4, yy-0.05, x+1.4, yy+0.25, layer, owner=o); self.hatch([(x+0.4, yy-0.05), (x+1.4, yy-0.05), (x+1.4, yy+0.25), (x+0.4, yy+0.25)], scale=0.08, owner=o)
            elif kind == 'bubble': self.circle(x+0.9, yy+0.1, 0.18, 'S-DIM', owner=o)
            self.text(x+1.9, yy, txt, TH_DIM, 'S-TEXT-NOTE', allowed=(o,), owner=o); yy -= 0.4
        return (x, y, x+w, y+h)
    # ---- tables with fitted text
    def table(self, x, y, cols, rows, rh=0.42, h=TH_DIM, header=True, title=None):
        o = self.nid('tab')
        if title: self.text(x, y+0.15, title, TH_NOTE, 'S-TEXT-NOTE', allowed=(o,), owner=o)
        W = sum(w for _, w in cols); n = len(rows) + (1 if header else 0)
        self.rect(x, y-n*rh, x+W, y, 'S-TITLE', owner=o)
        for i in range(1, n): self.line(x, y-i*rh, x+W, y-i*rh, 'S-TITLE', owner=o)
        cx = x
        for _, w in cols[:-1]: cx += w; self.line(cx, y-n*rh, cx, y, 'S-TITLE', owner=o)
        def cell(cx, cy, w, s, hh):
            e = self.raw_text(cx+0.1, cy, str(s), hh, 'S-TEXT-DIM'); b = self.tbox(e); avail = w - 0.2
            if b[2] - b[0] > avail:
                f = avail / (b[2] - b[0]); hh2 = max(0.12, hh*f); e.dxf.height = hh2; b = self.tbox(e)
                s2 = str(s)
                while b[2] - b[0] > avail and len(s2) > 3:
                    s2 = s2[:-2]; e.dxf.text = s2 + '.'; b = self.tbox(e)
            self.reg.add_box(b, o); self.reg.allowed[e.dxf.handle] = {o}; self.texts.append(e)
        yy = y
        if header:
            cx = x
            for name, w in cols: cell(cx, yy-rh*0.7, w, name, h); cx += w
            yy -= rh
        for r in rows:
            cx = x
            for (name, w), v in zip(cols, r): cell(cx, yy-rh*0.7, w, v, h); cx += w
            yy -= rh
        return y - n*rh
    def note_block(self, x, y, title, lines, h=TH_NOTE, width=None, numbered=False):
        """Wrapped note paragraphs; width in sheet units (default to the frame edge). Returns the bottom y."""
        width = width or (SHEET_W - 0.4 - x); o = self.nid('note'); dy = 1.45*h; cpl = max(20, int(width / (0.78*h)))
        if title: self.text(x, y, title, h, 'S-TEXT-NOTE', allowed=(o,), owner=o); y -= dy*1.15
        for i, s in enumerate(lines):
            pre = '%d. ' % (i+1) if numbered else ''
            for j, ln in enumerate(textwrap.wrap(s, cpl - len(pre))):
                self.text(x, y, (pre if j == 0 else ' '*len(pre)) + ln, h, 'S-TEXT-NOTE', allowed=(o,), owner=o); y -= dy
            y -= 0.25*dy
        return y
# ---------------------------------------------------------------- overlap checker
def check_sheet(doc, sh, ox, oy):
    """Independent pass over the DXF: every TEXT (and dimension text) box against every other text box and against
    LINE / LWPOLYLINE / CIRCLE / DIMENSION linework inside the sheet frame; the generator's allowed-owner sets exclude
    a text's own bubble / dimension / table grid / leader. Returns (text_text, text_line, details)."""
    msp = doc.modelspace(); x0, x1, y0, y1 = ox - 0.5, ox + SHEET_W + 0.5, oy - 0.5, oy + SHEET_H + 0.5
    inside = lambda b: b[0] >= x0 and b[2] <= x1 and b[1] >= y0 and b[3] <= y1
    boxes = []; segs = Registry(cell=2.0)
    def add_e(e, owner):
        t = e.dxftype()
        if t == 'LINE': segs.add_seg((e.dxf.start.x, e.dxf.start.y, e.dxf.end.x, e.dxf.end.y), owner)
        elif t == 'LWPOLYLINE':
            P = [(p[0], p[1]) for p in e.get_points()]
            if e.closed: P = P + [P[0]]
            for a, b in zip(P[:-1], P[1:]): segs.add_seg((a[0], a[1], b[0], b[1]), owner)
        elif t == 'CIRCLE':
            c, r = e.dxf.center, e.dxf.radius; pts = [(c.x + r*math.cos(2*math.pi*i/12), c.y + r*math.sin(2*math.pi*i/12)) for i in range(13)]
            for a, b in zip(pts[:-1], pts[1:]): segs.add_seg((a[0], a[1], b[0], b[1]), owner)
    for e in msp:
        t = e.dxftype()
        try: b = _bbox.extents([e]); bb = (b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y)
        except Exception: continue
        if not (bb[0] <= x1 and bb[2] >= x0 and bb[1] <= y1 and bb[3] >= y0): continue
        if t == 'TEXT': boxes.append((bb, e.dxf.handle, e.dxf.text))
        elif t == 'DIMENSION':
            o = 'dim' + e.dxf.handle
            for v in e.virtual_entities():
                if v.dxftype() in ('TEXT', 'MTEXT'):
                    vb = _bbox.extents([v]); boxes.append(((vb.extmin.x, vb.extmin.y, vb.extmax.x, vb.extmax.y), o + 'T', v.dxf.text if v.dxftype() == 'TEXT' else v.text))
                else: add_e(v, o)
        elif t in ('LINE', 'LWPOLYLINE', 'CIRCLE'):
            o = sh.reg.text_owner.get(e.dxf.handle, e.dxf.handle); add_e(e, o)
            if t == 'LWPOLYLINE' and e.closed and e.dxf.layer in FILL_LAYERS and (bb[2]-bb[0])*(bb[3]-bb[1]) <= FILL_MAX_AREA: segs.add_box(bb, o)
        elif t == 'HATCH': segs.add_box(bb, sh.reg.text_owner.get(e.dxf.handle, e.dxf.handle))
    diminfo = {'dim' + e.dxf.handle: tuple(round(v, 1) for v in (e.dxf.defpoint2.x, e.dxf.defpoint2.y, e.dxf.defpoint3.x, e.dxf.defpoint3.y)) for e in msp if e.dxftype() == 'DIMENSION'}
    allowed = sh.reg.allowed; tt = []; tl = []
    breg = Registry(cell=2.0)
    for i, (bb, hd, s) in enumerate(boxes): breg.add_box(bb, i)
    for i, (bb, hd, s) in enumerate(boxes):
        al = allowed.get(hd, set())
        for kind, o in breg.hits(bb, (i,), 0.0):
            if o > i and box_box(bb, boxes[o][0]): tt.append((s[:60], boxes[o][2][:60], tuple(round(v, 2) for v in bb), tuple(round(v, 2) for v in boxes[o][0])))
        for kind, o in segs.hits(bb, al, 0.0):
            if o == hd: continue
            tl.append((s, o, tuple(round(v, 2) for v in bb), diminfo.get(o, '')))
    return len(tt), len(tl), tt, tl

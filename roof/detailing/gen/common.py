import math, ezdxf
from ezdxf.enums import TextEntityAlignment as TA
PROJECT = 'Steel roof over existing slab - Tripoli'
REV = 'Rev 3 superstructure / Rev 4b bases'
DATE = '2026-09-28'
SHEET_W, SHEET_H = 42.0, 30.0
TH, TH_TITLE, TH_SMALL = 0.25, 0.4, 0.18
LAYERS = [('S-COL',5,'CONTINUOUS'),('S-PRIM',1,'CONTINUOUS'),('S-RAFT',3,'CONTINUOUS'),('S-PURL',4,'CONTINUOUS'),
          ('S-BRACE',6,'DASHED'),('S-OPEN',8,'CONTINUOUS'),('S-GRID',9,'CENTER'),('S-DIM',2,'CONTINUOUS'),
          ('S-TEXT',7,'CONTINUOUS'),('S-TITLE',7,'CONTINUOUS'),('S-DETAIL',7,'CONTINUOUS'),('S-HATCH',8,'CONTINUOUS'),
          ('S-DRAIN',4,'DASHDOT'),('S-EXIST',8,'CONTINUOUS')]
def new_doc():
    doc = ezdxf.new('R2013', setup=True)
    doc.header['$INSUNITS'] = 6
    doc.header['$LTSCALE'] = 0.5
    for n, c, lt in LAYERS: doc.layers.add(n, color=c, linetype=lt)
    common = dict(dimtxt=TH, dimasz=0.2, dimexo=0.08, dimexe=0.12, dimgap=0.06, dimtad=1, dimtih=0, dimtoh=0, dimclrt=7, dimclrd=2, dimclre=2, dimtxsty='Standard', dimlwd=-3)
    doc.dimstyles.new('S-M', dxfattribs=dict(common, dimdec=2, dimlfac=1.0, dimzin=0))      # plans: metres, 2 decimals
    doc.dimstyles.new('S-MM', dxfattribs=dict(common, dimdec=0, dimlfac=200.0, dimzin=8))  # details drawn 5x: text = true mm
    doc.dimstyles.new('S-MM1', dxfattribs=dict(common, dimdec=0, dimlfac=1000.0, dimzin=8))  # sections at 1:1: text in mm
    return doc
class Sheet:
    """A 42 x 30 sheet frame at model-space origin (ox, oy); helpers draw in sheet-local coordinates."""
    def __init__(self, msp, ox, oy, no, title, scale_note):
        self.msp, self.ox, self.oy, self.no, self.title = msp, ox, oy, no, title
        self.frame(scale_note)
    def P(self, x, y): return (self.ox + x, self.oy + y)
    def frame(self, scale_note):
        m = self.msp; L = {'layer': 'S-TITLE'}
        m.add_lwpolyline([self.P(0,0), self.P(SHEET_W,0), self.P(SHEET_W,SHEET_H), self.P(0,SHEET_H)], close=True, dxfattribs=dict(L, lineweight=50))
        m.add_line(self.P(0,2.5), self.P(SHEET_W,2.5), dxfattribs=L)
        for x in (14, 28, 36): m.add_line(self.P(x,0), self.P(x,2.5), dxfattribs=L)
        self.text(0.4, 1.9, 'PROJECT', TH_SMALL, layer='S-TITLE'); self.text(0.4, 1.2, PROJECT, 0.32, layer='S-TITLE')
        self.text(0.4, 0.5, 'ALTERNATIVE C - POST-AND-BEAM BRACED STEEL ROOF, SANDWICH PANELS', TH_SMALL, layer='S-TITLE')
        self.text(14.4, 1.9, 'SHEET TITLE', TH_SMALL, layer='S-TITLE'); self.text(14.4, 1.2, self.title, 0.32, layer='S-TITLE')
        self.text(14.4, 0.5, scale_note, TH_SMALL, layer='S-TITLE')
        self.text(28.4, 1.9, 'REVISION', TH_SMALL, layer='S-TITLE'); self.text(28.4, 1.2, REV, 0.22, layer='S-TITLE')
        self.text(28.4, 0.5, 'DATE ' + DATE + '   UNITS m ($INSUNITS 6), dim text mm where noted', TH_SMALL, layer='S-TITLE')
        self.text(36.4, 1.9, 'SHEET NO.', TH_SMALL, layer='S-TITLE'); self.text(36.4, 0.7, self.no, 0.9, layer='S-TITLE')
    def text(self, x, y, s, h=TH, layer='S-TEXT', align='LEFT', rot=0, color=None):
        a = {'LEFT': TA.LEFT, 'CENTER': TA.CENTER, 'RIGHT': TA.RIGHT, 'MIDDLE_CENTER': TA.MIDDLE_CENTER, 'MIDDLE_LEFT': TA.MIDDLE_LEFT, 'MIDDLE_RIGHT': TA.MIDDLE_RIGHT}[align]
        d = {'layer': layer, 'style': 'Standard', 'rotation': rot}
        if color is not None: d['color'] = color
        return self.msp.add_text(s, height=h, dxfattribs=d).set_placement(self.P(x, y), align=a)
    def line(self, x0, y0, x1, y1, layer='S-DETAIL', **kw):
        return self.msp.add_line(self.P(x0,y0), self.P(x1,y1), dxfattribs=dict(layer=layer, **kw))
    def pline(self, pts, layer='S-DETAIL', close=False, **kw):
        return self.msp.add_lwpolyline([self.P(*p) for p in pts], close=close, dxfattribs=dict(layer=layer, **kw))
    def rect(self, x0, y0, x1, y1, layer='S-DETAIL', **kw):
        return self.pline([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], layer, True, **kw)
    def circle(self, x, y, r, layer='S-DETAIL', **kw):
        return self.msp.add_circle(self.P(x,y), r, dxfattribs=dict(layer=layer, **kw))
    def hatch(self, pts, layer='S-HATCH', pattern='ANSI31', scale=0.15, color=8, angle=0):
        h = self.msp.add_hatch(color=color, dxfattribs={'layer': layer})
        if pattern == 'SOLID': h.set_solid_fill(color=color)
        else: h.set_pattern_fill(pattern, scale=scale, angle=angle)
        h.paths.add_polyline_path([self.P(*p) for p in pts], is_closed=True)
        return h
    def dim(self, x0, y0, x1, y1, off, style='S-M', angle=0, text=None):
        """Aligned linear dimension between two local points; off = distance of the dimension line from p1 (signed, normal)."""
        p1, p2 = self.P(x0,y0), self.P(x1,y1)
        if angle == 0: base = (p1[0], p1[1] + off)
        else: base = (p1[0] + off, p1[1])
        d = self.msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=style, override={'dimtxt': TH}, dxfattribs={'layer': 'S-DIM'}, text=text or '<>')
        d.render(); return d
    def dimh(self, x0, x1, y, off, style='S-M', text=None): return self.dim(x0, y, x1, y, off, style, 0, text)
    def dimv(self, y0, y1, x, off, style='S-M', text=None): return self.dim(x, y0, x, y1, off, style, 90, text)
    def bubble(self, x, y, top, bottom='', r=0.55, layer='S-TEXT'):
        self.circle(x, y, r, layer)
        if bottom:
            self.line(x-r, y, x+r, y, layer)
            self.text(x, y+0.08, top, TH, layer, 'CENTER'); self.text(x, y-r*0.5-0.1, bottom, TH_SMALL, layer, 'CENTER')
        else: self.text(x, y, top, TH, layer, 'MIDDLE_CENTER')
    def leader(self, pts, s, h=TH, layer='S-TEXT'):
        self.pline(pts, layer); x, y = pts[-1]; dx = 0.15 if pts[-1][0] >= pts[-2][0] else -0.15
        self.text(x+dx, y+0.05, s, h, layer, 'LEFT' if dx > 0 else 'RIGHT')
    def table(self, x, y, cols, rows, rh=0.42, h=TH_SMALL, header=True, layer='S-TEXT', title=None):
        """cols = [(name, width)], rows = list of lists. Draws grid + text; returns bottom y."""
        if title: self.text(x, y+0.15, title, TH, layer); 
        W = sum(w for _, w in cols); n = len(rows) + (1 if header else 0)
        self.rect(x, y-n*rh, x+W, y, layer)
        for i in range(1, n): self.line(x, y-i*rh, x+W, y-i*rh, layer)
        cx = x
        for _, w in cols[:-1]:
            cx += w; self.line(cx, y-n*rh, cx, y, layer)
        yy = y
        if header:
            cx = x
            for name, w in cols: self.text(cx+0.1, yy-rh*0.68, name, h, layer); cx += w
            yy -= rh
        for r in rows:
            cx = x
            for (name, w), v in zip(cols, r): self.text(cx+0.1, yy-rh*0.68, str(v), h, layer); cx += w
            yy -= rh
        return y - n*rh
    def north_arrow(self, x, y, s=1.2):
        self.pline([(x, y), (x-0.25*s, y-0.35*s), (x, y+s), (x+0.25*s, y-0.35*s)], 'S-TEXT', True)
        self.hatch([(x, y), (x, y+s), (x+0.25*s, y-0.35*s)], pattern='SOLID', color=7)
        self.text(x, y+s+0.15, 'N', 0.4, 'S-TEXT', 'CENTER')
    def note_block(self, x, y, title, lines, h=TH_SMALL, dy=0.3, wrap=None):
        import textwrap
        self.text(x, y, title, TH); yy = y - 0.15
        for s in lines:
            for ln in (textwrap.wrap(s, wrap) if wrap else [s]): yy -= dy; self.text(x, yy, ln, h)
        return yy

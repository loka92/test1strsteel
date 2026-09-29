"""S04 connection details D1-D11 at 5x (Rev 6a sections: IPE 300 / IPE 240 / HEA 140). All annotation through the placer."""
import math, textwrap
from common import *
from geom import *
OX, OY = 210.0, 8.0
K = 0.004
FIT = {}          # detail no -> (K, ox_rel, oy_rel, ytop_mm) from the measuring pass
SHIFT = {'D7': -1.0}   # horizontal shift (m) of a detail inside its frame, for details whose labels all fall on one side
_CUR = [None]
class NullSheet:
    """Sink used for the measuring pass: every Sheet call is a no-op."""
    ox = oy = 0.0
    def __getattr__(self, name): return lambda *a, **k: None
def prep(fn, W=10.2):
    """Run a detail once against a NullSheet to measure its extents (mm), then choose the scale (5x if it fits, else 4x)
    and centre it inside the drawing zone of its frame (zone: fy + 4.0 .. fy + 12.7, side lanes 2.0 m for the labels)."""
    fn(NullSheet(), 0.0, 0.0); d = _CUR[0]
    xmin, xmax, ymin, ymax = d.ext[0] - 40, d.ext[1] + 40, d.ext[2] - 70, d.ext[3] + 200
    w, h = xmax - xmin, ymax - ymin; Kf = 0.005 if (w*0.005 <= W - 5.0 and h*0.005 <= 8.4) else 0.004
    ox = W/2 - Kf*(xmin + xmax)/2 + SHIFT.get(d.no, 0.0); oy = 4.0 + (8.7 - Kf*h)/2 - Kf*ymin
    FIT[d.no] = (Kf, ox, oy, d.ext[3])
class D:
    """Detail frame W x 12.8 with a title strip; drawing coordinates in mm about (ox, oy); labels via the placer (deferred)."""
    def __init__(self, sh, fx, fy, no, title, sub, ox=1100, oy=2050, sheet='S04', W=10.2):
        self.sh, self.fx, self.fy, self.W, self.no = sh, fx, fy, W, no; self.tag = 'det' + no
        self.rec = isinstance(sh, NullSheet); self.ext = [1e9, -1e9, 1e9, -1e9]; _CUR[0] = self
        if no in FIT and not self.rec: self.K, oxr, oyr, self.ytop = FIT[no]; self.ox, self.oy = fx + oxr, fy + oyr
        else: self.K = K; self.ox, self.oy = fx + ox*K, fy + oy*K; self.ytop = 1000
        self.style = 'S-MM5' if abs(self.K - 0.005) < 1e-9 else 'S-MM'
        sh.rect(fx, fy, fx+W, fy+12.8, 'S-TITLE', owner=self.tag, lineweight=35); sh.line(fx, fy+1.6, fx+W, fy+1.6, 'S-TITLE', owner=self.tag); sh.line(fx, fy+3.9, fx+W, fy+3.9, 'S-TITLE', owner=self.tag)
        sh.bubble(fx+0.7, fy+0.85, no, sheet, 0.5); sh.text(fx+1.4, fy+1.0, title, TH_TITLE, 'S-TEXT-NOTE', allowed=(self.tag,), owner=self.tag)
        for i, ln in enumerate(textwrap.wrap(sub, int((W - 1.6)/(0.15*0.8)))[:3]): sh.text(fx+1.4, fy+0.7 - i*0.24, ln, 0.15, 'S-TEXT-NOTE', allowed=(self.tag,), owner=self.tag)
        self.bounds = (fx + 0.1, fy + 4.0, fx + W - 0.1, fy + 12.7)
        if not self.rec: sh.text(fx + W - 0.2, fy + 1.0, 'scale %dx' % round(self.K*1000), 0.16, 'S-TEXT-NOTE', 'RIGHT', allowed=(self.tag,), owner=self.tag)
    def P(self, x, y):
        if self.rec: e = self.ext; e[0] = min(e[0], x); e[1] = max(e[1], x); e[2] = min(e[2], y); e[3] = max(e[3], y)
        return (self.ox + x*self.K, self.oy + y*self.K)
    def spread(self, off):
        """Row offsets 60 / 100 / 140 -> 60 / 140 / 220 (rows clear of each other's text); offsets above 200 are used as given."""
        return off if (abs(off) <= 60 or abs(off) > 200) else math.copysign(60 + (abs(off) - 60)*2.0, off)
    # every geometry element gets its own owner (its handle), so labels are kept clear of ALL linework, own detail included
    def line(self, x0, y0, x1, y1, layer='S-DETAIL', owner=None, **kw): self.sh.line(*self.P(x0,y0), *self.P(x1,y1), layer, owner, **kw)
    def rect(self, x0, y0, x1, y1, layer='S-DETAIL', owner=None, **kw): self.sh.rect(*self.P(x0,y0), *self.P(x1,y1), layer, owner, **kw)
    def pline(self, pts, layer='S-DETAIL', close=False, owner=None, **kw): self.sh.pline([self.P(*p) for p in pts], layer, close, owner, **kw)
    def hatch(self, pts, scale=0.06, color=8, angle=45): self.sh.hatch([self.P(*p) for p in pts], 'S-HATCH', 'ANSI31', scale, color, angle)   # own handle = owner
    def circle(self, x, y, r, layer='S-DETAIL', **kw): self.sh.circle(*self.P(x, y), r*self.K, layer, None, **kw)
    def label(self, x, y, s, h=TH_DIM, rot=0, prefer='R'):
        """Annotation anchored at (x, y) mm; the placer finds a clear spot inside the frame and draws a leader if needed."""
        if prefer == 'R': c = [(0.15, 0.05, 'LEFT'), (0.15, -0.3, 'LEFT'), (0.15, 0.35, 'LEFT'), (0.6, 0.6, 'LEFT'), (0.6, -0.7, 'LEFT'), (-0.15, 0.05, 'RIGHT'), (-0.6, 0.6, 'RIGHT'), (-0.6, -0.7, 'RIGHT'), (1.2, 1.0, 'LEFT'), (1.2, -1.1, 'LEFT'), (-1.2, 1.0, 'RIGHT'), (-1.2, -1.1, 'RIGHT')]
        elif prefer == 'L': c = [(-0.15, 0.05, 'RIGHT'), (-0.15, -0.3, 'RIGHT'), (-0.15, 0.35, 'RIGHT'), (-0.6, 0.6, 'RIGHT'), (-0.6, -0.7, 'RIGHT'), (0.15, 0.05, 'LEFT'), (0.6, 0.6, 'LEFT'), (0.6, -0.7, 'LEFT'), (-1.2, 1.0, 'RIGHT'), (-1.2, -1.1, 'RIGHT'), (1.2, 1.0, 'LEFT'), (1.2, -1.1, 'LEFT')]
        else: c = [(0, 0.15, 'CENTER'), (0, -0.4, 'CENTER'), (0, 0.6, 'CENTER'), (0, -0.85, 'CENTER'), (0.8, 0.6, 'LEFT'), (-0.8, 0.6, 'RIGHT')]
        return self.sh.label(s, *self.P(x, y), h=h, layer='S-TEXT-DIM', rot=rot, cands=c, allowed=(self.tag,), bounds=self.bounds, side=prefer if prefer in ('R', 'L') else None)
    def _short(self, L):
        """Text width (sheet m) of the value and whether the dimension is too short to carry it between its extension lines."""
        w = 0.18*len(str(int(round(abs(L))))) - 0.02; return w, abs(L)*self.K < w + 0.08
    def dimh(self, x0, x1, y, off, out='R'):
        """Horizontal dimension; a value too long for the dimension is written outside, beyond the right (out 'R') or left ('L') end."""
        o = self.spread(off); self.P(x0, y + o); w, short = self._short(x1 - x0); loc = None
        if short:
            xe = max(x0, x1) if out == 'R' else min(x0, x1); sgn = 1 if out == 'R' else -1
            loc = (self.P(xe, 0)[0] - self.ox + sgn*(0.25 + w/2), y*self.K + o*self.K + (0.15 if o > 0 else -0.15)); self.P(xe + sgn*(0.35 + w)/self.K, y)
        self.sh.dimh(self.P(x0,y)[0], self.P(x1,y)[0], self.P(0,y)[1], o*self.K, self.style, loc=(self.ox + loc[0], self.oy + loc[1]) if loc else None, outer=True)
    def dimv(self, y0, y1, x, off, out='T'):
        """Vertical dimension; a value too long for the dimension is written outside, above the top (out 'T') or below the bottom ('B')."""
        o = self.spread(off); self.P(x + o, y0); w, short = self._short(y1 - y0); loc = None
        if short:
            ye = max(y0, y1) if out == 'T' else min(y0, y1); sgn = 1 if out == 'T' else -1
            loc = (x*self.K + o*self.K + (0.15 if o > 0 else -0.15), self.P(0, ye)[1] - self.oy + sgn*(0.25 + w/2)); self.P(x, ye + sgn*(0.35 + w)/self.K)
        self.sh.dimv(self.P(x,y0)[1], self.P(x,y1)[1], self.P(x,0)[0], o*self.K, self.style, loc=(self.ox + loc[0], self.oy + loc[1]) if loc else None, outer=True)
    def iprof(self, cx, yb, h, b, tw, tf, layer, rot=0):
        pts = [(-b/2,0),(b/2,0),(b/2,tf),(tw/2,tf),(tw/2,h-tf),(b/2,h-tf),(b/2,h),(-b/2,h),(-b/2,h-tf),(-tw/2,h-tf),(-tw/2,tf),(-b/2,tf)]
        if rot: pts = [(y - h/2, x) for x, y in pts]
        pts = [(cx+x, yb+y) for x, y in pts]; self.pline(pts, layer, True, lineweight=35); self.hatch(pts)
    def ielev(self, x0, x1, yb, h, tf, layer, slope=0.0):
        dy = (x1-x0)*slope; self.pline([(x0,yb),(x1,yb+dy),(x1,yb+dy+h),(x0,yb+h)], layer, True, lineweight=35)
        self.line(x0, yb+tf, x1, yb+dy+tf, layer); self.line(x0, yb+h-tf, x1, yb+dy+h-tf, layer)
    def bolt(self, x, y, d=20, L=60, vertical=False):
        hh, hw = 0.65*d, 1.6*d
        if not vertical: self.rect(x-L/2, y-d/2, x+L/2, y+d/2); self.rect(x-L/2-hh, y-hw/2, x-L/2, y+hw/2); self.rect(x+L/2, y-hw/2, x+L/2+hh, y+hw/2)
        else: self.rect(x-d/2, y-L/2, x+d/2, y+L/2); self.rect(x-hw/2, y-L/2-hh, x+hw/2, y-L/2); self.rect(x-hw/2, y+L/2, x+hw/2, y+L/2+hh)
    def hole(self, x, y, d=22): self.circle(x, y, d/2); self.line(x-d, y, x+d, y, 'S-GRID'); self.line(x, y-d, x, y+d, 'S-GRID')
    def weld(self, x, y, a, side=1):
        self.pline([(x, y), (x+25*side, y+25), (x+25*side, y)], 'S-DETAIL', True); self.sh.hatch([self.P(x,y), self.P(x+25*side,y+25), self.P(x+25*side,y)], 'S-HATCH', 'SOLID', color=7)
        self.label(x+25*side, y+12, 'a%d' % a, 0.16, prefer='R' if side > 0 else 'L')
    def title(self, row, s, y=None):
        """View caption: placed by the placer near the top of the view (row 1) or at the second view (row 2)."""
        y = ((self.ytop + 50) if row == 1 else -120) if y is None else y
        if self.rec:
            if row != 1: self.P(-700, y)
            return None
        return self.sh.label(s, self.ox - 700*self.K, self.oy + y*self.K, h=TH_DIM, layer='S-TEXT-NOTE', cands=[(0, 0, 'LEFT'), (0, 0.3, 'LEFT'), (0, -0.3, 'LEFT'), (0, 0.6, 'LEFT'), (0, -0.6, 'LEFT'), (0, 0.9, 'LEFT'), (0, -0.9, 'LEFT'), (0, 1.2, 'LEFT'), (0, -1.2, 'LEFT')], allowed=(self.tag,), leader=False, bounds=self.bounds)
    def notes(self, lines):
        """Note lines in the geometry-free band between the title strip and the drawing zone."""
        yy = self.fy + 3.65
        for s in lines:
            for ln in textwrap.wrap(s, int((self.W - 0.4)/(0.14*0.8))):
                if yy < self.fy + 1.75: return
                self.sh.text(self.fx+0.2, yy, ln, 0.14, 'S-TEXT-NOTE', allowed=(self.tag,), owner=self.tag); yy -= 0.235
# ---------------------------------------------------------------- details (mm; drawing origin at the frame's (700, 1500) mm)
def d1(sh, fx, fy):
    d = D(sh, fx, fy, 'D1', 'FIN PLATES', 'FP1 100x150x10 2 M20 8.8; FP2 160x150x10 2x2 M20 (p2 60) at the strip-chord splices R1/R3/R9/R11; IPE 240 to IPE 300 web')
    d.title(1, 'SECTION along the primary, top TOS + 30'); s = math.tan(math.radians(3.43))
    d.iprof(150, 0, 300, 150, 7.1, 10.7, 'S-PRIM'); d.label(150, 0, 'IPE 300 (level)', prefer='C')
    d.ielev(163.5, 640, 30, 240, 9.8, 'S-RAFT', slope=-s); d.label(500, 150, 'IPE 240, plumb cut')
    d.rect(153.5, 75, 253.5, 225, 'S-DETAIL', lineweight=50); d.label(253.5, 225, 'FP1 100x150x10')
    for y in (115, 185): d.bolt(203.5, y, 20, 40)
    d.weld(153.5, 225, 6, 1)
    d.dimv(75, 225, 75, -60); d.dimh(153.5, 253.5, 75, -100); d.dimv(0, 300, -60, -140)
    d.label(640, 30, 'rafter bottom +30', prefer='R')
    d.title(2, 'PLAN at the primary web: FP2 two-row plate', y=-300); y0 = -680
    d.line(-60, y0, 700, y0, 'S-PRIM', lineweight=35); d.line(-60, y0+75, 700, y0+75, 'S-PRIM'); d.line(-60, y0-75, 700, y0-75, 'S-PRIM'); d.label(-60, y0+75, 'primary web / flanges', prefer='R')
    for sgn in (1, -1):
        d.rect(240, y0+sgn*3.55, 400, y0+sgn*13.55, 'S-DETAIL', lineweight=50)
        d.line(320-3.1, y0+sgn*13.55, 320-3.1, y0+sgn*330, 'S-RAFT', lineweight=35); d.line(320+3.1, y0+sgn*13.55, 320+3.1, y0+sgn*330, 'S-RAFT', lineweight=35)
        d.line(320-60, y0+sgn*13.55, 320-60, y0+sgn*330, 'S-RAFT'); d.line(320+60, y0+sgn*13.55, 320+60, y0+sgn*330, 'S-RAFT')
        for x in (290, 350): d.rect(x-16, y0+sgn*13.55, x+16, y0+sgn*27, 'S-DETAIL'); d.rect(x-16, y0+sgn*3.55, x+16, y0-sgn*9, 'S-DETAIL')
    d.label(320, y0+330, 'rafter (north piece)', prefer='C'); d.label(320, y0-330, 'rafter (south piece)', prefer='C')
    d.dimh(290, 350, y0+13.55, 340, out='L'); d.dimh(240, 400, y0+13.55, 410)
    d.notes(['M20 8.8 in 22 round holes, snug tight, PLAIN plates (no slots); FP1 bolts e 40 / p 70. FP1 at every rafter / primary junction; FP2 (2 x 2 M20, p2 60) where the rafter is a strip chord: R1, R3, R9, R11; R5 strut splice FP1 (0.55).',
             'Web bearing on the 6.2 mm IPE 240 web governs: 64.6 kN per M20 (one row), 54.8 kN (two rows); max gravity reaction 21.3 kN (0.29). Force passes plate - weld - primary web - weld - plate.'])
def d2(sh, fx, fy):
    d = D(sh, fx, fy, 'D2', 'CAP PLATE', 'HEA 140 cap plate 200x280x20, a6 all round; 4 M20 8.8 through the IPE 300 bottom flange, gauge 90, pitch 200 (nuts clear the rafter flange)')
    d.title(1, 'ELEVATION normal to the primary (end column)')
    d.rect(-70, 0, 70, 480, 'S-COL', lineweight=35); d.label(70, 240, 'HEA 140 column (flange 140)')
    d.rect(-140, 480, 140, 500, 'S-DETAIL', lineweight=50); d.weld(70, 480, 6, 1); d.weld(-70, 480, 6, -1)
    d.ielev(-320, 320, 500, 300, 10.7, 'S-PRIM'); d.label(320, 800, 'IPE 300, level, no pack')
    for x in (-100, 100): d.bolt(x, 500, 20, 32, True)
    d.dimh(-100, 100, 800, 60); d.dimh(-140, 140, 800, 100); d.dimv(500, 800, 320, 60); d.dimv(0, 480, -160, -60)
    d.label(-140, 480, 'cap top = TOS - 270', prefer='L')
    d.title(2, 'PLAN of the cap plate'); y0 = -480
    d.rect(-140, y0-100, 140, y0+100, 'S-DETAIL', lineweight=50); d.rect(-66.5, y0-70, 66.5, y0+70, 'S-COL', linetype='DASHED'); d.label(-66.5, y0+70, 'HEA 140 below', prefer='L')
    d.line(-320, y0-75, 320, y0-75, 'S-PRIM'); d.line(-320, y0+75, 320, y0+75, 'S-PRIM'); d.line(-320, y0, 320, y0, 'S-PRIM', linetype='DASHED')
    for x in (-100, 100):
        for y in (-45, 45): d.hole(x, y0+y, 22)
    d.dimh(-100, 100, y0-100, -60); d.dimh(-140, 140, y0-100, -100); d.dimv(y0-45, y0+45, 320, 60); d.dimv(y0-100, y0+100, 320, 100)
    d.notes(['Cap plate 200 x 280 x 20 S275, holes 22; bolt rows 33 mm outside the 133 column depth (cantilever 0.11). Tension 44.6 kN (K12 uplift): bolt 0.08, flange T-stub 0.12; chord force 70.2 kN: interaction 0.24.',
             'Primaries bolted before the rafters are landed. No stiffeners. Slope is in the rafters only; primaries and cap plates are level.'])
def d3(sh, fx, fy):
    d = D(sh, fx, fy, 'D3', 'CHORD TIE', 'Primary continuity over an interior column (rows F and B): 10 mm tie plate 140 x 400 under both primary ends; gap 20')
    d.title(1, 'ELEVATION along the primary row')
    d.rect(-70, 0, 70, 480, 'S-COL', lineweight=35); d.rect(-140, 480, 140, 500, 'S-DETAIL', lineweight=50)
    d.rect(-200, 500, 200, 510, 'S-DETAIL', lineweight=50); d.label(-200, 505, 'tie plate 140x400x10', prefer='L')
    d.ielev(-420, -10, 510, 300, 10.7, 'S-PRIM'); d.ielev(10, 420, 510, 300, 10.7, 'S-PRIM'); d.label(-215, 810, 'primary end', prefer='C'); d.label(215, 810, 'primary end', prefer='C')
    for x in (-100, 100): d.bolt(x, 505, 20, 42, True)
    d.label(0, 810, 'gap 20', prefer='C'); d.dimh(-100, 100, 810, 60); d.dimh(-200, 200, 810, 100)
    d.title(2, 'PLAN: rafter continuity through the primary web'); y0 = -520
    d.line(-380, y0, 380, y0, 'S-PRIM', lineweight=35); d.line(-380, y0+75, 380, y0+75, 'S-PRIM'); d.line(-380, y0-75, 380, y0-75, 'S-PRIM')
    d.rect(-140, y0-100, 140, y0+100, 'S-DETAIL', linetype='DASHED'); d.label(-140, y0+100, 'cap plate below', prefer='L')
    for sgn in (1, -1):
        d.rect(250, y0+sgn*3.55, 350, y0+sgn*13.55, 'S-DETAIL', lineweight=50)
        d.line(300-60, y0+sgn*13.55, 300-60, y0+sgn*330, 'S-RAFT'); d.line(300+60, y0+sgn*13.55, 300+60, y0+sgn*330, 'S-RAFT'); d.line(300, y0+sgn*13.55, 300, y0+sgn*330, 'S-RAFT', lineweight=35)
    d.label(300, y0+330, 'rafter', prefer='C'); d.label(300, y0-330, 'rafter', prefer='C')
    d.notes(['Chord force <= 70 kN passes through the tie plate and the 4 M20 (2 per primary end); rafter strut force through the fin plates and the primary web. Rows A / G / H (eave beams): no tie plate.'])
def d4(sh, fx, fy):
    d = D(sh, fx, fy, 'D4', 'BRACE GUSSET', 'L70x7 tension-only diagonals, 10 mm gusset welded a6 to the column flange and the base plate (eave: cap-plate underside); 2 M20 8.8 per angle end')
    d.title(1, 'ELEVATION in the wall plane, column base')
    d.line(-150, 0, 700, 0, 'S-EXIST', lineweight=35); d.rect(-150, 25, 250, 45, 'S-COL', lineweight=50); d.rect(-150, 0, 250, 25, 'S-HATCH'); d.label(-150, 12, 'grout 25', prefer='L')
    d.rect(-70, 45, 70, 900, 'S-COL', lineweight=35); d.label(-70, 600, 'HEA 140 flange 140', prefer='L')
    ang = math.atan2(3.8, 5.0); c, s = math.cos(ang), math.sin(ang)
    d.pline([(70, 45), (70, 420), (150, 420), (460, 45)], 'S-DETAIL', True, lineweight=50); d.label(150, 420, 'gusset 10 mm')
    d.weld(70, 300, 6, 1); d.weld(300, 45, 6, 1)
    p0 = (170, 110); L = 700
    al = lambda t, o=0: (p0[0] + t*c - o*s, p0[1] + t*s + o*c)
    d.pline([al(0), al(L), al(L, 70), al(0, 70)], 'S-BRACE', True, lineweight=35); d.label(*al(500, 70), 'L70x7 diagonal')
    for t in (40, 150): d.hole(*al(t, 30), 22)
    d.label(*al(220, -10), 'e1 40, p1 110, e2 30', prefer='R'); d.line(0, 45, 0, -90, 'S-GRID'); d.label(0, -90, 'column CL', prefer='C')
    d.dimv(45, 420, -220, -60); d.dimh(70, 460, 45, -160)
    d.notes(['Gusset 10 mm S275 in the wall plane; angle net section 189 kN, 2 M20 shear 188 kN, gusset bearing 2 x 124 kN; max T_Ed 76.1 kN (B7) -> 0.41. Diagonal centrelines meet at the column CL at base-plate top and at the primary centre.',
             'X in every bay: both diagonals, crossing clipped with a 10 mm plate and 1 M16. Eave gusset: same plate welded to the column flange and the cap-plate underside.'])
def d5(sh, fx, fy):
    d = D(sh, fx, fy, 'D5', 'ROOF ROD GUSSET', 'M24 8.8 rods with turnbuckles; 8 mm gusset SHOP-welded a5 to the primary web, BOLTED 2 M16 to the rafter web; combined gusset RG-C at the NE corner')
    d.title(1, 'PLAN at a panel corner')
    d.line(-100, 0, 700, 0, 'S-PRIM', lineweight=35); d.line(-100, 75, 700, 75, 'S-PRIM'); d.line(-100, -75, 700, -75, 'S-PRIM'); d.label(600, 75, 'primary IPE 300', prefer='R')
    d.line(0, 0, 0, 700, 'S-RAFT', lineweight=35); d.line(-60, 13.55, -60, 700, 'S-RAFT'); d.line(60, 13.55, 60, 700, 'S-RAFT'); d.label(60, 650, 'rafter IPE 240')
    d.pline([(3.55, 3.1), (250, 3.1), (250, 60), (60, 250), (3.55, 250)], 'S-DETAIL', True, lineweight=50); d.label(250, 60, 'gusset 8, a5 to the primary')
    d.rect(3.1, 60, 30, 250, 'S-DETAIL', lineweight=35); d.label(30, 250, 'leg 2 M16 to the rafter web')
    for y in (110, 200): d.bolt(16, y, 16, 34)
    ang = math.atan2(5.9, 2.65); c, s = math.cos(ang), math.sin(ang); p = (135, 110); L = 500
    d.pline([(p[0]-12*s, p[1]+12*c), (p[0]+L*c-12*s, p[1]+L*s+12*c), (p[0]+L*c+12*s, p[1]+L*s-12*c), (p[0]+12*s, p[1]-12*c)], 'S-BRACE', True, lineweight=35)
    d.hole(p[0], p[1], 26); d.label(p[0], p[1], 'hole 26, nut + lock nut', prefer='R')
    tb = (p[0]+300*c, p[1]+300*s); d.pline([(tb[0]-60*c-22*s, tb[1]-60*s+22*c), (tb[0]+60*c-22*s, tb[1]+60*s+22*c), (tb[0]+60*c+22*s, tb[1]+60*s-22*c), (tb[0]-60*c+22*s, tb[1]-60*s-22*c)], 'S-BRACE', True, lineweight=35)
    d.label(tb[0]+22*s, tb[1], 'turnbuckle M24')
    d.rect(320, 250, 420, 420, 'S-RAFT', linetype='DASHED'); d.circle(370, 335, 30); d.label(420, 420, 'web hole 60 + ring 8')
    d.dimh(0, 250, 3.1, -380); d.dimv(3.1, 250, -140, -100); d.dimh(0, p[0], -75, -60, out='L'); d.dimv(0, p[1], -140, -60, out='B')
    d.notes(['Rods M24 8.8 (F_t,Rd 203 kN), max T 80.8 kN (RT-JOG, 0.40); gussets only at the 13 panel corners (RG). RG-C at C2, C4, C13, C14: one 10 mm gusset carries both rod sets (RT-N-E + RT-E, 59.6 + 0.3 x 53.1 kN), 2 M20 per rod end.',
             'No site welding on galvanised steel. RT-W / RT-E rods span two rafter cells: R2 / R10 passed through a bolted web clip; sag ties to the purlins at the crossing and at 3 m.'])
def d6(sh, fx, fy):
    d = D(sh, fx, fy, 'D6', 'WELL UPSTAND', 'T2 IPE 240 trimmer on FP1 to R5/R6; C100x50x3 upstand 150 above the panel; cap flashing and panel stop; same on R5/R6 and P8 (cricket side 270-300)')
    d.title(1, 'SECTION across trimmer T2, looking east')
    d.iprof(0, 0, 240, 120, 6.2, 9.8, 'S-RAFT'); d.label(0, 0, 'trimmer T2 IPE 240', prefer='C')
    d.rect(-200, 240, 200, 255, 'S-DETAIL'); d.label(-200, 247, 'seat plate 15', prefer='L')
    d.rect(-50, 255, 50, 655, 'S-DETAIL', lineweight=50); d.label(50, 500, 'upstand C100x50x3')
    d.label(-50, 262, '2 M12 to the seat', prefer='L')
    d.rect(60, 255, 130, 455, 'S-PURL'); d.label(130, 330, 'edge purlin Z200')
    d.rect(60, 455, 500, 505, 'S-DETAIL', lineweight=35); d.label(300, 505, 'PIR panel 50', prefer='C')
    d.pline([(200, 515), (60, 515), (60, 670), (-60, 670), (-60, 610), (-80, 610)], 'S-DETAIL', lineweight=35); d.label(60, 670, 'cap flashing 0.7')
    d.rect(50, 505, 60, 660, 'S-DETAIL'); d.label(-60, 610, 'panel stop / closer', prefer='L')
    d.dimv(505, 655, 250, 60); d.dimv(255, 455, 200, 60); d.dimv(0, 240, -150, -60); d.dimh(-50, 50, 255, -110)
    d.label(-460, 120, 'WELL (open)', prefer='R'); d.label(300, 120, 'ROOF', prefer='R')
    d.notes(['Upstand >= 150 above the panel top on all sides of both wells; soakers at panel seams; well-side face lined with the same coated sheet. Stair well: open to the north face (no trimmer); cricket on P8 (ridge 120, upstand 270-300).'])
def d7(sh, fx, fy):
    d = D(sh, fx, fy, 'D7', 'EAVE GUTTER', 'Rafter end, eave rail C200x60x2.5, brackets 40x5 @ 600, box gutter 150x100, fascia, first purlin, panel; two runs G-W (y 35.37) / G-E (y 35.87)')
    d.title(1, 'SECTION at the north eave, north on the right'); s = math.tan(math.radians(3.43))
    d.iprof(0, 0, 300, 150, 7.1, 10.7, 'S-PRIM'); d.label(0, 0, 'P4 IPE 300 on C1', prefer='C')
    d.rect(-70, -400, 70, -320, 'S-COL', lineweight=35); d.label(70, -360, 'HEA 140 (D2)')
    d.ielev(-600, 100, 30+600*s, 240, 9.8, 'S-RAFT', slope=-s); d.label(-350, 150, 'rafter ends +100', prefer='C')
    yt = 30 + 240 - 100*s
    d.rect(100, yt-200, 102.5, yt+5, 'S-PURL', lineweight=35); d.line(100, yt+5, 160, yt+5, 'S-PURL', lineweight=35); d.line(100, yt-200, 160, yt-200, 'S-PURL', lineweight=35); d.label(160, yt-100, 'eave rail C200x60x2.5, 2 M12')
    d.rect(-330, yt-10, -260, yt+190, 'S-PURL'); d.label(-260, yt+100, 'purlin Z200 @ 300', prefer='L')
    d.line(-600, yt+190+600*s, 250, yt+190-150*s, 'S-DETAIL', lineweight=35); d.line(-600, yt+240+600*s, 250, yt+240-150*s, 'S-DETAIL', lineweight=35); d.label(-450, yt+240+450*s, 'PIR panel 50', prefer='L')
    d.pline([(250, yt+240), (270, yt+240), (270, yt+120)], 'S-DETAIL'); d.label(270, yt+240, 'drip flashing 0.7, lap 60')
    d.pline([(160, yt-20), (200, yt-20), (200, yt+60), (360, yt+60), (360, yt+150)], 'S-DETAIL', lineweight=35); d.label(200, yt-20, 'bracket 40x5 @ 600')
    d.pline([(200, yt+140), (200, yt+40), (350, yt+40), (350, yt+130)], 'S-DRAIN', lineweight=50); d.label(275, yt+40, 'box gutter 150x100', prefer='C')
    d.rect(100, yt-330, 106, yt+60, 'S-DETAIL'); d.label(106, yt-300, 'fascia flashing')
    d.rect(70, -400, 120, yt-330, 'S-DETAIL'); d.label(120, -200, 'BoardX wall (D9)')
    d.rect(-40, -300, 30, -100, 'S-PURL'); d.label(-40, -200, 'top girt Z200', prefer='L')
    d.dimh(200, 350, yt+40, -180); d.dimv(yt+40, yt+140, 380, 60); d.dimh(-300, 100, 300, 330); d.dimv(0, 300, -650, -60)
    d.notes(['Gutter 0.7 galvanised + polyester (or 1.0 alu), riveted + butyl joints, fall 1:350 to DP1-DP4, EPDM expansion joint at each high point; stop ends and overflow spouts 100x30 at x 67.89 / 77.89 / 81.79 / 95.69.',
             'Loads 0.25 kN/m gravity, -0.50 kN/m uplift (zone F), 0.5 kN point at any bracket; fixed brackets at the outlets, sliding elsewhere. Rafters R1-R5 cantilever 0.10 past P1/P2 to y 35.37.'])
def d8(sh, fx, fy):
    d = D(sh, fx, fy, 'D8', 'PURLIN CLEAT', 'Z200x2.0 on a plate cleat 120x160x8, 2 M12; fly brace L50x5 from the rafter bottom flange to the purlin; anti-sag row at mid-span')
    d.title(1, 'SECTION across the rafter (looking north)')
    d.iprof(0, 0, 240, 120, 6.2, 9.8, 'S-RAFT'); d.label(0, 0, 'rafter IPE 240', prefer='C')
    d.rect(-4, 240, 4, 400, 'S-DETAIL', lineweight=50); d.rect(-60, 240, 60, 248, 'S-DETAIL', lineweight=50); d.label(4, 400, 'cleat 120x160x8, a4')
    d.pline([(4, 248), (4, 448), (74, 448), (74, 432), (20, 432), (20, 264), (-66, 264), (-66, 248)], 'S-PURL', True, lineweight=35); d.label(74, 448, 'Z200x2.0 purlin')
    for y in (300, 370): d.bolt(4, y, 12, 26)
    d.rect(-400, 448, 400, 498, 'S-DETAIL', lineweight=35); d.label(-400, 498, 'PIR panel 50', prefer='L')
    d.line(-60, 12, -300, 300, 'S-BRACE', lineweight=50); d.line(-75, 22, -315, 310, 'S-BRACE', lineweight=50); d.label(-315, 310, 'fly brace L50x5', prefer='L')
    d.bolt(-60, 6, 12, 22, True); d.hole(-300, 300, 14)
    d.dimv(240, 448, 100, 60); d.dimv(0, 240, -150, -60); d.dimh(-60, 60, 0, -60)
    d.notes(['Purlins simple span between rafters @ 1.5 m, one mid-span anti-sag row per span; fly braces at mid-span (L <= 6.6 m) and third points (7.5 / 9.2 m). Cleat uplift ~11 kN in zone F: 2 M12 8.8 (0.35). Supplier uplift capacity >= 9 kNm before order.'])
def d9(sh, fx, fy):
    d = D(sh, fx, fy, 'D9', 'GIRT, PANEL', 'Z200x2.0 girt on an L100x100x8 x 150 cleat to the column flange (2 M12); BoardX panel on the girt outer flange, screws @ 300')
    d.title(1, 'PLAN SECTION at a wall column, wall face below')
    d.iprof(0, 0, 133, 140, 5.5, 8.5, 'S-COL', rot=1); d.label(0, 66, 'HEA 140, web normal to the wall', prefer='C')
    d.pline([(-70, -70), (-70, -170), (-62, -170), (-62, -78), (20, -78), (20, -70)], 'S-DETAIL', True, lineweight=50); d.label(20, -100, 'cleat L100x100x8 x150')
    d.bolt(-66, -120, 12, 26)
    d.rect(-400, -170, 400, -168, 'S-PURL'); d.rect(-400, -240, 400, -238, 'S-PURL'); d.label(-400, -200, 'girt Z200x2.0', prefer='L')
    d.rect(-400, -240, 400, -290, 'S-DETAIL', lineweight=35); d.label(-400, -290, 'BoardX panel 50', prefer='L')
    d.line(-420, -290, 420, -290, 'S-DETAIL'); d.label(420, -300, 'outside')
    for x in (-250, 250): d.line(x, -240, x, -290, 'S-DETAIL', linetype='DASHED')
    d.label(250, -290, 'screws @ 300', prefer='R')
    d.dimv(-70, -290, 400, 60); d.dimh(-70, 70, 66, 60)
    d.notes(['Girts span column to column (sleeved on the 1.0 / 1.2 m rows K5-K7, K25-K19, K8-K6, K21-K22, K22-K23, K14-K4); rows 1.5 m elsewhere; bottom row 0.50 above the slab (sill D11), top row 150 below the eave beam; corner columns cleats on both flanges. Cleat bolts M12 8.8.'])
def d10(sh, fx, fy):
    d = D(sh, fx, fy, 'D10', 'WIND POST', 'HEA 140 at (77.61, 20.25), 280 inboard of the notch corner: slotted head to eave beam P14 (2 M20 in 22x60 slots); base 250x250x15, one dia 60 key, 2 M12')
    d.title(1, 'HEAD - elevation, P14 in section')
    d.iprof(0, 300, 300, 150, 7.1, 10.7, 'S-PRIM'); d.label(0, 600, 'P14 IPE 300 (eave beam, FP1 to R5)', prefer='C')
    d.rect(-70, -200, 70, 250, 'S-COL', lineweight=35); d.line(0, -200, 0, 250, 'S-COL'); d.label(70, -100, 'WP1 HEA 140')
    d.rect(-60, 100, 60, 300, 'S-DETAIL', lineweight=50); d.label(60, 200, 'cleat 120x200x10, a6 to P14')
    for y in (140, 220): d.rect(-11, y-30, 11, y+30); d.bolt(0, y, 20, 40)
    d.label(-11, 140, '2 M20 in 22x60 slots, snug', prefer='L')
    d.dimv(100, 300, -150, -60)
    d.title(2, 'BASE - plan at the notch corner', y=-300); y0 = -800
    d.line(-450, y0, 350, y0, 'S-EXIST', lineweight=35); d.line(-450, y0, -450, y0+450, 'S-EXIST', lineweight=35); d.label(-450, y0+450, 'slab edges', prefer='R')
    d.rect(-450, y0-60, 350, y0, 'S-EXIST', linetype='DASHED'); d.label(-100, y0-60, 'edge beam (GPR)', prefer='R')
    d.rect(-295, y0+155, -45, y0+405, 'S-DETAIL', lineweight=50); d.label(-45, y0+405, 'plate 250x250x15, key dia 60')
    d.rect(-236.5, y0+210, -103.5, y0+350, 'S-COL', linetype='DASHED'); d.circle(-170, y0+280, 30, lineweight=35)
    for x in (-270, -70): d.hole(x, y0+180, 14)
    d.dimh(-450, -170, y0+155, -60); d.dimv(y0, y0+280, -20, 60); d.dimh(-270, -70, y0+180, 260)
    d.notes(['Post centre 280 mm inboard of both slab edges: single dia 60 key with c1 = 250 both ways (41.9 kN vs 11.4 / 8.5 kN, 0.27); 2 M12 for location only; corner girts cantilever 280 to the wall line. Notch edge beam by GPR (else two Key B).'])
def d11(sh, fx, fy):
    d = D(sh, fx, fy, 'D11', 'WALL SILL', 'BoardX wall base at the slab edge: C100x50x3 sill rail on the slab, M8 anchors @ 600, drip flashing; bottom girt 0.50 above; well walls hall-side: blockwork (architect)')
    d.title(1, 'SECTION at the slab edge, outside left')
    d.line(-200, 0, 500, 0, 'S-EXIST', lineweight=35); d.line(-200, -300, 500, -300, 'S-EXIST', lineweight=35); d.line(-200, 0, -200, -300, 'S-EXIST', lineweight=50)
    d.hatch([(-200,-300),(500,-300),(500,0),(-200,0)], 0.12, 8, 45); d.label(400, -300, 'existing slab 300', prefer='C')
    d.pline([(-100, 0), (-100, 100), (-50, 100), (-50, 3), (-3, 3), (-3, 0)], 'S-PURL', True, lineweight=35); d.label(-3, 60, 'sill rail C100x50x3 on DPC')
    d.bolt(-75, 0, 8, 20, True); d.label(-75, 100, 'M8 anchors @ 600', prefer='L')
    d.rect(-150, 100, -100, 1100, 'S-DETAIL', lineweight=35); d.label(-150, 500, 'BoardX panel 50', prefer='L')
    d.rect(-100, 500, -30, 700, 'S-PURL'); d.label(-30, 600, 'bottom girt Z200 at 0.50 (D9)')
    d.pline([(-160, 130), (-170, 130), (-170, 60), (-160, 50)], 'S-DETAIL', lineweight=35); d.label(-170, 130, 'drip flashing 0.7', prefer='L')
    d.dimh(-200, -100, -300, -60); d.dimv(0, 100, -100, -60); d.dimv(0, 500, 60, 60)
    d.rect(-70, 45, -30, 500, 'S-COL', linetype='DASHED'); d.label(-30, 300, 'HEA 140 beyond (S05)')
    d.notes(['Wall base line 100 mm inside the slab face on all faces; panel bottom 100 above the slab; the sill carries the panel weight to the slab and closes the wall against water (drip outside). Hall-side well walls: blockwork on the existing well walls, by the architect.'])
def dnotes(sh, fx, fy):
    d = D(sh, fx, fy, 'GN', 'NOTES', 'General notes for D1-D11; see S00 for materials, bolts, welding, galvanising and tolerances', W=10.2)
    lines = ['Steel S275 J0; bolts 8.8 hot-dip galvanised, snug tight (no preload relied upon); M20 in 22 holes, M16 in 18, M12 in 14, M24 rods in 26; all holes round (no slots).',
             'Shop fillet welds a5-a8 as noted (E42 / S275 consumables). NO site welding on galvanised steel: rod gussets shop-welded to the primaries and bolted to the rafters (D5).',
             'Thermal: +/-30 K service, +45/-25 K erection; the E-W path B2 - RT-N-W - row F chord - RT-N-E - B1 carries 15 kN (wind) / 37 kN (erection) locked-in; designed for, no slotted holes.',
             'Rafter ends plumb-cut, no copes; primaries level on level cap plates (primary top TOS + 30, rafter top TOS); slope 6 % in the rafters only.',
             'Precamber 10-15 mm on the 9.2 m rafters R7-R10 (south spans) per design report Rev 6a; none on P13 (IPE 330).',
             'Fly braces at mid-span (L <= 6.6 m) and third points (7.5 / 9.2 m); anti-sag row at mid-span of every purlin span; purlin cleats 2 M12 8.8 (uplift ~11 kN, zone F).',
             'Erection: temporary plan bracing (crossed wire ropes or angles) in one rafter cell of each south band until the panels and purlin bridging are complete (S00 section 8).']
    yy = fy + 12.4
    for s in lines:
        for ln in textwrap.wrap(s, 76): sh.text(fx+0.2, yy, ln, 0.16, 'S-TEXT-NOTE', allowed=(d.tag,), owner=d.tag); yy -= 0.26
        yy -= 0.12
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S04', 'CONNECTION DETAILS D1 - D8', 'Details drawn 4x or 5x in model space (scale in each frame); DIMENSION text = true mm (dimlfac 250 / 200)')
    for i, f in enumerate([d1, d2, d3, d4, d5, d6, d7, d8]):
        r, c = divmod(i, 4); prep(f); f(sh, 0.3 + c*10.35, 16.4 - r*13.2)
    return sh

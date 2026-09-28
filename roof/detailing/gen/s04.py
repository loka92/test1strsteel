"""S04 connection details D1-D10, drawn 10x (1 m model = 100 mm real), dimension text in true mm (dimlfac 100)."""
import math
from common import *
from geom import *
OX, OY = 210.0, 8.0
import textwrap
K = 0.005    # model units per mm at 5x (1 m model = 200 mm real)
class D:
    """Detail frame; coordinates in mm relative to the frame's drawing origin."""
    def __init__(self, sh, fx, fy, no, title, sub, ox=700, oy=1400, sheet='S04', W=6.8):
        self.sh, self.fx, self.fy, self.W = sh, fx, fy, W; self.ox, self.oy = fx + ox*K, fy + oy*K
        sh.rect(fx, fy, fx+W, fy+12.8, 'S-DETAIL', lineweight=35); sh.line(fx, fy+1.4, fx+W, fy+1.4, 'S-DETAIL')
        sh.bubble(fx+0.7, fy+0.95, no, sheet, 0.5); sh.text(fx+1.4, fy+0.82, title, TH_TITLE, 'S-TEXT')
        for i, ln in enumerate(textwrap.wrap(sub, int(66*W/8.2))[:2]): sh.text(fx+1.4, fy+0.42 - i*0.26, ln, 0.14)
    def P(self, x, y): return (self.ox + x*K, self.oy + y*K)
    def line(self, x0, y0, x1, y1, layer='S-DETAIL', **kw): self.sh.line(*self.P(x0,y0), *self.P(x1,y1), layer, **kw)
    def rect(self, x0, y0, x1, y1, layer='S-DETAIL', **kw): self.sh.rect(*self.P(x0,y0), *self.P(x1,y1), layer, **kw)
    def pline(self, pts, layer='S-DETAIL', close=False, **kw): self.sh.pline([self.P(*p) for p in pts], layer, close, **kw)
    def hatch(self, pts, scale=0.06, color=8, angle=45): self.sh.hatch([self.P(*p) for p in pts], 'S-HATCH', 'ANSI31', scale, color, angle)
    def text(self, x, y, s, h=TH_SMALL, align='LEFT', rot=0, layer='S-TEXT'):
        px, py = self.P(x, y)
        if rot:
            self.sh.text(px, py, s, h, layer, align, rot); return 1
        if align == 'LEFT': avail = self.fx + self.W - 0.1 - px
        elif align == 'RIGHT': avail = px - self.fx - 0.1
        else: avail = 2*min(px - self.fx - 0.1, self.fx + self.W - 0.1 - px)
        n = max(10, int(avail/(h*0.72)))
        lines = textwrap.wrap(s, n) or ['']
        for i, ln in enumerate(lines): self.sh.text(px, py - i*1.5*h, ln, h, layer, align)
        return len(lines)
    def dimh(self, x0, x1, y, off): self.sh.dimh(self.P(x0,y)[0], self.P(x1,y)[0], self.P(0,y)[1], off*K, 'S-MM')
    def dimv(self, y0, y1, x, off): self.sh.dimv(self.P(x,y0)[1], self.P(x,y1)[1], self.P(x,0)[0], off*K, 'S-MM')
    def iprof(self, cx, yb, h, b, tw, tf, layer, rot=0):
        pts = [(-b/2,0),(b/2,0),(b/2,tf),(tw/2,tf),(tw/2,h-tf),(b/2,h-tf),(b/2,h),(-b/2,h),(-b/2,h-tf),(-tw/2,h-tf),(-tw/2,tf),(-b/2,tf)]
        if rot: pts = [(y - h/2, x) for x, y in pts]      # rotated 90: web horizontal, centred
        pts = [(cx+x, yb+y) for x, y in pts]
        self.pline(pts, layer, True, lineweight=35); self.hatch(pts)
    def ielev(self, x0, x1, yb, h, tf, layer, slope=0.0):
        """Side elevation of an I-beam (web visible): outline + flange lines; slope = rise per unit run."""
        dy = (x1-x0)*slope
        self.pline([(x0,yb),(x1,yb+dy),(x1,yb+dy+h),(x0,yb+h)], layer, True, lineweight=35)
        self.line(x0, yb+tf, x1, yb+dy+tf, layer); self.line(x0, yb+h-tf, x1, yb+dy+h-tf, layer)
    def bolt_side(self, x, y, d=20, L=60, vertical=False):
        """Bolt seen from the side: shank + head + nut, centred on (x,y), axis horizontal (or vertical)."""
        hh, hw = 0.65*d, 1.6*d
        if not vertical:
            self.rect(x-L/2, y-d/2, x+L/2, y+d/2, 'S-DETAIL'); self.rect(x-L/2-hh, y-hw/2, x-L/2, y+hw/2, 'S-DETAIL'); self.rect(x+L/2, y-hw/2, x+L/2+hh, y+hw/2, 'S-DETAIL')
        else:
            self.rect(x-d/2, y-L/2, x+d/2, y+L/2, 'S-DETAIL'); self.rect(x-hw/2, y-L/2-hh, x+hw/2, y-L/2, 'S-DETAIL'); self.rect(x-hw/2, y+L/2, x+hw/2, y+L/2+hh, 'S-DETAIL')
    def hole(self, x, y, d=22):
        self.sh.circle(*self.P(x,y), d/2*K, 'S-DETAIL'); self.line(x-d, y, x+d, y, 'S-GRID'); self.line(x, y-d, x, y+d, 'S-GRID')
    def weld(self, x, y, a, side=1, txt=None):
        self.pline([(x, y), (x+25*side, y+25), (x+25*side, y)], 'S-DETAIL', True); self.sh.hatch([self.P(x,y), self.P(x+25*side,y+25), self.P(x+25*side,y)], 'S-HATCH', 'SOLID', color=7)
        self.text(x+35*side if side > 0 else x-35, y+5, txt or ('a%d' % a), 0.16)
    def title(self, x, y, s): self.text(x, y, s, 0.2, 'LEFT')
    def notes(self, x, y, lines, dy=24):
        yy = y
        for s in lines:
            k = self.text(x, yy, s, 0.14); yy -= k*1.5*0.14/K

def d1(sh, fx, fy):
    d = D(sh, fx, fy, 'D1', 'RAFTER FIN PLATE', 'IPE 270 rafter to IPE 330 primary web; 2 M20 8.8 (3 M20, plate 220, on the 9.20 m rafters)')
    d.title(0, 1000, 'SECTION looking east along the primary (rafter from the south, slope 3.43 deg)')
    d.iprof(150, 0, 330, 160, 7.5, 11.5, 'S-PRIM'); d.text(150, -45, 'PRIMARY IPE 330 (level)', 0.16, 'CENTER')
    s = math.tan(math.radians(3.43))
    # rafter: bottom flange 10 above the primary bottom at the end, rising towards the south (right)
    x0 = 153.75 + 10; d.ielev(x0, 620, 10, 270, 10.2, 'S-RAFT', slope=-s)   # falls to the right = north; here primary is at the north end of the piece? draw generic fall to the left
    d.text(520, 150, 'RAFTER IPE 270', 0.16, 'CENTER'); d.text(300, 420, 'end cut plumb (3.43 deg to the flanges), no cope', 0.14)
    d.rect(153.75, 70, 253.75, 220, 'S-DETAIL', lineweight=50); d.text(300, 350, 'FIN PLATE 100x150x10 S275', 0.14)
    for y in (110, 180): d.bolt_side(203.75, y, 20, 40, False)
    d.weld(153.75, 220, 6, 1, 'a6 both sides')
    d.dimv(0, 10, 640, 60); d.dimv(70, 220, 300, 60); d.dimv(70, 110, 300, 100); d.dimv(110, 180, 300, 100); d.dimv(180, 220, 300, 100)
    d.dimh(153.75, 203.75, 70, -60); d.dimh(153.75, 253.75, 70, -100); d.dimh(153.75, 163.75, 280, 60)
    d.dimv(0, 330, -60, -60); d.dimv(280, 330, 660, 60)
    d.text(-60, 380, 'primary top = TOS + 50', 0.14); d.text(300, -90, 'rafter bottom 10 above the primary bottom (flush)', 0.14)
    d.title(0, -120, 'PLAN at the primary web (fin plates both sides in line, rafter continuity D3)')
    y0 = -500
    d.line(-50, y0, 700, y0, 'S-PRIM', lineweight=35); d.line(-50, y0+80, 700, y0+80, 'S-PRIM'); d.line(-50, y0-80, 700, y0-80, 'S-PRIM')
    d.text(-40, y0+95, 'primary IPE 330 web / flange edges', 0.16)
    for sgn in (1, -1):
        d.rect(300, y0+sgn*3.75, 400, y0+sgn*13.75, 'S-DETAIL', lineweight=50)
        d.line(350-3.3, y0+sgn*13.75, 350-3.3, y0+sgn*360, 'S-RAFT', lineweight=35); d.line(350+3.3, y0+sgn*13.75, 350+3.3, y0+sgn*360, 'S-RAFT', lineweight=35)
        d.line(350-67.5, y0+sgn*13.75, 350-67.5, y0+sgn*360, 'S-RAFT'); d.line(350+67.5, y0+sgn*13.75, 350+67.5, y0+sgn*360, 'S-RAFT')
        d.rect(334, y0+sgn*13.75, 366, y0+sgn*27, 'S-DETAIL'); d.rect(334, y0+sgn*3.75, 366, y0+sgn*(-9), 'S-DETAIL')
    d.text(350, y0+370, 'rafter (north piece)', 0.14, 'CENTER'); d.text(350, y0-395, 'rafter (south piece)', 0.14, 'CENTER')
    d.dimh(300, 350, y0+13.75, 300); d.dimh(300, 400, y0+13.75, 340); d.dimv(y0+3.75, y0+13.75, 420, 60)
    d.notes(-60, y0-440, ['Bolts M20 8.8 in 22 round holes, snug tight, PLAIN fin plates everywhere (no slotted holes): the E-W thermal path B2 - RT-N-W - row F chord - RT-N-E - B1 is designed for +/-20 K service / +/-30 K erection.',
        'Max end reaction 35.2 kN; web bearing governs at 0.45. One fin plate per rafter end, both sides of the primary web in line.'])
def d2(sh, fx, fy):
    d = D(sh, fx, fy, 'D2', 'CAP PLATE', 'HEA 160 cap plate 200x280x20, 4 M20 8.8 through the IPE 330 bottom flange, gauge 90 pitch 200')
    d.title(0, 1000, 'ELEVATION normal to the primary (end column shown; interior column: 2 bolts per primary end, D3)')
    d.rect(-80, 0, 80, 520, 'S-COL', lineweight=35); d.line(-80, 0, 80, 0, 'S-COL'); d.text(0, 250, 'HEA 160 column (flange face 160)', 0.16, 'CENTER', 90)
    d.rect(-140, 520, 140, 540, 'S-DETAIL', lineweight=50); d.weld(80, 520, 6, 1, 'a6 all round'); d.weld(-80, 520, 6, -1, 'a6')
    d.ielev(-320, 320, 540, 330, 11.5, 'S-PRIM'); d.text(340, 760, 'PRIMARY IPE 330, level on the cap plate (no pack: slope is in the rafters)', 0.14)
    for x in (-100, 100): d.bolt_side(x, 540, 20, 32, True)
    d.dimh(-100, 100, 520, -60); d.dimh(-140, 140, 520, -100); d.dimv(520, 540, 160, 60); d.dimv(540, 870, 160, 60); d.dimv(0, 520, -160, -60)
    d.text(-380, 30, 'cap top = TOS - 280', 0.16)
    d.title(0, -80, 'PLAN of the cap plate (primary axis horizontal)')
    y0 = -500
    d.rect(-140, y0-100, 140, y0+100, 'S-DETAIL', lineweight=50)
    d.iprof(0, y0-80, 160, 152, 6, 9, 'S-COL', rot=1) if False else None
    d.rect(-80, y0-76, 80, y0+76, 'S-COL', linetype='DASHED'); d.line(0, y0-76, 0, y0+76, 'S-COL', linetype='DASHED'); d.text(0, y0+90, 'HEA 160 below (web across the wall)', 0.14, 'CENTER')
    d.line(-320, y0-80, 320, y0-80, 'S-PRIM'); d.line(-320, y0+80, 320, y0+80, 'S-PRIM'); d.line(-320, y0, 320, y0, 'S-PRIM', linetype='DASHED')
    for x in (-100, 100):
        for y in (-45, 45): d.hole(x, y0+y, 22)
    d.dimh(-100, 100, y0-100, -60); d.dimh(-140, 140, y0-100, -100); d.dimv(y0-45, y0+45, 160, 60); d.dimv(y0-100, y0+100, 160, 100)
    d.notes(-380, y0-260, ['Cap plate 200 x 280 x 20 S275, welded a6 all round to the column; holes 22.', 'Tension 66.7 kN (uplift K12) -> bolt 0.12, flange T-stub 0.16; chord shear 61 kN -> 0.25.',
        'Primaries bolted before the rafters are landed (nuts clear the passing rafter flange).', 'Stiffeners: none required (HEA 160 flanges under the IPE 330 web, bearing 0.10).'])
def d3(sh, fx, fy):
    d = D(sh, fx, fy, 'D3', 'CHORD TIE', 'Primary continuity over the column (rows F and B): 10 mm tie plate under both primary ends')
    d.title(0, 1000, 'ELEVATION along the primary row')
    d.rect(-80, 0, 80, 520, 'S-COL', lineweight=35); d.rect(-140, 520, 140, 540, 'S-DETAIL', lineweight=50)
    d.rect(-200, 540, 200, 550, 'S-DETAIL', lineweight=50); d.text(-200, 585, 'TIE PLATE 140 x 400 x 10 (pack)', 0.16)
    d.ielev(-420, -10, 550, 330, 11.5, 'S-PRIM'); d.ielev(10, 420, 550, 330, 11.5, 'S-PRIM')
    d.text(-215, 900, 'primary end', 0.16, 'CENTER'); d.text(215, 900, 'primary end', 0.16, 'CENTER')
    for x in (-100, 100): d.bolt_side(x, 545, 20, 42, True)
    d.text(30, 890, 'gap 20', 0.14); d.dimh(-100, 100, 520, -60); d.dimh(-200, 200, 520, -100); d.dimv(540, 550, 220, 60)
    d.title(0, -80, 'PLAN: rafter continuity through the primary web (fin plates in line, D1)')
    y0 = -520
    d.line(-380, y0, 380, y0, 'S-PRIM', lineweight=35); d.line(-380, y0+80, 380, y0+80, 'S-PRIM'); d.line(-380, y0-80, 380, y0-80, 'S-PRIM')
    d.rect(-140, y0-100, 140, y0+100, 'S-DETAIL', linetype='DASHED'); d.text(-135, y0+110, 'cap plate below', 0.14)
    for sgn in (1, -1):
        d.rect(250, y0+sgn*3.75, 350, y0+sgn*13.75, 'S-DETAIL', lineweight=50)
        d.line(300-67.5, y0+sgn*13.75, 300-67.5, y0+sgn*380, 'S-RAFT'); d.line(300+67.5, y0+sgn*13.75, 300+67.5, y0+sgn*380, 'S-RAFT')
        d.line(300, y0+sgn*13.75, 300, y0+sgn*380, 'S-RAFT', lineweight=35)
    d.text(300, y0+395, 'rafter R', 0.16, 'CENTER'); d.text(300, y0-420, 'rafter R', 0.16, 'CENTER')
    d.notes(-380, y0-470, ['Chord force <= 61 kN passes through the tie plate and the 4 M20 (2 per primary end).', 'Rafter post force <= 38 kN passes through the fin plates and the primary web (bolt shear).',
        'Gap between primary ends 20 mm; ends cut square. Rows A/G/H: no tie plate (eave beams).'])
def d4(sh, fx, fy):
    d = D(sh, fx, fy, 'D4', 'BRACING GUSSET', 'L70x7 tension-only diagonals, 10 mm gusset to the column flange and base plate; 2 M20 8.8 per angle end')
    d.title(0, 1000, 'ELEVATION in the wall plane at the column base (eave gusset: same, under the cap plate)')
    d.line(-150, 0, 700, 0, 'S-EXIST', lineweight=35); d.text(600, -40, 'slab', 0.14)
    d.rect(-150, 40, 250, 65, 'S-COL', lineweight=50); d.rect(-150, 0, 250, 40, 'S-HATCH'); d.text(-140, 15, 'grout 40', 0.14)
    d.rect(-80, 65, 80, 900, 'S-COL', lineweight=35); d.text(0, 700, 'HEA 160 (flange 160 in the wall plane)', 0.16, 'CENTER', 90)
    ang = math.atan2(3.8, 5.0); c, s = math.cos(ang), math.sin(ang)
    g = [(80, 65), (80, 420), (150, 420), (460, 65)]; d.pline(g, 'S-DETAIL', True, lineweight=50); d.text(200, 100, 'GUSSET 10 mm', 0.16)
    d.weld(80, 300, 6, 1, 'a6'); d.weld(300, 65, 6, 1, 'a6')
    # angle along the diagonal: centreline from (80, 65+...) through the gusset
    p0 = (180, 130); L = 700
    def along(t, off=0): return (p0[0] + t*c - off*s, p0[1] + t*s + off*c)
    d.pline([along(0, 0), along(L, 0), along(L, 70), along(0, 70)], 'S-BRACE', True, lineweight=35); d.text(*along(380, 90), 'L70x7 (one per diagonal)', 0.16, 'LEFT', math.degrees(ang))
    for t in (40, 150):
        x, y = along(t, 30); d.hole(x, y, 22)
    d.text(*along(220, -70), 'e1 40, p1 110, e2 30 (angle leg)', 0.14, 'LEFT', math.degrees(ang))
    d.line(0, 65, 0, -90, 'S-GRID'); d.text(10, -80, 'column CL', 0.14)
    d.dimv(0, 40, -220, -60); d.dimv(40, 65, -220, -60); d.dimv(65, 420, -220, -100); d.dimh(80, 460, 65, -160)
    d.notes(-150, -220, ['Gusset 10 mm S275 in the wall plane, welded a6 to the outer column flange and to the base plate (or cap plate underside).',
        'Angle net section 189 kN, 2 M20 shear 188 kN, gusset bearing 2 x 124 kN; max T_Ed 72.1 kN (B8) -> 0.38 / 0.57.',
        'Diagonal centrelines meet at the column CL at base-plate top and at the primary centre (h = cap + 170).', 'Base gusset centreline offset 76 mm from the column axis: base plate and keys per bases_C.md Rev 4 (S05).',
        'X in every bay: both diagonals, crossing clipped with a 10 mm plate and 1 M16 at mid-length.'])
def d5(sh, fx, fy):
    d = D(sh, fx, fy, 'D5', 'ROOF ROD GUSSET', 'M24 8.8 rods with turnbuckles; 8 mm gussets SHOP-WELDED to the primary web and BOLTED 2 M16 to the rafter web (no site welding); web hole where a rod passes R2 / R10')
    d.title(0, 1000, 'PLAN at a panel corner (rafter web vertical, primary web horizontal)')
    d.line(-100, 0, 700, 0, 'S-PRIM', lineweight=35); d.line(-100, 80, 700, 80, 'S-PRIM'); d.line(-100, -80, 700, -80, 'S-PRIM'); d.text(600, 95, 'primary IPE 330', 0.16)
    d.line(0, 0, 0, 700, 'S-RAFT', lineweight=35); d.line(-67.5, 13.75, -67.5, 700, 'S-RAFT'); d.line(67.5, 13.75, 67.5, 700, 'S-RAFT'); d.text(80, 650, 'rafter IPE 270', 0.16)
    g = [(3.3, 3.75), (250, 3.75), (250, 60), (60, 250), (3.3, 250)]; d.pline(g, 'S-DETAIL', True, lineweight=50); d.text(70, 25, 'GUSSET 8 mm, shop-welded a5 to the primary web (bottom flange level)', 0.13)
    d.rect(3.3, 60, 30, 250, 'S-DETAIL', lineweight=35); d.text(-100, 300, 'gusset leg 8 mm bolted to the rafter web: 2 M16 8.8 in 18 holes', 0.12)
    for y in (110, 200): d.bolt_side(16, y, 16, 34, False)
    d.rect(320, 250, 420, 420, 'S-RAFT', linetype='DASHED'); d.sh.circle(*d.P(370, 335), 30*K, 'S-DETAIL'); d.text(320, 440, 'R2 / R10 web hole dia 60 (RT-W / RT-E rods over two bays), stiffened with a 8 mm ring plate', 0.12)
    ang = math.atan2(5.9, 2.65); c, s = math.cos(ang), math.sin(ang)
    for t in (0, 1):
        pass
    p = (135, 110); L = 520
    d.pline([(p[0]-12*s, p[1]+12*c), (p[0]+L*c-12*s, p[1]+L*s+12*c), (p[0]+L*c+12*s, p[1]+L*s-12*c), (p[0]+12*s, p[1]-12*c)], 'S-BRACE', True, lineweight=35)
    d.hole(p[0], p[1], 26); d.text(p[0]+40, p[1]-30, 'hole 26, nut + lock nut each side', 0.14)
    tb = (p[0]+300*c, p[1]+300*s); d.rect(tb[0]-25*c-20*s, tb[1]-25*s+20*c, tb[0]+25*c+20*s, tb[1]+25*s-20*c, 'S-BRACE') if False else None
    d.pline([(tb[0]-60*c-22*s, tb[1]-60*s+22*c), (tb[0]+60*c-22*s, tb[1]+60*s+22*c), (tb[0]+60*c+22*s, tb[1]+60*s-22*c), (tb[0]-60*c+22*s, tb[1]-60*s-22*c)], 'S-BRACE', True, lineweight=35)
    d.text(tb[0]+40, tb[1]-10, 'turnbuckle M24 (one per rod)', 0.14)
    d.dimh(0, 250, 3.75, -130); d.dimv(3.75, 250, -140, -60); d.dimh(0, p[0], p[1], 200); d.dimv(0, p[1], 330, 60)
    d.notes(-100, -260, ['Rods M24 8.8 (F_t,Rd 203 kN), max T_Ed 47.6 kN (RT-W); rod at the panel diagonal angle in plan (2.05-9.2 m panels).',
        'Rods run at the bottom-flange level of the rafters; sag ties to the purlins at the crossing and at 3 m centres.',
        'RT-W / RT-E: rods over two rafter bays pass the intermediate rafter (R2 / R10) through a dia 60 web hole with an 8 mm ring plate, shop-drilled; no site welding anywhere (galvanised steel).',
        'Pretension by turnbuckle to remove sag only (snug); lock nuts after adjustment. All gussets hot-dip galvanised.'])
def d6(sh, fx, fy):
    d = D(sh, fx, fy, 'D6', 'WELL UPSTAND', 'T2 IPE 270 trimmer on fin plates (D1) to R5/R6; C100x50x3 upstand 150 above the panel; flashing and panel stop')
    d.title(0, 1000, 'SECTION across trimmer T2 (north edge of the elevator well), looking east')
    d.iprof(0, 0, 270, 135, 6.6, 10.2, 'S-RAFT'); d.text(0, -45, 'TRIMMER T2 IPE 270', 0.16, 'CENTER')
    d.rect(-200, 270, 200, 285, 'S-DETAIL'); d.text(-380, 275, 'cont. 15 mm plate seat', 0.14)   # optional seat plate for the upstand
    d.rect(-50, 285, 50, 285+200+50+150, 'S-DETAIL', lineweight=50); d.text(60, 500, 'UPSTAND C100x50x3 S350GD, posts @ 600 + top rail', 0.16)
    d.line(-50, 285, 50, 285, 'S-DETAIL'); d.text(-60, 290, '2 M12 to the seat / flange', 0.14, 'RIGHT')
    # purlin and panel on the roof side (right = south, roof)
    d.rect(60, 285, 130, 485, 'S-PURL'); d.text(140, 330, 'edge purlin Z200', 0.14)
    d.rect(60, 485, 500, 535, 'S-DETAIL', lineweight=35); d.text(250, 545, 'PIR panel 50', 0.16, 'CENTER')
    d.pline([(500, 535), (-60, 535)], 'S-DETAIL') if False else None
    # flashing over the upstand
    d.pline([(200, 545), (60, 545), (60, 700), (-60, 700), (-60, 640), (-80, 640)], 'S-DETAIL', lineweight=35); d.text(80, 715, 'cap flashing 0.7 mm coated, drip into the well, laps 200 on the panel, sealed', 0.14)
    d.rect(50, 535, 60, 690, 'S-DETAIL'); d.text(-450, 610, 'panel stop / closer', 0.14)
    d.dimv(535, 685, 250, 60); d.dimv(285, 485, 200, 60); d.dimv(0, 270, -150, -60); d.dimh(-50, 50, 285, -110)
    d.text(-460, 120, 'ELEVATOR WELL (open)', 0.16); d.text(300, 120, 'ROOF', 0.16)
    d.notes(-460, -160, ['Same detail on rafters R5 / R6 beside both wells and on P8 (south edge of the stair well, cricket side: upstand 270-300 at the cricket ridge); the stair well is open to the north face (no trimmer there).',
        'Upstand height >= 150 above the panel top on all sides; soakers at panel seams; well-side face lined with the same coated sheet.',
        'Trimmer ends: fin plates 100x150x10, 2 M20 to the rafter webs (D1). Upstand line load 0.30 kN/m (G) included in the trimmer check (0.02).',
        'Elevator well south side: upstand merged with the notch verge flashing (0.2 m strip capped 5 % both ways).'])
def d7(sh, fx, fy):
    d = D(sh, fx, fy, 'D7', 'EAVE + GUTTER', 'Rafter end, eave rail C200x60x2.5, brackets 40x5 @ 600, box gutter 150x100, fascia, first purlin, panel, wall panel')
    d.title(0, 1000, 'SECTION through the north eave at a rafter (looking east; north on the right)')
    s = math.tan(math.radians(3.43))
    d.iprof(0, 0, 330, 160, 7.5, 11.5, 'S-PRIM'); d.text(0, -45, 'eave primary P4 IPE 330 on C1', 0.16, 'CENTER')
    d.rect(-80, -420, 80, 0-330+330-330+330-330, 'S-COL') if False else None
    d.rect(-80, -430, 80, -350, 'S-COL', lineweight=35); d.line(-80, -350, 80, -350, 'S-COL'); d.text(100, -400, 'column HEA 160 (cap plate D2)', 0.14)
    d.ielev(-600, 100, 10+600*s, 270, 10.2, 'S-RAFT', slope=-s); d.text(-350, 150, 'rafter IPE 270 (fin plate D1), ends 100 past the primary', 0.14, 'CENTER')
    yt = 10 + 270 - 100*s   # rafter top at the end x=100
    d.rect(100, yt-200, 102.5, yt+5, 'S-PURL', lineweight=35); d.line(100, yt+5, 160, yt+5, 'S-PURL', lineweight=35); d.line(100, yt-200, 160, yt-200, 'S-PURL', lineweight=35)
    d.text(110, yt-260, 'eave rail C200x60x2.5 bolted 2 M12 to each rafter end', 0.14)
    d.rect(-330, yt-10, -260, yt+190, 'S-PURL'); d.text(-300, yt+205, 'purlin Z200 @ 300 from the edge', 0.14, 'CENTER')
    d.line(-600, yt+190+600*s, 250, yt+190-150*s, 'S-DETAIL', lineweight=35); d.line(-600, yt+240+600*s, 250, yt+240-150*s, 'S-DETAIL', lineweight=35)
    d.text(-450, yt+270, 'PIR panel 50, overhang 150 past the rail', 0.14)
    d.pline([(250, yt+240), (270, yt+240), (270, yt+120)], 'S-DETAIL'); d.text(280, yt+180, 'drip flashing 0.7, laps 60 into the gutter', 0.14)
    # bracket + gutter
    d.pline([(160, yt-20), (200, yt-20), (200, yt+60), (360, yt+60), (360, yt+150)], 'S-DETAIL', lineweight=35); d.text(205, yt+70, 'bracket 40x5 galv. @ 600', 0.14)
    d.pline([(200, yt+140), (200, yt+40), (350, yt+40), (350, yt+130)], 'S-DRAIN', lineweight=50); d.text(275, yt+15, 'BOX GUTTER 150x100, outer lip 10 lower', 0.14, 'CENTER')
    d.rect(100, yt-330, 106, yt+60, 'S-DETAIL'); d.text(110, yt-140, 'fascia flashing', 0.14)
    d.rect(80, -430, 130, yt-330, 'S-DETAIL'); d.text(140, -100, 'BoardX wall panel on the top girt (D9)', 0.14)
    d.rect(-40, -300, 30, -100, 'S-PURL'); d.text(-100, -200, 'top girt Z200', 0.14, 'RIGHT')
    d.dimh(200, 350, yt+40, -180); d.dimv(yt+40, yt+140, 380, 60); d.dimh(0, 100, 330, 80); d.dimh(0, -300, 330, 130); d.dimv(0, 330, -650, -60); d.dimv(280, 330, -650, -100) if False else None
    d.notes(-620, -520, ['Gutter 0.7 mm galvanised + polyester (or 1.0 alu), riveted + butyl joints, fall 1:350 to outlets DP1-DP4, EPDM expansion joint at each high point.',
        'Loads: 0.25 kN/m gravity, -0.50 kN/m uplift (zone F), 0.5 kN point at any bracket; fixed brackets at the outlets, sliding elsewhere.',
        'Two runs: G-W at y 35.37 (x 67.89-77.89, eave beams P1/P2, rafters R1-R5 cantilever 0.10 past them) and G-E at y 35.87 (x 81.79-95.69); stop ends and overflow spouts 100x30 at x 67.89 / 77.89 / 81.79 / 95.69.'])
def d8(sh, fx, fy):
    d = D(sh, fx, fy, 'D8', 'PURLIN CLEAT', 'Z200x2.0 on a plate cleat 2 M12; fly brace L50x5 from the rafter bottom flange to the purlin')
    d.title(0, 1000, 'SECTION across the rafter (looking north)')
    d.iprof(0, 0, 270, 135, 6.6, 10.2, 'S-RAFT'); d.text(0, -45, 'RAFTER IPE 270', 0.16, 'CENTER')
    d.rect(-4, 270, 4, 430, 'S-DETAIL', lineweight=50); d.rect(-60, 270, 60, 278, 'S-DETAIL', lineweight=50); d.text(70, 400, 'CLEAT: plate 120x160x8 welded to the flange (a4), or bolted 2 M12', 0.14)
    # Z purlin: web vertical at x ~ 8..10, flanges 70 top to the right, bottom to the left
    d.pline([(4, 278), (4, 478), (74, 478), (74, 462), (20, 462), (20, 294), (-66, 294), (-66, 278)], 'S-PURL', True, lineweight=35); d.text(80, 470, 'Z200x2.0 purlin', 0.14)
    for y in (330, 400): d.bolt_side(4, y, 12, 26, False)
    d.rect(-400, 478, 400, 528, 'S-DETAIL', lineweight=35); d.text(-380, 540, 'PIR panel 50, screws to every purlin', 0.14)
    # fly brace from the bottom flange to the purlin bottom flange (45 deg)
    fb = [(-60, 12), (-60+60, 12+60*0)]
    d.pline([(-55, 12), (-65, 12), (-330, 290), (-320, 290)], 'S-BRACE', True, lineweight=35) if False else None
    d.line(-60, 12, -300, 300, 'S-BRACE', lineweight=50); d.line(-75, 22, -315, 310, 'S-BRACE', lineweight=50)
    d.text(-320, 330, 'FLY BRACE L50x5, 1 M12 each end, both sides of the rafter', 0.14)
    d.bolt_side(-60, 6, 12, 22, True); d.hole(-300, 300, 14)
    d.text(-460, 310, 'to the purlin bottom flange (cleat L50)', 0.12)
    d.dimv(270, 478, 100, 60); d.dimv(330, 400, 100, 100); d.dimv(0, 270, -150, -60); d.dimh(-60, 60, 270, -100)
    d.notes(-460, -160, ['Purlins simple span between rafters, 1.5 m centres, one mid-span anti-sag row per span (rod M12 + cleats); sleeved on the 4.07 m stair strip.',
        'Fly braces: at mid-span for rafter spans <= 6.6 m, at the third points for the 7.5 and 9.2 m spans (LTB under uplift, segment 2.2-3.25 m).',
        'Cleat bolts M12 8.8 in 14 holes (18x14 slotted along the purlin for the sleeved rows). Supplier uplift capacity >= 9 kNm required before order.'])
def d9(sh, fx, fy):
    d = D(sh, fx, fy, 'D9', 'GIRT + PANEL', 'Z200x2.0 girt on an L100x100x8 cleat to the column flange; BoardX panel on the girt outer flange')
    d.title(0, 1000, 'PLAN SECTION at a wall column (wall face at the bottom of the view)')
    d.iprof(0, 0, 152, 160, 6, 9, 'S-COL', rot=1); d.text(0, 100, 'HEA 160, web normal to the wall', 0.16, 'CENTER')
    # outer flange at y = -80; cleat angle on the flange face
    d.pline([(-80, -80), (-80, -180), (-72, -180), (-72, -88), (20, -88), (20, -80)], 'S-DETAIL', True, lineweight=50); d.text(30, -100, 'CLEAT L100x100x8 x 150 long, welded a5 or 2 M12 to the flange', 0.14)
    d.bolt_side(-76, -130, 12, 26, False)
    # Z girt: web vertical? girt runs along the wall (x direction here); in plan section its web is vertical (z), so we see the girt as a 200 deep... plan shows the girt depth normal to wall = 70 (flange) -> draw flange width 70
    d.rect(-400, -180, 400, -178, 'S-PURL'); d.rect(-400, -250, 400, -248, 'S-PURL'); d.text(-380, -230, 'girt Z200x2.0 (web vertical, depth 200 in elevation; flange 70 shown)', 0.14)
    d.rect(-400, -250, 400, -300, 'S-DETAIL', lineweight=35); d.text(-380, -340, 'BoardX wall panel (50 assumed) - product data to be confirmed', 0.14)
    d.line(-420, -300, 420, -300, 'S-DETAIL'); d.text(430, -310, 'outside', 0.14)
    for x in (-250, 250): d.line(x, -250, x, -300, 'S-DETAIL', linetype='DASHED'); d.text(x+10, -280, 'self-drilling screw @ 300', 0.12)
    d.dimv(-80, -180, 120, 60); d.dimv(-180, -250, 120, 60); d.dimv(-250, -300, 120, 60); d.dimh(-80, 80, 76, 60)
    d.notes(-420, -420, ['Girts span column to column (simple, or sleeved on the 1.0 / 1.2 m rows: K5-K7, K25-K19, K8-K6, K21-K22, K22-K23, K14-K4).',
        'Rows 1.5 m elsewhere; bottom row 0.50 m above the slab, top row 150 below the eave beam; corner columns: cleats on both flanges.',
        'Wall net wind 2.15 kN/m2 (zone A 2.73 within 2.4 m of a corner). Cleat bolts M12 8.8; girt bolts M12 in 14 holes.',
        'Column sway limit h/150 (BoardX): bay sway 4 mm + diaphragm drift 10 mm < 20-28 mm.'])
def d10(sh, fx, fy):
    d = D(sh, fx, fy, 'D10', 'WIND POST WP1', 'HEA 160 at (77.61, 20.25), 280 inboard of the notch corner: slotted head to eave beam P14; base 250x250x15, dia 60 key, 2 M12 (S05)')
    d.title(0, 1000, 'HEAD - elevation looking north (eave beam P14 in section)')
    d.iprof(0, 300, 330, 160, 7.5, 11.5, 'S-PRIM'); d.text(0, 645, 'P14 IPE 330 (eave beam, fin plate to R5)', 0.16, 'CENTER')
    d.rect(-80, -200, 80, 250, 'S-COL', lineweight=35); d.line(0, -200, 0, 250, 'S-COL'); d.text(100, -100, 'WP1 HEA 160', 0.16)
    d.rect(-60, 100, 60, 300, 'S-DETAIL', lineweight=50); d.text(70, 180, 'CLEAT plate 120x200x10 welded a6 to the P14 bottom flange', 0.14)
    for y in (140, 220): d.rect(-11, y-30, 11, y+30, 'S-DETAIL'); d.bolt_side(0, y, 20, 40, False)
    d.text(70, 130, '2 M20 in 22x60 vertical slots, snug (no vertical load transfer)', 0.14)
    d.dimv(250, 300, -150, -60); d.dimv(100, 300, -150, -100)
    d.title(0, -280, 'BASE - plan at the slab corner (notch), Rev 4 position')
    y0 = -700
    d.line(-450, y0, 350, y0, 'S-EXIST', lineweight=35); d.line(-450, y0, -450, y0+450, 'S-EXIST', lineweight=35); d.text(-440, y0+460, 'slab edges (notch corner)', 0.14)
    d.rect(-450, y0-60, 350, y0, 'S-EXIST', linetype='DASHED'); d.text(-100, y0-50, 'edge beam assumed - core to confirm', 0.12)
    d.rect(-295, y0+155, -45, y0+405, 'S-DETAIL', lineweight=50); d.text(-170, y0+420, 'plate 250x250x15, dia 60 key centred', 0.14, 'CENTER')
    d.rect(-246, y0+204, -94, y0+356, 'S-COL', linetype='DASHED'); d.sh.circle(*d.P(-170, y0+280), 30*K, 'S-DETAIL', lineweight=35)
    for x in (-270, -70): d.hole(x, y0+180, 14)
    d.dimh(-450, -170, y0+155, -60); d.dimv(y0, y0+280, -20, 60); d.dimh(-270, -70, y0+180, 260)
    d.notes(-450, y0-140, ['Post centre 280 mm inboard of both slab edges (Rev 4): single dia 60 key with c1 = 250 both ways; 2 M12 for location only; corner girts cantilever 280 to the wall line.',
        'Shear 11.8 / 8.8 kN (E-W / N-S) vs 38.2 kN edge breakout (0.31); no uplift (slotted head). Notch edge beam to be confirmed by core (else type S plate with two Key B).', 'Wall panel and girts on both faces (S2 and notch face EN) fix to the post flanges (D9).'])
def d11(sh, fx, fy):
    d = D(sh, fx, fy, 'D11', 'WALL SILL / BASE RAIL', 'BoardX wall base at the slab edge: C100x50x3 sill rail on the slab, M8 anchors @ 600, drip flashing; bottom girt 0.50 above; well walls hall-side: blockwork (architect)', W=6.8)
    d.title(0, 1000, 'SECTION at the slab edge (outside on the left)')
    d.line(-200, 0, 500, 0, 'S-EXIST', lineweight=35); d.line(-200, -250, 500, -250, 'S-EXIST', lineweight=35); d.line(-200, 0, -200, -250, 'S-EXIST', lineweight=50)
    d.hatch([(-200,-250),(500,-250),(500,0),(-200,0)], 0.12, 8, 45); d.text(-190, -240, 'existing slab / edge beam (survey datum = slab top)', 0.12)
    d.pline([(-100, 0), (-100, 100), (-50, 100), (-50, 3), (-3, 3), (-3, 0)], 'S-PURL', True, lineweight=35); d.text(-40, 60, 'SILL RAIL C100x50x3 S350GD, continuous, on 5 mm DPC / sealant', 0.12)
    for x in (-75,): d.bolt_side(x, 0, 8, 20, True); d.text(-40, 110, 'M8 resin anchors @ 600 (h_ef 60), 100 from the edge', 0.12)
    d.rect(-150, 100, -100, 1100, 'S-DETAIL', lineweight=35); d.text(-160, 500, 'BoardX wall panel (50 assumed)', 0.12, 'RIGHT', 90)
    d.rect(-100, 500, -30, 700, 'S-PURL'); d.text(-20, 560, 'bottom girt Z200 at 0.50 (D9)', 0.12)
    d.pline([(-160, 130), (-170, 130), (-170, 60), (-160, 50)], 'S-DETAIL', lineweight=35); d.text(-350, 140, 'drip flashing 0.7, sealed to the panel', 0.11)
    d.line(-200, -30, -100, -30, 'S-DETAIL'); d.text(-350, -60, '100 to the slab edge', 0.11)
    d.dimh(-200, -100, 0, -60); d.dimv(0, 100, 20, 60); d.dimv(0, 500, 60, 60)
    d.rect(-80, 65, -30, 500, 'S-COL', linetype='DASHED'); d.text(-25, 300, 'HEA 160 beyond, base per S05', 0.11)
    d.notes(-350, -320, ['Wall base line: 100 mm inside the slab face on N1 / N2 / S / E / W faces; panel bottom 100 above the slab; sill rail carries the panel weight to the slab and closes the wall against water (drip outside).',
        'Well walls on the hall side: blockwork on the existing well walls, by the architect (not steel); the 150 upstands (D6) sit on the steel trimmers / rafters.'], 22)
def dnotes(sh, fx, fy):
    d = D(sh, fx, fy, 'GN', 'CONNECTION NOTES', 'General notes for all connections D1-D11', W=6.8)
    d.notes(-650, 1000, ['Steel S275 J0; bolts 8.8 hot-dip galvanised, snug tight (no preload relied upon); M20 in 22 holes, M16 in 18, M12 in 14, M24 rods in 26; all holes round (no slots, C4).',
        'Welds: shop fillet welds a5-a8 as noted, E42 / S275 consumables; NO site welding (galvanised steel): rod gussets shop-welded to the primaries and bolted to the rafters (D5).',
        'Thermal: conditioned hall +/-20 K service, +/-30 K erection; the E-W restraint path B2 - RT-N-W - row F chord - RT-N-E - B1 carries a locked-in 10 kN (service) / 15 kN (erection); K1, K2, K5, K7 are B2 bases.',
        'Galvanising EN ISO 1461 (85 um) after fabrication; touch-up zinc-rich on site cuts. Cold-formed Z / C S350GD+Z275.',
        'Rafter ends plumb-cut, no copes; primaries level on level cap plates; slope 6 % in the rafters only.',
        'Fly braces at mid-span (L <= 6.6 m) and third points (7.5 / 9.2 m); anti-sag row at mid-span of every purlin span; purlin-cleat uplift ~11 kN in zone F: 2 M12 8.8 per cleat.',
        'North face jog: west eave beams P1 / P2 at y 35.22, rafters R1-R5 cantilever 0.10 past them to y 35.37; east eave at y 35.87; stair well open to the north face (wall header 2 x C200x60x2.5, no eave beam).'], 22)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S04', 'CONNECTION DETAILS D1 - D11', 'Details drawn 5x in model space (1 m = 200 mm); DIMENSION text = true mm (dimlfac 200)')
    fns = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, dnotes]
    for i, f in enumerate(fns):
        r, c = divmod(i, 6); f(sh, 0.3 + c*6.9, 16.2 - r*13.2)
    return sh
